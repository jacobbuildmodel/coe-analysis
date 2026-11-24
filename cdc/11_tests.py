"""
11_tests.py -- the controls, the gate and the four scored tests of THESIS.md.

  python3 cdc/11_tests.py [--series out/series.csv] [--out out]

Writes out/tests.csv (one line per control and test) and out/launches.csv
(every launch and payout, described). Each scored test ends in one word:
HOLDS, FAILS, NOT SCORED (a control failed, or the test cannot see a step of
0.5 percentage points) or PENDING (its months are not published yet).
"""
import argparse
import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cdclib as L  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
CONTROL_FIRST, CONTROL_LAST = (2015, 2), (2026, 10)
REVISION_MONTHS = (1, 4, 7, 10)
GST_JANUARIES = [(2023, 1), (2024, 1)]
TESTS = [  # id, role in events.csv, rule
    ("T1", "T1_T2", "size"),
    ("T2", "T1_T2", "rank"),
    ("T3", "T3", "size"),
    ("T4", "T4", "range"),
]
# T4 is one launch. One launch against 16 placebo years cannot reach p below
# 0.05 (the smallest possible p is 1/17), so T4 has its own line: the largest
# placebo excess. It is scored whenever the controls pass.


def launches(events, role):
    return [(int(e["year"]), int(e["month"])) for e in events if e["role"] == role]


def controls(series):
    ch = L.monthly_abs_changes(series[L.ELECTRICITY], CONTROL_FIRST, CONTROL_LAST)
    a = [v for (y, m), v in ch.items() if m in REVISION_MONTHS]
    b = [v for (y, m), v in ch.items() if m not in REVISION_MONTHS]
    p1 = L.rank_sum_p(a, b)
    c2 = L.pooled(series, GST_JANUARIES, comps=())
    return [
        dict(id="C1", statistic="rank-sum p, electricity, revision months above other months",
             value=p1, line="p < 0.05", result="PASS" if p1 < L.ALPHA else "FAIL",
             note=f"{len(a)} revision months, {len(b)} other months"),
        dict(id="C2", statistic="placebo p, hawker row alone, January 2023 and 2024",
             value=c2["p"], line="p < 0.05", result="PASS" if c2["p"] < L.ALPHA else "FAIL",
             note=f"mean excess {c2['s']:+.3f} pp; placebo draws {c2['null_n']} ({c2['null_how']})"),
    ]


def score(test_id, rule, res, controls_pass):
    if res is None:
        return dict(id=test_id, statistic="", value="", line="", result="PENDING",
                    note="launch window not published yet")
    if rule == "size":
        stat, value, line = "mean excess, pp", res["s"], f"below {L.LINE}"
        holds = res["s"] < L.LINE
    elif rule == "rank":
        stat, value, line = "placebo p of the mean excess", res["p"], "p >= 0.05"
        holds = res["p"] >= L.ALPHA
    else:  # range: one launch against the largest placebo excess; no gate D
        stat, value = "excess, pp", res["s"]
        line = f"at or below the largest placebo excess ({res['null_max']:+.4f})"
        holds = res["s"] <= res["null_max"]
    if not controls_pass:
        result = "NOT SCORED"
        why = "a positive control failed"
    elif rule != "range" and res["detect"] < L.POWER:
        result = "NOT SCORED"
        why = "gate D: cannot see a 0.5 pp step"
    else:
        result, why = ("HOLDS" if holds else "FAILS"), "scored"
    note = (f"{why}; S {res['s']:+.3f} pp; p {res['p']:.4f}; q95 {res['q95']:+.3f}; "
            f"gate D detection {res['detect']:.3f}; smallest step seen 4 times in 5 "
            f"{res['mde']:.3f} pp; placebo draws {res['null_n']} "
            f"({res['null_how']}); launches {len(res['excess'])}")
    return dict(id=test_id, statistic=stat, value=value, line=line, result=result, note=note)


def describe(series, events):
    rows = []
    rel = L.relative(series, L.HAWKER, L.COMPARISON)
    for e in events:
        ym = (int(e["year"]), int(e["month"]))
        try:
            parts = L.event_parts(rel, ym, 1, 1)
        except ValueError:
            parts = None
        rows.append(dict(id=e["id"], kind=e["kind"], role=e["role"],
                         window=f"{L.add(ym, -1)[0]}-{L.add(ym, -1)[1]:02d} to "
                                f"{L.add(ym, 1)[0]}-{L.add(ym, 1)[1]:02d}",
                         change_pct="" if parts is None else f"{parts[0]:.4f}",
                         excess_pp="" if parts is None else f"{parts[1]:.4f}",
                         placebo_years="" if parts is None else len(parts[3])))
    return rows


def run(series_path, events_path, out_dir):
    series, events = L.load_series(series_path), L.load_events(events_path)
    rows = controls(series)
    ok = all(r["result"] == "PASS" for r in rows)
    for test_id, role, rule in TESTS:
        rows.append(score(test_id, rule, L.pooled(series, launches(events, role)), ok))
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "tests.csv", "w", newline="", encoding="ascii") as f:
        w = csv.DictWriter(f, ["id", "statistic", "value", "line", "result", "note"],
                           lineterminator="\n")
        w.writeheader()
        for r in rows:
            r = dict(r)
            if isinstance(r["value"], float):
                r["value"] = f"{r['value']:.4f}"
            w.writerow(r)
    desc = describe(series, events)
    with open(out_dir / "launches.csv", "w", newline="", encoding="ascii") as f:
        w = csv.DictWriter(f, list(desc[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(desc)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", default=str(HERE / "out" / "series.csv"))
    ap.add_argument("--events", default=str(HERE / "events.csv"))
    ap.add_argument("--out", default=str(HERE / "out"))
    a = ap.parse_args()
    for r in run(a.series, a.events, pathlib.Path(a.out)):
        v = f"{r['value']:.4f}" if isinstance(r["value"], float) else r["value"]
        print(f"{r['id']:3s} {r['result']:10s} {r['statistic']}: {v} (line: {r['line']})")
        print(f"      {r['note']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

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


def t1_headline(row, res, rows):
    """THESIS section 8: result sentence, T2 sentence and title, filled by
    L.headline from T1's own verdict. T2 never picks the title."""
    if res is None:
        return None
    verdict = {"HOLDS": "HOLDS", "FAILS": "FAILS"}.get(row["result"], "NOT SCORED")
    w = sum(res["changes"]) / len(res["changes"])
    return L.headline(verdict, W=w, P=w - res["s"], S=res["s"], p=res["p"],
                      m=res["mde"], d=res["detect"],
                      failed_controls=[r["id"] for r in rows
                                       if r["id"] in ("C1", "C2") and r["result"] != "PASS"])


def a5_beside_t2(series, launch_list):
    """THESIS section 7: a steady rise of the gap after 2021 that has nothing
    to do with launches shows in every window, so T2 can fail with no launch
    step. A5 (each window less its own earlier pace) measures this and is
    printed beside T2. Reported here, never scored here: A5's own line is in
    12_alternatives.py."""
    r = L.pooled(series, launch_list, detrend=True)
    if r is None:
        return "; A5 beside T2: launch window not published yet"
    return (f"; A5 beside T2 (each window less its own earlier pace; reported, "
            f"not scored): S {r['s']:+.3f} pp; p {r['p']:.4f}")


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
        ls = launches(events, role)
        res = L.pooled(series, ls)
        row = score(test_id, rule, res, ok)
        if test_id == "T1":
            row["headline"] = t1_headline(row, res, rows)
        if test_id == "T2":
            row["note"] += a5_beside_t2(series, ls)
        rows.append(row)
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "tests.csv", "w", newline="", encoding="ascii") as f:
        w = csv.DictWriter(f, ["id", "statistic", "value", "line", "result", "note"],
                           lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            r = dict(r)
            if isinstance(r["value"], float):
                r["value"] = f"{r['value']:.4f}"
            w.writerow(r)
    t1 = next((r.get("headline") for r in rows if r["id"] == "T1"), None)
    with open(out_dir / "headline.txt", "w", encoding="ascii", newline="") as f:
        if t1:
            f.write(f"TITLE: {t1['title']}\nRESULT: {t1['result']}\n")
            if t1["t2"]:
                f.write(f"T2: {t1['t2']}\n")
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
        if r.get("headline"):
            h = r["headline"]
            print(f"      TITLE:  {h['title']}\n      RESULT: {h['result']}")
            if h["t2"]:
                print(f"      T2:     {h['t2']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

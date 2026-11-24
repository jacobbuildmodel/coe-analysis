"""
12_alternatives.py -- the sealed alternative specifications (ALTERNATIVES.md).

  python3 cdc/12_alternatives.py [--series out/series.csv] [--out out]

Each alternative changes one thing in the main specification to answer one
named referee objection, and is scored by the same rule as its test
(controls, gate D, the 0.5 line or p). Writes out/alternatives.csv and prints,
per test, how many alternatives give the same result as the main
specification. That share is reported beside the test. It is never a second
verdict.
"""
import argparse
import csv
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cdclib as L  # noqa: E402

_spec = importlib.util.spec_from_file_location("tests11", HERE / "11_tests.py")
T = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T)

# code: (objection answered, changes to the estimator, change to the launch list)
ALTS = {
    "A1": ("the window is too short", dict(post=3), None),
    "A2": ("the comparison rows are substitutes and some take vouchers",
           dict(comps=("1",)), None),
    "A3a": ("the geometric mean of two rows hides one of them (restaurants only)",
            dict(comps=("1.11.1",)), None),
    "A3b": ("the geometric mean of two rows hides one of them (fast food only)",
            dict(comps=("1.11.2",)), None),
    "A4": ("the placebo years hold a GST rise and the pandemic",
           dict(drop_years=(2007, 2020, 2021)), None),
    "A5": ("a fixed pre-2022 baseline ignores the trend", dict(detrend=True), None),
    "A6": ("the June 2026 launch followed an energy shock", {},
           lambda ls: [x for x in ls if x != (2026, 6)]),
    "A7": ("the June 2024 launch came on the 25th", {},
           lambda ls: [(2024, 7) if x == (2024, 6) else x for x in ls]),
}
PER_TEST = {
    "T1": ["A1", "A2", "A3a", "A3b", "A4", "A5", "A6", "A7"],
    "T2": ["A1", "A2", "A3a", "A3b", "A4", "A5", "A6", "A7"],
    "T3": ["A1", "A2", "A3a", "A3b", "A4", "A5"],
    "T4": ["A1", "A2", "A3a", "A3b", "A4", "A5"],
}


def run(series_path, events_path, out_dir):
    series, events = L.load_series(series_path), L.load_events(events_path)
    ok = all(c["result"] == "PASS" for c in T.controls(series))
    rows, summary = [], {}
    for test_id, role, rule in T.TESTS:
        base = T.launches(events, role)
        main = T.score(test_id, rule, L.pooled(series, base), ok)
        rows.append(dict(test=test_id, spec="main", objection="", result=main["result"],
                         value=main["value"], same_as_main="yes", note=main["note"]))
        same = 0
        for code in PER_TEST[test_id]:
            objection, kwargs, change = ALTS[code]
            ls = change(base) if change else base
            r = T.score(test_id, rule, L.pooled(series, ls, **kwargs), ok)
            keep = r["result"] == main["result"]
            same += keep
            rows.append(dict(test=test_id, spec=code, objection=objection,
                             result=r["result"], value=r["value"],
                             same_as_main="yes" if keep else "no", note=r["note"]))
        summary[test_id] = (main["result"], same, len(PER_TEST[test_id]))
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "alternatives.csv", "w", newline="", encoding="ascii") as f:
        w = csv.DictWriter(f, ["test", "spec", "objection", "result", "value",
                               "same_as_main", "note"], lineterminator="\n")
        w.writeheader()
        for r in rows:
            r = dict(r)
            if isinstance(r["value"], float):
                r["value"] = f"{r['value']:.4f}"
            w.writerow(r)
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", default=str(HERE / "out" / "series.csv"))
    ap.add_argument("--events", default=str(HERE / "events.csv"))
    ap.add_argument("--out", default=str(HERE / "out"))
    a = ap.parse_args()
    for test_id, (res, same, n) in run(a.series, a.events, pathlib.Path(a.out)).items():
        print(f"{test_id}: main {res}; {same} of {n} alternatives give the same result")
    return 0


if __name__ == "__main__":
    sys.exit(main())

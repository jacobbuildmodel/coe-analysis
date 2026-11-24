"""
test_pipeline.py -- steps 10, 11 and 12 end to end on invented data.

  python3 -m unittest discover -s cdc/tests -p "test_*.py" -v

Each scenario must come out as designed: no planted effect -> every test
holds; a planted 0.8 per cent step -> every test fails; too much noise or a
failed control -> nothing is scored. No real value is read.
"""
import csv
import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
CDC = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(CDC))
import make_fixtures  # noqa: E402


def run_pipeline(scenario, end=(2027, 2)):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"cdc_{scenario}_"))
    make_fixtures.build(tmp / "raw", scenario, end)
    for script, args in (("10_load.py", ["--raw", str(tmp / "raw"), "--out", str(tmp / "out")]),
                         ("11_tests.py", ["--series", str(tmp / "out" / "series.csv"),
                                          "--out", str(tmp / "out")]),
                         ("12_alternatives.py", ["--series", str(tmp / "out" / "series.csv"),
                                                 "--out", str(tmp / "out")])):
        r = subprocess.run([sys.executable, str(CDC / script)] + args,
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise AssertionError(f"{script} failed on {scenario}:\n{r.stdout}\n{r.stderr}")
    with open(tmp / "out" / "tests.csv", newline="", encoding="ascii") as f:
        tests = {r["id"]: r for r in csv.DictReader(f)}
    with open(tmp / "out" / "alternatives.csv", newline="", encoding="ascii") as f:
        alts = list(csv.DictReader(f))
    return tests, alts


class Pipeline(unittest.TestCase):
    def results(self, tests):
        return {k: v["result"] for k, v in tests.items()}

    def test_null_every_test_holds(self):
        tests, alts = run_pipeline("null")
        self.assertEqual(self.results(tests), {
            "C1": "PASS", "C2": "PASS", "T1": "HOLDS", "T2": "HOLDS",
            "T3": "HOLDS", "T4": "HOLDS"})
        main = [a for a in alts if a["spec"] == "main"]
        self.assertTrue(all(a["same_as_main"] == "yes" for a in main))
        self.assertIn("A5 beside T2", tests["T2"]["note"])
        self.assertNotIn("A5 beside T2", tests["T1"]["note"])

    def test_planted_every_test_fails(self):
        tests, alts = run_pipeline("planted")
        self.assertEqual(self.results(tests), {
            "C1": "PASS", "C2": "PASS", "T1": "FAILS", "T2": "FAILS",
            "T3": "FAILS", "T4": "FAILS"})
        self.assertGreater(float(tests["T1"]["value"]), 0.6)
        self.assertLess(float(tests["T1"]["value"]), 1.0)

    def test_forward_test_pending_before_its_months(self):
        tests, _ = run_pipeline("null", end=(2026, 10))
        self.assertEqual(tests["T4"]["result"], "PENDING")
        self.assertEqual(tests["T1"]["result"], "HOLDS")

    def test_noise_means_not_scored(self):
        tests, _ = run_pipeline("noisy")
        for t in ("T1", "T2", "T3"):
            self.assertEqual(tests[t]["result"], "NOT SCORED")
            self.assertIn("gate D", tests[t]["note"])
        self.assertIn(tests["T4"]["result"], ("HOLDS", "FAILS"))

    def test_failed_control_means_not_scored(self):
        for scenario, control in (("flat_power", "C1"), ("no_gst", "C2")):
            tests, _ = run_pipeline(scenario)
            self.assertEqual(tests[control]["result"], "FAIL")
            for t in ("T1", "T2", "T3", "T4"):
                self.assertEqual(tests[t]["result"], "NOT SCORED")
                self.assertIn("control", tests[t]["note"])

    def test_sign_and_size_of_the_estimator(self):
        spec = importlib.util.spec_from_file_location("cdclib", CDC / "cdclib.py")
        lib = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lib)
        flat = {(y, m): 100.0 for y in range(2005, 2027) for m in range(1, 13)}
        hawker = dict(flat)
        for ym in hawker:
            if ym >= (2024, 6):
                hawker[ym] = 101.0
        series = {"1.11.3": hawker, "1.11.1": dict(flat), "1.11.2": dict(flat)}
        res = lib.pooled(series, [(2024, 6)])
        self.assertAlmostEqual(res["s"], 1.0, places=9)
        self.assertEqual(res["placebo_n"], [17])
        self.assertEqual(lib.placebo_years(12, 1, 1), list(range(2005, 2021)))
        self.assertEqual(lib.placebo_years(1, 1, 1), list(range(2006, 2022)))
        self.assertEqual(lib.placebo_years(5, 1, 1), list(range(2005, 2022)))

    def test_placebo_years_main_and_a4(self):
        spec = importlib.util.spec_from_file_location("cdclib", CDC / "cdclib.py")
        lib = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lib)
        # Main specification (THESIS section 4, step 2).
        self.assertEqual(lib.placebo_years(12, 1, 1), list(range(2005, 2021)))  # 16
        self.assertEqual(lib.placebo_years(5, 1, 1), list(range(2005, 2022)))   # 17
        self.assertEqual(lib.placebo_years(6, 1, 1), list(range(2005, 2022)))   # 17
        self.assertEqual(lib.placebo_years(1, 1, 1), list(range(2006, 2022)))   # 16
        # A4: every placebo window with a month in 2007, 2020 or 2021 is
        # dropped, its first month included, so January 2008 (window 2007 Dec
        # to 2008 Feb) goes.
        drop = (2007, 2020, 2021)
        self.assertEqual(lib.placebo_years(1, 1, 1, drop_years=drop),
                         [2006] + list(range(2009, 2020)))
        self.assertNotIn(2008, lib.placebo_years(1, 1, 1, drop_years=drop))
        self.assertEqual(lib.placebo_years(12, 1, 1, drop_years=drop),
                         [2005] + list(range(2008, 2019)))
        for m in (5, 6):
            self.assertEqual(lib.placebo_years(m, 1, 1, drop_years=drop),
                             [2005, 2006] + list(range(2008, 2020)))


if __name__ == "__main__":
    unittest.main()

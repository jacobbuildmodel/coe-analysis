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
        for scenario, control in (("flat_power", "C1"), ("no_gst", "C2"), ("regime", "C2")):
            tests, _ = run_pipeline(scenario)
            self.assertEqual(tests[control]["result"], "FAIL")
            for t in ("T1", "T2", "T3", "T4"):
                self.assertEqual(tests[t]["result"], "NOT SCORED")
                self.assertIn("control", tests[t]["note"])

    def test_january_only_step_fails_t3_alone(self):
        tests, _ = run_pipeline("jan_only")
        self.assertEqual(self.results(tests), {
            "C1": "PASS", "C2": "PASS", "T1": "HOLDS", "T2": "HOLDS",
            "T3": "FAILS", "T4": "HOLDS"})

    def test_c2_is_the_restaurant_rows_less_their_earlier_pace(self):
        lib = _lib()
        flat = {(y, m): 100.0 for y in range(2005, 2027) for m in range(1, 13)}
        rest = {}
        for (y, m) in flat:   # 1 per cent a month faster from 2022, no step
            n = max(0, (y - 2022) * 12 + m) if y >= 2022 else 0
            rest[(y, m)] = 100.0 * 1.01 ** n
        series = {"1.11.3": dict(flat), "1.11.1": rest, "1.11.2": dict(rest)}
        both = dict(series, RESTAURANTS=lib.geometric_mean_row(series, lib.COMPARISON))
        res = lib.pooled(both, [(2023, 1), (2024, 1)], hawker="RESTAURANTS", comps=(), detrend=True)
        self.assertAlmostEqual(res["s"], 0.0, places=6)
        self.assertEqual(res["placebo_n"], [15, 15])
        stepped = {k: v * (1.01 if k >= (2023, 1) else 1.0) for k, v in flat.items()}
        series = {"1.11.3": dict(flat), "1.11.1": stepped, "1.11.2": dict(flat)}
        both = dict(series, RESTAURANTS=lib.geometric_mean_row(series, lib.COMPARISON))
        res = lib.pooled(both, [(2023, 1)], hawker="RESTAURANTS", comps=(), detrend=True)
        self.assertAlmostEqual(res["s"], 100.0 * (1.01 ** 0.5 - 1.0), places=6)

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


def _lib():
    spec = importlib.util.spec_from_file_location("cdclib", CDC / "cdclib.py")
    lib = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lib)
    return lib


class Headline(unittest.TestCase):
    """THESIS section 8: the sealed sentences and titles, on invented numbers."""

    def h(self, verdict, **kw):
        kw.setdefault("p", 0.30)
        kw.setdefault("m", 0.62)
        return _lib().headline(verdict, **kw)

    def test_every_title_within_100_characters(self):
        lib = _lib()
        self.assertEqual(len(set(lib.TITLES)), 4)
        for t in lib.TITLES:
            self.assertLessEqual(len(t), 100)

    def test_held_s045_w095(self):
        h = self.h("HOLDS", W=0.95, P=0.50, S=0.45)
        self.assertEqual(h["title"], _lib().TITLE_HELD)
        r = h["result"]
        self.assertIn("hawker prices rose by an average of 0.95 per cent against restaurant prices", r)
        self.assertIn("an average rise of 0.50 per cent", r)
        self.assertIn("0.45 percentage points more than usual, below the 0.5-point", r)
        self.assertTrue(r.endswith("so the thesis held."))
        self.assertNotIn("not its cause", r)

    def test_held_negative_s(self):
        h = self.h("HOLDS", W=0.10, P=0.40, S=-0.30)
        self.assertEqual(h["title"], _lib().TITLE_HELD)
        self.assertIn("hawker prices rose by an average of 0.10 per cent", h["result"])
        self.assertIn("0.30 percentage points less than usual, below", h["result"])
        self.assertNotIn("-0.", h["result"])
        h = self.h("HOLDS", W=-0.10, P=-0.40, S=0.30)
        self.assertIn("hawker prices fell by an average of 0.10 per cent", h["result"])
        self.assertIn("an average fall of 0.40 per cent", h["result"])
        self.assertIn("0.30 percentage points more than usual", h["result"])

    def test_held_with_a_step_takes_the_fifth_title(self):
        lib = _lib()
        h = self.h("HOLDS", W=0.50, P=0.20, S=0.30, p=0.01, m=0.62)
        self.assertEqual(h["title"], lib.TITLE_HELD_STEP)
        self.assertIn("turns up in 1.0 per cent of comparisons", h["t2"])
        self.assertIn("(p = 0.010), so a step showed;", h["t2"])
        self.assertIn("a step of 0.62 percentage points four times in five.", h["t2"])
        self.assertIn("the thesis held", h["result"])
        # a falling raw gap (case Bn): the same title, the result sentence says "fell"
        h = self.h("HOLDS", W=-0.20, P=-0.50, S=0.30, p=0.02)
        self.assertEqual(h["title"], lib.TITLE_HELD_STEP)
        self.assertIn("hawker prices fell by an average of 0.20 per cent", h["result"])
        # no step shown: the held title
        h = self.h("HOLDS", W=0.50, P=0.20, S=0.30, p=0.30)
        self.assertEqual(h["title"], lib.TITLE_HELD)
        self.assertIn("so no step showed beyond the usual swings;", h["t2"])
        self.assertIn("30.0 per cent", h["t2"])
        # p below 0.05 with S at or below 0 cannot take a title that says "above usual"
        self.assertEqual(self.h("HOLDS", W=0.0, P=0.0, S=0.0, p=0.04)["title"], lib.TITLE_HELD)

    def test_failed_one_title_for_both_signs_of_w(self):
        lib = _lib()
        for W, P, S in ((0.80, 0.20, 0.60), (0.30, -0.40, 0.70), (-0.20, -0.80, 0.60), (0.0, -0.60, 0.60)):
            h = self.h("FAILS", W=W, P=P, S=S)
            self.assertEqual(h["title"], lib.TITLE_FAILED)
            self.assertIn(f"{'rose' if W >= 0 else 'fell'} by an average of {abs(W):.2f} per cent",
                          h["result"])
            self.assertIn(f"{S:.2f} percentage points more than usual, at or above the 0.5-point",
                          h["result"])
            self.assertTrue(h["result"].endswith(
                "so the thesis failed. The index shows a step in the months the "
                "vouchers were issued, not its cause."))

    def test_t2_picks_only_between_the_two_held_titles(self):
        lib = _lib()
        for p in (0.001, 0.049, 0.05, 0.9):
            held = self.h("HOLDS", W=0.4, P=0.0, S=0.4, p=p)["title"]
            self.assertEqual(held, lib.TITLE_HELD_STEP if p < 0.05 else lib.TITLE_HELD)
            self.assertEqual(self.h("FAILS", W=0.6, P=0.0, S=0.6, p=p)["title"], lib.TITLE_FAILED)

    def test_not_scored_by_a_control(self):
        lib = _lib()
        h = self.h("NOT SCORED", failed_controls=["C1"])
        self.assertEqual(h["title"], lib.TITLE_NOT_SCORED)
        self.assertEqual((h["t2"], h["t3"]), ("", ""))
        self.assertIn("its electricity-tariff check, which shows whether", h["result"])
        self.assertIn("so the test cannot be relied on to see a step in hawker prices", h["result"])
        self.assertNotIn("this size", h["result"])
        self.assertNotIn("GST rises", h["result"])
        h = self.h("NOT SCORED", failed_controls=["C2"])
        self.assertIn("its GST check, which shows whether", h["result"])
        self.assertTrue(h["result"].endswith(
            "The GST rises that check looks for may have reached restaurant prices "
            "outside the December to February window, or not at all."))
        h = self.h("NOT SCORED", failed_controls=["C2", "C1"])
        self.assertIn("its electricity-tariff and GST checks, which show whether", h["result"])
        self.assertEqual(h["title"], lib.TITLE_NOT_SCORED)

    def test_not_scored_by_gate_d(self):
        lib = _lib()
        h = self.h("NOT SCORED", d=0.62)
        self.assertEqual(h["title"], lib.TITLE_NOT_SCORED)
        self.assertIn("only 62 per cent of the time, short of the 80 per cent required", h["result"])
        self.assertIn("cannot be relied on to see a step of that size", h["result"])
        self.assertIn("only 79.7 per cent", self.h("NOT SCORED", d=0.797)["result"])
        self.assertIn("only 79.96 per cent", self.h("NOT SCORED", d=0.7996)["result"])

    def test_no_printed_figure_reaches_a_bar_its_value_does_not(self):
        h = self.h("HOLDS", W=0.70, P=0.204, S=0.496)
        self.assertIn("0.496 percentage points more than usual, below", h["result"])
        h = self.h("HOLDS", W=0.70, P=0.2004, S=0.4996)
        self.assertIn("0.4996 percentage points more than usual, below", h["result"])
        h = self.h("FAILS", W=0.70, P=0.196, S=0.504)
        self.assertIn("0.50 percentage points more than usual, at or above", h["result"])
        h = self.h("HOLDS", W=0.0, P=0.496, S=-0.496)
        self.assertIn("0.496 percentage points less than usual", h["result"])
        h = self.h("HOLDS", W=0.4, P=0.1, S=0.3, p=0.0499)
        self.assertIn("turns up in 4.99 per cent", h["t2"])
        self.assertIn("(p = 0.0499), so a step showed", h["t2"])
        h = self.h("HOLDS", W=0.4, P=0.1, S=0.3, p=0.0501)
        self.assertIn("turns up in 5.0 per cent", h["t2"])
        self.assertIn("(p = 0.050), so no step showed", h["t2"])

    def test_t3_sentence_only_when_t3_differs(self):
        lib = _lib()
        same = self.h("HOLDS", W=0.4, P=0.1, S=0.3, t3=dict(verdict="HOLDS", S=0.2, d=0.9))
        self.assertEqual(same["t3"], "")
        self.assertEqual(self.h("HOLDS", W=0.4, P=0.1, S=0.3)["t3"], "")
        h = self.h("HOLDS", W=0.4, P=0.1, S=0.3, t3=dict(verdict="FAILS", S=0.97, d=0.9))
        self.assertTrue(h["t3"].startswith(
            "At the two January launches without a GST rise (January 2025 and January 2026), "
            "the same comparison came to an average of 0.97 percentage points more than usual "
            "for January (the Januaries of 2006 to 2021), at or above the 0.5-point step, so "
            "the prediction for those two launches failed; the index shows a step in those months, "
            "not its cause."))
        self.assertTrue(h["t3"].endswith("The title covers only the five launches outside January."))
        self.assertEqual(h["title"], lib.TITLE_HELD)
        h = self.h("FAILS", W=0.8, P=0.2, S=0.6, t3=dict(verdict="HOLDS", S=-0.4996, d=0.9))
        self.assertIn("0.4996 percentage points less than usual for January", h["t3"])
        self.assertIn("so the prediction for those two launches held.", h["t3"])
        h = self.h("HOLDS", W=0.4, P=0.1, S=0.3, t3=dict(verdict="NOT SCORED", S=0.1, d=0.797))
        self.assertIn("the test was not scored: it would catch an average step of 0.5 percentage "
                      "points only 79.7 per cent of the time", h["t3"])
        # T1 not scored: no T3 sentence beside "no verdict"
        self.assertEqual(self.h("NOT SCORED", d=0.6, t3=dict(verdict="HOLDS", S=0.1, d=0.9))["t3"], "")

    def test_11_tests_prints_the_same_text(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="cdc_headline_"))
        make_fixtures.build(tmp / "raw", "jan_only", (2027, 2))
        for script, args in (("10_load.py", ["--raw", str(tmp / "raw"), "--out", str(tmp / "out")]),
                             ("11_tests.py", ["--series", str(tmp / "out" / "series.csv"),
                                              "--out", str(tmp / "out")])):
            r = subprocess.run([sys.executable, str(CDC / script)] + args,
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        txt = (tmp / "out" / "headline.txt").read_text(encoding="ascii")
        self.assertIn("TITLE: " + _lib().TITLE_HELD, txt)
        self.assertIn("RESULT: At the five CDC voucher launches", txt)
        self.assertIn("so the thesis held.", txt)
        self.assertIn("T2: A difference this large", txt)
        self.assertIn("T3: At the two January launches without a GST rise", txt)
        self.assertIn("so the prediction for those two launches failed", txt)
        self.assertIn("TITLE:  " + _lib().TITLE_HELD, r.stdout)


if __name__ == "__main__":
    unittest.main()

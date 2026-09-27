"""
test_pipeline.py -- the PWM analysis on synthetic data only.

  python3 -m unittest discover -s pwm/tests -p "test_*.py" -v

Every number is invented (tests/fixtures/, tests/make_fixtures.py). Three
kinds of test:
  * the guard: nothing reads pwm/raw/ before pwm/SEALED exists;
  * end to end: steps 10-15 on a copy of the fixtures, twice, byte-identical,
    with the checksum and reproduction checks catching tampering;
  * branches: each outcome of T1-T5, every verdict branch, the scorecard and
    the T4 priority rule, forced by moving the invented numbers.
"""
import contextlib
import importlib.util
import io
import math
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
PWM = os.path.dirname(HERE)
FIX = os.path.join(HERE, "fixtures")
sys.path.insert(0, PWM)

import pwmlib as L  # noqa: E402


def mod(name):
    spec = importlib.util.spec_from_file_location(name.replace(".py", "").replace("1", "m1", 1),
                                                  os.path.join(PWM, name))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


LOAD, TESTS = mod("10_load.py"), mod("11_tests.py")


def rb(path):
    with open(path, "rb") as f:
        return f.read()


def rt(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def wt(path, text, mode="w"):
    with open(path, mode, encoding="utf-8", newline="") as f:
        f.write(text)


def csv_rows(path):
    import csv
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def step(script, root, *extra):
    return subprocess.run([sys.executable, os.path.join(PWM, script), "--root", root, *extra],
                          capture_output=True, text=True)


def copy_fixtures(dst):
    shutil.copytree(FIX, dst)
    return dst


class Guard(unittest.TestCase):
    def test_loader_refuses_real_raw_before_seal(self):
        self.assertFalse(os.path.exists(L.SEALED), "pwm/SEALED exists: the suite runs before the seal only")
        for script in ("10_load.py", "15_reproduce.py"):
            r = subprocess.run([sys.executable, os.path.join(PWM, script)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 3, script)
            self.assertIn("REFUSED", r.stderr)

    def test_guard_logic(self):
        with tempfile.TemporaryDirectory() as d:
            real, sealed = os.path.join(d, "raw"), os.path.join(d, "SEALED")
            os.makedirs(real)
            old = (L.REAL_RAW, L.SEALED)
            try:
                L.REAL_RAW, L.SEALED = os.path.realpath(real), sealed
                with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                    L.guard(real)
                open(sealed, "w").close()
                self.assertEqual(L.guard(real), real)
                self.assertEqual(L.guard(FIX), FIX)
            finally:
                L.REAL_RAW, L.SEALED = old


class EndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.root = copy_fixtures(os.path.join(cls.tmp, "a"))
        for s in ("10_load.py", "11_tests.py", "12_figures.py", "13_results.py", "15_reproduce.py"):
            r = step(s, cls.root)
            assert r.returncode == 0, (s, r.stdout, r.stderr)
        r = step("14_manifest.py", cls.root)
        assert r.returncode == 0, r.stderr

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def T(self, root=None):
        return {r["key"]: r["value"] for r in L.read_csv(os.path.join(root or self.root, "out", "tests.csv"))}

    def test_base_fixture_outcomes(self):
        T = self.T()
        for t in ("T1", "T2", "T3", "T4", "T5"):
            self.assertEqual(T[f"{t}_outcome"], "SURVIVE", t)
        self.assertEqual(T["verdict"], "Covered jobs look more like monopsony; the rest of the bottom kept pace.")
        self.assertEqual(T["T4_series"], "workers")
        self.assertTrue(T["T4_cleaning_status"].startswith("described, not scored"))
        self.assertEqual(T["T4_industries_scored"], "security landscape")
        self.assertAlmostEqual(float(T["expected_held"]), 2.55)

    def test_check_passes_and_catches_tampering(self):
        self.assertEqual(step("14_manifest.py", self.root, "--check").returncode, 0)
        other = copy_fixtures(os.path.join(self.tmp, "tamper"))
        shutil.copytree(os.path.join(self.root, "out"), os.path.join(other, "out"))
        shutil.copytree(os.path.join(self.root, "figs"), os.path.join(other, "figs"))
        for f in ("RESULTS.md", "number_manifest.csv", "CHECKSUMS.md5"):
            shutil.copy(os.path.join(self.root, f), other)
        wt(os.path.join(other, "RESULTS.md"), "tampered\n", "a")
        r = step("14_manifest.py", other, "--check")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("MISMATCH RESULTS.md", r.stdout)
        # reproduction catches a changed number in tests.csv
        p = os.path.join(other, "out", "tests.csv")
        wt(p, rt(p).replace("T2_pooled,0.15", "T2_pooled,0.25", 1))
        r = step("15_reproduce.py", other)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("DIFFERS T2_pooled", r.stdout)

    def test_deterministic_and_formatted(self):
        second = copy_fixtures(os.path.join(self.tmp, "b"))
        for s in ("10_load.py", "11_tests.py", "12_figures.py", "13_results.py"):
            self.assertEqual(step(s, second).returncode, 0, s)
        for sub in ("out", "figs"):
            for f in sorted(os.listdir(os.path.join(self.root, sub))):
                a = rb(os.path.join(self.root, sub, f))
                b = rb(os.path.join(second, sub, f))
                self.assertEqual(a, b, f"{sub}/{f} differs between two runs")
                self.assertNotIn(b"\r\n", a, f)
                a.decode("ascii")
        self.assertEqual(rb(os.path.join(self.root, "RESULTS.md")), rb(os.path.join(second, "RESULTS.md")))
        for r in L.read_csv(os.path.join(self.root, "out", "tests.csv")):
            try:
                v = float(r["value"])
            except ValueError:
                continue
            self.assertEqual(r["value"], L.FLOAT % v if r["value"] not in ("True", "False") else r["value"])

    def test_no_t4_series_as_in_the_real_data(self):
        """The real case: no workers count, no qualifying LFS lines."""
        root = copy_fixtures(os.path.join(self.tmp, "no_t4"))
        os.remove(os.path.join(root, "raw", "w2x_workers_by_industry_assumed.csv"))
        os.remove(os.path.join(root, "T4_LFS_LINES.csv"))
        for s in ("10_load.py", "11_tests.py", "12_figures.py", "13_results.py", "15_reproduce.py"):
            self.assertEqual(step(s, root).returncode, 0, s)
        T = self.T(root)
        self.assertEqual((T["T4_outcome"], T["T4_series"]), ("NOT SCORED", "none"))
        self.assertEqual(T["verdict"], "The record cannot tell the two models apart; the rest of the bottom kept pace.")
        self.assertEqual((T["scored_tests"], T["n_scored"], T["conf_T4"]), ("T1 T2 T3 T5", "4", "not scored"))
        self.assertAlmostEqual(float(T["expected_held"]), 1.95)
        md = rt(os.path.join(root, "RESULTS.md"))
        self.assertIn(L.GAP, md)
        self.assertNotIn("monopsony-like", md)

    def test_results_failures_first_and_synthetic_stamp(self):
        md = rt(os.path.join(self.root, "RESULTS.md"))
        self.assertTrue(md.startswith("# SYNTHETIC FIXTURE RUN"))
        self.assertLess(md.index("## Tests that did not survive"), md.index("## Tests that survived"))

    def test_every_listed_sensitivity_reported(self):
        sens = L.read_csv(os.path.join(self.root, "out", "sensitivities.csv"))
        variants = {(r["test"], r["variant"]) for r in sens}
        for v in [("T1", "without June 2009"), ("T1", "Junes after the last pre-period break"),
                  ("T1", "2007-2008 added"), ("T2", "basic instead of gross"),
                  ("T2", "median instead of 25th percentile"), ("T2", "dropping 2022"),
                  ("T2", "first transition June counted as post"),
                  ("T2", "all successors of a grade split averaged"), ("T2", "Number Covered weights"),
                  ("T2", "2007-2008 added"), ("T4", "lfs series"), ("T5", "all successors averaged")]:
            self.assertIn(v, variants)
        loo = [v for t, v in variants if v.startswith("leaving out")]
        self.assertEqual(len(loo), 8)


class Branches(unittest.TestCase):
    """Force each outcome by moving the invented numbers in memory."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        root = copy_fixtures(os.path.join(cls.tmp, "r"))
        assert step("10_load.py", root).returncode == 0
        cls.base = TESTS.load(os.path.join(root, "out"))
        cls.conf = TESTS.confidences(os.path.join(root, "THESIS.md"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def data(self):
        lines, lfs, t4s, t4c = self.base
        return lines.copy(), lfs.copy(), t4s.copy(), dict(t4c)

    def run_(self, lines, lfs, t4s, t4c, conf=None):
        T, *_ = TESTS.run(lines, lfs, t4s, t4c, conf if conf is not None else self.conf)
        return T

    @staticmethod
    def shift(lines, group, years, dlog, measures=("p25_gross", "p25_basic", "med_gross")):
        m = (lines["group"] == group) & lines["june"].isin(list(years))
        for c in measures:
            lines.loc[m, c] = lines.loc[m, c] * math.exp(dlog)

    @staticmethod
    def trend(lines, group, years, per_year):
        for y in years:
            Branches.shift(lines, group, [y], per_year * (y - 2009))

    # ---- T1
    def test_t1_fails_for_one_group(self):
        lines, *rest = self.data()
        self.trend(lines, "security", L.PRE["security"], 0.02)
        T = self.run_(lines, *rest)
        self.assertEqual(T["T1_outcome"], "FAIL")
        self.assertEqual(T["T1_security_pass"], False)
        self.assertEqual(T["T2_groups_scored"], "cleaning landscape")
        self.assertNotIn("T2_security_est", T)
        self.assertFalse(any(k.startswith("T5_security") for k in T))
        self.assertNotEqual(T["verdict_A"], "the record cannot say what the ladder did")

    def test_t1_fails_for_every_group(self):
        lines, *rest = self.data()
        for g in L.COVERED:
            self.trend(lines, g, L.PRE[g], 0.03)
        T = self.run_(lines, *rest)
        self.assertEqual((T["T1_outcome"], T["T2_outcome"], T["T5_outcome"]), ("FAIL", "NOT SCORED", "NOT SCORED"))
        self.assertEqual(T["verdict_A"], "the record cannot say what the ladder did")
        self.assertNotIn("T2", T["scored_tests"].split())

    def test_t1_cannot_run(self):
        lines, *rest = self.data()
        lines = lines[~lines["june"].isin([2009, 2010, 2011])]
        T = self.run_(lines, *rest)
        self.assertEqual((T["T1_outcome"], T["T2_outcome"], T["T5_outcome"]), ("NOT SCORED",) * 3)
        self.assertEqual(T["verdict_A"], "the record cannot say what the ladder did")

    # ---- T2
    def test_t2_inconclusive(self):
        lines, *rest = self.data()
        for g in L.COVERED:
            self.shift(lines, g, L.POST[g], -0.08)
        T = self.run_(lines, *rest)
        self.assertEqual(T["T2_outcome"], "INCONCLUSIVE")
        self.assertTrue(0.05 <= float(T["T2_pooled"]) < 0.10)
        self.assertEqual(T["verdict_A"], "the record cannot tell the two models apart")

    def test_t2_fails_on_pooled(self):
        lines, *rest = self.data()
        for g in L.COVERED:
            self.shift(lines, g, L.POST[g], -0.12)
        T = self.run_(lines, *rest)
        self.assertEqual(T["T2_outcome"], "FAIL")
        self.assertEqual(T["verdict_A"],
                         "the ladder did not measurably lift pay at the bottom of the jobs it covered")

    def test_t2_fails_on_one_group_at_or_below_zero(self):
        lines, *rest = self.data()
        self.shift(lines, "security", L.POST["security"], -0.2)
        for g in ("cleaning", "landscape"):
            self.shift(lines, g, L.POST[g], 0.1)
        T = self.run_(lines, *rest)
        self.assertGreaterEqual(float(T["T2_pooled"]), 0.10)
        self.assertLessEqual(float(T["T2_security_est"]), 0)
        self.assertEqual(T["T2_outcome"], "FAIL")

    # ---- T3
    def test_t3_fails(self):
        lines, *rest = self.data()
        for c in lines.loc[lines["side"] == "comparison", "group"].unique():
            self.shift(lines, c, [2017, 2018, 2019], -0.1)
        T = self.run_(lines, *rest)
        self.assertEqual(T["T3_outcome"], "FAIL")
        self.assertEqual(T["verdict_B"], "the rest of the bottom fell behind")

    def test_t3_not_computable(self):
        lines, lfs, t4s, t4c = self.data()
        lfs = lfs[~lfs["year"].isin([2017, 2018, 2019])]
        T = self.run_(lines, lfs, t4s, t4c)
        self.assertEqual(T["T3_outcome"], "NOT SCORED")
        self.assertEqual(T["verdict_B"], "the record cannot say whether the rest of the bottom kept pace")
        self.assertNotIn("T3", T["scored_tests"].split())

    # ---- T4
    def t4mod(self, unit, years, factor, t4s):
        m = (t4s["series"] == "workers") & (t4s["unit"] == unit) & t4s["year"].isin(list(years))
        t4s.loc[m, "count"] = t4s.loc[m, "count"] * factor
        return t4s

    def test_t4_not_scored_gives_cannot_tell_apart(self):
        lines, lfs, t4s, t4c = self.data()
        t4c["main"], t4c["sensitivity"] = "none", "none"
        T = self.run_(lines, lfs, t4s, t4c)
        self.assertEqual(T["T4_outcome"], "NOT SCORED")
        self.assertEqual(T["T2_outcome"], "SURVIVE")
        self.assertEqual(T["verdict_A"], "the record cannot tell the two models apart")
        self.assertNotIn("T4", T["scored_tests"].split())

    def test_t4_fails_gives_competitive(self):
        lines, lfs, t4s, t4c = self.data()
        t4s = self.t4mod("security", L.POST["security"], 0.85, t4s)
        T = self.run_(lines, lfs, t4s, t4c)
        self.assertEqual(T["T4_outcome"], "FAIL")
        self.assertEqual(T["verdict_A"], "covered jobs look more like a competitive market")

    def test_t4_inconclusive(self):
        lines, lfs, t4s, t4c = self.data()
        t4s = self.t4mod("security", L.POST["security"], 0.93, t4s)
        T = self.run_(lines, lfs, t4s, t4c)
        self.assertEqual(T["T4_outcome"], "INCONCLUSIVE")
        self.assertEqual(T["verdict_A"], "the record cannot tell the two models apart")

    def test_t4_survives_below_zero_is_not_monopsony(self):
        lines, lfs, t4s, t4c = self.data()
        t4s = self.t4mod("landscape", L.POST["landscape"], 0.975, t4s)
        T = self.run_(lines, lfs, t4s, t4c)
        self.assertEqual(T["T4_outcome"], "SURVIVE")
        self.assertLess(float(T["T4_landscape_est"]), 0)
        self.assertEqual(T["verdict_A"], "the record cannot tell the two models apart")

    def test_t4_pretrend_drops_an_industry(self):
        lines, lfs, t4s, t4c = self.data()
        for y in range(2010, 2015):
            t4s = self.t4mod("security", [y], math.exp(0.05 * (y - 2010)), t4s)
        T = self.run_(lines, lfs, t4s, t4c)
        self.assertEqual(T["T4_security_status"], "dropped: pre-trend")
        self.assertEqual(T["T4_industries_scored"], "landscape")

    def test_t4_every_industry_fails_pretrend(self):
        lines, lfs, t4s, t4c = self.data()
        for g in ("security", "landscape"):
            for y in range(2010, 2015):
                t4s = self.t4mod(g, [y], math.exp(0.05 * (y - 2010)), t4s)
        T = self.run_(lines, lfs, t4s, t4c)
        self.assertEqual(T["T4_outcome"], "NOT SCORED")

    # ---- T5
    def test_t5_fails(self):
        lines, *rest = self.data()
        self.shift(lines, "cleaning", [2022], math.log(0.9), measures=("p25_basic",))
        T = self.run_(lines, *rest)
        self.assertEqual(T["T5_outcome"], "FAIL")
        self.assertLess(float(T["T5_cleaning_2022_ratio"]), 0.97)
        self.assertEqual(T["T2_outcome"], "SURVIVE")

    def test_t5_missing_basic_drops_title_then_fails_if_none_left(self):
        lines, *rest = self.data()
        m = (lines["group"] == "security") & (lines["june"] == 2018) & (lines["series"] == "main")
        lines.loc[m, "p25_basic"] = float("nan")
        T = self.run_(lines, *rest)
        self.assertNotIn("T5_security_2018_ratio", T)
        self.assertEqual(T["T5_outcome"], "FAIL")
        self.assertEqual(T["T2_outcome"], "SURVIVE")        # T2 reads gross: untouched

    # ---- missing-year rule
    def test_missing_year_drops_title_everywhere(self):
        lines, *rest = self.data()
        m = (lines["group"] == "C waiter") & (lines["june"] == 2017)
        lines.loc[m, "p25_gross"] = float("nan")
        _, dropped = TESTS.select(lines)
        self.assertEqual([d[1] for d in dropped], ["51312"])
        rows, _ = TESTS.select(lines)
        self.assertEqual(int(((rows["group"] == "C waiter")).sum()), 1)   # only 2009's 51230 left

    # ---- scorecard
    def test_scorecard(self):
        lines, *rest = self.data()
        for g in L.COVERED:
            self.shift(lines, g, L.POST[g], -0.12)
        T = self.run_(lines, *rest)
        held = [t for t in ("T1", "T2", "T3", "T4", "T5") if T[f"{t}_outcome"] == "SURVIVE"]
        self.assertEqual(int(T["n_held"]), len(held))
        conf = {"T1": .4, "T2": .5, "T3": .6, "T4": .6, "T5": .45}
        want = sum((conf[t] - (t in held)) ** 2 for t in conf) / 5
        self.assertAlmostEqual(float(T["brier"]), want)
        T = self.run_(lines, *rest, conf={t: None for t in conf})
        self.assertTrue(str(T["brier"]).startswith("not set"))

    def test_confidences_read_from_thesis(self):
        self.assertEqual(TESTS.confidences(os.path.join(PWM, "THESIS.md")),
                         {t: None for t in ("T1", "T2", "T3", "T4", "T5")})
        self.assertEqual(self.conf, {"T1": .4, "T2": .5, "T3": .6, "T4": .6, "T5": .45})


class T4Priority(unittest.TestCase):
    """The THESIS section 4 priority rule, on small invented raw folders."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.raw = os.path.join(self.tmp, "raw")
        os.makedirs(self.raw)
        for f in ("w2a_services_detailed_industry.csv", "w2x_workers_by_industry_assumed.csv",
                  "w2b_lfs_occupation_status.csv"):
            shutil.copy(os.path.join(FIX, "raw", f), self.raw)
        self.lines = os.path.join(self.tmp, "T4_LFS_LINES.csv")
        shutil.copy(os.path.join(FIX, "T4_LFS_LINES.csv"), self.lines)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def roles(self):
        _, choice, roles = LOAD.load_t4(self.raw, self.lines)
        return dict((k, v) for k, v in roles), {(c[0], c[3]): c[6] for c in choice}

    def restrict_workers(self, first):
        p = os.path.join(self.raw, "w2x_workers_by_industry_assumed.csv")
        rows = csv_rows(p)
        keep = [0] + [i for i, h in enumerate(rows[0]) if h.isdigit() and int(h) >= first]
        with open(p, "w", newline="") as f:
            __import__("csv").writer(f, lineterminator="\n").writerows([[r[i] for i in keep] for r in rows])

    def test_both_qualify_workers_main_lfs_sensitivity(self):
        r, adm = self.roles()
        self.assertEqual((r["main"], r["sensitivity"]), ("workers", "lfs"))
        self.assertFalse(adm[("workers", "cleaning")])
        self.assertTrue(adm[("workers", "security")])

    def test_only_lfs_is_main(self):
        os.remove(os.path.join(self.raw, "w2x_workers_by_industry_assumed.csv"))
        r, _ = self.roles()
        self.assertEqual((r["main"], r["sensitivity"]), ("lfs", "none"))

    def test_workers_too_short_falls_to_lfs(self):
        self.restrict_workers(2012)
        r, adm = self.roles()
        self.assertFalse(r["workers_qualifies"])
        self.assertEqual(r["main"], "lfs")

    def test_neither_not_scored(self):
        os.remove(os.path.join(self.raw, "w2x_workers_by_industry_assumed.csv"))
        wt(self.lines, "file,unit,occupation_column,occupation,count_column,filters\n")
        r, _ = self.roles()
        self.assertEqual((r["main"], r["sensitivity"]), ("none", "none"))

    def test_w2a_without_workers_block_is_not_a_candidate(self):
        os.remove(os.path.join(self.raw, "w2x_workers_by_industry_assumed.csv"))
        self.assertIsNone(LOAD.workers_candidates(self.raw))

    def test_series_from_2009_admits_cleaning(self):
        p = os.path.join(self.raw, "w2x_workers_by_industry_assumed.csv")
        rows = csv_rows(p)
        rows[0].append("2009")
        for r in rows[1:]:
            r.append(r[-1])
        with open(p, "w", newline="") as f:
            __import__("csv").writer(f, lineterminator="\n").writerows(rows)
        _, adm = self.roles()
        self.assertTrue(adm[("workers", "cleaning")])

    def test_two_workers_candidates_refused(self):
        shutil.copy(os.path.join(self.raw, "w2x_workers_by_industry_assumed.csv"),
                    os.path.join(self.raw, "w2f_copy.csv"))
        with self.assertRaises(AssertionError):
            LOAD.workers_candidates(self.raw)


class Loader(unittest.TestCase):
    def test_suppression_marks_are_missing(self):
        self.assertTrue(math.isnan(LOAD.number("-")))
        self.assertTrue(math.isnan(LOAD.number("s")))
        self.assertEqual(LOAD.number("1,234"), 1234.0)

    def test_every_fixture_june_parsed_from_headers(self):
        with tempfile.TemporaryDirectory() as d:
            root = copy_fixtures(os.path.join(d, "r"))
            self.assertEqual(step("10_load.py", root).returncode, 0)
            log = L.read_csv(os.path.join(root, "out", "load_log.csv"))
            self.assertEqual(sorted({int(r["june"]) for r in log}), list(range(2009, 2026)))
            for r in log:
                self.assertIn("p25_", r["columns"])


if __name__ == "__main__":
    unittest.main()

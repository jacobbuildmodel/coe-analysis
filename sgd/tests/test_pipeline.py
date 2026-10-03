"""
test_pipeline.py -- the sgd analysis on synthetic data only.

  python3 -m unittest discover -s sgd/tests -p "test_*.py" -v

Every number is invented (tests/make_fixtures.py builds the raw files in a
temporary directory). Three kinds of test:
  * the guard: nothing reads sgd/raw/ before sgd/SEALED exists;
  * end to end: steps 10-15 on a fixture, twice, byte-identical, with the
    checksum and reproduction checks catching tampering;
  * branches: each outcome of T1, T2, T3, T4 and T7, gate C passing and
    failing, every verdict branch and the scorecard, forced by moving the
    invented numbers.
"""
import contextlib
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SGD = os.path.dirname(HERE)
sys.path.insert(0, SGD)
sys.path.insert(0, HERE)

import sgdlib as L  # noqa: E402
import make_fixtures as F  # noqa: E402


def mod(name):
    spec = importlib.util.spec_from_file_location("m_" + name.replace(".py", ""), os.path.join(SGD, name))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


TESTS = mod("11_tests.py")


def step(script, root=None, *extra):
    cmd = [sys.executable, os.path.join(SGD, script)] + (["--root", root] if root else []) + list(extra)
    return subprocess.run(cmd, capture_output=True, text=True)


def run_through(root, last="11_tests.py"):
    for s in ("10_load.py", "11_tests.py", "12_figures.py", "13_results.py"):
        r = step(s, root)
        if r.returncode:
            raise AssertionError(f"{s} failed: {r.stderr[-800:]}")
        if s == last:
            break
    return {r["key"]: r["value"] for r in L.read_csv(os.path.join(root, "out", "tests.csv"))}


class Tmp(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="sgd_test_")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def build(self, name="fx", **knobs):
        return F.build(os.path.join(self.tmp, name), **knobs)


class Guard(unittest.TestCase):
    @unittest.skipIf(os.path.exists(L.SEALED), "sgd/SEALED exists: the real-path refusal is checked "
                                                "before the seal only; test_guard_logic still covers the rule")
    def test_refuses_real_raw_before_seal(self):
        for script in ("10_load.py", "15_reproduce.py"):
            r = step(script)
            self.assertEqual(r.returncode, 3, script)
            self.assertIn("REFUSED", r.stderr)

    def test_guard_logic(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(L.guard(d), d)
        with mock.patch.object(L, "SEALED", os.path.join(SGD, "__no_such_file__")):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as e:
                    L.guard(os.path.join(SGD, "raw"))
        self.assertEqual(e.exception.code, 3)


class EndToEnd(Tmp):
    def full(self, root):
        for s in ("10_load.py", "11_tests.py", "12_figures.py", "13_results.py"):
            r = step(s, root)
            self.assertEqual(r.returncode, 0, f"{s}: {r.stderr[-800:]}")
        self.assertEqual(step("14_manifest.py", root).returncode, 0)
        r = step("14_manifest.py", root, "--check")
        self.assertEqual(r.returncode, 0, r.stdout)
        r = step("15_reproduce.py", root)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn(", 0 differ", r.stdout)

    def test_full_run_twice_identical(self):
        a, b = self.build("a"), self.build("b")
        self.full(a)
        self.full(b)
        files = sorted(os.path.relpath(os.path.join(d, f), a) for d, _, fs in os.walk(a) for f in fs
                       if not d.startswith(os.path.join(a, "raw")) and not f.endswith(".md5"))
        self.assertTrue(any(f.endswith(".svg") for f in files))
        for f in files:
            with open(os.path.join(a, f), "rb") as x, open(os.path.join(b, f), "rb") as y:
                self.assertEqual(x.read(), y.read(), f)
        with open(os.path.join(a, "RESULTS.md"), encoding="utf-8") as fh:
            self.assertTrue(fh.readline().startswith("# SYNTHETIC FIXTURE RUN"))

    def test_tampering_is_caught(self):
        a = self.build()
        self.full(a)
        with open(os.path.join(a, "RESULTS.md"), "a", encoding="utf-8") as fh:
            fh.write("\nedited\n")
        self.assertNotEqual(step("14_manifest.py", a, "--check").returncode, 0)
        path = os.path.join(a, "out", "tests.csv")
        with open(path, encoding="utf-8") as fh:
            rows = fh.read().replace("T2_P,0.", "T2_P,9.", 1)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(rows)
        r = step("15_reproduce.py", a)
        self.assertEqual(r.returncode, 1)
        self.assertIn("DIFFERS T2_P", r.stdout)


class Branches(Tmp):
    def test_default_all_survive(self):
        R = run_through(self.build())
        for t in L.SCORED:
            self.assertEqual(R[f"{t}_outcome"], "SURVIVE", t)
        self.assertEqual(R["gateC_pass"], "True")
        self.assertEqual(R["verdict_A_yen"],
                         "most of the Singapore dollar's rise against the yen was the yen falling against everyone")
        self.assertEqual(R["verdict_B"], "the broad path followed MAS's decisions more closely than growth")
        self.assertAlmostEqual(float(R["T2_S"]) + float(R["T2_P"]) + float(R["T2_R"]), 1.0, places=6)

    def test_t1_fail_gates_share_tests(self):
        R = run_through(self.build(mas_bias=0.01))
        self.assertEqual(R["T1_outcome"], "FAIL")
        for t, name in (("T2", "yen"), ("T3", "ringgit")):
            self.assertEqual(R[f"{t}_outcome"], "NOT SCORED")
            self.assertIn("T1", R[f"{t}_reason"])
        self.assertEqual(R["verdict_A_yen"], "the record cannot split the Singapore dollar's rise against the yen")

    def test_t2_premise_false(self):
        R = run_through(self.build(jpy_scored=0.6))
        self.assertEqual(R["T2_outcome"], "NOT SCORED")
        self.assertTrue(R["T2_reason"].startswith("premise false"))
        self.assertEqual(R["T2_S"], "")
        self.assertEqual(R["verdict_A_yen"], "the Singapore dollar did not rise against the yen")

    def test_t2_fail(self):
        R = run_through(self.build(jpy_scored=-0.1, k_p=0.08))
        self.assertEqual(R["T2_outcome"], "FAIL")
        self.assertIn("Singapore dollar rising against everyone", R["verdict_A_yen"])

    def test_t2_inconclusive_rule(self):
        R = {"T1_scored_JPY_ok": True}
        fake = {"b": 0.1, "s": 0.04, "nx": -0.045, "e": 0.015, "S": 0.40, "P": 0.45, "R": 0.15}
        W = {"scored": ("2021-01", "2025-12", L.SCORED_START, L.SCORED_END)}
        with mock.patch.object(TESTS, "split", return_value=fake):
            TESTS.share_test({}, W, R, "T2", "JPY")
        self.assertEqual(R["T2_outcome"], "INCONCLUSIVE")

    def test_t4_fail_and_inconclusive(self):
        self.assertEqual(run_through(self.build("f", sgd_vol=0.03))["T4_outcome"], "FAIL")
        self.assertEqual(run_through(self.build("i", sgd_vol=0.011))["T4_outcome"], "INCONCLUSIVE")

    def test_t4_missing_series(self):
        R = run_through(self.build("one", drop_areas=("KR",)))
        self.assertEqual(R["T4_present"], "10")
        self.assertEqual(R["T4_outcome"], "SURVIVE")
        R = run_through(self.build("three", drop_areas=("KR", "TH", "ID")))
        self.assertEqual(R["T4_outcome"], "NOT SCORED")

    def test_gate_c_fails_on_noise_and_on_short_overlap(self):
        for name, kw in (("noise", {"sneer_noise": 0.01}), ("short", {"sneer_from": "2024-01-05"})):
            R = run_through(self.build(name, **kw))
            self.assertEqual(R["gateC_pass"], "False", name)
            self.assertEqual(R["T4_outcome"], "NOT SCORED", name)
            self.assertEqual(R["T7_outcome"], "NOT SCORED", name)
            self.assertEqual(R["verdict_B"], "the record cannot say whether the broad path followed MAS or growth")
            self.assertEqual(R["verdict_T4"], "the record cannot say whether the Singapore dollar was the steadiest")
            for t in ("T1", "T2", "T3"):
                self.assertNotEqual(R[f"{t}_outcome"], "NOT SCORED", name)
        self.assertLess(int(run_through(self.build("s2", sneer_from="2024-01-05"))["gateC_changes"]), L.GATE_MIN)

    def test_t7_fail_and_inconclusive(self):
        self.assertEqual(run_through(self.build("f", k_p=0.0, k_g=0.01))["T7_outcome"], "FAIL")
        R = run_through(self.build("i", k_p=0.01))
        self.assertEqual(R["T7_outcome"], "INCONCLUSIVE")
        self.assertIn("by less than the line", R["verdict_B"])

    def thesis_with(self, root, confs):
        """A copy of THESIS.md in the fixture root with the five confidences
        set to `confs` (percent strings), or to [JACOB] when confs is None."""
        import re
        with open(os.path.join(SGD, "THESIS.md"), encoding="utf-8") as fh:
            text = fh.read()
        pat = re.compile(r"\*\*Confidence at seal: (?:\[JACOB\]\.|\d+(?:\.\d+)?%)\*\*")
        self.assertEqual(len(pat.findall(text)), 5)
        vals = iter(confs or ["[JACOB]"] * 5)
        text = pat.sub(lambda m: "**Confidence at seal: " + (lambda v: v + "." if v == "[JACOB]" else v + "%")(
            next(vals)) + "**", text)
        with open(os.path.join(root, "THESIS.md"), "w", encoding="utf-8") as fh:
            fh.write(text)

    def test_scorecard_with_and_without_confidences(self):
        root = self.build()
        self.thesis_with(root, None)
        R = run_through(root)
        self.assertEqual(R["expected_held"], "")
        self.assertEqual(R["conf_T1"], "[JACOB]")
        self.thesis_with(root, ["60", "70", "25", "65", "65"])
        R = run_through(root)
        conf = [0.60, 0.70, 0.25, 0.65, 0.65]
        self.assertAlmostEqual(float(R["expected_held"]), sum(conf), places=6)
        brier = sum((c - 1) ** 2 for c in conf) / 5          # all five survive in the default fixture
        self.assertAlmostEqual(float(R["brier"]), brier, places=6)
        self.assertEqual(R["n_scored"], "5")

    def test_not_scored_drops_out_of_count_and_brier(self):
        root = self.build(jpy_scored=0.6)                     # T2's premise false: T2 not scored
        self.thesis_with(root, ["50", "90", "40", "80", "30"])
        R = run_through(root)
        scored = R["scored_tests"].split()
        self.assertNotIn("T2", scored)
        conf = {"T1": 0.50, "T3": 0.40, "T4": 0.80, "T7": 0.30}
        self.assertAlmostEqual(float(R["expected_held"]), sum(conf[t] for t in scored), places=6)
        brier = sum((conf[t] - (R[t + "_outcome"] == "SURVIVE")) ** 2 for t in scored) / len(scored)
        self.assertAlmostEqual(float(R["brier"]), brier, places=6)


class Units(unittest.TestCase):
    def test_ranks_average_ties(self):
        self.assertEqual(TESTS.ranks([3, 1, 3, 2]), [3.5, 1.0, 3.5, 2.0])

    def test_spearman_perfect_and_reverse(self):
        self.assertAlmostEqual(TESTS.spearman([1, 2, 3, 4], [10, 20, 30, 40]), 1.0)
        self.assertAlmostEqual(TESTS.spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)
        self.assertIsNone(TESTS.spearman([1, 2, 3], [5, 5, 5]))

    def test_intervals_tile_and_last_needs_two_months(self):
        ms = L.months("2000-01", "2001-12")
        D = {"neer": {"SG": {m: 100.0 + i for i, m in enumerate(ms)}},
             "gdp": {f"{y}-Q{q}": float(q) for y in (2000, 2001) for q in (1, 2, 3, 4)},
             "cpi": {}, "mps": [{"date": "20000414", "p": "1", "slope": "same", "recentre_score": "0"},
                                {"date": "20001014", "p": "0", "slope": "zero", "recentre_score": "0"},
                                {"date": "20011214", "p": "1", "slope": "steeper", "recentre_score": "0"}]}
        iv, dropped = TESTS.intervals(D)
        self.assertEqual([(x["start"], x["end"]) for x in iv], [("2000-03", "2000-09"), ("2000-09", "2001-11")])
        self.assertEqual(dropped, 0)
        self.assertEqual(iv[0]["g"], 2.5)                    # quarters ending 2000-06 and 2000-09

    def test_fine_scores(self):
        D = {"mps": [{"date": "1", "slope": "same", "recentre_score": "0"},
                     {"date": "2", "slope": "steeper", "recentre_score": "1"},
                     {"date": "3", "slope": "flatter", "recentre_score": "0"},
                     {"date": "4", "slope": "zero", "recentre_score": "-1"},
                     {"date": "5", "slope": "steeper", "recentre_score": "0"}]}
        self.assertEqual(TESTS.fine_scores(D), {"1": 1, "2": 3, "3": 1, "4": -1, "5": 1})

    def test_printed_forms(self):
        self.assertEqual(L.printed("T2_P", "0.637406"), "0.6374")
        self.assertEqual(L.printed("T4_rank", "2"), "2")
        self.assertEqual(L.printed("gateC_changes", "331"), "331")
        self.assertEqual(L.printed("brier", "0.21625"), "0.216")
        self.assertIsNone(L.printed("T2_outcome", "SURVIVE"))


if __name__ == "__main__":
    unittest.main()

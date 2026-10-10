"""
13_results.py -- ROOT/RESULTS.md from ROOT/out/, failures first.

Order (Checkpoint 1, THESIS_ADDENDUM item 1): a failures-first list; gate C
(the correlation and the number of monthly changes); the five scored tests,
failures first (FAIL, INCONCLUSIVE, NOT SCORED, then SURVIVE); the scorecard
(held against expected, Brier score); the verdict as section 8 fixes it, with
the weak-evidence sentences of T3 and T7 verbatim from THESIS; then every
sealed sensitivity, marked not scored.

Each test carries its sealed wording verbatim (the Prediction, Survive if and
Fail if lines of THESIS.md, read at run time), its outcome label as sealed,
its numbers, and Jacob's confidence at seal. Every number is printed through
sgdlib.printed, which 14_manifest.py also uses. A run on anything but sgd/ is
stamped SYNTHETIC in its first line.
"""
import glob
import os
import re

import sgdlib as L

ORDER = {"FAIL": 0, "INCONCLUSIVE": 1, "NOT SCORED": 2, "SURVIVE": 3}
NAMES = {"T1": "T1. The split closes (the design test)",
         "T2": "T2. The yen: most of the rise was the yen falling",
         "T3": "T3. The ringgit: most of the rise was the ringgit falling",
         "T4": "T4. The slow path: the Singapore dollar is the steadiest in the set",
         "T7": "T7. Policy or growth: what the broad path followed"}

def p(T, key):
    v = L.printed(key, T.get(key))
    return v if v is not None else (T.get(key) or "n/a")


def _section(text, head):
    m = re.search(rf"^### {re.escape(head)}.*?(?=^### |^## |\Z)", text, re.S | re.M)
    return m.group(0) if m else ""


def _bullet(sec, label):
    m = re.search(rf"^- \*\*{re.escape(label)}\*\*(.*?)(?=^- |^\s*$|\Z)", sec, re.S | re.M)
    return " ".join(m.group(1).split()) if m else None


def sealed_wording(thesis_path):
    """{test: [(label, text)]}: the Prediction, Survive if (Pass if for gate
    C) and Fail if lines of each section, verbatim; and {test: sentence}, the
    'Weak evidence, stated now.' bullets of T3 and T7, verbatim."""
    text = open(thesis_path, encoding="utf-8").read()
    words, weak = {}, {}
    for t in L.SCORED + ("Gate C",):
        sec = _section(text, t + ".")
        items = []
        for label in ("Prediction.", "Survive if:", "Pass if:", "Fail if:"):
            v = _bullet(sec, label)
            if v:
                items.append((label, v))
        words[t] = items
        w = _bullet(sec, "Weak evidence, stated now.")
        if w:
            weak[t] = w
    return words, weak


def conf(T, t):
    c = T.get(f"conf_{t}")
    try:
        return "{:.0f}%".format(100 * float(c))
    except (TypeError, ValueError):
        return "[JACOB]"


def body(t, T):
    out = []
    if t == "T1":
        for w, name in (("scored", "January 2021 to December 2025"), ("long", "August 2005 on")):
            for cur in L.QUESTION:
                k = f"T1_{w}_{cur}"
                st = T.get(k + "_status")
                out.append(f"- {cur}, {name}: change in the cross rate {p(T, k + '_b')}; "
                           f"residual share {p(T, k + '_R')} (line 0.20 in size), "
                           f"BIS against MAS {p(T, k + '_mad')} on {p(T, k + '_mad_count')} months (line 0.005); "
                           f"{'passes' if T.get(k + '_ok') == 'True' else 'fails'}" + (f" ({st})" if st else "") + ".")
        out.append("- THESIS fixes no interval for T1: each check is a comparison of levels.")
    elif t in ("T2", "T3"):
        out.append(f"- change in the cross rate b {p(T, t + '_b')}; Singapore dollar's broad index s "
                   f"{p(T, t + '_s')}; partner's broad index {p(T, t + '_nx')}; residual {p(T, t + '_e')}.")
        out.append(f"- shares of the rise: Singapore dollar rising {p(T, t + '_S')}, partner falling "
                   f"{p(T, t + '_P')}, neither {p(T, t + '_R')}. No sampling interval: each share is a "
                   f"ratio of two level changes.")
    elif t == "T4":
        sds = sorted((float(v), k.split("_")[1]) for k, v in T.items() if k.startswith("T4_") and k.endswith("_sd"))
        out.append("- monthly swing of each broad index (standard deviation of the monthly log change): "
                   + ", ".join(f"{a} {p(T, f'T4_{a}_sd')}" for _, a in sds) + ".")
        out.append(f"- {p(T, 'T4_present')} of 11 present; the Singapore dollar ranks {p(T, 'T4_rank')} "
                   f"and is steadier than {p(T, 'T4_steadier_than')} partners. THESIS fixes no interval "
                   f"for T4: it is a rank.")
    elif t == "T7":
        out.append(f"- {p(T, 'T7_intervals')} intervals ({p(T, 'T7_dropped_count')} dropped for a missing value).")
        out.append(f"- rho with MAS's decisions {p(T, 'T7_rho_p')}; rho with growth {p(T, 'T7_rho_g')}; "
                   f"D {p(T, 'T7_D')} (90% bootstrap interval {p(T, 'T7_D_lo')} to {p(T, 'T7_D_hi')}, "
                   f"reported, not used in the rule).")
        out.append(f"- gate C beside it: correlation {p(T, 'gateC_r')} on {p(T, 'gateC_changes')} monthly changes.")
    if T.get(f"{t}_reason"):
        out.append(f"- not scored because: {T[t + '_reason']}.")
    return out


def section(t, T, words):
    o = T[f"{t}_outcome"]
    head = f"### {NAMES[t]}: {o}"
    head += f" (Jacob's confidence at seal: {conf(T, t)})"
    lines = [head, "", "Sealed wording (THESIS.md, verbatim):", ""]
    quoted = [f"> **{label}** {txt}" for label, txt in words.get(t, [])] or ["> (not found)"]
    lines += [q for pair in zip(quoted, [">"] * len(quoted)) for q in pair][:-1]
    return lines + [""] + body(t, T) + [""]


def gate_section(T, words):
    ok = T["gateC_pass"] == "True"
    lines = [f"## Gate C. The BIS index stands in for MAS's own: {'PASS' if ok else 'FAIL'}", "",
             "A gate, not a scored test: no confidence, not in the scorecard. Sealed wording "
             "(THESIS.md, verbatim):", ""]
    quoted = [f"> **{label}** {txt}" for label, txt in words.get("Gate C", [])] or ["> (not found)"]
    lines += [q for pair in zip(quoted, [">"] * len(quoted)) for q in pair][:-1]
    lines += ["", f"- correlation of monthly log changes, BIS broad index against MAS's S$NEER: "
                  f"{p(T, 'gateC_r')}, on {p(T, 'gateC_changes')} monthly changes (lines 0.90 and 120). "
                  f"THESIS fixes no interval for it.",
              "- " + ("T4 and T7 are read as sealed." if ok else
                      "T4 and T7 read \"the record cannot say\" and are not scored."), ""]
    return lines


def failures(T):
    """One line per gate or test that did not hold, for the top of the file."""
    out = []
    if T["gateC_pass"] != "True":
        out.append(f"- Gate C: FAIL (correlation {p(T, 'gateC_r')} on {p(T, 'gateC_changes')} changes).")
    for t in sorted(L.SCORED, key=lambda t: (ORDER[T[f"{t}_outcome"]], t)):
        o = T[f"{t}_outcome"]
        if o != "SURVIVE":
            why = f": {T[t + '_reason']}" if T.get(t + "_reason") else ""
            out.append(f"- {NAMES[t]}: {o}{why} (Jacob's confidence {conf(T, t)}).")
    return out or ["- None: gate C passed and every scored test survived."]


def main():
    a = L.args("sgd step 13: RESULTS.md")
    P = L.paths(a.root)
    out = P["out"]
    T = {r["key"]: r["value"] for r in L.read_csv(os.path.join(out, "tests.csv"))}
    sens = L.read_csv(os.path.join(out, "sensitivities.csv"))
    words, weak = sealed_wording(P["thesis"])
    real = os.path.realpath(P["root"]) == os.path.realpath(L.SGD)
    md = ["# RESULTS: the Singapore dollar, the yen and the ringgit" if real else
          "# SYNTHETIC FIXTURE RUN: every number below is invented. Not a finding.", "",
          "Written by `13_results.py` from `out/`. Tests as sealed in `THESIS.md` (commit 9e46034); "
          "failures first. Outcome labels as sealed: SURVIVE, FAIL, INCONCLUSIVE, NOT SCORED. "
          "Confidences are Jacob's, set at the seal.", "",
          f"Windows: scored {T['window_scored']}; long {T['window_long']}.", "",
          "## What did not hold (failures first)", ""]
    md += failures(T) + [""]
    md += gate_section(T, words)
    tests = sorted(L.SCORED, key=lambda t: (ORDER[T[f"{t}_outcome"]], t))
    md += ["## The scored tests, failures first", ""]
    for t in tests:
        md += section(t, T, words)
    md += ["## Scorecard", "",
           f"- Scored: {T['scored_tests'] or 'none'} ({p(T, 'n_scored')}); held: {p(T, 'n_held')}. "
           f"Gate C is not counted; a test not scored drops out of the count and the Brier score."]
    for t in L.SCORED:
        md.append(f"- {t}: {T[f'{t}_outcome']}; Jacob's confidence at seal {conf(T, t)}.")
    md.append(f"- Held {p(T, 'n_held')} of {p(T, 'n_scored')} scored, against an expected "
              f"{p(T, 'expected_held')} (the sum of Jacob's confidences for the tests scored; 2.68 if "
              f"all five are scored).")
    md.append(f"- Brier score: {p(T, 'brier')} (mean over the scored tests).")
    md += ["", "## Verdict (THESIS section 8)", "", f"**{T['verdict']}**", "",
           f"- **Part A, the yen:** {T['verdict_A_yen']}.",
           f"- **Part A, the ringgit:** {T['verdict_A_ringgit']}."]
    if "T3" in weak:
        md.append(f"  - Weak evidence, stated at the seal (T3): {weak['T3']}")
    md.append("- The long-run split (August 2005 on) is reported with the sensitivities and does not "
              "change Part A.")
    md.append(f"- **Part B, the broad path:** {T['verdict_B']}.")
    if T["T7_outcome"] in ("SURVIVE", "FAIL", "INCONCLUSIVE") and "T7" in weak:
        md.append(f"  - Weak evidence, stated at the seal (T7): {weak['T7']}")
    md.append(f"- Gate C beside Part B: correlation {p(T, 'gateC_r')} on {p(T, 'gateC_changes')} "
              f"monthly changes.")
    if T.get("verdict_T4"):
        md.append(f"- {T['verdict_T4'][0].upper() + T['verdict_T4'][1:]}.")
    else:
        md.append(f"- T4 is reported with the verdict and does not change its wording: {T['T4_outcome']}.")
    md += ["", "## Sensitivities and descriptive checks (reported, NOT SCORED)", "",
           "Every row is a sealed sensitivity or descriptive check (THESIS sections 5, 6 and 7). None "
           "enters the score or the verdict.", "",
           "| Test | Variant | Key | Value | Scored |", "|---|---|---|---|---|"]
    for r in sens:
        v = r["value"]
        try:
            v = "{:.4f}".format(float(v))
        except ValueError:
            pass
        md.append(f"| {r['test']} | {r['variant']} | {r['key']} | {v} | not scored |")
    md.append("")
    post = os.path.join(out, "postresults.csv")
    if os.path.exists(post):
        md += ["## Post-results numbers for the article (NOT SCORED)", "",
               "Written by `11b_postresults.py` from `out/` (THESIS_ADDENDUM item 5): per-cent forms "
               "(100 x (exp(x) - 1)) of log changes, shares in per cent, rounded forms of tested numbers, "
               "and the specimen. None changes a sealed number, outcome or the verdict.", "",
               "| Key | Printed | Meaning |", "|---|---|---|"]
        for r in L.read_csv(post):
            md.append(f"| {r['key']} | {r['printed']} | {r['meaning']} |")
        md.append("")
    # Added after outside review, not sealed (THESIS_ADDENDUM item 10).
    review = sorted(glob.glob(os.path.join(out, "review_*.csv")))
    review = [f for f in review if not f.endswith("review_rolling_windows.csv")]
    if review:
        md += ["## After outside review (added after outside review, not sealed, NOT SCORED)", "",
               "Written by `16_review.py` from `out/` and raw/s1c, raw/s8 (THESIS_ADDENDUM item 10). "
               "None changes a sealed number, outcome, threshold or the verdict.", ""]
        for f in review:
            md += [f"### {os.path.basename(f)}", "", "| Key | Printed | Meaning |", "|---|---|---|"]
            for r in L.read_csv(f):
                md.append(f"| {r['key']} | {r['printed']} | {r['meaning']} |")
            md.append("")
    L.write_text(P["results"], "\n".join(md))
    print(f"  {os.path.relpath(P['results'], P['root'])}: {len(md)} lines")


if __name__ == "__main__":
    main()

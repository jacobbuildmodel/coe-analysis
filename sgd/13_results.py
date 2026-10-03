"""
13_results.py -- ROOT/RESULTS.md from ROOT/out/, failures first.

Order: the verdict (Part A for the yen and the ringgit, Part B for the broad
path, with gate C beside Part B and T7's weak-evidence sentence when T7
survives); then every scored test that did not survive (FAIL, then
INCONCLUSIVE, then NOT SCORED); then those that survived; then gate C; then
the scorecard; then the sensitivities (reported, not scored) and T7's
intervals.

Each test carries its sealed wording verbatim (the Prediction, Survive if and
Fail if lines of THESIS.md, read at run time), its outcome label as sealed,
its numbers, and Jacob's confidence at seal. Every number is printed through
sgdlib.printed, which 14_manifest.py also uses. A run on anything but sgd/ is
stamped SYNTHETIC in its first line.
"""
import os
import re

import sgdlib as L

ORDER = {"FAIL": 0, "INCONCLUSIVE": 1, "NOT SCORED": 2, "SURVIVE": 3}
NAMES = {"T1": "T1. The split closes (the design test)",
         "T2": "T2. The yen: most of the rise was the yen falling",
         "T3": "T3. The ringgit: most of the rise was the ringgit falling",
         "T4": "T4. The slow path: the Singapore dollar is the steadiest in the set",
         "T7": "T7. Policy or growth: what the broad path followed"}
WEAK_T7 = ("The design leans toward the rival: the band is the path MAS keeps the index on, so a "
           "result that the path followed MAS's decisions is weak evidence that MAS rather than the "
           "economy moved the Singapore dollar.")


def p(T, key):
    v = L.printed(key, T.get(key))
    return v if v is not None else (T.get(key) or "n/a")


def sealed_wording(thesis_path):
    text = open(thesis_path, encoding="utf-8").read()
    out = {}
    for t in L.SCORED:
        sec = re.search(rf"^### {t}\..*?(?=^### |^## |\Z)", text, re.S | re.M)
        items = []
        if sec:
            for label in ("Prediction.", "Survive if:", "Fail if:"):
                m = re.search(rf"^- \*\*{re.escape(label)}\*\*(.*?)(?=^- |^\s*$|\Z)", sec.group(0), re.S | re.M)
                if m:
                    items.append((label, " ".join(m.group(1).split())))
        out[t] = items
    return out


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
                   f"and is steadier than {p(T, 'T4_steadier_than')} partners.")
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


def main():
    a = L.args("sgd step 13: RESULTS.md")
    P = L.paths(a.root)
    out = P["out"]
    T = {r["key"]: r["value"] for r in L.read_csv(os.path.join(out, "tests.csv"))}
    sens = L.read_csv(os.path.join(out, "sensitivities.csv"))
    words = sealed_wording(P["thesis"])
    real = os.path.realpath(P["root"]) == os.path.realpath(L.SGD)
    md = ["# RESULTS: the Singapore dollar, the yen and the ringgit" if real else
          "# SYNTHETIC FIXTURE RUN: every number below is invented. Not a finding.", "",
          "Written by `13_results.py` from `out/`. Tests as sealed in `THESIS.md`; failures first. "
          "Outcome labels as sealed: SURVIVE, FAIL, INCONCLUSIVE, NOT SCORED.", "",
          f"Windows: scored {T['window_scored']}; long {T['window_long']}.", "",
          "## Verdict", "", f"**{T['verdict']}**", "",
          f"- **Part A, the yen:** {T['verdict_A_yen']}.",
          f"- **Part A, the ringgit:** {T['verdict_A_ringgit']}.",
          f"- **Part B, the broad path:** {T['verdict_B']}."]
    if T["T7_outcome"] == "SURVIVE":
        md.append(f"- {WEAK_T7}")
    md.append(f"- Gate C: correlation {p(T, 'gateC_r')} on {p(T, 'gateC_changes')} monthly changes "
              f"({'passed' if T['gateC_pass'] == 'True' else 'failed'}; line 0.90 on at least 120).")
    if T.get("verdict_T4"):
        md.append(f"- {T['verdict_T4'][0].upper() + T['verdict_T4'][1:]}.")
    md.append("")
    tests = sorted(L.SCORED, key=lambda t: (ORDER[T[f"{t}_outcome"]], t))
    md += ["## Tests that did not survive", ""]
    bad = [t for t in tests if T[f"{t}_outcome"] != "SURVIVE"]
    if not bad:
        md += ["None.", ""]
    for t in bad:
        md += section(t, T, words)
    md += ["## Tests that survived", ""]
    good = [t for t in tests if T[f"{t}_outcome"] == "SURVIVE"]
    if not good:
        md += ["None.", ""]
    for t in good:
        md += section(t, T, words)
    md += ["## Scorecard", "",
           f"- Scored: {T['scored_tests'] or 'none'} ({p(T, 'n_scored')}); held: {p(T, 'n_held')}. "
           f"Gate C is not counted."]
    for t in L.SCORED:
        md.append(f"- {t}: {T[f'{t}_outcome']}; confidence at seal {conf(T, t)}.")
    md.append(f"- Held {p(T, 'n_held')} of {p(T, 'n_scored')} scored, against an expected "
              f"{p(T, 'expected_held')} (the sum of the confidences of the scored tests).")
    md.append(f"- Brier score: {p(T, 'brier')} (mean over the scored tests; tests not scored drop out).")
    md += ["", "## Sensitivities (reported, not scored)", "",
           "Every row is a sealed sensitivity or descriptive check. None enters the score or the verdict.", "",
           "| Test | Variant | Key | Value | Scored |", "|---|---|---|---|---|"]
    for r in sens:
        v = r["value"]
        try:
            v = "{:.4f}".format(float(v))
        except ValueError:
            pass
        md.append(f"| {r['test']} | {r['variant']} | {r['key']} | {v} | not scored |")
    md.append("")
    L.write_text(P["results"], "\n".join(md))
    print(f"  {os.path.relpath(P['results'], P['root'])}: {len(md)} lines")


if __name__ == "__main__":
    main()

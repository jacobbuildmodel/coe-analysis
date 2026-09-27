"""
13_results.py -- ROOT/RESULTS.md from ROOT/out/, failures first.

Order: the verdict sentence and the leans THESIS section 8 requires beside
it; then every test that did not survive (FAIL, then INCONCLUSIVE, then NOT
SCORED); then those that survived; then the sensitivities (reported, not
scored), the titles the missing-year rule dropped, and the scorecard. Every
number is printed through pwmlib.printed, which 14_manifest.py also uses.

A run on anything but pwm/ is stamped SYNTHETIC in its first line.
"""
import os

import pwmlib as L

ORDER = {"FAIL": 0, "INCONCLUSIVE": 1, "NOT SCORED": 2, "SURVIVE": 3}
NAMES = {"T1": "T1. Parallel before (the design test)",
         "T2": "T2. The suit fits: pay rose where the ladder was hung",
         "T3": "T3. The rest of the bottom kept pace",
         "T4": "T4. The jobs survived the fitting",
         "T5": "T5. The first rung shows up in the survey"}
WEAK = ("A monopsony-like result is weak evidence and a competitive result is strong evidence, "
        "because the design leans toward the monopsony reading.")


def p(T, key):
    return L.printed(key, T.get(key)) or T.get(key, "")


def body(t, T):
    lines = []
    if t == "T1":
        for g in L.COVERED:
            if T.get(f"T1_{g}_slope"):
                lines.append(f"- {g}: drift {p(T, f'T1_{g}_slope')} a year (90% interval "
                             f"{p(T, f'T1_{g}_lo')} to {p(T, f'T1_{g}_hi')}), {p(T, f'T1_{g}_pre_junes')} "
                             f"pre-period Junes; line 0.010; {'passes' if T[f'T1_{g}_pass'] == 'True' else 'fails'}.")
            else:
                lines.append(f"- {g}: {T.get(f'T1_{g}_pass')} ({p(T, f'T1_{g}_pre_junes')} Junes).")
    elif t == "T2":
        for g in L.COVERED:
            if T.get(f"T2_{g}_est"):
                lines.append(f"- {g}: {p(T, f'T2_{g}_est')} (90% interval {p(T, f'T2_{g}_lo')} to "
                             f"{p(T, f'T2_{g}_hi')}).")
        if T.get("T2_pooled"):
            lines.append(f"- pooled: {p(T, 'T2_pooled')} (90% interval {p(T, 'T2_pooled_lo')} to "
                         f"{p(T, 'T2_pooled_hi')}); survive at 0.10 with every group above 0, fail "
                         f"below 0.05 or any group at or below 0.")
        lines.append(f"- groups scored: {T.get('T2_groups_scored') or 'none (T1)'}.")
    elif t == "T3":
        if T.get("T3_shortfall"):
            lines.append(f"- comparison set C, growth {p(T, 'T3_growth_c')} (start mean {p(T, 'T3_start_c')} "
                         f"over {p(T, 'T3_n_start')} Junes, end mean {p(T, 'T3_end_c')} over "
                         f"{p(T, 'T3_n_end')} Junes).")
            lines.append(f"- the middle (LFS median, excluding employer CPF), growth {p(T, 'T3_growth_mid')}.")
            lines.append(f"- shortfall {p(T, 'T3_shortfall')}; line 0.05.")
        else:
            lines.append("- not computable: fewer than two start-window Junes, or no end-window value.")
    elif t == "T4":
        lines.append(f"- series: {T.get('T4_series')} (priority rule, THESIS section 4).")
        for g in L.COVERED:
            if T.get(f"T4_{g}_status"):
                est = (f"{p(T, f'T4_{g}_est')} (90% interval {p(T, f'T4_{g}_lo')} to {p(T, f'T4_{g}_hi')})"
                       if T.get(f"T4_{g}_est") else "no estimate")
                pt = f", pre-trend {p(T, f'T4_{g}_pretrend')} a year" if T.get(f"T4_{g}_pretrend") else ""
                lines.append(f"- {g}: {T[f'T4_{g}_status']}; {p(T, f'T4_{g}_pre_years')} pre-period "
                             f"years{pt}; relative change {est}.")
    elif t == "T5":
        for g in L.COVERED:
            rs = sorted((k, v) for k, v in T.items() if k.startswith(f"T5_{g}_") and k.endswith("_ratio"))
            if rs:
                lines.append(f"- {g}: " + ", ".join(f"{k.split('_')[2]} {p(T, k)}" for k, _ in rs) + ".")
        if T.get("T5_min_ratio"):
            lines.append(f"- lowest ratio {p(T, 'T5_min_ratio')}; line 0.97.")
    return lines


def main():
    a = L.args("PWM step 13: RESULTS.md")
    P = L.paths(a.root)
    out = P["out"]
    T = {r["key"]: r["value"] for r in L.read_csv(os.path.join(out, "tests.csv"))}
    sens = L.read_csv(os.path.join(out, "sensitivities.csv"))
    dropped = L.read_csv(os.path.join(out, "dropped_titles.csv"))
    real = os.path.realpath(P["root"]) == os.path.realpath(L.PWM)
    md = []
    md.append("# RESULTS: minimum wage or the Progressive Wage Model" if real else
              "# SYNTHETIC FIXTURE RUN: every number below is invented. Not a finding.")
    md.append("")
    md.append("Written by `13_results.py` from `out/`. Tests as sealed in `THESIS.md`; "
              "failures first.")
    md.append("")
    md.append("## Verdict")
    md.append("")
    md.append(f"**{T['verdict']}**")
    md.append("")
    md.append(f"{WEAK}")
    md.append("")
    md.append("- The pay test leans the other way (T2): in-house workers dilute the covered side and "
              "the LQS lifted the comparison side, so a pay gain found is strong evidence and none "
              "found is weak.")
    md.append("- Part B leans toward \"kept pace\" (T3): the LQS was a floor under the uncovered jobs "
              "too, so \"kept pace\" is weak evidence and \"fell behind\" is strong evidence.")
    md.append("- The record cannot say what a national floor would have done in jobs no ladder "
              "reached.")
    md.append(f"- T4 read the {T.get('T4_series')} series.")
    tests = sorted(("T1", "T2", "T3", "T4", "T5"), key=lambda t: (ORDER[T[f"{t}_outcome"]], t))
    md.append("")
    md.append("## Tests that did not survive")
    md.append("")
    bad = [t for t in tests if T[f"{t}_outcome"] != "SURVIVE"]
    if not bad:
        md.append("None.")
        md.append("")
    for t in bad:
        md += [f"### {NAMES[t]}: {T[f'{t}_outcome']}", ""] + body(t, T) + [""]
    md.append("## Tests that survived")
    md.append("")
    good = [t for t in tests if T[f"{t}_outcome"] == "SURVIVE"]
    if not good:
        md.append("None.")
        md.append("")
    for t in good:
        md += [f"### {NAMES[t]}: SURVIVE", ""] + body(t, T) + [""]
    md.append("## Sensitivities (reported, not scored)")
    md.append("")
    md.append("| Test | Variant | Key | Value |")
    md.append("|---|---|---|---|")
    for r in sens:
        v = r["value"]
        try:
            v = "{:.4f}".format(float(v))
        except ValueError:
            pass
        md.append(f"| {r['test']} | {r['variant']} | {r['key']} | {v} |")
    md.append("")
    md.append("## Titles dropped by the missing-year rule")
    md.append("")
    if not dropped:
        md.append("None.")
    for r in dropped:
        md.append(f"- {r['group']} {r['code']} {r['title']} ({r['measure']}, {r['variant']}): "
                  f"missing in {r['missing_junes']}.")
    md.append("")
    md.append("## Scorecard")
    md.append("")
    md.append(f"- Scored: {T['scored_tests'] or 'none'} ({p(T, 'n_scored')}); held: {p(T, 'n_held')}.")
    for t in ("T1", "T2", "T3", "T4", "T5"):
        c = T.get(f"conf_{t}")
        cs = c if c == "[JACOB]" else "{:.0f}%".format(100 * float(c))
        md.append(f"- {t}: {T[f'{t}_outcome']}; confidence at seal {cs}.")
    md.append(f"- Expected number holding: {p(T, 'expected_held')}. Brier score: {p(T, 'brier')}.")
    md.append("")
    L.write_text(P["results"], "\n".join(md))
    print(f"  {os.path.relpath(P['results'], P['root'])}: {len(md)} lines")


if __name__ == "__main__":
    main()

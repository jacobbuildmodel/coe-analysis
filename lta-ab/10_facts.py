"""
10_facts.py -- every number in the lta-ab evidence note, from raw/ only.

Descriptive only: what the published COE record showed, to the cut-off set by
the checker (the first October 2026 bidding exercise). No forecast, no model.

Reads (all in lta-ab/raw/, md5s in raw/RETRIEVED.txt and CHECKSUMS.md5):
  d1_coe_bidding_results_20261011.csv      LTA via data.gov.sg, per exercise
  d2_quota_premium_pqp_monthly_20261011.csv SingStat M651121 via data.gov.sg,
                                            monthly, PQP to the column for Aug 2026
  d3_lta_m11_coe_results_2025_2026.pdf     LTA "M11 COE Results 2025-2026",
                                            PQP rows to "PQP for Oct 2026"
  office/LTA_CONSTANTS.csv                 amounts and dates quoted from LTA's
                                            consultation paper, with paragraphs
and, for one cross-check only, the repository's root raw.csv (md5 asserted).

Writes (lta-ab/out/):
  exercises.csv   one row per exercise: premiums and quotas for A, B, E; gaps
  pqp_monthly.csv one row per month: PQP for A and B applying in that month
  a_above_b.csv   every exercise in which Category A cleared above Category B
  facts.csv       key, value, printed, definition: every number the note uses
  checks.csv      the cross-checks and their results

Definitions (fixed here, before any number was looked at in the note):
  gap          premium(B) - premium(A), dollars, per exercise
  windows      set by the data's start and the 2022 rule change, not by results
               (checker's ruling of 12 Oct 2026), used in this order everywhere:
    w1  January 2010, exercise 1, to the cut-off (the whole record held)
    w2  since the 2022 change to Category A's power threshold for electric
        cars: from May 2022, exercise 1 (LTA news release of 14 Apr 2022,
        para 3, raw/c2b_lta_news_coe_quota_may_jul_2022.html)
    w3  the last 12 months: the 24 exercises ending at the cut-off
    w4  the latest exercise (the cut-off)
  PQP month M  the PQP that applied in month M. SingStat's column for month m
               holds the PQP set after m's second exercise, which applies in
               m + 1 (asserted below against LTA's own "PQP for <month>" rows)
  PQP windows  w1 months 2010-01 to 2026-10 with a published PQP; w2 months from
               2022-05; w3 the 12 months to 2026-10; w4 October 2026
  gap change   for exercise t in a window, |gap(t) - gap(same exercise number,
               6 or 12 calendar months earlier)|; the earlier exercise may lie
               before the window start; pairs with no earlier exercise (the 2020
               suspension, the record's first months) are skipped
"""
import csv
import hashlib
import math
import os
import re
import sys

import pandas as pd
import pypdf

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "out")
ROOT_RAW = os.path.join(HERE, "..", "raw.csv")
ROOT_RAW_MD5 = "7b68a001709821c71ece5b8ed209d4d3"

CUTOFF = ("2026-10", 1)          # the checker's ruling, 11 Oct 2026
FULL_START = ("2010-01", 1)
W2_START = ("2022-05", 1)       # LTA news release, 14 Apr 2022, para 3
N_12M = 24
MON = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
MONTH_NAME = {v: k for k, v in MON.items()}
LONG = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
        8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def dollars(x):
    return "{:,}".format(int(x))


def rnd(x):
    """Round half up to a whole number (no banker's rounding)."""
    return int(math.floor(x + 0.5))


def label(month, ex):
    y, m = month.split("-")
    return f"{LONG[int(m)]} {y}, exercise {ex}"


def constants():
    c = {}
    for r in csv.DictReader(open(os.path.join(HERE, "office", "LTA_CONSTANTS.csv"), encoding="utf-8")):
        c[r["key"]] = int(r["value"])
    return c


def load_bidding():
    df = pd.read_csv(os.path.join(RAW, "d1_coe_bidding_results_20261011.csv"), dtype=str)
    for col in ["quota", "bids_success", "bids_received", "premium"]:
        df[col] = pd.to_numeric(df[col].str.replace(",", "", regex=False))
    df["bidding_no"] = df["bidding_no"].astype(int)
    df["cat"] = df["vehicle_class"].str.replace("Category ", "", regex=False)
    # The two documented corrections of the root README (verified there against
    # published results). Applied only if the source still carries the error.
    m1 = (df.month == "2010-01") & (df.bidding_no == 2) & (df.cat == "D")
    m2 = (df.month == "2010-02") & (df.bidding_no == 1) & (df.cat == "B")
    corrections = 0
    if df.loc[m1, "premium"].iloc[0] == 20090:
        df.loc[m1, "premium"] = 852
        corrections += 1
    if df.loc[m2, "quota"].iloc[0] == 1154:
        df.loc[m2, "quota"] = 693
        corrections += 1
    return df, corrections


def wide(df):
    w = df[df.cat.isin(["A", "B", "E"])].pivot_table(
        index=["month", "bidding_no"], columns="cat", values=["premium", "quota"], aggfunc="first")
    w.columns = [f"{a}_{b}" for a, b in w.columns]
    w = w.reset_index().sort_values(["month", "bidding_no"]).reset_index(drop=True)
    keep = [(m, b) for m, b in zip(w.month, w.bidding_no) if FULL_START <= (m, b) <= CUTOFF]
    w = w[[k in set(keep) for k in zip(w.month, w.bidding_no)]].reset_index(drop=True)
    assert (w.month.iloc[-1], w.bidding_no.iloc[-1]) == CUTOFF, "data does not reach the cut-off"
    assert not w.isna().any().any()
    for c in ["premium_A", "premium_B", "premium_E", "quota_A", "quota_B", "quota_E"]:
        w[c] = w[c].astype(int)
    w["gap"] = w.premium_B - w.premium_A
    w["gap_EB"] = w.premium_E - w.premium_B
    w["label"] = [label(m, b) for m, b in zip(w.month, w.bidding_no)]
    return w


def load_singstat():
    rows = {r[0]: r[1:] for r in csv.reader(open(os.path.join(RAW, "d2_quota_premium_pqp_monthly_20261011.csv"), encoding="utf-8"))}
    hdr = [(int(h[:4]), MON[h[4:]]) for h in rows["DataSeries"]]

    def series(name):
        return {k: int(v) for k, v in zip(hdr, rows[name]) if v.strip() not in ("-", "")}
    s = {}
    for cat, nm in [("A", "Cars Up To 1600cc And 97kW"), ("B", "Cars Above 1600cc Or 97kW")]:
        s[f"pqp_{cat}"] = series(f"{nm}, Prevailing Quota Premium, 2nd Bidding")
        s[f"qp1_{cat}"] = series(f"{nm}, Quota Premium, 1st Bidding")
        s[f"qp2_{cat}"] = series(f"{nm}, Quota Premium, 2nd Bidding")
    return s


def load_m11():
    pqp = {}
    for page in pypdf.PdfReader(os.path.join(RAW, "d3_lta_m11_coe_results_2025_2026.pdf")).pages:
        for line in page.extract_text().splitlines():
            m = re.match(r"PQP1? for (\w{3}) (\d{4}) \$([\d,]+) \$([\d,]+)", line)
            if m:
                pqp[(int(m[2]), MON[m[1]])] = (int(m[3].replace(",", "")), int(m[4].replace(",", "")))
    return pqp


def nxt(k):
    y, m = k
    return (y + 1, 1) if m == 12 else (y, m + 1)


def main():
    os.makedirs(OUT, exist_ok=True)
    C = constants()
    checks = []
    df, corrections = load_bidding()
    w = wide(df)

    # Check 1: the fresh file against the root raw.csv on every overlapping row.
    assert md5(ROOT_RAW) == ROOT_RAW_MD5
    old = pd.read_csv(ROOT_RAW, dtype=str)
    new = pd.read_csv(os.path.join(RAW, "d1_coe_bidding_results_20261011.csv"), dtype=str)
    key = ["month", "bidding_no", "vehicle_class"]
    mrg = old.merge(new, on=key, how="left", suffixes=("_old", "_new"), indicator=True)
    assert (mrg["_merge"] == "both").all(), "a root raw.csv row is missing from the fresh file"
    diff = 0
    for col in ["quota", "bids_success", "bids_received", "premium"]:
        a = mrg[col + "_old"].str.replace(",", "", regex=False)
        b = mrg[col + "_new"].str.replace(",", "", regex=False)
        diff += int((a != b).sum())
    checks.append(("fresh bidding file vs root raw.csv, rows compared", len(mrg)))
    checks.append(("fresh bidding file vs root raw.csv, cells differing", diff))
    checks.append(("documented corrections applied (root README)", corrections))
    assert diff == 0

    # Check 2: per-exercise premiums for A and B against SingStat's monthly series.
    S = load_singstat()
    n2 = bad2 = 0
    for m, b, pa, pb in zip(w.month, w.bidding_no, w.premium_A, w.premium_B):
        k = (int(m[:4]), int(m[5:]))
        src = S[f"qp{b}_A"], S[f"qp{b}_B"]
        if k in src[0]:
            n2 += 1
            bad2 += int(src[0][k] != pa) + int(src[1][k] != pb)
    checks.append(("premiums A and B vs SingStat M651121, exercises compared", n2))
    checks.append(("premiums A and B vs SingStat M651121, values differing", bad2))
    assert bad2 == 0

    # Check 3: PQP alignment. SingStat's month m equals LTA's "PQP for m + 1".
    M11 = load_m11()
    ov = [k for k in S["pqp_A"] if nxt(k) in M11]
    hits = sum(1 for k in ov if M11[nxt(k)] == (S["pqp_A"][k], S["pqp_B"][k]))
    checks.append(("PQP: SingStat month m equals LTA 'PQP for m+1', months compared", len(ov)))
    checks.append(("PQP: SingStat month m equals LTA 'PQP for m+1', months matching", hits))
    assert hits == len(ov) and len(ov) >= 12

    # The PQP that applied in each month: SingStat shifted one month, then LTA's
    # M11 for the months SingStat does not yet cover.
    pq = {nxt(k): (S["pqp_A"][k], S["pqp_B"][k], "SingStat M651121") for k in S["pqp_A"]}
    for k, (a, b) in M11.items():
        if k not in pq:
            pq[k] = (a, b, "LTA M11")
    months = sorted(k for k in pq if (2010, 1) <= k <= (2026, 10))
    p = pd.DataFrame([{"month": f"{y}-{m:02d}", "pqp_A": pq[(y, m)][0], "pqp_B": pq[(y, m)][1],
                       "source": pq[(y, m)][2]} for y, m in months])
    p["gap"] = p.pqp_B - p.pqp_A
    p["gap_pct_of_A"] = 100 * p.gap / p.pqp_A
    assert p.month.iloc[-1] == "2026-10"

    # Check 4: LTA's PQP definition (M11 footnote 1, paper footnote 3) recomputed:
    # the mean of the quota premiums in the latest three months with bidding.
    allx = df[df.cat.isin(["A", "B"])].copy()
    bymonth = {}
    for (m, cat), g in allx.groupby(["month", "cat"]):
        bymonth.setdefault(m, {})[cat] = list(g.premium)
    mlist = sorted(bymonth)
    n4 = ok4 = 0
    for i in range(3, len(mlist)):
        y, mm = int(mlist[i - 1][:4]), int(mlist[i - 1][5:])
        k = nxt((y, mm))
        if k not in pq:
            continue
        last3 = mlist[i - 3:i]
        for j, cat in enumerate("AB"):
            vals = [v for m in last3 for v in bymonth[m][cat]]
            n4 += 1
            ok4 += int(abs(sum(vals) / len(vals) - pq[k][j]) <= 1)
    checks.append(("PQP recomputed as 3-month mean of premiums, values compared", n4))
    checks.append(("PQP recomputed as 3-month mean of premiums, within $1", ok4))

    # ---- facts -------------------------------------------------------------
    F = []

    def fact(key, value, printed, definition):
        F.append({"key": key, "value": value, "printed": printed, "definition": definition})

    w2 = w[[(m, b) >= W2_START for m, b in zip(w.month, w.bidding_no)]]
    windows = {"w1": w, "w2": w2, "w3": w.tail(N_12M), "w4": w.tail(1)}
    gap_at = {(m, b): g for m, b, g in zip(w.month, w.bidding_no, w.gap)}

    def back(m, k):
        y, mm = int(m[:4]), int(m[5:]) - k
        while mm < 1:
            y, mm = y - 1, mm + 12
        return f"{y}-{mm:02d}"

    def pct(x):
        return str(rnd(x)) if abs(x) >= 1 else "{:.1f}".format(x)
    fact("cutoff_label", 0, label(*CUTOFF), "the last exercise used (checker's ruling)")
    for wn, d in windows.items():
        fact(f"n_ex_{wn}", len(d), str(len(d)), f"exercises in the {wn} window")
        fact(f"start_{wn}", 0, d.label.iloc[0], f"first exercise in the {wn} window")
        med = d.gap.median()
        fact(f"gap_median_{wn}", med, dollars(rnd(med)), f"median B-A premium gap, {wn}, dollars")
        fact(f"gap_mean_{wn}", d.gap.mean(), dollars(rnd(d.gap.mean())), f"mean B-A gap, {wn}")
        rel = 100 * d.gap / d.premium_A
        fact(f"gap_rel_median_{wn}", rel.median(), pct(rel.median()),
             f"median of (B-A)/A per exercise, per cent, {wn}")
        lo_ = d.loc[d.gap.idxmin()]
        if lo_.gap < 0:
            fact(f"a_over_b_max_{wn}", int(-lo_.gap), dollars(-lo_.gap), f"largest margin of A above B, {wn}, dollars")
            fact(f"a_over_b_max_when_{wn}", 0, lo_.label, f"exercise of the largest margin of A above B, {wn}")
        fact(f"gap_max_{wn}", int(d.gap.max()), dollars(d.gap.max()), f"largest B-A gap, {wn}")
        fact(f"gap_max_when_{wn}", 0, d.loc[d.gap.idxmax()].label, f"exercise of the largest B-A gap, {wn}")
        for k in (6, 12):
            ch = [abs(g - gap_at[(back(m, k), b)]) for m, b, g in zip(d.month, d.bidding_no, d.gap)
                  if (back(m, k), b) in gap_at]
            med_ch = pd.Series(ch).median()
            fact(f"gap_change_{k}m_median_{wn}", med_ch, dollars(rnd(med_ch)),
                 f"median absolute change in the B-A gap over {k} months, exercise-matched, {wn}")
            fact(f"gap_change_{k}m_n_{wn}", len(ch), str(len(ch)), f"exercise pairs in that median, {wn}")
        fact(f"a_above_b_{wn}", int((d.gap < 0).sum()), str(int((d.gap < 0).sum())), f"exercises with A above B, {wn}")
        fact(f"a_equal_b_{wn}", int((d.gap == 0).sum()), str(int((d.gap == 0).sum())), f"exercises with A equal to B, {wn}")
        for thr_key in ["step_option_b", "step_option_a", "span_both"]:
            thr = C[thr_key] if thr_key != "span_both" else C["rebate_max"] + C["surcharge_max"]
            n = int((d.gap >= thr).sum())
            fact(f"gap_ge_{thr_key}_{wn}", n, str(n), f"exercises with B-A gap >= {thr}, {wn}")
            fact(f"gap_ge_{thr_key}_{wn}_pct", 100 * n / len(d), str(rnd(100 * n / len(d))), f"per cent of exercises with gap >= {thr}, {wn}")
    fact("span_both", C["rebate_max"] + C["surcharge_max"], dollars(C["rebate_max"] + C["surcharge_max"]),
         "lowest-to-highest band difference in both LTA options: rebate_max + surcharge_max")

    # LTA's statement: A above B on three occasions, Feb to Jun 2026 (paper 1.8).
    lo, hi = "2026-%02d" % C["claim_from_month"], "2026-%02d" % C["claim_to_month"]
    claim = w[(w.month >= lo) & (w.month <= hi)]
    n_claim = int((claim.gap < 0).sum())
    fact("claim_exercises", len(claim), str(len(claim)), "exercises February to June 2026")
    fact("claim_a_above_b", n_claim, str(n_claim), "of which A cleared above B")
    fact("claim_agrees", int(n_claim == C["claim_occasions"]), "agrees" if n_claim == C["claim_occasions"] else "differs",
         "whether the count equals LTA's 'three occasions'")
    y26 = w[w.month >= "2026-01"]
    fact("a_above_b_2026", int((y26.gap < 0).sum()), str(int((y26.gap < 0).sum())), "A above B, Jan 2026 to the cut-off")
    fact("n_ex_2026", len(y26), str(len(y26)), "exercises, Jan 2026 to the cut-off")
    n_other = len(y26) - int((y26.gap < 0).sum())
    fact("n_ex_2026_other", n_other, str(n_other), "exercises in 2026 to the cut-off in which A did not clear above B")
    pre26 = w[w.month < "2026-01"]
    fact("a_above_b_before_2026", int((pre26.gap < 0).sum()), str(int((pre26.gap < 0).sum())), "A above B, 2010 to Dec 2025")
    # The median of (B-A)/A per exercise, by calendar year (2026 to the cut-off).
    yr = w.assign(year=w.month.str[:4], rel=100 * w.gap / w.premium_A).groupby("year").rel.median()
    fact("gap_rel_year_min", yr.min(), str(rnd(yr.min())), "lowest calendar-year median of (B-A)/A, per cent")
    fact("gap_rel_year_min_year", 0, yr.idxmin(), "the year of that lowest median")
    fact("gap_rel_year_max", yr.max(), str(rnd(yr.max())), "highest calendar-year median of (B-A)/A, per cent")
    fact("gap_rel_year_max_year", 0, yr.idxmax(), "the year of that highest median")
    yr.rename("median_gap_pct_of_A").to_csv(os.path.join(OUT, "gap_rel_by_year.csv"), lineterminator="\n", float_format="%.4f")
    cut = w.iloc[-1]
    fact("gap_cutoff", int(cut.gap), dollars(cut.gap), "B-A gap at the cut-off exercise")

    # F3, PQP.
    pw = {"w1": p, "w2": p[p.month >= "%s" % W2_START[0]], "w3": p.tail(12), "w4": p.tail(1)}
    for wn, d in pw.items():
        fact(f"pqp_n_{wn}", len(d), str(len(d)), f"months with a PQP, {wn}")
        fact(f"pqp_start_{wn}", 0, f"{LONG[int(d.month.iloc[0][5:])]} {d.month.iloc[0][:4]}", f"first month, {wn}")
        fact(f"pqp_gap_median_{wn}", d.gap.median(), dollars(rnd(d.gap.median())), f"median PQP B-A gap, {wn}")
        fact(f"pqp_gap_min_{wn}", int(d.gap.min()), dollars(d.gap.min()), f"smallest PQP B-A gap, {wn} (negative: A above B)")
        ab = d[d.gap <= 0]
        fact(f"pqp_a_ge_b_months_{wn}", 0, "; ".join(f"{LONG[int(m[5:])]} {m[:4]}" for m in ab.month) or "none",
             f"months with A's PQP at or above B's, {wn}")
        fact(f"pqp_gap_max_{wn}", int(d.gap.max()), dollars(d.gap.max()), f"largest PQP B-A gap, {wn}")
        fact(f"pqp_gap_pct_median_{wn}", d.gap_pct_of_A.median(), pct(d.gap_pct_of_A.median()), f"median PQP gap as % of A's PQP, {wn}")
        fact(f"pqp_a_ge_b_{wn}", int((d.gap <= 0).sum()), str(int((d.gap <= 0).sum())), f"months with A's PQP at or above B's, {wn}")
    last = p.iloc[-1]
    fact("pqp_gap_oct2026", int(last.gap), dollars(last.gap), "PQP B-A gap, October 2026")
    fact("pqp_gap_pct_oct2026", last.gap_pct_of_A, "{:.1f}".format(last.gap_pct_of_A), "as % of A's PQP, October 2026")
    fact("w2_start_label", 0, label(*W2_START), "first exercise of window 2")
    fact("w2_start_month", 0, W2_START[0], "first month of window 2 (PQP)")
    fact("pqp_A_oct2026", int(last.pqp_A), dollars(last.pqp_A), "A's PQP, October 2026")
    fact("pqp_B_oct2026", int(last.pqp_B), dollars(last.pqp_B), "B's PQP, October 2026")

    # F2, quota shares (sums of quota over the window).
    for wn, d in windows.items():
        sa, sb, se = d.quota_A.sum(), d.quota_B.sum(), d.quota_E.sum()
        fact(f"quota_A_share_{wn}", 100 * sa / (sa + sb), str(rnd(100 * sa / (sa + sb))), f"A's % of A+B quota, {wn}")
        fact(f"quota_E_share_{wn}", 100 * se / (sa + sb + se), str(rnd(100 * se / (sa + sb + se))), f"E's % of A+B+E quota, {wn}")

    # F4, Category E against B and A.
    for wn, d in windows.items():
        n_eb = int((d.premium_E < d.premium_B).sum())
        n_top = int(((d.premium_E >= d.premium_A) & (d.premium_E >= d.premium_B)).sum())
        fact(f"e_below_b_{wn}", n_eb, str(n_eb), f"exercises with E below B, {wn}")
        fact(f"e_at_or_above_both_{wn}", n_top, str(n_top), f"exercises with E at or above both A and B, {wn}")
        fact(f"gap_EB_median_{wn}", d.gap_EB.median(), dollars(rnd(d.gap_EB.median())), f"median E-B gap, {wn}")

    # ---- write -------------------------------------------------------------
    w.to_csv(os.path.join(OUT, "exercises.csv"), index=False, lineterminator="\n")
    p.to_csv(os.path.join(OUT, "pqp_monthly.csv"), index=False, lineterminator="\n", float_format="%.4f")
    w[w.gap < 0][["month", "bidding_no", "label", "premium_A", "premium_B", "gap"]].to_csv(
        os.path.join(OUT, "a_above_b.csv"), index=False, lineterminator="\n")
    pd.DataFrame(F).to_csv(os.path.join(OUT, "facts.csv"), index=False, lineterminator="\n", float_format="%.6f")
    pd.DataFrame(checks, columns=["check", "result"]).to_csv(os.path.join(OUT, "checks.csv"), index=False, lineterminator="\n")
    for c, r in checks:
        print(f"  {c}: {r}")
    print(f"  {len(F)} facts written to out/facts.csv")


if __name__ == "__main__":
    sys.exit(main())

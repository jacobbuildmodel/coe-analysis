"""
04_mps_coding.py -- office/MPS_CODING.csv: one row per MAS monetary policy
statement, coded by the MPS coding rule (THESIS section 5) from the decision
paragraphs in office/MPS_CANDIDATES.txt (written by 03_mps_candidates.py).

  python3 sgd/04_mps_coding.py

The codes below were set by the researcher on 3 October 2026, reading only
MPS_CANDIDATES.txt. This script does not decide any code. It
  - checks that every quote is a verbatim substring of the paragraph it cites;
  - attaches S5a's own Slope, Width and Level cells for the date, as the
    cross-check (raw/s5a_mas_past_mp_decisions.html);
  - applies the checker's ruling of 3 October 2026 on the centre: where the
    statement's words give no direction (re-centred "at the prevailing
    level", flagged recentre_no_direction) or are AMBIGUOUS, the direction
    is taken from S5a's Level cell, MAS's own record of the decision. The
    statement-based code stays in centre_statement and the source of each
    direction in centre_source;
  - derives the slope in force, the re-centring score and p by the THESIS
    mapping;
  - writes office/MPS_CODING.csv.
It exits non-zero if a quote is not found or a date has no S5a row.
"""
import csv
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.join(HERE, "office", "MPS_CANDIDATES.txt")
S5A = os.path.join(HERE, "raw", "s5a_mas_past_mp_decisions.html")
OUT = os.path.join(HERE, "office", "MPS_CODING.csv")

NONE_W = "(no width wording)"
NONE_C = "(no re-centring wording)"

# date, slope, width, centre, recentre_no_direction, source (statement:para),
# quote_slope, quote_width, quote_centre, review, note
CODES = [
    ("20010222", "same", "same", "unchanged", "no", "20010712:3",
     "MAS decided to maintain this stance of a modest appreciation", "within an unchanged policy band", NONE_C,
     "yes", "Own decision paragraph excluded by an outcome marker and not read; coded from the 12 Jul 2001 "
            "statement's description of the January 2001 decision."),
    ("20010712", "zero", "same", "unchanged", "no", "20010712:16",
     "a policy band centred on a zero percent appreciation of the S$NEER", NONE_W, NONE_C, "no", ""),
    ("20011010", "zero", "wider", "unchanged", "no", "20011010:5",
     "will continue to be centred on a zero percent appreciation of the S$NEER",
     "decided to widen the policy band", NONE_C, "no", ""),
    ("20020102", "zero", "narrower", "unchanged", "yes", "20020102:23",
     "maintain a zero percent appreciation path for the policy band", "restoring a narrower policy band",
     "centred on the current level of the S$NEER", "yes",
     "Centred on the current level, no direction word: unchanged by rule. S5a gives a direction."),
    ("20020711", "zero", "same", "unchanged", "no", "20020711:20",
     "maintain its current policy stance of a zero per cent appreciation", NONE_W, NONE_C, "no", ""),
    ("20030102", "zero", "same", "unchanged", "no", "20030102:12",
     "maintain the neutral policy stance of a zero percent appreciation",
     "no change in the level at which the policy band is centred and in the width of the band",
     "no change in the level at which the policy band is centred", "no", ""),
    ("20030710", "zero", "same", "unchanged", "yes", "20030710:10",
     "while maintaining a zero percent appreciation path", "The width of the band will remain unchanged",
     "re-centre the exchange rate policy band at the current level of the S$NEER", "yes",
     "No direction word: unchanged by rule. S5a gives a direction; the 12 Apr 2004 statement (para 2) "
     "describes it as 'a re-centring of the policy band at a lower level in July 2003'."),
    ("20031010", "zero", "same", "unchanged", "no", "20031010:12",
     "maintain the current neutral policy stance of a zero percent appreciation",
     "no change in the level at which the policy band is centred and in the width of the band",
     "no change in the level at which the policy band is centred", "no", ""),
    ("20040412", "steeper", "same", "unchanged", "no", "20081010:2",
     "MAS has maintained the policy of a modest and gradual appreciation of the Singapore dollar nominal "
     "effective exchange rate (S$NEER) policy band since April 2004", NONE_W, NONE_C, "yes",
     "The statement's only candidate (para 2) recaps 2003 and states no April 2004 decision. Coded from "
     "MAS's later descriptions (10 Oct 2008 para 2; 11 Oct 2005 para 12 'adopted since April 2004') and "
     "S5a: a move from zero to an appreciating slope is steeper by rule."),
    ("20041011", "same", "same", "unchanged", "no", "20041011:11",
     "maintaining its policy of a modest and gradual appreciation of the S$NEER",
     "There will be no change in the slope or the width of the policy band", NONE_C, "no", ""),
    ("20050412", "same", "same", "unchanged", "no", "20050412:14",
     "maintain the current policy of a modest and gradual appreciation of the S$NEER policy band",
     "There will be no change in the slope or the width of the policy band", NONE_C, "no", ""),
    ("20051011", "same", "same", "unchanged", "no", "20051011:12",
     "maintain its current policy of a modest and gradual appreciation of the S$NEER policy band",
     "There will be no change in the level, slope or width of the policy band",
     "There will be no change in the level, slope or width of the policy band", "no", ""),
    ("20060411", "same", "same", "unchanged", "no", "20060411:12",
     "maintain the current policy of a modest and gradual appreciation of the S$NEER policy band",
     "nor any change to its slope or width", "There will be no re-centring of the policy band", "no", ""),
    ("20061010", "same", "same", "unchanged", "no", "20061010:13",
     "maintain the policy of a modest and gradual appreciation of the S$NEER policy band",
     "or any change to its slope or width", "There will be no re-centring of the policy band", "no", ""),
    ("20070410", "same", "same", "unchanged", "no", "20070410:11",
     "maintain the policy of a modest and gradual appreciation of the S$NEER policy band",
     "or any change to its slope or width", "There will be no re-centring of the policy band", "no", ""),
    ("20071010", "steeper", "same", "unchanged", "no", "20071010:10",
     "we will increase slightly the slope of the S$NEER policy band", "or any change in its width",
     "There will be no re-centring of the policy band", "no", ""),
    ("20080410", "same", "same", "up", "no", "20080410:12",
     "There will be no change to the slope or width of the policy band",
     "There will be no change to the slope or width of the policy band",
     "an upward shift of the policy band", "no",
     "Also: 're-centre the exchange rate policy band at the prevailing level of the S$NEER'."),
    ("20081010", "zero", "same", "unchanged", "no", "20081010:8",
     "shifting its policy stance to a zero percent appreciation of the S$NEER policy band",
     "there will be no re-centring of the band or change to its width",
     "there will be no re-centring of the band", "no",
     "The extracted paragraph merges MAS's inflation outlook with the decision (disclosed)."),
    ("20090414", "zero", "same", "unchanged", "yes", "20090414:10",
     "while keeping the zero percent appreciation path", "The width of the band will remain unchanged",
     "re-centre the exchange rate policy band to the prevailing level of the S$NEER", "yes",
     "No direction word: unchanged by rule. S5a gives a direction; the 14 Apr 2010 statement (para 2) "
     "says 'The policy band was re-centred downwards in April last year'."),
    ("20091012", "zero", "same", "unchanged", "no", "20091012:9",
     "maintain the current policy stance of a zero percent appreciation of the S$NEER policy path",
     "There will be no change to the width of the policy band",
     "the level at which it is centred", "no", ""),
    ("20100414", "steeper", "same", "unchanged", "yes", "20100414:7",
     "shift the policy band from that of a zero percent appreciation to one of modest and gradual appreciation",
     "There will be no change to the width of the policy band",
     "re-centre the exchange rate policy band at the prevailing level of the S$NEER", "yes",
     "No direction word: unchanged by rule. S5a gives a direction."),
    ("20101014", "steeper", "wider", "unchanged", "no", "20101014:7",
     "the slope of the policy band will be increased slightly", "widened slightly",
     "with no change to the level at which the band is centred", "no",
     "The paragraph also quotes MAS's CPI forecasts (disclosed)."),
    ("20110414", "same", "same", "up", "no", "20110414:7",
     "There will be no change to the slope and width of the band",
     "There will be no change to the slope and width of the band",
     "re-centre the exchange rate policy band upwards", "no",
     "Also: 're-centred below the prevailing level of the S$NEER'."),
    ("20111014", "flatter", "same", "unchanged", "no", "20111014:13",
     "the slope of the policy band will be reduced", "with no change to the width of the band",
     "the level at which it is centred", "no",
     "Still positive: 'continue with the policy of a modest and gradual appreciation'."),
    ("20120413", "steeper", "narrower", "unchanged", "no", "20120413:10",
     "The slope will be increased slightly", "restoring a narrower policy band",
     "there will be no change to the level at which the band is centred", "no", ""),
    ("20121012", "same", "same", "unchanged", "no", "20121012:13",
     "maintain the policy of a modest and gradual appreciation of the S$NEER policy band",
     "There will be no change to the slope and width of the policy band",
     "as well as the level at which it is centred", "no", ""),
    ("20130412", "same", "same", "unchanged", "no", "20130412:13",
     "maintain its policy of a modest and gradual appreciation of the S$NEER policy band",
     "There will be no change to the slope and width of the policy band",
     "as well as the level at which it is centred", "no", ""),
    ("20131014", "same", "same", "unchanged", "no", "20131014:11",
     "There will be no change to the slope of the policy band", "will be kept unchanged",
     "and the level at which it is centred", "no", ""),
    ("20140414", "same", "same", "unchanged", "no", "20140414:15",
     "There will be no change to the slope of the policy band", "The width of the band will be kept unchanged",
     "and the level at which it is centred", "no", ""),
    ("20141014", "same", "same", "unchanged", "no", "20141014:15",
     "There will be no change to the slope and width of the policy band",
     "There will be no change to the slope and width of the policy band",
     "and the level at which it is centred", "no", ""),
    ("20150128", "flatter", "same", "unchanged", "no", "20150128:14",
     "the slope of the policy band will be reduced", "with no change to its width",
     "and the level at which it is centred", "no",
     "Still positive: 'continue with the policy of a modest and gradual appreciation'."),
    ("20150414", "same", "same", "unchanged", "no", "20150414:15",
     "There will be no change to the slope and width of the policy band",
     "There will be no change to the slope and width of the policy band",
     "and the level at which it is centred", "no", ""),
    ("20151014", "flatter", "same", "unchanged", "no", "20151014:13",
     "the rate of appreciation will be reduced slightly",
     "There will be no change to the width of the policy band",
     "and the level at which it is centred", "no", ""),
    ("20160414", "zero", "same", "unchanged", "no", "20160414:14",
     "set the rate of appreciation of the S$NEER policy band at zero percent", NONE_W, NONE_C, "no",
     "The second candidate (para 16) states an S$NEER outcome (disclosed)."),
    ("20161014", "zero", "same", "unchanged", "no", "20161014:15",
     "maintain the rate of appreciation of the S$NEER policy band at zero percent",
     "The width of the policy band and the level at which it is centred will be unchanged",
     "The width of the policy band and the level at which it is centred will be unchanged", "no", ""),
    ("20170413", "zero", "same", "unchanged", "no", "20170413:14",
     "maintain the rate of appreciation of the S$NEER policy band at zero percent",
     "The width of the policy band and the level at which it is centred will be unchanged",
     "The width of the policy band and the level at which it is centred will be unchanged", "no", ""),
    ("20171013", "zero", "same", "unchanged", "no", "20171013:14",
     "maintain the rate of appreciation of the S$NEER policy band at zero percent",
     "The width of the policy band and the level at which it is centred will be unchanged",
     "The width of the policy band and the level at which it is centred will be unchanged", "no", ""),
    ("20180413", "steeper", "same", "unchanged", "no", "20180413:17",
     "increase slightly the slope of the S$NEER policy band, from zero percent previously",
     "The width of the policy band and the level at which it is centred will be unchanged",
     "The width of the policy band and the level at which it is centred will be unchanged", "no", ""),
    ("20181012", "steeper", "same", "unchanged", "no", "20181012:16",
     "increase slightly the slope of the S$NEER policy band",
     "The width of the policy band and the level at which it is centred will be unchanged",
     "The width of the policy band and the level at which it is centred will be unchanged", "no", ""),
    ("20190412", "same", "same", "unchanged", "no", "20190412:15",
     "maintain the current rate of appreciation of the S$NEER policy band",
     "There will be no change to its width and the level at which it is centred",
     "There will be no change to its width and the level at which it is centred", "no", ""),
    ("20191014", "flatter", "same", "unchanged", "no", "20191014:15",
     "reduce slightly the rate of appreciation of the S$NEER policy band",
     "There will be no change to the width of the policy band and the level at which it is centred",
     "There will be no change to the width of the policy band and the level at which it is centred", "no", ""),
    ("20200330", "zero", "same", "unchanged", "yes", "20200330:18",
     "adopt a zero percent per annum rate of appreciation of the policy band",
     "There will be no change to the width of the policy band",
     "starting at the prevailing level of the S$NEER", "yes",
     "Band starts at the prevailing level, no direction word: unchanged by rule. S5a gives a direction."),
    ("20201014", "zero", "same", "unchanged", "no", "20201014:17",
     "maintain a zero percent per annum rate of appreciation of the policy band",
     "The width of the policy band and the level at which it is centred will be unchanged",
     "The width of the policy band and the level at which it is centred will be unchanged", "no", ""),
    ("20210414", "zero", "same", "unchanged", "no", "20210414:14",
     "maintain a zero percent per annum rate of appreciation of the policy band",
     "The width of the policy band and the level at which it is centred will be unchanged",
     "The width of the policy band and the level at which it is centred will be unchanged", "no", ""),
    ("20211014", "steeper", "same", "unchanged", "no", "20211014:16",
     "raise slightly the slope of the S$NEER policy band, from zero percent previously",
     "The width of the policy band and the level at which it is centred will be unchanged",
     "The width of the policy band and the level at which it is centred will be unchanged", "no", ""),
    ("20220125", "steeper", "same", "unchanged", "no", "20220125:15",
     "raise slightly the rate of appreciation of the S$NEER policy band",
     "The width of the policy band and the level at which it is centred will be unchanged",
     "The width of the policy band and the level at which it is centred will be unchanged", "no", ""),
    ("20220414", "steeper", "same", "unchanged", "yes", "20220414:19",
     "increase slightly the rate of appreciation of the policy band",
     "There will be no change to the width of the policy band",
     "re-centre the mid-point of the exchange rate policy band at the prevailing level of the S$NEER", "yes",
     "No direction word: unchanged by rule ('further tighten' is not a centre trigger). S5a gives a direction."),
    ("20220714", "same", "same", "AMBIGUOUS", "no", "20220714:16",
     "There will be no change to the slope and width of the band",
     "There will be no change to the slope and width of the band",
     "re-centre the mid-point of the S$NEER policy band up to its prevailing level", "yes",
     "'up to its prevailing level': 'up' is not a listed trigger, and the wording also fits "
     "'re-centred at the prevailing level' (unchanged, flagged). Fits two categories: AMBIGUOUS."),
    ("20221014", "same", "same", "AMBIGUOUS", "no", "20221014:18",
     "There will be no change to the slope and width of the band",
     "There will be no change to the slope and width of the band",
     "re-centre the mid-point of the S$NEER policy band up to its prevailing level", "yes",
     "As 14 Jul 2022: AMBIGUOUS."),
    ("20230414", "same", "same", "unchanged", "no", "20230414:17",
     "maintain the prevailing rate of appreciation of the S$NEER policy band",
     "There will be no change to its width and the level at which it is centred",
     "There will be no change to its width and the level at which it is centred", "no", ""),
    ("20231013", "same", "same", "unchanged", "no", "20231013:13",
     "maintain the prevailing rate of appreciation of the S$NEER policy band",
     "There will be no change to its width and the level at which it is centred",
     "There will be no change to its width and the level at which it is centred", "no", ""),
    ("20240129", "same", "same", "unchanged", "no", "20240129:16",
     "maintain the prevailing rate of appreciation of the S$NEER policy band",
     "There will be no change to its width and the level at which it is centred",
     "There will be no change to its width and the level at which it is centred", "no", ""),
    ("20240412", "same", "same", "unchanged", "no", "20240412:14",
     "maintain the prevailing rate of appreciation of the S$NEER policy band",
     "There will be no change to its width and the level at which it is centred",
     "There will be no change to its width and the level at which it is centred", "no", ""),
    ("20240726", "same", "same", "unchanged", "no", "20240726:16",
     "maintain the prevailing rate of appreciation of the S$NEER policy band",
     "There will be no change to its width and the level at which it is centred",
     "There will be no change to its width and the level at which it is centred", "no", ""),
    ("20241014", "same", "same", "unchanged", "no", "20241014:16",
     "maintain the prevailing rate of appreciation of the S$NEER policy band",
     "There will be no change to its width and the level at which it is centred",
     "There will be no change to its width and the level at which it is centred", "no", ""),
    ("20250124", "flatter", "same", "unchanged", "no", "20250124:13",
     "reduce slightly the slope of the S$NEER policy band",
     "There will be no change to the width of the policy band or the level at which it is centred",
     "There will be no change to the width of the policy band or the level at which it is centred", "no", ""),
    ("20250414", "flatter", "same", "unchanged", "no", "20250414:13",
     "the rate of appreciation will be reduced slightly",
     "There will be no change to the width of the band and the level at which it is centred",
     "There will be no change to the width of the band and the level at which it is centred", "no", ""),
    ("20250730", "same", "same", "unchanged", "no", "20250730:13",
     "maintain the prevailing rate of appreciation of the S$NEER policy band",
     "There will be no change to its width and the level at which it is centred",
     "There will be no change to its width and the level at which it is centred", "no", ""),
    ("20251014", "same", "same", "unchanged", "no", "20251014:15",
     "maintain the prevailing rate of appreciation of the S$NEER policy band",
     "There will be no change to its width and the level at which it is centred",
     "There will be no change to its width and the level at which it is centred", "no", ""),
    ("20260129", "same", "same", "unchanged", "no", "20260129:12",
     "maintain the prevailing rate of appreciation of the S$NEER policy band",
     "There will be no change to its width and the level at which it is centred",
     "There will be no change to its width and the level at which it is centred", "no", ""),
    ("20260414", "steeper", "same", "unchanged", "no", "20260414:14",
     "increase slightly the rate of appreciation of the S$NEER policy band",
     "There will be no change to its width and the level at which it is centred",
     "There will be no change to its width and the level at which it is centred", "no", ""),
    ("20260727", "steeper", "same", "unchanged", "no", "20260727:14",
     "increase the rate of appreciation of the policy band very slightly",
     "There will be no change to the width of the policy band and the level at which it is centred",
     "There will be no change to the width of the policy band and the level at which it is centred", "no", ""),
]

MONTHS = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}


def candidates():
    """{(date, para): text} from MPS_CANDIDATES.txt."""
    out, date = {}, None
    for line in open(CAND, encoding="utf-8"):
        m = re.match(r"=== (\d{8})", line)
        if m:
            date = m.group(1)
        m = re.match(r"\[para (\d+)\] (.*)", line.rstrip("\n"))
        if m:
            out[(date, int(m.group(1)))] = m.group(2)
    return out


def s5a_rows():
    """{yyyymmdd: (slope, width, level)} from S5a's table."""
    t = open(S5A, encoding="utf-8", errors="replace").read()
    tab = re.search(r"<table.*?</table>", t, re.S).group(0)
    out = {}
    for r in re.findall(r"<tr.*?</tr>", tab, re.S):
        cells = [" ".join(html.unescape(re.sub(r"<[^>]+>", " ", c)).split())
                 for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, re.S)]
        m = re.match(r"(\d{1,2}) ([A-Z][a-z]{2}) (\d{4})", cells[0]) if cells else None
        if m and len(cells) >= 4:
            out[f"{m.group(3)}{MONTHS[m.group(2)]:02d}{int(m.group(1)):02d}"] = tuple(cells[1:4])
    return out


def main():
    C, S = candidates(), s5a_rows()
    bad = 0
    rows = []
    sif = None
    for (date, slope, width, centre, nodir, src, qs, qw, qc, review, note) in CODES:
        sd, sp = src.split(":")
        para = C.get((sd, int(sp)))
        if para is None:
            print(f"  {date}: source {src} not in MPS_CANDIDATES.txt")
            bad += 1
            para = ""
        for q in (qs, qw, qc):
            if q not in (NONE_W, NONE_C) and q not in para:
                print(f"  {date}: quote not found in {src}: {q!r}")
                bad += 1
        if date not in S:
            print(f"  {date}: no S5a row")
            bad += 1
        s5 = S.get(date, ("", "", ""))
        centre_statement, centre_source = centre, "statement"
        if nodir == "yes" or centre == "AMBIGUOUS":
            lvl = s5[2].lower()
            d = "up" if "upward" in lvl else "down" if "downward" in lvl else None
            if d is None:
                print(f"  {date}: ruling needs a direction in S5a's Level cell, found {s5[2]!r}")
                bad += 1
            else:
                centre, centre_source = d, "S5a Level cell (checker ruling, 3 Oct 2026)"
        # slope in force (THESIS section 5 mapping); AMBIGUOUS slope keeps the previous value
        if slope == "zero":
            sif = 0
        elif slope == "negative":
            sif = -1
        elif slope in ("steeper", "flatter"):
            sif = 1
        elif slope == "same":
            sif = 1 if sif is None else sif
        rc = {"up": 1, "down": -1}.get(centre, 0)   # unchanged and AMBIGUOUS count 0 (THESIS T7)
        rows.append([date, f"s5b_mas_mps_{date}.html", slope, width, centre, centre_statement, centre_source,
                     nodir, sif, rc, sif + rc,
                     src, qs, qw, qc, s5[0], s5[1], s5[2], review, note])
    missing = sorted(set(S) - {r[0] for r in rows})
    for d in missing:
        print(f"  S5a date {d} has no coded row")
        bad += 1
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["date", "statement_file", "slope", "width", "centre", "centre_statement", "centre_source",
                    "recentre_no_direction",
                    "slope_in_force", "recentre_score", "p", "source_para", "quote_slope", "quote_width",
                    "quote_centre", "s5a_slope", "s5a_width", "s5a_level", "checker_review", "note"])
        w.writerows(rows)
    print(f"  {len(rows)} rows written to {os.path.relpath(OUT, HERE)}; "
          f"{sum(r[18] == 'yes' for r in rows)} flagged for the checker; "
          f"{sum(r[6] != 'statement' for r in rows)} centre directions from S5a; {bad} problem(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

"""
02_occupation_map.py -- write office/OCCUPATION_MAP.csv from office/titles_listing.txt.

Reads only the title listing (titles, codes and headers from 01_titles.py);
opens no wage file. The lineages below were fixed from that listing before
any wage value was seen (THESIS section 4); this script checks each listed
code and title against the listing and marks any June where a title is
absent from the all-industries table.

Column `series` holds exactly one of main, sensitivity or excluded, so a
script can filter on it; `series_note` says why (checker reviews of c16f695
and 41921ee/77dd3f3, fixed before any value):
- a grade split keeps only the successor(s) on the sector's lowest rung in
  the main series; all successors averaged is the sensitivity;
- at the June 2015 workplace split, a cleaning successor stays only if the
  SSOC 2010-2015 correspondence maps it from 9113;
- a title missing in any scored June of its group's window is dropped
  (excluded), from the main series and the sensitivity alike.
Every link is settled from the SSOC tables in raw/ (w1d_*).
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
lines=open(HERE / 'office' / 'titles_listing.txt', encoding='utf-8').read().splitlines()
# ALL-industries titles by year (gross file for 2009-2011)
allt={};year=None;sec=None
for l in lines:
    if l.startswith('=== June'): year=int(l.split()[2]); allt[year]={}; continue
    if l.startswith('  ['): sec=('all industries' in l) and not ('basic' in l); continue
    if not sec or l.startswith('    header'): continue
    m=re.match(r'\s+(\d{4,5})?\s+(.*)',l)
    if m and m.group(1): allt[year][m.group(1)+' '+m.group(2).strip()]=1
def has(y,code,title):
    return any(k.startswith(code+' ') and k[len(code)+1:].lower().replace(' ','')==title.lower().replace(' ','') for k in allt[y])
def role(group,y):
    if y in (2020,2021): return 'excluded (2020-2021)'
    if y>=2023: return 'after window (shown, not scored)'
    if group=='cleaning':
        return 'pre' if y<=2012 else 'transition' if y<=2015 else 'post'
    if group in ('security','landscape'):
        return 'pre' if y<=2014 else 'transition' if y<=2016 else 'post'
    # comparison serves all windows
    return {2013:'cleaning transition; security/landscape pre',2014:'cleaning transition; security/landscape pre',
            2015:'transition (all)',2016:'cleaning post; security/landscape transition'}.get(y,'pre (all)' if y<=2012 else 'post (all)')
def ver(y):
    return 'SSOC 2005 (codes; header unlabelled)' if y==2009 else 'SSOC 2010 (codes; header unlabelled)' if y==2010 else 'SSOC 2010' if y<=2014 else 'SSOC 2015' if y<=2019 else 'SSOC 2020' if y<=2024 else 'SSOC 2024'
# lineages: group -> list of (years, code, title, link_note)
# Link notes cite the SSOC tables in raw/ (checker review of 41921ee/77dd3f3):
C05 = 'w1d_ssoc2010_correspondence.xls'
H10 = 'w1d_ssoc2010_report.pdf'
C15 = 'w1d_ssoc2015_correspondence.xls'
C20 = 'w1d_ssoc2020_correspondence.xlsx'
L={
'security':[
 ((2009,),'51440','Private security guard',''),
 (range(2010,2020),'5414','Security guard',f'June 2010: SSOC 2005 51440 -> SSOC 2010 54140, one-to-one ({C05}); 5414 = 54140 alone in the SSOC 2010 hierarchy ({H10}): linked. 2011-2014: same text. June 2015: 54140 -> 54141 security supervisor + 54142 private security officer ({C15}), so 5414 keeps the same members: linked.'),
 (range(2020,2026),'54144','Private security officer',f'June 2020: 54142 -> 54143 + 54144 ({C20})'),
 (range(2020,2026),'54143','Senior private security officer',f'June 2020: 54142 -> 54143 + 54144 ({C20})'),
 (range(2020,2026),'54142','Security supervisor',f'June 2020: 54141 -> 54141 + 54142 ({C20})'),
 (range(2020,2026),'54141','Senior security supervisor',f'June 2020: 54141 -> 54141 + 54142 ({C20})'),
],
'landscape':[
 ((2009,),'93111','Gardener',''),
 ((2010,),'92141','Garden labourer',f'SSOC 2005 93111 -> SSOC 2010 92141, one-to-one ({C05}): linked'),
 (range(2011,2020),'9214','Park and garden maintenance worker',f'June 2011: aggregate 9214 = 92141 garden labourer + 92142 grass cutter + 92143 tree cutter + 92149 other park and garden maintenance workers ({H10}): linked through the hierarchy; broader than 92141 (composition lean, THESIS T1). 2012-2019: same text; SSOC 2015 keeps all four codes ({C15}).'),
 (range(2020,2023),'9214','Park, garden and landscape maintenance worker',f'same code, text changed at June 2020; the four 2015 codes map only to 92141, 92142 and 92149, all inside 9214 ({C20}): same members, linked'),
 (range(2023,2026),'92142','Landscape worker','after window'),
],
'cleaning':[
 ((2009,),'91291','Office cleaner',''),
 ((2009,),'91292','Cleaner (Industrial establishment)',''),
 ((2010,),'91131','Office cleaner',f'SSOC 2005 91291 -> 91131, one-to-one ({C05}): linked'),
 ((2010,),'91132','Cleaner (industrial establishment)',f'SSOC 2005 91292 -> 91132, one-to-one ({C05}): linked'),
 (range(2011,2015),'9113','Cleaner in offices and other establishments',f'June 2011: aggregate 9113 = 91131 + 91132 + 91139 cleaner in offices and other establishments nec ({H10}): linked through the hierarchy; adds 91139 (composition lean, THESIS T1)'),
 (range(2015,2020),'91130','Office cleaner',f'June 2015: 91131 -> 91130 ({C15}): 9113 successor'),
 (range(2015,2020),'91140','Industrial establishment cleaner',f'June 2015: 91132 -> 91140 ({C15}): 9113 successor; ABSENT from the June 2018 table'),
 (range(2015,2020),'91160','Residential area cleaner (eg HDB estates, condominiums, private apartments, common areas within residential estates)',f'June 2015: from 91139 in part ({C15}): 9113 successor'),
 (range(2015,2020),'91170','Cleaner in open areas (eg bus stops, drains, waterways, overhead bridges, roads, expressways, parks, beaches)',f'June 2015: from 96130 sweeper and related worker only ({C15}, sheet ssoc2015-ssoc2010): not a 9113 successor; ABSENT from the June 2019 table'),
 (range(2015,2020),'91151','Food and beverage establishment cleaner (eg restaurants, food courts, hawker centres)',f'June 2015: from 91139 in part ({C15}): 9113 successor'),
 (range(2015,2020),'91190','Cleaner in other establishments (eg shopping malls, schools, hospitals, places of worship)',f'June 2015: from 91139 in part, and from 96130 sweeper in part ({C15}): 9113 successor'),
 (range(2020,2023),'91131','Office, commercial and industrial establishments indoor cleaner',f'June 2020: from 91130, 91140 and 91190, each in part ({C20})'),
 (range(2020,2023),'91132','Office, commercial and industrial establishments outdoor cleaner',f'June 2020: from 91130, 91140 and 91190, each in part ({C20})'),
 (range(2020,2023),'91133','Office, commercial and industrial establishments multi-skilled cleaner cum machine operator',f'June 2020: from 91130, 91140 and 91190, each in part ({C20})'),
 (range(2020,2023),'91161','Residential and open areas general cleaner',f'June 2020: from 91160 and 91170, each in part ({C20})'),
 (range(2020,2023),'91151','Food and beverage establishments general cleaner',f'June 2020: from 91151 in part; its multi-skilled part goes to 91154, not published ({C20})'),
],
'C shop sales assistant':[((2009,),'52102','Shop sales assistant',''),(range(2010,2026),'52202','Shop sales assistant',f'same text; 52102 -> 52202 one-to-one ({C05}); unchanged in 2015 and 2020: linked')],
'C cashier':[((2009,),'42111','Cashier',''),((2010,),'5230','Cashiers and ticket clerk',f'June 2010: 42111 -> 52302 one-to-one ({C05}), but only aggregate 5230 = 52301 cage/count supervisor + 52302 cashier + 52303 office cashier + 52309 other cashiers and ticket clerks is published ({H10}): linked through the hierarchy, broader for this one June (composition lean, THESIS T1)'),(range(2011,2023),'52302','Cashier',f'June 2011: 52302 published again: linked; unchanged in 2015 and 2020 ({C15}, {C20})'),(range(2023,2026),'52302','Cashier (general)','after window')],
'C waiter':[((2009,),'51230','Waiter',''),(range(2010,2026),'51312','Waiter',f'same text: linked; 51230 -> 51311 captain waiter/waiter supervisor + 51312 waiter ({C05}), so narrower from 2010 (composition lean, THESIS T1)')],
'C kitchen assistant':[((2009,),'91222','Kitchen assistant',''),(range(2010,2026),'94101','Kitchen assistant',f'same text: linked; 91222 -> 94101 + 94103 fast food preparer ({C05}), so narrower from 2010 (composition lean, THESIS T1)')],
'C food/drink stall assistant':[((2009,),'91223','Food and drink stall assistant',''),(range(2010,2026),'94102','Food/Drink stall assistant',f'June 2010: text differs ("and" vs "/"); 91223 -> 94102 one-to-one ({C05}): linked')],
'C general office clerk':[((2009,),'41201','Office clerk',''),(range(2010,2023),'4110','General office clerk',f'June 2010: 41201 -> 41101 ({C05}); OWS publishes aggregate 4110 = 41101 + 41102 filing and copying clerk + 41103 personnel/HR clerk + 41109 other administrative clerks ({H10}): linked through the hierarchy, broader from 2010 (composition lean, THESIS T1). SSOC 2015 (v2018) folds 41102 into 41101, inside the aggregate.'),(range(2023,2025),'41101','Office clerk (including filing and copying)','after window'),((2025,),'41101','Office clerk','after window')],
'C lorry driver':[((2009,),'83260','Lorry driver',''),(range(2010,2026),'83321','Lorry driver',f'same text; 83260 -> 83321 one-to-one ({C05}): linked')],
'C van driver':[((2009,),'83242','Van driver',''),(range(2010,2026),'83223','Van driver',f'same text; 83242 -> 83223 one-to-one ({C05}): linked')],
}
LOWEST_2012 = "lowest rung, w3_cleaning_tcc_report_2012.pdf (at least $1,000) and w3_cleaning_tcc_2016.pdf Annex C (General/Indoor Cleaners, e.g. offices, schools, hospitals and polyclinics; F&B General Cleaners)"
LOWEST_2021 = "lowest rung, w3_cleaning_col_order_2021.pdf para 1.1"
# (group, code) -> (series, series_note); series is exactly main, sensitivity or excluded
SERIES = {
    ("security", "54144"): ("main", "Security Officer rank, the lowest (w3_security_stc_2017.pdf Annex C): grade-split rule"),
    ("security", "54143"): ("sensitivity", "Senior SO rank: higher grade (grade-split rule)"),
    ("security", "54142"): ("sensitivity", "Security Supervisor rank: higher grade (grade-split rule)"),
    ("security", "54141"): ("sensitivity", "Senior Security Supervisor rank: higher grade (grade-split rule)"),
    ("cleaning", "91130"): ("main", LOWEST_2012),
    ("cleaning", "91190"): ("main", LOWEST_2012),
    ("cleaning", "91140"): ("excluded", "dropped from the main series and the sensitivity: missing-year rule, absent June 2018. The rule as written drops a title missing in any scored June from its group, so it is dropped, not kept as a sensitivity"),
    ("cleaning", "91160"): ("sensitivity", "9113 successor, but spans HDB estates (conservancy group, higher rung) and condominiums (w3_cleaning_mom_page.pdf); its exclusion from the main series is a stated lean toward FAIL at T2"),
    ("cleaning", "91170"): ("excluded", "workplace-split rule: not a 9113 successor; also absent June 2019 (missing-year rule)"),
    ("cleaning", "91131"): ("main", "General/Indoor Cleaners, " + LOWEST_2021),
    ("cleaning", "91132"): ("sensitivity", "Outdoor/Healthcare/Restroom Cleaners rung, above the lowest (grade-split rule)"),
    ("cleaning", "91133"): ("sensitivity", "Multi-skilled Cleaner cum Machine Operator rung, above the lowest (grade-split rule)"),
    ("cleaning", "91161"): ("sensitivity", "conservancy General Cleaners rung, above the lowest; successor of 91160 (and of 91170, which the workplace-split rule excludes)"),
}


def series(group, year, code):
    if year <= 2014:
        return ("main", "")                   # before any split: whole lines
    if group == "cleaning" and code == "91151":
        if year <= 2019:
            return ("main", "9113 successor; " + LOWEST_2012)
        return ("main", "F&B General Cleaners, " + LOWEST_2021)
    return SERIES.get((group, code), ("main", ""))


rows=[];missing=[]
for g,ls in L.items():
    for yrs,code,title,note in ls:
        for y in yrs:
            ok=has(y,code,title)
            if not ok and not ('ABSENT' in note and ((y==2018 and code=='91140') or (y==2019 and code=='91170'))):
                # try prefix match for long titles
                ok=any(k.startswith(code+' '+title[:25]) for k in allt[y])
            present='yes' if ok else 'NO'
            if not ok: missing.append((g,y,code,title))
            rows.append([g,y,role(g if not g.startswith('C ') else 'C',y),ver(y),code,title,present,*series(g,y,code),note])
with open(HERE / 'office' / 'OCCUPATION_MAP.csv', 'w', newline='', encoding='utf-8') as f:
    w=csv.writer(f,lineterminator='\n')
    w.writerow(['group','june','june_role','classification','ssoc_code','title_as_published','in_all_industries_table','series','series_note','link_and_break_note'])
    w.writerows(sorted(rows,key=lambda r:(r[0],r[1],r[4])))
    X=[
     ('excluded','hotel cleaners','9112 Cleaner and helper in hotels and related establishments (2011-2022); 91293/91122 Hotel cleaner (2009-2010, 2023-)','hotel housekeeping is mostly in-house, unbound until Sep 2022; title also mixes helpers'),
     ('excluded','dishwashers and table-top cleaners','91224 Dish washer (2009); 94104 Dish washer/Plate collector (2010-2014); 91152 Dish washer/Plate collector/Table-top cleaner (2015-2019); 91153 Dishwasher and 91152 Table-top cleaner (2020-)','ladder ambiguous: named in the cleaning ladder F&B group (w3_cleaning_col_order_2021.pdf) and in food services from 2023; title moves between cleaner and food groups; excluded from both sides'),
     ('excluded','gardener/horticultural/nursery worker','6113 (2015-2019); 61133 (2020-)','first published June 2015, absent from the pre-period; nursery and farm work outside LCR maintenance'),
     ('excluded','building structure cleaner','71332 (2010, 2012-2013)','construction trade (facade cleaning), not the cleaning ladder'),
     ('excluded','food service counter attendant','52492 (2010-)','absent from June 2009: dropped by the missing-year rule'),
     ('excluded','tea server/steward','94104 (2015-)','first published June 2015'),
     ('excluded','car drivers','none published','no car-driver title in any OWS table; the comparison drivers are van and lorry drivers'),
     ('excluded','waste truck, trailer-truck drivers; lorry attendant','83326/83324; 83322; 93335','waste management ladder (2023) and cleaning conservancy roles; trailer-truck and attendants not named in THESIS'),
     ('excluded','aircraft, ship, motor-vehicle, window cleaners; laundry workers','various','not general cleaning covered by the cleaning ladder'),
    ]
    for a,b,c,d in X:
        w.writerow([b,'',a,'',c.split(' ')[0],c,'','excluded','',d])
print(f'wrote office/OCCUPATION_MAP.csv: {len(rows)} rows')
print('absent from the all-industries table:', [(g, y, c) for g, y, c, _ in missing])

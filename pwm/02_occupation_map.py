"""
02_occupation_map.py -- write office/OCCUPATION_MAP.csv from office/titles_listing.txt.

Reads only the title listing (titles, codes and headers from 01_titles.py);
opens no wage file. The lineages below were fixed from that listing before
any wage value was seen (THESIS section 4); this script checks each listed
code and title against the listing and marks any June where a title is
absent from the all-industries table.
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
L={
'security':[
 ((2009,),'51440','Private security guard',''),
 (range(2010,2020),'5414','Security guard','2010: text differs from 2009 title; link via SSOC 2005-2010 correspondence, PENDING. 2011-2019: same text.'),
 (range(2020,2026),'54144','Private security officer','split of 5414 at June 2020; link via SSOC 2015-2020 correspondence, PENDING'),
 (range(2020,2026),'54143','Senior private security officer','split of 5414 at June 2020; link via SSOC 2015-2020 correspondence, PENDING'),
],
'landscape':[
 ((2009,),'93111','Gardener',''),
 ((2010,),'92141','Garden labourer','text differs from 2009 title; link via SSOC 2005-2010 correspondence, PENDING'),
 (range(2011,2020),'9214','Park and garden maintenance worker','2011: 4-digit aggregate replaces 5-digit 92141 (different text); link via the SSOC 2010 hierarchy, PENDING. 2012-2019: same text.'),
 (range(2020,2023),'9214','Park, garden and landscape maintenance worker','same code, text changed at June 2020; link via SSOC 2015-2020 correspondence, PENDING'),
 (range(2023,2026),'92142','Landscape worker','after window'),
],
'cleaning':[
 ((2009,),'91291','Office cleaner',''),
 ((2009,),'91292','Cleaner (Industrial establishment)',''),
 ((2010,),'91131','Office cleaner','same text as 2009: linked'),
 ((2010,),'91132','Cleaner (industrial establishment)','same text as 2009 (case only): linked'),
 (range(2011,2015),'9113','Cleaner in offices and other establishments','June 2011: 4-digit aggregate replaces 91131 + 91132 (merge); link via the SSOC 2010 hierarchy, PENDING'),
 (range(2015,2020),'91130','Office cleaner','June 2015: split of 9113 (candidate successor); SSOC 2010-2015 correspondence, PENDING'),
 (range(2015,2020),'91140','Industrial establishment cleaner','candidate successor of 9113; ABSENT from the June 2018 table'),
 (range(2015,2020),'91160','Residential area cleaner (eg HDB estates, condominiums, private apartments, common areas within residential estates)','candidate successor of 9113, PENDING correspondence'),
 (range(2015,2020),'91170','Cleaner in open areas (eg bus stops, drains, waterways, overhead bridges, roads, expressways, parks, beaches)','candidate successor of 9113; ABSENT from the June 2019 table'),
 (range(2015,2020),'91151','Food and beverage establishment cleaner (eg restaurants, food courts, hawker centres)','candidate successor of 9113, PENDING correspondence'),
 (range(2020,2023),'91131','Office, commercial and industrial establishments indoor cleaner','June 2020: SSOC 2015-2020 split/merge, PENDING correspondence'),
 (range(2020,2023),'91132','Office, commercial and industrial establishments outdoor cleaner','June 2020: PENDING correspondence'),
 (range(2020,2023),'91133','Office, commercial and industrial establishments multi-skilled cleaner cum machine operator','June 2020: new title; PENDING correspondence'),
 (range(2020,2023),'91161','Residential and open areas general cleaner','June 2020: merge of 91160 + 91170; PENDING correspondence'),
 (range(2020,2023),'91151','Food and beverage establishments general cleaner','June 2020: text changed; PENDING correspondence'),
],
'C shop sales assistant':[((2009,),'52102','Shop sales assistant',''),(range(2010,2026),'52202','Shop sales assistant','same text: linked')],
'C cashier':[((2009,),'42111','Cashier',''),((2010,),'5230','Cashiers and ticket clerk','June 2010: merge with ticket clerks; link via SSOC 2005-2010 correspondence, PENDING'),(range(2011,2023),'52302','Cashier','June 2011: split back out of 5230; PENDING'),(range(2023,2026),'52302','Cashier (general)','after window')],
'C waiter':[((2009,),'51230','Waiter',''),(range(2010,2026),'51312','Waiter','same text: linked')],
'C kitchen assistant':[((2009,),'91222','Kitchen assistant',''),(range(2010,2026),'94101','Kitchen assistant','same text: linked')],
'C food/drink stall assistant':[((2009,),'91223','Food and drink stall assistant',''),(range(2010,2026),'94102','Food/Drink stall assistant','June 2010: text differs ("and" vs "/"); link via SSOC 2005-2010 correspondence, PENDING')],
'C general office clerk':[((2009,),'41201','Office clerk',''),(range(2010,2023),'4110','General office clerk','June 2010: text differs; link via SSOC 2005-2010 correspondence, PENDING'),(range(2023,2025),'41101','Office clerk (including filing and copying)','after window'),((2025,),'41101','Office clerk','after window')],
'C lorry driver':[((2009,),'83260','Lorry driver',''),(range(2010,2026),'83321','Lorry driver','same text: linked')],
'C van driver':[((2009,),'83242','Van driver',''),(range(2010,2026),'83223','Van driver','same text: linked')],
}
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
            rows.append([g,y,role(g if not g.startswith('C ') else 'C',y),ver(y),code,title,present,note])
with open(HERE / 'office' / 'OCCUPATION_MAP.csv', 'w', newline='', encoding='utf-8') as f:
    w=csv.writer(f,lineterminator='\n')
    w.writerow(['group','june','june_role','classification','ssoc_code','title_as_published','in_all_industries_table','link_and_break_note'])
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
        w.writerow([b,'',a,'',c.split(' ')[0],c,'',d])
print(f'wrote office/OCCUPATION_MAP.csv: {len(rows)} rows')
print('absent from the all-industries table:', [(g, y, c) for g, y, c, _ in missing])

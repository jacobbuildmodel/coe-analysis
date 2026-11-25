"""
make_fixtures.py -- invented CPI rows in the shape SingStat serves them.

  build(directory, scenario, end=(2027, 2))

No real value is used anywhere: every index is generated here from a seed.
Scenarios (all share one seed, so they differ only by what is planted):
  null       no launch effect; tariff steps in electricity; a January 2023
             and 2024 step in every food row and in All Items
  planted    as null, plus a lasting 0.8 per cent step in the hawker row in
             every CDC launch month of events.csv
  noisy      as planted, with six times the month-to-month noise in the
             hawker row (gate D must then refuse to score; the restaurant rows
             keep their noise, so C2 still passes)
  flat_power as null, with no tariff steps in electricity (C1 must fail)
  no_gst     as null, with no January 2023 and 2024 step in the restaurant
             rows 1.11.1 and 1.11.2 (C2 must fail)
  regime     as no_gst, with the restaurant rows rising 0.6 per cent a month
             faster from 2022 Jan (C2 must fail: a faster pace is not a step)
  jan_only   as null, plus a lasting 0.8 per cent step in the hawker row in
             January 2025 and January 2026 only (T3 fails, T1 holds: the T3
             sentence prints)
"""
import csv
import json
import math
import pathlib
import random

HERE = pathlib.Path(__file__).resolve().parent
NAMES = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
FOOD = {"1.11.3": 0.08, "1.11.1": 0.10, "1.11.2": 0.15, "1": 0.05}   # noise sd, per cent
PLANT = 0.8


def cdc_launches():
    with open(HERE.parent / "events.csv", newline="", encoding="ascii") as f:
        return {(int(e["year"]), int(e["month"])) for e in csv.DictReader(f)
                if e["kind"] == "cdc_voucher"}


def months(first, last):
    y, m = first
    while (y, m) <= last:
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def build(directory, scenario, end=(2027, 2)):
    rng = random.Random(20261127)
    scale = 6.0 if scenario == "noisy" else 1.0
    restaurants = ("1.11.1", "1.11.2")
    launches = cdc_launches()
    rows = {}
    for code, sd in FOOD.items():
        level, obs = math.log(60.0), {}
        for y, m in months((2005, 1), end):
            noise = rng.gauss(0.0, sd * (scale if code == "1.11.3" else 1.0))
            step = 0.18 + (0.25 if m == 1 else 0.0) + noise
            if (y, m) in ((2023, 1), (2024, 1)):
                if not (scenario in ("no_gst", "regime") and code in restaurants):
                    step += 1.0
            if scenario == "regime" and code in restaurants and (y, m) >= (2022, 1):
                step += 0.6
            if scenario == "jan_only" and code == "1.11.3" and (y, m) in ((2025, 1), (2026, 1)):
                step += PLANT
            if code == "1.11.3" and scenario in ("planted", "noisy") and (y, m) in launches:
                step += PLANT
            level += step / 100.0
            obs[(y, m)] = level
        rows[code] = obs
    level, obs = math.log(90.0), {}
    for y, m in months((2015, 1), end):
        step = rng.gauss(0.0, 0.02)
        if m in (1, 4, 7, 10) and scenario != "flat_power":
            step += rng.choice((-1, 1)) * rng.uniform(1.0, 5.0)
        level += step / 100.0
        obs[(y, m)] = level
    rows["1.03.2.3"] = obs
    directory = pathlib.Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for code, obs in rows.items():
        cols = [{"key": f"{y} {NAMES[m - 1]}", "value": f"{math.exp(v):.3f}"}
                for (y, m), v in sorted(obs.items())]
        body = {"Data": {"id": "M213751", "row": [
            {"seriesNo": code, "rowText": "INVENTED", "columns": cols}]}}
        (directory / f"M213751_{code}.json").write_text(json.dumps(body),
                                                        encoding="ascii")
    return directory

"""
Municipal waste processing script.

Builds the processed municipal waste table per country for the dashboard, from the
interim municipal waste indicators.

Input:  data/interim/env_wasmun.parquet, one row per country (geo) and year (time), 2010-2024:
    municipal_waste_gen_pc      waste generated, kg per person
    municipal_waste_gen_total   waste generated, thousand tonnes
    municipal_waste_rcy_total   waste recycled, thousand tonnes
    municipal_waste_rcy_rate    recycled / generated, share 0-1
Output: data/processed/municipal_waste.json, one record per country (geo) and year
(overwritten on each run). Columns:
    geo     country code: the 27 EU Member States and EU27_2020 (src/geo, keep_eu27)
    year    year (whole number), 2010-2024
    mw_pc   municipal waste generated, kg per person
    mw_tt   municipal waste generated, thousand tonnes
    mw_pc_day  municipal waste generated, kg per person per day: mw_pc / 365 (also in leap
            years), two decimals; for a human-scale figure (EU27 2023: 510 kg = 1.40 kg a day)
Missing values are empty (null).

Run cell by cell (# %%) in the VS Code Interactive Window, or from anywhere:
    .venv/Scripts/python scripts/processed/municipal_waste.py
"""

# %%
import pandas as pd

from geo import keep_eu27
from paths import DIR_PROCESSED, interim_file

FILE_WASMUN = interim_file("env_wasmun")
OUTPUT = DIR_PROCESSED / "municipal_waste.json"
DAYS_PER_YEAR = 365  # also in leap years: a rounded human-scale figure, not an exact daily rate

# import the interim municipal waste data
df_wasmun = pd.read_parquet(FILE_WASMUN)

df_wasmun.head()


# %%
# Keep geo, time and waste generated, with short names:
#   mw_pc  municipal waste generated, kg per person
#   mw_tt  municipal waste generated, thousand tonnes
#   year   year as a whole number (time in the interim data is text)
#   mw_pc_day  kg per person per day = mw_pc / 365, two decimals
# Keep only the 27 EU Member States and EU27_2020 (drops non-EU countries).
df_mw = (
    df_wasmun[["geo", "time", "municipal_waste_gen_pc", "municipal_waste_gen_total"]]
    .rename(columns={"municipal_waste_gen_pc": "mw_pc", "municipal_waste_gen_total": "mw_tt"})
    .assign(year=lambda d: d["time"].astype(int),
            mw_pc_day=lambda d: (d["mw_pc"] / DAYS_PER_YEAR).round(2))
    [["geo", "year", "mw_pc", "mw_tt", "mw_pc_day"]]
    .pipe(keep_eu27)
    .sort_values(["geo", "year"])
    .reset_index(drop=True)
)

df_mw.head()


# %%
# Save as a list of records; empty values are written as null
DIR_PROCESSED.mkdir(parents=True, exist_ok=True)
df_mw.to_json(OUTPUT, orient="records", indent=2, force_ascii=False)
print(f"saved {len(df_mw)} rows to {OUTPUT}")

# %%

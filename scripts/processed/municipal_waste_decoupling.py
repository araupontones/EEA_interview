"""
Municipal waste decoupling: compare the change in municipal waste generated per person with
the change in real GDP per person, per country and year.

Both series are indexed to BASE_YEAR = 100, so they can be shown on one axis. Waste is
decoupled from economic growth when the GDP index rises faster than the waste index:
    relative decoupling   waste grows, but more slowly than GDP
    absolute decoupling   waste stays flat or falls while GDP grows

Base year: 2011, the first year with municipal waste data for all 27 EU countries
(Denmark has no figure for 2010). A country without a value in the base year gets an empty
index.

Input:
    data/interim/env_wasmun.parquet   municipal waste generated, kg per person
    data/interim/nama_10_pc.parquet   real GDP per person, euro at 2020 prices
Output: data/processed/municipal_waste_decoupling.json, one record per country (geo) and year
(overwritten on each run). Columns:
    geo            country code: the 27 EU Member States and EU27_2020 (src/geo, keep_eu27)
    year           year (whole number)
    mw_pc          municipal waste generated, kg per person
    gdp_pc         real GDP per person, euro at 2020 prices
    mw_pc_index    mw_pc, BASE_YEAR = 100, one decimal
    gdp_pc_index   gdp_pc, BASE_YEAR = 100, one decimal
Only country-years present in both sources are kept (2010-2024). Missing values are empty.

Run cell by cell (# %%) in the VS Code Interactive Window, or from anywhere:
    .venv/Scripts/python scripts/processed/municipal_waste_decoupling.py
"""

# %%
import pandas as pd

from geo import keep_eu27
from paths import DIR_PROCESSED, interim_file

OUTPUT = DIR_PROCESSED / "municipal_waste_decoupling.json"
BASE_YEAR = 2011

# import the interim data
df_wasmun = pd.read_parquet(interim_file("env_wasmun"))
df_gdp = pd.read_parquet(interim_file("nama_10_pc"))

# %%
# Join waste per person and GDP per person by country and year.
# Inner join: keeps the country-years present in both sources (years 2010-2024 of the waste data).
# Keep only the 27 EU Member States and EU27_2020 (drops non-EU countries).
df_decoupling = (
    df_wasmun[["geo", "time", "municipal_waste_gen_pc"]]
    .rename(columns={"municipal_waste_gen_pc": "mw_pc"})
    .merge(df_gdp, on=["geo", "time"], how="inner", validate="1:1")
    .pipe(keep_eu27)
    .assign(year=lambda d: d["time"].astype(int))
    .drop(columns="time")
    [["geo", "year", "mw_pc", "gdp_pc"]]
    .sort_values(["geo", "year"])
    .reset_index(drop=True)
)

df_decoupling.head()

# %%
# Index both series to BASE_YEAR = 100 within each country.
# Countries without a value in BASE_YEAR get an empty index.
for col in ["mw_pc", "gdp_pc"]:
    base = df_decoupling["geo"].map(
        df_decoupling.loc[df_decoupling["year"] == BASE_YEAR].set_index("geo")[col]
    )
    df_decoupling[f"{col}_index"] = (df_decoupling[col] / base * 100).round(1)

df_decoupling.loc[df_decoupling["geo"] == "EU27_2020"]

# %%
# Save as a list of records; empty values are written as null
DIR_PROCESSED.mkdir(parents=True, exist_ok=True)
df_decoupling.to_json(OUTPUT, orient="records", indent=2, force_ascii=False)
print(f"saved {len(df_decoupling)} rows to {OUTPUT}")

# %%

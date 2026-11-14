"""
Build the packaging recycling rates from the Eurostat source env_waspacr
(Recycling rates of packaging waste for monitoring compliance with policy targets,
by type of packaging).

The raw data has one row per country, year, packaging type (waste) and rate method (unit).
This script keeps:
    year 2023
    unit RT_TGT2025, the rate calculated under the rules for the 2025 target and onwards
and adds the packaging name from the codebook (e.g. W150102 -> Plastic packaging).

Output columns:
    geo          country code
    time         year (text, "2023")
    waste_name   packaging type, including the total "Packaging" (W1501)
    value        recycling rate, in %
One row per country and packaging type. Missing rates are kept as empty values.

Input:  data/raw/env_waspacr/df.parquet and lookup.json
Output: data/interim/env_waspacr.parquet (overwritten on each run)

Run from anywhere:
    .venv/Scripts/python scripts/interim/env_waspacr.py

Developed in notebooks/python/05_create_packaging.ipynb.
"""

import json

import pandas as pd

from paths import DIR_INTERIM, interim_file, raw_dir

DATA_SOURCE = 'env_waspacr'
DATA_RAW_DIR = raw_dir(DATA_SOURCE)
EXPORT_DIR = DIR_INTERIM
EXPORT_FILE = interim_file(DATA_SOURCE)

YEAR = "2023"
UNIT = "RT_TGT2025"  # Rate (2025 target and onwards)


def build_indicators(df, codebook):
    """Return the recycling rate by country and packaging type for YEAR and UNIT."""
    df = df.copy()
    df['waste_name'] = df['waste'].map(codebook['waste'])

    rows = (df['time'] == YEAR) & (df['unit'] == UNIT)
    return df.loc[rows, ['geo', 'time', 'waste_name', 'value']]


def main():
    df = pd.read_parquet(DATA_RAW_DIR / "df.parquet")
    with open(DATA_RAW_DIR / "lookup.json", encoding="utf-8") as f:
        codebook = json.load(f)

    df_final = build_indicators(df, codebook)
    df_final = validate(df_final)

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    df_final.to_parquet(EXPORT_FILE, index=False)
    n_missing = df_final['value'].isna().sum()
    print(f"{DATA_SOURCE}: saved {len(df_final)} rows ({n_missing} without a value) to {EXPORT_FILE}")


# =====================================================================================
# DATA VALIDATION
# From this point onwards, the indicators are checked, and values that cannot be shown in
# the dashboard are adjusted. Each adjustment only applies while the value is still in the
# source, so it stops having an effect if Eurostat revises the data.
# See dashboard_notes/method_notes.md.
# =====================================================================================

# Cyprus (CY), steel packaging.
# Issue: the recycling rate of steel packaging for Cyprus is far above 100 % (221.5 % in
# 2023; above 190 % in every year since 2017, 369.1 % in 2020). This is the published
# figure, also used in the Commission's early warning assessment, so it is not an error.
# Adjustment: the value is set to empty (NA) so it does not distort the charts, which show
# recycling rates on a scale from 0 to 105 %. It only applies when the value is above
# 200 %, so a revised figure from Eurostat is kept as it is.
CY_STEEL_MAX = 200.0


def validate(df):
    """Return df with values that cannot be shown in the dashboard set to empty, and report each one."""
    df = df.copy()

    cy_steel = (
        (df['geo'] == 'CY')
        & (df['waste_name'] == 'Steel packaging')
        & (df['value'] > CY_STEEL_MAX)
    )
    for _, row in df.loc[cy_steel].iterrows():
        print(f"validation: CY Steel packaging {row['time']} = {row['value']} % "
              f"(above {CY_STEEL_MAX:.0f} %), set to empty")
    df.loc[cy_steel, 'value'] = pd.NA

    return df


if __name__ == "__main__":
    main()

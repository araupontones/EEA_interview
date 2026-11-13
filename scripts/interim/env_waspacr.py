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

Developed in notebooks/python/5.create_packaging.ipynb.
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]  # scripts/interim -> project root
DATA_SOURCE = 'env_waspacr'
DATA_RAW_DIR = ROOT / "data/raw" / DATA_SOURCE
EXPORT_DIR = ROOT / "data/interim"
EXPORT_FILE = EXPORT_DIR / f"{DATA_SOURCE}.parquet"

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

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    df_final.to_parquet(EXPORT_FILE, index=False)
    n_missing = df_final['value'].isna().sum()
    print(f"{DATA_SOURCE}: saved {len(df_final)} rows ({n_missing} without a value) to {EXPORT_FILE}")


if __name__ == "__main__":
    main()

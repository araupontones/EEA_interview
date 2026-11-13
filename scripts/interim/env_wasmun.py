"""
Build the municipal waste indicators from the Eurostat source env_wasmun
(Municipal waste by waste management operations).

The raw data has one row per country, year, unit and waste operation. This script
keeps the combinations needed and turns them into one row per country (geo) and year
(time) with these indicators:
    municipal_waste_gen_pc      waste generated, kg per person    (KG_HAB, GEN)
    municipal_waste_gen_total   waste generated, thousand tonnes  (THS_T, GEN)
    municipal_waste_rcy_total   waste recycled, thousand tonnes   (THS_T, RCY)
    municipal_waste_rcy_rate    recycled / generated, share 0-1

Input:  data/raw/env_wasmun/df.parquet
Output: data/interim/env_wasmun.parquet (overwritten on each run)

Run from anywhere:
    .venv/Scripts/python scripts/interim/env_wasmun.py

Developed in notebooks/python/4.create_mw_pc.ipynb.
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]  # scripts/interim -> project root
DATA_SOURCE = 'env_wasmun'
DATA_RAW_DIR = ROOT / "data/raw" / DATA_SOURCE
EXPORT_DIR = ROOT / "data/interim"
EXPORT_FILE = EXPORT_DIR / f"{DATA_SOURCE}.parquet"


def select_indicator(df, unit, wst_oper, name):
    """Return geo, time and the value for one unit and waste operation, with value renamed to `name`."""
    rows = (df['unit'] == unit) & (df['wst_oper'] == wst_oper)
    return df.loc[rows, ['geo', 'time', 'value']].rename(columns={'value': name})


def build_indicators(df):
    """Return one row per geo-time with the municipal waste indicators."""
    df_gen_pc    = select_indicator(df, 'KG_HAB', 'GEN', 'municipal_waste_gen_pc')     # kg per person
    df_gen_total = select_indicator(df, 'THS_T',  'GEN', 'municipal_waste_gen_total')  # thousand tonnes
    df_rcy_total = select_indicator(df, 'THS_T',  'RCY', 'municipal_waste_rcy_total')  # thousand tonnes

    # Left join on recycling, so years without recycling data are kept.
    df_merged = (
        df_gen_pc
        .merge(df_gen_total, on=['geo', 'time'])
        .merge(df_rcy_total, on=['geo', 'time'], how='left')
    )

    # Recycling rate = recycled / generated (RCY = material recycling + composting and digestion)
    df_merged['municipal_waste_rcy_rate'] = (
        df_merged['municipal_waste_rcy_total'] / df_merged['municipal_waste_gen_total']
    )
    return df_merged


def main():
    df = pd.read_parquet(DATA_RAW_DIR / "df.parquet")
    df_merged = build_indicators(df)

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    df_merged.to_parquet(EXPORT_FILE, index=False)
    print(f"{DATA_SOURCE}: saved {len(df_merged)} rows to {EXPORT_FILE}")


if __name__ == "__main__":
    main()

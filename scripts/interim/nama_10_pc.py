"""
Build GDP per person from the Eurostat source nama_10_pc
(Gross domestic product (GDP) and main components per capita - annual data).

The raw data has one row per country, year, national accounts item (na_item) and unit.
This script keeps:
    na_item B1GQ            Gross domestic product at market prices
    unit    CLV20_EUR_HAB   Chain linked volumes (2020), euro per capita
i.e. real GDP per person, in euro at 2020 prices. Real (not current prices) so that the
change over time shows growth of the economy, not inflation. This is the measure used to
compare with waste generation (decoupling).

Output columns:
    geo      country code, including EU and euro area totals (e.g. EU27_2020)
    time     year (text, e.g. "2023")
    gdp_pc   real GDP per person, euro at 2020 prices
One row per country and year, all years in the raw data (2010 onwards). Missing values are
kept as empty values.

Input:  data/raw/nama_10_pc/df.parquet
Output: data/interim/nama_10_pc.parquet (overwritten on each run)

Run from anywhere:
    .venv/Scripts/python scripts/interim/nama_10_pc.py
"""

import pandas as pd

from paths import DIR_INTERIM, interim_file, raw_dir

DATA_SOURCE = 'nama_10_pc'
DATA_RAW_DIR = raw_dir(DATA_SOURCE)
EXPORT_DIR = DIR_INTERIM
EXPORT_FILE = interim_file(DATA_SOURCE)

NA_ITEM = "B1GQ"          # Gross domestic product at market prices
UNIT = "CLV20_EUR_HAB"    # Chain linked volumes (2020), euro per capita


def build_indicators(df):
    """Return one row per geo-time with real GDP per person (gdp_pc)."""
    rows = (df['na_item'] == NA_ITEM) & (df['unit'] == UNIT)
    return (
        df.loc[rows, ['geo', 'time', 'value']]
        .rename(columns={'value': 'gdp_pc'})
        .reset_index(drop=True)
    )


def main():
    df = pd.read_parquet(DATA_RAW_DIR / "df.parquet")
    df_final = build_indicators(df)

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    df_final.to_parquet(EXPORT_FILE, index=False)
    n_missing = df_final['gdp_pc'].isna().sum()
    print(f"{DATA_SOURCE}: saved {len(df_final)} rows ({n_missing} without a value) to {EXPORT_FILE}")


if __name__ == "__main__":
    main()

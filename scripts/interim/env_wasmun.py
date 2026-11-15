"""
Build the municipal waste indicators from the Eurostat source env_wasmun
(Municipal waste by waste management operations).

The raw data has one row per country, year, unit and waste operation. This script
keeps the combinations needed and turns them into one row per country (geo) and year
(time) with these indicators:
    municipal_waste_gen_pc          waste generated, kg per person          (KG_HAB, GEN)
    municipal_waste_gen_total       waste generated, thousand tonnes        (THS_T, GEN)
    municipal_waste_rcy_total       recycling, thousand tonnes              (THS_T, RCY)
    municipal_waste_rcy_rate        RCY / generated, share 0-1
Treatment by operation, all in thousand tonnes (THS_T):
    municipal_waste_trt_total       waste treatment, all operations         (TRT)
    municipal_waste_prp_reu_total   preparing for re-use                    (PRP_REU)
    municipal_waste_rcy_m_total     recycling, material                     (RCY_M)
    municipal_waste_rcy_c_d_total   recycling, composting and digestion     (RCY_C_D)
    municipal_waste_rcv_e_total     energy recovery, R1                     (RCV_E)
    municipal_waste_dsp_i_total     incineration without energy recovery, D10 (DSP_I)
    municipal_waste_dsp_l_total     landfill and other disposal, D1-D7, D12 (DSP_L_OTH)

RCY is kept for the recycling rate already used in the dashboard. It is not the sum of the
operations: RCY = RCY_M + RCY_C_D, plus PRP_REU for some countries and years. The treatment
shares must be built from the components (PRP_REU, RCY_M, RCY_C_D), never from RCY, or
preparing for re-use is counted twice. DSP_I_RCV_E (all incineration) = RCV_E + DSP_I, so
it is not kept. See docs/method_notes.md, section 2.

Data validation (end of the script): Eurostat publishes no EU27 total for an operation in a
year when a Member State is missing (EU27 2023: incineration without energy recovery and
landfill, because Latvia has no figure). The EU27 value is then estimated as the sum of the
Member States, with each missing Member State at its previous-year value (Eurostat's own
method for EU aggregates). The column municipal_waste_eu27_estimated is True where this
was done.

Input:  data/raw/env_wasmun/df.parquet, data/lookups/geo_eu27.json
Output: data/interim/env_wasmun.parquet (overwritten on each run)

Run from anywhere:
    .venv/Scripts/python scripts/interim/env_wasmun.py

Developed in notebooks/python/04_create_mw_pc.ipynb.
"""

import pandas as pd

from geo import EU27_TOTAL, eu27_countries
from paths import DIR_INTERIM, interim_file, raw_dir

DATA_SOURCE = 'env_wasmun'
DATA_RAW_DIR = raw_dir(DATA_SOURCE)
EXPORT_DIR = DIR_INTERIM
EXPORT_FILE = interim_file(DATA_SOURCE)

# Treatment operations kept, in thousand tonnes: Eurostat code -> column name
TREATMENT = {
    'TRT':       'municipal_waste_trt_total',
    'PRP_REU':   'municipal_waste_prp_reu_total',
    'RCY_M':     'municipal_waste_rcy_m_total',
    'RCY_C_D':   'municipal_waste_rcy_c_d_total',
    'RCV_E':     'municipal_waste_rcv_e_total',
    'DSP_I':     'municipal_waste_dsp_i_total',
    'DSP_L_OTH': 'municipal_waste_dsp_l_total',
}


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

    # Recycling rate = recycled / generated (RCY = material recycling + composting and digestion,
    # and for some countries and years also preparing for re-use)
    df_merged['municipal_waste_rcy_rate'] = (
        df_merged['municipal_waste_rcy_total'] / df_merged['municipal_waste_gen_total']
    )

    # Treatment by operation (thousand tonnes), left joins: a missing operation stays empty.
    for code, name in TREATMENT.items():
        df_merged = df_merged.merge(select_indicator(df, 'THS_T', code, name),
                                    on=['geo', 'time'], how='left')
    return df_merged


def main():
    df = pd.read_parquet(DATA_RAW_DIR / "df.parquet")
    df_merged = build_indicators(df)
    df_merged = validate(df_merged)

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    df_merged.to_parquet(EXPORT_FILE, index=False)
    print(f"{DATA_SOURCE}: saved {len(df_merged)} rows to {EXPORT_FILE}")


# =====================================================================================
# DATA VALIDATION
# From this point onwards, the indicators are checked, and values that cannot be used in
# the dashboard are adjusted. Each adjustment only applies while the issue is still in the
# source, so it stops having an effect if Eurostat revises the data.
# See docs/method_notes.md, section 2 ("Treatment across the waste hierarchy").
# =====================================================================================

# EU27 total missing for a treatment operation.
# Issue: Eurostat publishes no EU27 total for an operation in a year if a Member State has
# no figure for it. In the current release, the EU27 2023 values for incineration without
# energy recovery (DSP_I) and landfill (DSP_L_OTH) are missing because Latvia has none, so
# the EU27 treatment shares for 2023 would be incomplete.
# Adjustment: the EU27 value is estimated as the sum of the 27 Member States, with each
# missing Member State at its previous-year value. This is how Eurostat estimates missing
# countries in EU aggregates (env_wasmun metadata, section 18.5). In years with all Member
# States, this sum matches the published EU27 total within 3 thousand tonnes.
# The rule only fills an empty EU27 value, so it stops applying as soon as Eurostat
# publishes one. It is not applied to PRP_REU, which Eurostat never publishes for the EU27
# and which many Member States do not report (it stays empty). The rule is skipped if a
# missing Member State has no previous-year value either.
EU27_ESTIMATED_OPERATIONS = ['TRT', 'RCY_M', 'RCY_C_D', 'RCV_E', 'DSP_I', 'DSP_L_OTH']


def validate(df):
    """Return df with missing EU27 treatment totals estimated, and report each one."""
    df = df.copy()
    df['municipal_waste_eu27_estimated'] = False
    countries = eu27_countries()
    df_ms = df[df['geo'].isin(countries)]

    for code in EU27_ESTIMATED_OPERATIONS:
        col = TREATMENT[code]
        wide = df_ms.pivot(index='time', columns='geo', values=col).reindex(columns=countries)
        wide = wide.sort_index()
        previous = wide.shift(1)  # previous-year value of each Member State

        eu_rows = df.index[(df['geo'] == EU27_TOTAL) & df[col].isna()]
        for i in eu_rows:
            year = df.at[i, 'time']
            if year not in wide.index:
                continue
            values = wide.loc[year]
            missing = values.index[values.isna()].tolist()
            if previous.loc[year, missing].isna().any():
                print(f"validation: {EU27_TOTAL} {code} {year} missing, not estimated "
                      f"(no previous-year value for {missing})")
                continue
            estimate = values.fillna(previous.loc[year]).sum()
            df.at[i, col] = estimate
            df.at[i, 'municipal_waste_eu27_estimated'] = True
            filled = ', '.join(f"{g} at its {int(year) - 1} value {previous.at[year, g]:.0f}"
                               for g in missing)
            print(f"validation: {EU27_TOTAL} {code} {year} missing, estimated as sum of "
                  f"Member States = {estimate:.0f} thousand tonnes ({filled})")
    return df


if __name__ == "__main__":
    main()

"""
Municipal waste treatment processing script.

Builds the shares of municipal waste generated that go to each treatment operation, per
country and year, for the waste hierarchy in the dashboard, and the same operations in kg
per person a year (for the sankey of waste generated -> levels of the hierarchy).

All shares are of waste GENERATED (not of waste treated), in % with one decimal, so they
are measured like the recycling rate and the EU targets (recycling and landfill targets are
set as a share of municipal waste generated). Because treatment is not always equal to
generation (temporary storage, exports, weight losses in pre-treatment, waste not
collected), the operations do not always add up to 100 %; the remainder is kept in
`unaccounted_pct`. See docs/method_notes.md, section 2 ("Treatment across the waste hierarchy").

Kg per person a year (`*_kg_pc` columns): share of waste generated (unrounded) x municipal
waste generated per person (`municipal_waste_gen_pc`, kg, Eurostat's own per-person figure,
the same value as `mw_pc` in municipal_waste.json), i.e. operation (thousand tonnes) / waste
generated (thousand tonnes) x waste generated per person (kg). All from the same env_wasmun
rows as the shares, so the kg columns add up to `mw_kg_pc` like the shares add up to 100 %
(up to rounding). Rounded to one decimal (the dashboard can round for display).

Mapping of the Eurostat operations to the five steps of the waste hierarchy
(Waste Framework Directive, Art. 4):
    1. Prevention               no share (waste not generated; see waste per person)
    2. Preparing for re-use     PRP_REU
    3. Recycling                RCY_M (material) + RCY_C_D (composting and digestion)
    4. Other recovery           RCV_E (incineration with energy recovery, R1)
    5. Disposal                 DSP_I (incineration without energy recovery, D10)
                                + DSP_L_OTH (landfill and other disposal, D1-D7, D12)
The recycling share is built from RCY_M and RCY_C_D, never from RCY, which includes
preparing for re-use for some countries and years: this would count it twice.

Input:  data/interim/env_wasmun.parquet (thousand tonnes per operation, see its docstring)
Output: data/processed/municipal_waste_treatment.json, one record per country (geo) and
year (overwritten on each run). Columns:
    geo                     country code: the 27 EU Member States and EU27_2020 (keep_eu27)
    year                    year (whole number), 2010-2024
    mw_tt                   municipal waste generated, thousand tonnes
    prep_reuse_pct          preparing for re-use (PRP_REU), % of generated
    recycling_material_pct  material recycling (RCY_M), % of generated
    recycling_compost_pct   composting and digestion (RCY_C_D), % of generated
    recycling_pct           recycling step: material + composting and digestion, % of generated
    energy_recovery_pct     other recovery step: incineration with energy recovery (RCV_E)
    incineration_pct        incineration without energy recovery (DSP_I), % of generated
    landfill_pct            landfill and other disposal (DSP_L_OTH), % of generated
    disposal_pct            disposal step: incineration without energy recovery + landfill
    unaccounted_pct         100 - (prep_reuse + recycling + energy_recovery + disposal);
                            generated waste not in any reported operation (negative if more
                            was treated than generated). Empty if a step other than
                            preparing for re-use is missing; where preparing for re-use is
                            missing, it may contain it.
    treated_pct             all waste treated (TRT), % of generated
    mw_kg_pc                municipal waste generated, kg per person a year (= mw_pc in
                            municipal_waste.json)
    prep_reuse_kg_pc, recycling_material_kg_pc, recycling_compost_kg_pc, recycling_kg_pc,
    energy_recovery_kg_pc, incineration_kg_pc, landfill_kg_pc, disposal_kg_pc,
    unaccounted_kg_pc       the same operations and steps as the *_pct columns, in kg per
                            person a year, one decimal; empty where the share is empty;
                            unaccounted_kg_pc negative where unaccounted_pct is (Portugal)
    estimated               True where the EU27 value of an operation was estimated by the
                            interim data validation (EU27 2023: incineration without energy
                            recovery and landfill, Latvia missing)
Missing values are empty (null). Preparing for re-use is empty for the EU27 (Eurostat
publishes no EU27 total) and for Member States that do not report it (most years before 2020).

Run cell by cell (# %%) in the VS Code Interactive Window, or from anywhere:
    .venv/Scripts/python scripts/processed/municipal_waste_treatment.py
"""

# %%
import pandas as pd

from geo import keep_eu27
from paths import DIR_PROCESSED, interim_file

FILE_WASMUN = interim_file("env_wasmun")
OUTPUT = DIR_PROCESSED / "municipal_waste_treatment.json"

# import the interim municipal waste data, EU27 only
df_wasmun = pd.read_parquet(FILE_WASMUN).pipe(keep_eu27)

df_wasmun.head()


# %%
# Shares of waste generated, in %, one per operation (thousand tonnes / thousand tonnes)
gen = df_wasmun["municipal_waste_gen_total"]


def pct(col):
    """Return column `col` as a % of waste generated."""
    return df_wasmun[col] / gen * 100


df_trt = pd.DataFrame({
    "geo": df_wasmun["geo"],
    "year": df_wasmun["time"].astype(int),
    "mw_tt": gen,
    "prep_reuse_pct": pct("municipal_waste_prp_reu_total"),
    "recycling_material_pct": pct("municipal_waste_rcy_m_total"),
    "recycling_compost_pct": pct("municipal_waste_rcy_c_d_total"),
    "energy_recovery_pct": pct("municipal_waste_rcv_e_total"),
    "incineration_pct": pct("municipal_waste_dsp_i_total"),
    "landfill_pct": pct("municipal_waste_dsp_l_total"),
    "treated_pct": pct("municipal_waste_trt_total"),
    "estimated": df_wasmun["municipal_waste_eu27_estimated"],
})

# Hierarchy steps: sums are empty if one part is missing (min_count), never filled with zero
df_trt["recycling_pct"] = df_trt[["recycling_material_pct", "recycling_compost_pct"]].sum(axis=1, min_count=2)
df_trt["disposal_pct"] = df_trt[["incineration_pct", "landfill_pct"]].sum(axis=1, min_count=2)

# Remainder: preparing for re-use counts as zero only here, where it is not reported, so the
# remainder can still be calculated; the other steps must all be present.
steps = df_trt[["recycling_pct", "energy_recovery_pct", "disposal_pct"]]
df_trt["unaccounted_pct"] = (
    100 - steps.sum(axis=1, min_count=3) - df_trt["prep_reuse_pct"].fillna(0)
)

df_trt.describe().T


# %%
# Kg per person a year: unrounded share x waste generated per person (kg). Empty where the
# share or the per-person figure is empty.
KG_STEPS = [
    "prep_reuse", "recycling_material", "recycling_compost", "recycling",
    "energy_recovery", "incineration", "landfill", "disposal", "unaccounted",
]
df_trt["mw_kg_pc"] = df_wasmun["municipal_waste_gen_pc"]
for step in KG_STEPS:
    df_trt[f"{step}_kg_pc"] = df_trt[f"{step}_pct"] / 100 * df_trt["mw_kg_pc"]

df_trt.filter(regex="geo|year|_kg_pc").query("year == 2023")


# %%
# Round rates and kg per person to one decimal, order the columns, keep rows with waste generated
COLUMNS = [
    "geo", "year", "mw_tt",
    "prep_reuse_pct", "recycling_material_pct", "recycling_compost_pct", "recycling_pct",
    "energy_recovery_pct", "incineration_pct", "landfill_pct", "disposal_pct",
    "unaccounted_pct", "treated_pct",
    "mw_kg_pc", *[f"{step}_kg_pc" for step in KG_STEPS],
    "estimated",
]
num_cols = [c for c in COLUMNS if c.endswith(("_pct", "_kg_pc"))]
df_trt[num_cols] = df_trt[num_cols].round(1)
df_trt = (
    df_trt.loc[df_trt["mw_tt"].notna(), COLUMNS]
    .sort_values(["geo", "year"])
    .reset_index(drop=True)
)

df_trt.query("year == 2023")


# %%
# Save as a list of records; empty values are written as null
DIR_PROCESSED.mkdir(parents=True, exist_ok=True)
df_trt.to_json(OUTPUT, orient="records", indent=2, force_ascii=False)
print(f"saved {len(df_trt)} rows to {OUTPUT}")

# %%

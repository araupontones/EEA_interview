"""
Recycling data processing script:
This script processes recycling data for analysis and reporting purposes.
It reads recycling data from data/interim/env_waspacr.parquet.
And data/interim/env_wasmun.parquet.
From wasmum, it takes the municipal recycling data.
From waspacr, it takes the packaging recycling data.

It makes formats consistent for analysis.
And append the data for combined analysis.
Then it calculates the distance to the 2025 recycling target, in percentage points
(value - target), using data/lookups/recycling_targets.json.

Output: data/processed/recycling_distance_to_target.json, one record per country (geo) and
waste category (waste_name), 2023 (overwritten on each run). Columns:
    geo, time, waste_name, value (recycling rate, %), distance_to_target (p.p.)

Run from anywhere, after the interim scripts:
    .venv/Scripts/python scripts/processed/recycling_distance_to_target.py
"""

# %%
import pandas as pd
from paths import interim_file
from paths import DIR_LOOKUPS, DIR_PROCESSED

OUTPUT = DIR_PROCESSED / "recycling_distance_to_target.json"

FILE_WASPACR = interim_file("env_waspacr")
FILE_WASMUN = interim_file("env_wasmun")

# import the raw data from the interim files
df_waspacr = pd.read_parquet(FILE_WASPACR)
df_wasmun = pd.read_parquet(FILE_WASMUN)

#import lookup of target years
lookup_target_years = pd.read_json(DIR_LOOKUPS / "recycling_targets.json")



#make formats consistent for analysis

# %%
## Municipal waste: keep 2023 and the recycling rate in the same format as waspacr
## (share 0-1 -> percentage with one decimal, e.g. 0.681 -> 68.1)
df_mun_2023 = (
    df_wasmun.loc[df_wasmun["time"] == "2023", ["geo", "time", "municipal_waste_rcy_rate"]]
    .rename(columns={"municipal_waste_rcy_rate": "value"})
    .assign(
        waste_name="Municipal waste",
        value=lambda d: (d["value"] * 100).round(1),
    )
    [["geo", "time", "waste_name", "value"]]
)


# %%
# Append municipal and packaging recycling rates
df_appended = pd.concat([df_mun_2023, df_waspacr], ignore_index=True)

df_appended.head()

# %%
# Distance to the 2025 target, in percentage points: value - target
# Negative = below the target, positive = above it.
# Empty when the rate is missing or the category has no target
# (Metallic packaging, Other packaging).
df_targets = (
    df_appended
    .merge(lookup_target_years[["waste_name", "target_2025"]], on="waste_name", how="left", validate="m:1")
    .assign(distance_to_target=lambda d: (d["value"] - d["target_2025"]).round(1))
    .drop(columns="target_2025")
)

df_targets.head()

# %%
# Save as a list of records; empty values are written as null
DIR_PROCESSED.mkdir(parents=True, exist_ok=True)
df_targets.to_json(OUTPUT, orient="records", indent=2, force_ascii=False)
print(f"saved {len(df_targets)} rows to {OUTPUT}")

# %%
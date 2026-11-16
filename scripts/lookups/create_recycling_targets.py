"""
Create the lookup of EU recycling targets for each waste category in the recycling data
(scripts/processed/recycling_distance_to_target.py, df_appended).

Targets are recycling rates in %, in the same format as the data (e.g. 65.0):
    Municipal waste   Waste Framework Directive 2008/98/EC, Art. 11(2)(c)-(d),
                      as amended by Directive (EU) 2018/851 (preparing for re-use and recycling)
    Packaging types   Packaging and Packaging Waste Directive 94/62/EC, Art. 6(1)(f) (all
                      packaging) and 6(1)(g) (materials), as amended by Directive (EU) 2018/852
                      (Steel packaging = ferrous metals). The 2025 targets were set by the
                      Directive; Regulation (EU) 2025/40 (PPWR), Art. 52(1), carries them over.
Metallic packaging and Other packaging have no EU target: they are kept with empty targets
so every category in the data has a row.

Output columns:
    waste_name    same labels as df_appended
    target_2025   recycling target for 2025, in %
    target_2030   recycling target for 2030, in %
    legal_basis   legal act that sets the target
    article       article that sets the 2025 target (for packaging, the 2030 targets are in
                  Art. 6(1)(h) and (i) of the Directive)

Output: data/lookups/recycling_targets.json, one record per waste category (overwritten on each run)

Run from anywhere:
    .venv/Scripts/python scripts/lookups/create_recycling_targets.py
"""

import json

import pandas as pd

from paths import DIR_LOOKUPS

OUTPUT = DIR_LOOKUPS / "recycling_targets.json"

WFD = "Waste Framework Directive 2008/98/EC (as amended by Directive (EU) 2018/851)"
PPWD = "Packaging and Packaging Waste Directive 94/62/EC (as amended by Directive (EU) 2018/852)"

# waste_name, target_2025, target_2030, legal_basis, article
TARGETS = [
    ("Municipal waste",               55.0, 60.0, WFD,  "Art. 11(2)"),
    ("Packaging",                     65.0, 70.0, PPWD, "Art. 6(1)(f)"),
    ("Plastic packaging",             50.0, 55.0, PPWD, "Art. 6(1)(g)"),
    ("Wooden packaging",              25.0, 30.0, PPWD, "Art. 6(1)(g)"),
    ("Steel packaging",               70.0, 80.0, PPWD, "Art. 6(1)(g)"),  # ferrous metals
    ("Aluminium packaging",           50.0, 60.0, PPWD, "Art. 6(1)(g)"),
    ("Glass packaging",               70.0, 75.0, PPWD, "Art. 6(1)(g)"),
    ("Paper and cardboard packaging", 75.0, 85.0, PPWD, "Art. 6(1)(g)"),
    ("Metallic packaging",            None, None, None, None),  # no EU target
    ("Other packaging",               None, None, None, None),  # no EU target
]

df_targets = pd.DataFrame(
    TARGETS, columns=["waste_name", "target_2025", "target_2030", "legal_basis", "article"]
)

# Save as a list of records; empty targets (NaN) are written as null
records = df_targets.astype(object).where(df_targets.notna(), None).to_dict(orient="records")

DIR_LOOKUPS.mkdir(parents=True, exist_ok=True)
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)
    f.write("\n")

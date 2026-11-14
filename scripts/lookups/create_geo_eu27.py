"""
Create the lookup of the geographies covered by the processed data: the 27 EU member
states and the EU27 total, with their Eurostat geo code and display name.

Takes the country names from the geo dimension of demo_gind and keeps only the EU27
codes listed in this script, then adds the EU27 total (EU27_2020) with the short name
"EU27". The processed scripts filter their data with this lookup (src/geo, keep_eu27),
and the dashboard can use it to show names instead of codes.

Input:  data/raw/demo_gind/lookup.json
Output: data/lookups/geo_eu27.json, 28 entries, e.g. {"BE": "Belgium", ..., "EU27_2020": "EU27"}
(overwritten on each run; do not edit by hand, change this script instead)

Run from anywhere:
    .venv/Scripts/python scripts/lookups/create_geo_eu27.py

Run it again only if the EU membership changes or demo_gind is downloaded again.
"""

import json
import logging
import pandas as pd

from paths import DIR_LOOKUPS, raw_dir

#log = logging.getLogger(__name__)

LOOKUP = raw_dir("demo_gind") / "lookup.json"
OUTPUT = DIR_LOOKUPS / "geo_eu27.json"

# Eurostat geo codes of the EU27 member states (note: Greece is EL, not GR)
EU27 = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU", "IE",
    "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE",
}

# Open lookups of countries
with open(LOOKUP, encoding='utf-8') as f:
    geo = json.load(f)['geo']

# keep only EU 27 states
EU27_geo = {k: v for k, v in geo.items() if k in EU27}

# add the EU27 total, with a short display name
# (the Eurostat label is "European Union - 27 countries (from 2020)")
EU27_geo["EU27_2020"] = "EU27"

#save in OUTPUT
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(EU27_geo, f, indent=2, ensure_ascii=False)
    f.write("\n")
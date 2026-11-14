"""
Create the lookup of the 27 EU member states, with their Eurostat geo code and name.

Takes the country list from the geo dimension of demo_gind and keeps only the EU27
codes listed in this script. Use the result to filter any dataset to EU27 countries.

Input:  data/raw/demo_gind/lookup.json
Output: data/lookups/geo_eu27.json, e.g. {"BE": "Belgium", ...} (overwritten on each run)

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

#save in OUTPUT
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(EU27_geo, f, indent=2, ensure_ascii=False)
    f.write("\n")
"""
Create the lookup of the 27 EU member states, with their Eurostat geo code and name.

Takes the country list from the geo dimension of demo_gind and keeps only the EU27
codes listed in this script. Use the result to filter any dataset to EU27 countries.

Input:  data/raw/demo_gind/lookup.json
Output: data/lookups/geo_EU27.json, e.g. {"BE": "Belgium", ...} (overwritten on each run)

Run from anywhere:
    .venv/Scripts/python scripts/lookups/create_eu27_lookup.py

Run it again only if the EU membership changes or demo_gind is downloaded again.
"""

import json
import logging
from pathlib import Path
import pandas as pd

#log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]  # scripts/lookups -> project root
LOOKUP = ROOT / "data/raw/demo_gind/lookup.json"
OUTPUT = ROOT / "data/lookups/geo_EU27.json"

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
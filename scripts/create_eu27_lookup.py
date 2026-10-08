import json
import logging
from pathlib import Path
import pandas as pd

#log = logging.getLogger(__name__)

LOOKUP = Path("C:/repositaries/4.personal/EEA_interview/data/raw/demo_gind/lookup.json")
OUTPUT = Path("data/lookups/geo_EU27.json")

# Eurostat geo codes of the EU27 member states (note: Greece is EL, not GR)
EU27 = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU", "IE",
    "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE",
}

# Open lookups of countries
geo=json.load(open(LOOKUP,encoding='utf-8'))['geo']

# keep only EU 27 states
EU27_geo = {k: v for k, v in geo.items() if k in EU27}

#save in OUTPUT
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(EU27_geo, f, indent=2, ensure_ascii=False)
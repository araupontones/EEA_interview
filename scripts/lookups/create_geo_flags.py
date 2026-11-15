"""
Create the lookup from geography code to flag code, for the flags shown in the dashboard.

The dashboard shows flags from the flag-icons npm package (MIT licence, pinned in
dashboard/package.json), which names its files after lower-case ISO 3166-1 alpha-2 codes
(e.g. flags/1x1/at.svg). Eurostat codes are the same as ISO codes, except:
    EL          Greece, ISO code GR
    EU27_2020   the EU27 total, shown with the EU flag (flag-icons code "eu")

Input:  data/lookups/geo_eu27.json (the geographies in the processed data)
Output: data/lookups/geo_flags.json, geography code -> flag code, e.g. "AT": "at"
        (overwritten on each run)

Run from anywhere:
    .venv/Scripts/python scripts/lookups/create_geo_flags.py
"""

import json

from geo import eu27_geos
from paths import DIR_LOOKUPS

OUTPUT = DIR_LOOKUPS / "geo_flags.json"

# Eurostat codes whose flag code is not the lower-case Eurostat code
EXCEPTIONS = {
    "EL": "gr",
    "EU27_2020": "eu",
}


def main():
    geos = eu27_geos()
    flags = {geo: EXCEPTIONS.get(geo, geo.lower()) for geo in geos}

    bad = {geo: code for geo, code in flags.items() if len(code) != 2 or not code.isalpha()}
    if bad:
        raise ValueError(f"flag codes must be two letters, add these to EXCEPTIONS: {bad}")

    DIR_LOOKUPS.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(flags, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"saved {len(flags)} flag codes to {OUTPUT}")


if __name__ == "__main__":
    main()

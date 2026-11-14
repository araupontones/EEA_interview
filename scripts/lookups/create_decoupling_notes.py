"""
Create the notes shown under the decoupling chart in the dashboard.

The dashboard shows the general note for every country, and a country note when the
selected country (or the EU27) needs care. Where a note has a break_year, the dashboard
also marks that year on the chart.

The texts summarise dashboard_notes/method_notes.md (sections 5 and 6). When the method
notes change, update the texts here and run the pipeline. Do not edit the JSON by hand.

Output columns:
    general_note     text shown for every country
    country_notes    one record per geography with a note:
        geo          country code (27 Member States or EU27_2020)
        break_year   year of a break in the series of waste per person, or null
        note         text shown when this geography is selected

Input:  data/lookups/geo_eu27.json (to check the country codes)
Output: data/lookups/decoupling_notes.json (overwritten on each run)

Run from anywhere:
    .venv/Scripts/python scripts/lookups/create_decoupling_notes.py
"""

import json

from geo import eu27_geos
from paths import DIR_LOOKUPS

OUTPUT = DIR_LOOKUPS / "decoupling_notes.json"

GENERAL_NOTE = (
    "Both lines show the change since 2011 (2011 = 100): an index of 110 means 10 % higher "
    "than in 2011. GDP is in real terms (2020 prices), so it shows the growth of the economy, "
    "not inflation. When the GDP line is above the waste line, the economy grew more than "
    "waste per person: waste is decoupled from economic growth."
)

# geo, break_year, note
COUNTRY_NOTES = [
    ("EU27_2020", None,
     "In 2020 and 2021 the lines are affected by COVID-19: GDP fell while waste per person "
     "rose, likely because people spent more time at home. The EU27 waste figure also rises "
     "from 2020 because Austria, Belgium "
     "and Slovakia started to count municipal waste from businesses (see their notes)."),
    ("CZ", 2017,
     "From 2017 Czechia also counts municipal-type waste from businesses and waste collected "
     "outside the municipal system. This raised waste per person by 44 % from 2016 to 2017: "
     "a change in definition, not more waste. Before the change, waste grew more slowly than GDP."),
    ("BE", 2020,
     "From 2020 Belgium reports municipal waste as defined in EU law, including similar waste "
     "from businesses. This raised waste per person by 75 % from 2019 to 2020: a change in "
     "definition, not more waste. Before the change, waste per person fell while GDP grew."),
    ("AT", 2020,
     "From 2020 Austria also counts municipal waste from businesses (commerce and industry). "
     "This raised waste per person by 42 % from 2019 to 2020: a change in definition, not "
     "more waste. Before the change, waste grew more slowly than GDP."),
    ("SK", 2020,
     "From 2020 Slovakia uses a new definition of municipal waste that also covers waste from "
     "businesses, which raised waste per person by 14 %. Waste per person was already growing "
     "faster than GDP before the change (+35 % from 2011 to 2019, against +22 % for GDP)."),
    ("LU", 2016,
     "Eurostat marks a break in the series of waste per person in 2016 (change in method). "
     "Before the break, waste per person fell while GDP grew."),
    ("IE", None,
     "Irish GDP is inflated by the accounts of multinational companies (it rose by 23 % in "
     "2015 alone), so the GDP line overstates the growth of the Irish economy, and decoupling "
     "looks stronger than it is."),
]


def main():
    allowed = set(eu27_geos())
    unknown = [geo for geo, _, _ in COUNTRY_NOTES if geo not in allowed]
    if unknown:
        raise ValueError(f"notes for geographies not in the processed data: {unknown}")

    notes = {
        "general_note": GENERAL_NOTE,
        "country_notes": [
            {"geo": geo, "break_year": break_year, "note": note}
            for geo, break_year, note in COUNTRY_NOTES
        ],
    }

    DIR_LOOKUPS.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"saved {len(COUNTRY_NOTES)} country notes to {OUTPUT}")


if __name__ == "__main__":
    main()

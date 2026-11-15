"""
Create the notes shown under the decoupling chart in the dashboard.

The dashboard shows the general note for every geography, the break note when the EU27 is
selected (the EU27 total includes those changes), and a country note when the selected
geography needs care: a change in definition or method that moves its trend, or a caveat on
GDP. Country notes are written only where the cause is documented (Eurostat metadata and its
annex "Country specific notes on municipal waste"). Where a note has a break_year, the dashboard
also marks that year on the chart.

The texts summarise docs/method_notes.md (sections 5 and 6). When the method
notes change, update the texts here and run the pipeline. Do not edit the JSON by hand.

Output columns:
    caption          chart title; the dashboard replaces {name} with the selected geography
    labels           legend and line labels:
        mw_pc_index      the waste line
        gdp_pc_index     the GDP line
        reference        the grey EU27 lines shown behind a selected country (legend)
        reference_mw_pc_index, reference_gdp_pc_index
                         line-end labels of the two grey EU27 lines
        base_year        the dashed line at 100
        break_year       the marker on the break year
    general_note     text shown for every country
    break_note       text shown with the EU27: which countries changed their definition of
                     municipal waste, so their waste line jumps (built from DEFINITION_CHANGES
                     and the break years in COUNTRY_NOTES, so the texts always match)
    country_notes    one record per geography with a note:
        geo          country code (27 Member States or EU27_2020)
        break_year   year of a break in the series of waste per person, or null
        note         text shown when this geography is selected

Input:  data/lookups/geo_eu27.json (country codes and names)
Output: data/lookups/decoupling_notes.json (overwritten on each run)

Run from anywhere:
    .venv/Scripts/python scripts/lookups/create_decoupling_notes.py
"""

import json

from geo import eu27_geos
from paths import DIR_LOOKUPS

INPUT_NAMES = DIR_LOOKUPS / "geo_eu27.json"
OUTPUT = DIR_LOOKUPS / "decoupling_notes.json"

CAPTION = "Municipal waste and real GDP per person, 2011 = 100: {name}"

LABELS = {
    "mw_pc_index": "Waste per person",
    "gdp_pc_index": "GDP per person",
    "reference": "EU27",
    "reference_mw_pc_index": "EU27 waste per person",
    "reference_gdp_pc_index": "EU27 GDP per person",
    "base_year": "2011 = 100",
    "break_year": "Break in series",
}

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
     "rose, likely because people spent more time at home. The EU27 waste figure also includes "
     "the changes in definition of several Member States (see below), so the real rise in "
     "waste is smaller than the line shows."),
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
     "From 2016 Luxembourg defines municipal waste by waste codes, which includes more waste "
     "from sources other than households; before, it counted only the waste under the "
     "responsibility of the public sector. This raised waste per person by 34 % from 2015 to "
     "2016: a change in definition, not more waste. Before the change, waste per person fell "
     "while GDP grew."),
    ("EE", 2014,
     "From 2014 Estonia includes packaging waste in municipal waste (not included until 2013). "
     "Waste per person rose by 22 % from 2013 to 2014, mostly because of this change; Eurostat "
     "also mentions more mixed municipal waste and more separate collection in bigger towns. "
     "Before the change, waste per person fell while GDP grew."),
    ("SI", 2013,
     "From 2013 Slovenia also counts waste from special waste collectors, which was not "
     "included before. Waste per person rose by 14 % from 2012 to 2013, partly because of "
     "this change."),
    ("IE", 2014,
     "Irish GDP is inflated by the accounts of multinational companies (it rose by 23 % in "
     "2015 alone), so the GDP line overstates the growth of the Irish economy, and decoupling "
     "looks stronger than it is. Eurostat marks a break in waste per person in 2014 (improved "
     "method to estimate household waste not collected by waste services); there are no "
     "figures for 2013 and 2015."),
]

# Countries whose waste per person jumped because they widened their definition of municipal
# waste to include waste from businesses (method notes, section 6), with the rise in waste per
# person in the year of the change (%). Their break years are in COUNTRY_NOTES.
# Estonia (2014, packaging waste added) and Slovenia (2013, special waste collectors added)
# are not listed: their changes are not about waste from businesses; see their country notes.
DEFINITION_CHANGES = {"LU": 34, "CZ": 44, "BE": 75, "AT": 42, "SK": 14}


def join_names(names):
    """'A', 'A and B', 'A, B and C'."""
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"


def build_break_note(names):
    """Break note, with the countries grouped by the year of the change."""
    break_years = {geo: year for geo, year, _ in COUNTRY_NOTES}
    missing = [geo for geo in DEFINITION_CHANGES if break_years.get(geo) is None]
    if missing:
        raise ValueError(f"no break_year in COUNTRY_NOTES for: {missing}")

    years = sorted({break_years[geo] for geo in DEFINITION_CHANGES})
    groups = [
        f"{join_names([names[g] for g in DEFINITION_CHANGES if break_years[g] == year])} "
        f"(from {year})"
        for year in years
    ]
    rises = DEFINITION_CHANGES.values()
    return (
        f"Change in definition: {join_names(groups)} started to include municipal waste from "
        f"businesses. Their waste per person rose by {min(rises)} % to {max(rises)} % in the "
        f"year of the change, without more waste being generated, so their figures cannot be "
        f"compared with their earlier years. Select a country to see the year of its change "
        f"on the chart."
    )


def main():
    allowed = set(eu27_geos())
    unknown = [geo for geo, _, _ in COUNTRY_NOTES if geo not in allowed]
    if unknown:
        raise ValueError(f"notes for geographies not in the processed data: {unknown}")

    with open(INPUT_NAMES, encoding="utf-8") as f:
        names = json.load(f)

    notes = {
        "caption": CAPTION,
        "labels": LABELS,
        "general_note": GENERAL_NOTE,
        "break_note": build_break_note(names),
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

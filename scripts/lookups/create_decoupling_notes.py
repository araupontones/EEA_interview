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

CAPTION = "{name}: waste per person and the economy, compared with 2011"

LABELS = {
    "mw_pc_index": "Waste per person",
    "gdp_pc_index": "Economy (GDP per person)",
    "reference": "EU27",
    "reference_mw_pc_index": "EU27 waste",
    "reference_gdp_pc_index": "EU27 economy",
    "base_year": "2011 level (100)",
    "break_year": "Counting changed",
}

GENERAL_NOTE = (
    "Both lines start at 100 in 2011, so you can compare how fast each one grew: 110 means "
    "10% more than in 2011. The economy is GDP per person, adjusted for inflation (2020 prices). "
    "When the blue line is above the orange one, the economy grew faster than waste. This is "
    "called decoupling."
)

# geo, break_year, note (plain wording by the ux-copywriter; figures from docs/findings.md
# §1 bullets 4-6, 10-11 and §2 bullets 4-6)
COUNTRY_NOTES = [
    ("EU27_2020", None,
     "The EU figure includes the countries that changed what they count, so the real rise in "
     "waste is probably smaller than the line shows."),
    ("CZ", 2017,
     "From 2017 Czechia also counts similar waste from businesses. Its waste per person jumped "
     "by 44% in one year: a change in counting, not more waste generated. Before the change, "
     "waste grew more slowly than the economy."),
    ("BE", 2020,
     "From 2020 Belgium also counts similar waste from businesses. Its waste per person jumped "
     "by 75% in one year: a change in counting, not more waste generated. Before the change, "
     "waste per person fell while the economy grew."),
    ("AT", 2020,
     "From 2020 Austria also counts waste from shops and businesses. Its waste per person "
     "jumped by 42% in one year: a change in counting, not more waste generated. Before the "
     "change, waste grew more slowly than the economy."),
    ("SK", 2020,
     "From 2020 Slovakia also counts waste from businesses, which raised its waste per person "
     "by 14% in one year. But its waste was already growing faster than its economy before "
     "that: +35% against +22% from 2011 to 2019."),
    ("LU", 2016,
     "From 2016 Luxembourg counts more waste from sources other than homes. Its waste per "
     "person jumped by 34% in one year: a change in counting, not more waste generated. "
     "Before the change, waste per person fell while the economy stayed about the same."),
    ("EE", 2014,
     "From 2014 Estonia also counts packaging waste. Its waste per person rose by 22% in one "
     "year, when it started counting packaging waste. Before the change, waste per person fell while the "
     "economy grew."),
    ("SI", 2013,
     "From 2013 Slovenia also counts waste from special waste collectors. Its waste per person "
     "rose by 14% in one year, partly because of this change."),
    ("IE", 2014,
     "Ireland's GDP per person jumped by 23.5% in 2015 alone, mostly because multinational "
     "companies moved assets such as intellectual property to Ireland (Irish Central "
     "Statistics Office). So the economy looks bigger than it is, and decoupling looks "
     "stronger than it is; the fall in waste per person is not affected. Ireland also changed how "
     "it estimates household waste in 2014, and there are no waste figures for 2013 and "
     "2015."),
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
        f"Some countries changed what they count: {join_names(groups)} started counting "
        f"waste from businesses, so their waste per person jumped by {min(rises)}% to "
        f"{max(rises)}% in one year without more waste being generated. The EU figure "
        f"includes these jumps. Pick one of these countries to see the year of its change."
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

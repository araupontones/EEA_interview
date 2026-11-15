"""
Create the texts shown with the municipal waste bar chart in the dashboard.

The chart shows municipal waste per person by country for the latest year with data for all
27 Member States. It compares countries in one year, not years, so the breaks in series are
explained under the decoupling chart (create_decoupling_notes.py), not here.

When the texts change, update them here and run the pipeline. Do not edit the JSON by hand.

Output keys:
    caption        chart title; the dashboard replaces {year} with the year shown
    card           labels of the card shown when hovering a bar, one per value shown:
        label        name of the value
        unit         unit shown after the value
    general_note   text shown under the chart

Output: data/lookups/municipal_waste_notes.json (overwritten on each run)

Run from anywhere:
    .venv/Scripts/python scripts/lookups/create_municipal_waste_notes.py
"""

import json

from paths import DIR_LOOKUPS

OUTPUT = DIR_LOOKUPS / "municipal_waste_notes.json"

CAPTION = "Municipal waste generated per person (kg), {year}"

# Hover card: one entry per column of data/processed/municipal_waste.json shown in the card
CARD = {
    "mw_pc": {"label": "Waste per person", "unit": "kg"},
    "mw_tt": {"label": "Waste generated", "unit": "thousand tonnes"},
}

GENERAL_NOTE = (
    "Municipal waste is waste collected from households and similar waste from businesses, "
    "such as shops, offices and public institutions. Differences between countries partly "
    "reflect what each country counts as municipal waste."
)

def main():
    notes = {
        "caption": CAPTION,
        "card": CARD,
        "general_note": GENERAL_NOTE,
    }

    DIR_LOOKUPS.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"saved the municipal waste notes to {OUTPUT}")


if __name__ == "__main__":
    main()

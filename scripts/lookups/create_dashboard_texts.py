"""
Create the texts of the dashboard page: hero, waste hierarchy, section headings,
distance-to-target chart texts, closing panel, methodological note, "How I did this" and
interface labels.

Chart-specific notes of the other charts stay in their own lookups (decoupling_notes.json,
municipal_waste_notes.json, data_sources.json). The wording was proposed by the
ux-copywriter agent and approved by the user (docs/communication.md, 15 November 2026);
facts come only from docs/findings.md. "How I did this" describes the project itself
(sources: README.md, CLAUDE.md).

**Figures are not written here.** Texts that show a figure use placeholders in braces
(e.g. "{eu_kg}"); the dashboard fills them from the processed data files
(dashboard/src/lib/keyFigures.js), so they follow every new download. Placeholders:
    {year}              latest year with waste per person for all 27 Member States
    {eu_kg}             EU27 municipal waste generated per person, kg ({year})
    {download_date}     latest date a Eurostat dataset was downloaded (data_sources.json)
    {eu_mt}             EU27 municipal waste generated, million tonnes ({year}; findings §1 bullet 1)
    {max_country}, {min_country}, {ratio}
                        Member States with the most and least waste per person among those
                        without a change in definition, and the ratio (findings §1 bullet 12)
    {n_above}           number of Member States above the EU27 figure
    {gdp_growth}, {waste_growth}
                        EU27 change since 2011 in real GDP per person and waste per person, %
    {n_absolute}        Member States with absolute decoupling ({year})
    {landfill}, {landfill_2011}
                        EU27 share of municipal waste landfilled, % ({year}, 2011)
    {plastic_met}, {plastic_n}
                        Member States reaching the plastic packaging target, and with data
    ladder values: {recycling}, {energy_recovery}, {landfill}, {incineration}, {unaccounted}
    hover card: {value}, {distance}, {target}

The names and order of the waste-hierarchy steps follow the Waste Framework Directive
(Directive 2008/98/EC, Art. 4).

Input:  none (texts written in this script)
Output: data/lookups/dashboard_texts.json (overwritten on each run)

Run from anywhere:
    .venv/Scripts/python scripts/lookups/create_dashboard_texts.py
"""

import json

from paths import DIR_LOOKUPS

OUTPUT = DIR_LOOKUPS / "dashboard_texts.json"

HERO = {
    "eyebrow": "Waste in the EU, from best to worst",
    "title": "Where does our waste go?",
    # lede as parts in reading order: text, and figures set in bold (lib/keyFigures.js fills them)
    "lede": [
        {"text": "On average, each of us in the EU generates "},
        {"figure": "{eu_kg} kg"},
        {"text": " of municipal waste a year. Follow it down the waste hierarchy, from best to worst "
                 "for the environment, and find your country. And "},
        {"figure": "{landfill} %"},
        {"text": " of the EU's municipal waste still goes to landfill, down from {landfill_2011} % "
                 "in 2011."},
    ],
    # byline under the lede: author (link to LinkedIn) · publication date (fixed, change it when
    # republishing), and below it the date of the latest Eurostat download (from the data)
    "byline": {
        "author": "Andrés Arau",
        "url": "https://www.linkedin.com/in/andr%C3%A9s-arau-017b1127/",
        "date": "15 November 2026",
        "data_note": "Data downloaded from Eurostat on {download_date}",
    },
    "cta": "Follow your waste",
}

# Waste hierarchy (Waste Framework Directive, Art. 4), best to worst.
# section: id of the section that covers the step, or None (shown greyed).
# value: EU27 figure shown in the step ({year}), or None; explanation: one plain line.
HIERARCHY_STEPS = [
    ("prevention", "Prevention", "decoupling",
     "Don't generate the waste in the first place.",
     None),
    ("preparing_for_reuse", "Preparing for re-use", None,
     "Check, clean or repair things so they can be used again.",
     None),  # no EU figure: 8 Member States do not report it (findings §4)
    ("recycling", "Recycling", "distance-to-target",
     "Turn waste into new materials, or into compost.",
     "{recycling} %"),
    ("other_recovery", "Other recovery", None,
     "Burn waste to make energy.",
     "{energy_recovery} %"),
    ("disposal", "Disposal", None,
     "Bury it in landfill, or burn it without using the energy.",
     "{landfill} % landfill"),
]

HIERARCHY = {
    "title": "The waste hierarchy: where the EU's municipal waste goes ({year})",
    "intro": "The waste hierarchy is how the EU ranks what to do with waste, from best to worst "
             "for the environment.",
    "burnt": "Also disposal: {incineration} % burnt without energy recovery",
    "not_accounted": "Not in the figures: {unaccounted} %",
    "not_accounted_note": (
        "Counted when it was generated, but in no treatment figure. Eurostat lists possible "
        "reasons, such as estimates, storage, trade or waste counted twice; the data does not "
        "say which."
    ),
}

# section id -> texts (ids are the anchors used in the dashboard sections)
SECTIONS = {
    # introduction to the waste hierarchy: the pyramid with the EU figures, and an explanation
    # next to each level (dashboard/src/sections/waste_hierarchy/WasteHierarchySection.jsx)
    "waste-hierarchy": {
        "step": None,
        "eyebrow": None,
        "title": "The waste hierarchy",
        "key_message": None,
        "lede": "The waste hierarchy is how the EU ranks what to do with waste, from best to worst "
                "for the environment. Here is where the EU's municipal waste went in {year}.",
        "try": None,
        # link under a level that has its own section: "→ " + that section's title
        "see_also": "See: {title}",
    },
    "municipal-waste": {
        "eyebrow": None,
        "title": "How much waste do we generate?",
        "key_message": "In {year}, the EU generated about {eu_mt} million tonnes of municipal "
                       "waste, about {eu_kg} kg per person.",
        "lede": "Municipal waste is the waste from our homes, plus similar waste from shops and "
                "offices.",
        "try": "Find your country: is its bar longer or shorter than the EU27 bar? "
               "{n_above} countries are above it.",
        "step": None,
    },
    "decoupling": {
        "eyebrow": "Prevention, over time",
        "title": "Can the economy grow without more waste?",
        "key_message": "Mostly yes: since 2011 the EU's economy grew by {gdp_growth} % per "
                       "person, but waste per person by only {waste_growth} %.",
        "lede": "When the blue line (the economy) is above the orange line (waste), the economy "
                "has grown more than waste since 2011. In {n_absolute} countries, waste per person even "
                "fell while the economy grew.",
        "try": "Search for the Netherlands: its economy grew, and its waste per person fell "
               "more than in any other country.",
        "step": "prevention",
    },
    "distance-to-target": {
        "eyebrow": "Recycling",
        "title": "Are we recycling enough?",
        "key_message": "The EU already beats its 2025 target for packaging, but is still short "
                       "for municipal waste and plastic.",
        "lede": "Each dot is a country in {target_year}, two years before the deadline. Blue dots have "
                "reached the 2025 target; red and orange dots are still below it.",
        "try": "Find your country: has your country met the 2025 target for each type of waste?",
        "step": "recycling",
    },
    "method-note": {
        "eyebrow": "About the data",
        "title": "Methodological note",
        "key_message": None,
        "lede": None,
        "try": None,
        "step": None,
    },
    "how-i-did-this": {
        "eyebrow": "About the data",
        "title": "How I did this",
        "key_message": None,
        "lede": None,
        "try": None,
        "step": None,
    },
}

# texts of the distance-to-target chart
DISTANCE_TO_TARGET = {
    "caption": "Recycling rates in {target_year}, compared with the 2025 targets",
    "aria_label": "Recycling rates in {target_year} by country and type of waste, compared with the "
                  "2025 targets",
    "legend": {
        "below": "Below the 2025 target",
        "met": "Target reached",
        "axis": "Points below or above the target",
        "target": "2025 target",
        "eu": "EU27",
    },
    "hover": {
        "rate": "{value} % recycled",
        "above": "{distance} points above the 2025 target of {target} %",
        "below": "{distance} points below the 2025 target of {target} %",
        "on": "Right on the 2025 target of {target} %",
    },
    "notes": [
        "Below the target in 2023 doesn't mean failing. Countries still had two years to go, "
        "and 8 countries postponed the municipal waste deadline (they must reach at least 50 % "
        "by 2025). 7 postponed some packaging materials; which ones is not known yet.",
        "Poland changed how it measures in 2023: its treatment figures are now reported "
        "directly by companies instead of being partly estimated. Its recycling rate fell from "
        "40.9 % to 27.6 % while its waste stayed the same, so 2023 cannot be compared with "
        "earlier years.",
        "The municipal waste rate includes composting and, for some countries, preparing "
        "things for re-use.",
        "Some packaging rates are above 100 % (Slovenia, Poland), which makes them look further "
        "above the target than they are. Cyprus's steel rate (221.5 %) is left out. Bulgaria, "
        "Czechia and Hungary have no packaging rates for 2023.",
    ],
}

CLOSING = {
    "eyebrow": "Back to the waste hierarchy",
    "title": "Recycling is only halfway up the waste hierarchy",
    "text": "The EU recycles almost half of its municipal waste. It beats its packaging target "
            "but is still short for municipal waste and plastic. And the top of the waste hierarchy is generating less waste in the first place, and there the EU "
            "has hardly moved: about {eu_kg} kg per person, much as in 2011.",
    "cta": "Back to the top",
}

# methodological note: (bold lead, text), plain language, facts from docs/findings.md
METHOD_NOTE = [
    ("Where the numbers come from.",
     "All figures come from Eurostat, the EU's statistics office: municipal waste (env_wasmun), "
     "packaging recycling (env_waspacr) and GDP per person (nama_10_pc). Each chart names its "
     "sources and the date we downloaded them. Figures in the texts are for 2023, the latest "
     "year with data for all 27 countries; the line charts go up to 2024."),
    ("Countries count waste differently.",
     "Czechia, Belgium, Austria, Slovakia and Luxembourg widened their definition to include "
     "similar waste from businesses: their waste per person jumped in one year without more "
     "waste being generated. Estonia and Slovenia added other waste, which partly explains "
     "their jumps. The EU figure includes these jumps."),
    ("Some jumps have no known cause.",
     "Romania (2011), Finland (2022) and Latvia (2015) show large jumps that are not explained; "
     "they should be checked with the countries."),
    ("Recycling, two ways.",
     "The recycling rate (47.9 % for the EU) also counts some preparing for re-use, as the "
     "target does. The waste hierarchy at the top of the page shows recycling on its own (47.7 %), with re-use as its own "
     "level, so nothing is counted twice."),
    ("The waste hierarchy figures don't always add up to 100 %.",
     "Each level is a share of the waste generated, like the recycling targets. Some waste "
     "generated shows up in no treatment figure: 5.0 % for the EU, and more than a tenth in "
     "7 countries. We show it as 'not in the figures' rather than guess where it went. The "
     "EU's 2023 landfill figure is our own estimate, because Latvia has none."),
    ("Targets.",
     "The 2025 recycling targets are set by EU law: 55 % for municipal waste (Waste Framework "
     "Directive) and 65 % for all packaging, with separate targets per material (Packaging and "
     "Packaging Waste Regulation). 2023 is a snapshot two years before the deadline, and some "
     "countries legally postponed it."),
    ("The economy.",
     "GDP per person is adjusted for inflation (2020 prices). Ireland's GDP is pushed up by multinational "
     "companies, so its decoupling looks stronger than it is."),
]

# How I did this: the project itself (sources: README.md, CLAUDE.md), no findings
HOW_I_DID_THIS = [
    ("Data straight from the source.",
     "The data is downloaded from Eurostat's online data service (its API), so every figure "
     "can be traced back to the dataset it comes from, and each chart says when it was "
     "downloaded."),
    ("An analysis pipeline in Python.",
     "A chain of Python scripts takes the data through four layers: raw downloads (never "
     "edited), lookup tables (the EU countries, the recycling targets, the texts of this "
     "page), indicators built from each dataset, and the final tables this page reads. One "
     "command rebuilds everything in the right order and checks that only the 27 EU countries "
     "and the EU total reach the dashboard. Where a source value needed fixing, the fix is "
     "written down with its reason, and it stops applying if Eurostat corrects the value."),
    ("A page built with D3 and React.",
     "D3 does the maths (scales, lines, axes) and React draws the charts. The page is rebuilt "
     "and published on GitHub Pages every time the data or the code changes."),
    ("Built with Claude and a team of AI agents.",
     "The project was built with Claude Code, working with specialised agents: a data "
     "scientist that owns the pipeline and turns questions into checked findings; a data "
     "storyteller that shapes the story; a UX copywriter that writes the texts; a brand "
     "designer that proposed the visual identity; and a fact-checker that checks every text "
     "against the findings, and the findings against the data. Every text on this page may only use facts from the project's written "
     "findings, and every decision is logged in the project notes."),
]

# links at the end of "How I did this"
HOW_I_DID_THIS_LINKS = [
    {"text": "See the code and the project notes",
     "url": "https://github.com/araupontones/EEA_interview"},
    {"text": "Connect with me on LinkedIn",
     "url": "https://www.linkedin.com/in/andr%C3%A9s-arau-017b1127/"},
]

UI = {
    "about_chart": "About this chart",
    "search_placeholder": "Find your country",
    "search_aria": "Find a country in this chart",
}


def main():
    step_keys = {key for key, *_ in HIERARCHY_STEPS}
    bad = {sid: s["step"] for sid, s in SECTIONS.items() if s["step"] not in step_keys | {None}}
    if bad:
        raise ValueError(f"sections pointing to unknown hierarchy steps: {bad}")
    bad = [key for key, _, section, *_ in HIERARCHY_STEPS if section and section not in SECTIONS]
    if bad:
        raise ValueError(f"hierarchy steps pointing to unknown sections: {bad}")

    texts = {
        "hero": HERO,
        "hierarchy": {
            **HIERARCHY,
            "steps": [
                {"key": key, "name": name, "section": section, "explanation": explanation,
                 "value": value}
                for key, name, section, explanation, value in HIERARCHY_STEPS
            ],
        },
        "sections": SECTIONS,
        "distance_to_target": DISTANCE_TO_TARGET,
        "closing": CLOSING,
        "method_note": [{"lead": lead, "text": text} for lead, text in METHOD_NOTE],
        "how_i_did_this": [{"lead": lead, "text": text} for lead, text in HOW_I_DID_THIS],
        "how_i_did_this_links": HOW_I_DID_THIS_LINKS,
        "ui": UI,
    }

    DIR_LOOKUPS.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(texts, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"saved the dashboard texts to {OUTPUT}")


if __name__ == "__main__":
    main()

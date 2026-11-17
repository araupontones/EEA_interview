"""
Create the texts of the dashboard page: hero, waste hierarchy, section headings,
distance-to-target and waste-treatment chart texts, closing panel, methodological note, "How I did this" and
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
    {recycling_rate}    EU27 municipal recycling rate as in the targets chart, % (findings §3, §4)
    {recycling_kg}, {energy_kg}, {disposal_kg}
                        EU27 kg per person recycled, burnt for energy, disposed of ({year};
                        findings §4 bullet 2)
    {disposal}          EU27 share of municipal waste disposed of (landfill and incineration
                        without energy recovery), % ({year}; findings §4 bullet 1)
    sankey (filled in the chart): {name}, {kg}, {share}, {label}
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
    "eyebrow": "Waste in the EU, country by country",
    "title": "Where does our waste go?",
    # lede as parts in reading order: text, and figures set in bold (lib/keyFigures.js fills them)
    "lede": [
        {"text": "In {year}, each of us in the EU generated on average "},
        {"figure": "{eu_kg} kg"},
        {"text": " of municipal waste. "},
        {"figure": "{landfill}%"},
        {"text": " of it went to landfill, down from {landfill_2011}% in 2011. Follow it down the "
                 "waste hierarchy, from best to worst for the environment, and find your country."},
    ],
    # byline under the lede: author (link to LinkedIn) · publication date (fixed, change it when
    # republishing), and below it the date of the latest Eurostat download (from the data)
    "byline": {
        "author": "Andrés Arau",
        "url": "https://www.linkedin.com/in/andr%C3%A9s-arau-017b1127/",
        "date": "15 November 2026",
        "data_note": "Data downloaded from Eurostat on {download_date}",
        # reviewer feedback, 16 November 2026: say plainly what the page is not
        "disclaimer": "An independent learning exercise built from Eurostat data. Not an EEA "
                      "or European Commission product.",
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
     "{recycling}%"),
    ("other_recovery", "Other recovery", "waste-treatment",
     "Burn waste and use the energy.",
     "{energy_recovery}%"),
    ("disposal", "Disposal", "waste-treatment",
     "Bury it in landfill, or burn it without using the energy.",
     "{landfill}% landfill"),
]

HIERARCHY = {
    "title": "The waste hierarchy: where the EU's municipal waste goes ({year})",
    "burnt": "Also disposal: {incineration}% burnt without energy recovery",
    "not_accounted": "Not in the figures: {unaccounted}%",
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
        "key_message": "Mostly yes: since 2011 the EU's economy grew by {gdp_growth}% per "
                       "person, but waste per person by only {waste_growth}%.",
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
        # reviewer feedback, 16 November 2026: no compliance wording ("reached", "beats");
        # targets bind Member States, not the EU; Eurostat rates are not compliance figures
        "key_message": "The EU-wide packaging rate is already above the 2025 target level, but "
                       "the rates for municipal waste and plastic are still below it.",
        "lede": "Each dot is a country's Eurostat recycling rate in {target_year}, two years before "
                "the deadline. Blue dots are at or above the 2025 target level; red and orange dots "
                "are below it.",
        "try": "Find your country: is it at or above the 2025 target level for each type of "
               "waste?",
        "step": "recycling",
    },
    # sankey of where the waste generated per person goes (sections/waste_treatment/)
    "waste-treatment": {
        "eyebrow": "Other recovery and disposal",
        "title": "Where do our {eu_kg} kg of waste end up?",
        "key_message": "Of the {eu_kg} kg each of us generated in {year}, about {recycling_kg} kg "
                       "({recycling}%) were recycled, {energy_kg} kg ({energy_recovery}%) burnt for "
                       "energy and {disposal_kg} kg ({disposal}%) disposed of.",
        "lede": "Follow a year of municipal waste, per person, down the waste hierarchy. The "
                "wider the band, the more kilos go that way.",
        "try": "Try Austria, which recycles the most per person, Malta, which landfills the "
               "most per person, and Denmark, which burns the most per person for energy.",
        # levels filled in the section icon (a list: the section covers several levels)
        "step": ["other_recovery", "disposal"],
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
        "met": "Target reached",  # kept short (user, 16 November 2026); the lede gives the caveat
        "axis": "Points below or above the target",
        "target": "2025 target",
        "eu": "EU27",
    },
    "hover": {
        "rate": "{value}% recycled",
        "above": "{distance} points above the 2025 target of {target}%",
        "below": "{distance} points below the 2025 target of {target}%",
        "on": "Right on the 2025 target of {target}%",
    },
    "notes": [
        "Below the target in 2023 doesn't mean failing. Countries still had two years to go, "
        "and 8 countries postponed the municipal waste deadline (they must reach at least 50% "
        "by 2025). 8 countries postponed some packaging materials: Czechia (aluminium), "
        "Greece, Croatia and Hungary (plastic and glass), Luxembourg (plastic), Portugal "
        "(aluminium and glass), Sweden (glass) and Malta.",
        "Poland changed how it measures in 2023: its treatment figures are now reported "
        "directly by companies instead of being partly estimated. Its recycling rate fell from "
        "40.9% to 27.6% while its waste stayed the same, so 2023 cannot be compared with "
        "earlier years.",
        "The municipal waste rate includes composting and, for some countries, preparing "
        "things for re-use.",
        "Some packaging rates are above 100% (Slovenia, Poland), which makes them look further "
        "above the target than they are. Cyprus's steel rate (221.5%) is left out. Bulgaria, "
        "Czechia and Hungary have no packaging rates for 2023.",
    ],
}

# texts of the waste-treatment sankey (sections/waste_treatment/WasteTreatmentSankey.jsx).
# Node and band keys match the columns of municipal_waste_treatment.json (*_kg_pc).
WASTE_TREATMENT = {
    "caption": "{name}: where each person's municipal waste went in {year}, in kg",
    "aria_label": "Sankey chart: municipal waste generated per person in {name} in {year}, split "
                  "by level of the waste hierarchy",
    "source": "Waste generated",
    "levels": {
        "prep_reuse": "Preparing for re-use",
        "recycling": "Recycling",
        "energy_recovery": "Other recovery",
        "disposal": "Disposal",
        "unaccounted": "Not in the figures",
    },
    "bands": {
        "recycling_material": "Material recycling",
        "recycling_compost": "Composting and digestion",
        "energy_recovery": "Burnt for energy",
        "landfill": "Landfill",
        "incineration": "Burnt without using the energy",
    },
    "value": "{kg} kg",
    # one-line definition of each level, under its label on wide screens (copywriter, 16 Nov 2026)
    "level_notes": {
        "prep_reuse": "Checked or repaired to be used again",
        "recycling": "Made into new materials, or compost",
        "energy_recovery": "Burnt, and the energy is used",
        "disposal": "Got rid of: the last option",
        "unaccounted": "Counted, but in no treatment figure",
    },
    # explanation of each level in the hover card (on small screens, the only place it shows)
    "level_hover": {
        "prep_reuse": "Things checked, cleaned or repaired so they can be used again. Second "
                      "best, after not making the waste at all.",
        "recycling": "Waste made into new materials, or into compost. Next best after preparing "
                     "for re-use.",
        "energy_recovery": "Burnt in plants that use the energy. Below recycling: the waste is "
                           "burnt, not made into something new. Above disposal, where it is "
                           "buried or burnt without using the energy.",
        "disposal": "Mostly buried in landfill, or burnt without using the energy. The last "
                    "option in the waste hierarchy.",
        "unaccounted": "Counted when it was generated, but in no treatment figure. The data "
                       "does not show what happened to it.",
        # added for the EU27 (findings §4 bullets 2-3)
        "unaccounted_eu": "It includes the small amount prepared for re-use.",
    },
    # recycling, other recovery and disposal: kg and share of the waste generated
    "value_share": "{kg} kg ({share}%)",
    "missing": "Not reported",  # a country without a figure (null in the data)
    "no_eu_figure": "No EU figure",  # preparing for re-use, EU27
    "hover": {
        "kg": "{kg} kg per person a year",
        "share": "{share}% of the waste generated",
    },
    # notes under the chart, each shown only when it applies
    "notes": {
        "reuse_missing_eu": "There is no EU figure for preparing for re-use: Eurostat publishes "
                            "none, and 8 countries do not report it. The little that is prepared "
                            "for re-use is inside 'not in the figures'.",
        "reuse_missing_country": "{name} does not report preparing for re-use, so that level is "
                                 "empty.",
        "not_accounted": "Not in the figures: waste counted when it was generated, but in no "
                         "treatment figure. The data does not say where it went.",
        "two_recycling": "Recycling here ({recycling}% for the EU) leaves out preparing for "
                         "re-use. Some countries count re-use in the recycling rate in the section "
                         "above ({recycling_rate}%), which is why the two differ.",
    },
    # country notes (geo -> text), shown when the country is selected
    "country_notes": {
        "PT": "Portugal treated more waste than it generated in {year}, so it has no 'not in the "
              "figures' band. The data does not say why.",
        "PL": "Poland changed how it measures in 2023: companies now report treatment directly, "
              "instead of it being partly estimated. That is why 21.5% of its waste is not in "
              "the figures. Its 2023 figures cannot be compared with earlier years.",
        "LV": "Latvia has no disposal figure for 2023, so its chart has no disposal and no "
              "'not in the figures' band, and is incomplete.",
    },
    "about": "Each band is a share of all municipal waste generated in {name} in {year}, turned "
             "into kg per person: the country's waste divided by its people. These are yearly "
             "averages, not what one household throws away. They include similar waste from "
             "businesses where a country counts it. Eurostat has no EU figure for landfill and "
             "burning without energy recovery in 2023, and Latvia has none either. I estimated "
             "both by adding up all 27 countries, using Latvia's 2022 figures.",
    "table": {
        "show": "Show as a table",
        "headers": ["Level of the waste hierarchy", "Where it goes", "Kg per person a year",
                    "% of the waste generated"],
    },
}

CLOSING = {
    "eyebrow": "Back to the waste hierarchy",
    "title": "Recycling is only halfway up the waste hierarchy",
    "text": "The EU recycles almost half of its municipal waste. Its EU-wide packaging rate is "
            "above the 2025 target level, but the rates for municipal waste and plastic are still "
            "below it. And the top of the waste hierarchy is generating less waste in the first place, and there the EU "
            "has hardly moved: about {eu_kg} kg per person, much as in 2011.",
    "cta": "Back to the top",
}

# methodological note: (bold lead, text), plain language, facts from docs/findings.md
METHOD_NOTE = [
    ("Where the numbers come from.",
     "All figures come from Eurostat, the EU's statistics office: municipal waste (env_wasmun), "
     "packaging recycling (env_waspacr) and GDP per person (nama_10_pc). Each chart names its "
     "sources and the date I downloaded them. Figures in the texts are for 2023, the latest "
     "year with data for all 27 countries; the line chart goes up to 2024."),
    ("Countries count waste differently.",
     "Czechia, Belgium, Austria, Slovakia and Luxembourg widened their definition to include "
     "similar waste from businesses: their waste per person jumped in one year without more "
     "waste being generated. Estonia and Slovenia added other waste, which partly explains "
     "their jumps. The EU figure includes these jumps."),
    ("Some jumps have no known cause.",
     "Waste per person fell sharply in Romania (2011) and Finland (2022 and 2023), and rose "
     "sharply in Latvia (2015). These changes are not explained; they should be checked with "
     "the countries."),
    ("Recycling, two ways.",
     "The recycling rate (47.9% for the EU) also counts some preparing for re-use, as the "
     "target does. The waste hierarchy, and the chart of where each person's waste ends "
     "up, show recycling on its own (47.7%), with "
     "re-use as its own level, so nothing is counted twice."),
    ("The waste hierarchy figures don't always add up to 100%.",
     "Each level is a share of the waste generated, like the recycling targets. Some waste "
     "generated shows up in no treatment figure: 5.0% for the EU, and more than a tenth in "
     "7 countries. I show it as 'not in the figures' rather than guess where it went. The "
     "EU's 2023 landfill and burnt-without-energy figures are my own estimate, as Latvia "
     "has no figure for them."),
    ("Targets.",
     "The 2025 recycling targets are set by EU law: 55% for municipal waste (Waste Framework "
     "Directive) and 65% for all packaging, with separate targets per material (Packaging and "
     "Packaging Waste Directive, now carried over by the new Packaging Regulation). 2023 is a snapshot two years before the deadline, and some "
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
     "url": "https://github.com/araupontones/waste_management"},
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
    # a section's step is one level, a list of levels, or None
    as_list = lambda step: step if isinstance(step, list) else [step]
    bad = {sid: s["step"] for sid, s in SECTIONS.items()
           if any(k not in step_keys | {None} for k in as_list(s["step"]))}
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
        "waste_treatment": WASTE_TREATMENT,
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

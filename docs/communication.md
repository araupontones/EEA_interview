# Communication

How the dashboard communicates, as it stands now: who it is for, the story it tells, the key message of each section, the voice, the words it uses and how it looks. This is the brief for the data-storyteller, ux-copywriter and brand-designer agents (`.claude/agents/`).

How this file relates to the others:
- **Facts** are only in [findings.md](findings.md). This file never restates a figure: a key message points to the finding it comes from (e.g. "findings §1, bullet 2"), so a figure changes in one place only.
- **Final texts** shown in the dashboard live in the lookups (`data/lookups/*.json`, built by `scripts/lookups/create_*.py`). This file holds the messages and rules the texts follow, not a copy of every label.
- **When and why** each communication decision was taken is logged in [decisions.md](decisions.md), with a link to the section of this file it changed.

Agents propose changes to this file; the main session applies them after the user approves.

Last updated: 15 November 2026.

## 1. Audience and goal

- The general public in Europe, with no background in waste or environmental policy. They read little: they scan headlines, look at charts and leave.
- Most do not know the waste hierarchy of the Waste Framework Directive: **prevention, preparing for re-use, recycling, other recovery, disposal**.
- Goal: in a few minutes, and mostly through the charts and key messages, visitors learn why waste management and the circular economy matter, and where their own country stands. The dashboard is a tool to explore and play with, not an institutional report.
- Language: English only.

## 2. Storyline

The dashboard follows the waste hierarchy from top to bottom: the reader learns the hierarchy first, then sees the levels the data covers, in the hierarchy's order. Approved on 15 November 2026.

1. **Hero and "The waste hierarchy".** The hero asks the question and gives the EU kg per person and the landfill share. The first section shows the waste hierarchy as an inverted pyramid of its five levels (prevention, preparing for re-use, recycling, other recovery, disposal), with the EU27 figure where there is one (findings §4) and each level's explanation beside it; levels with a section link to it, the others are greyed. Prevention shows no figure; preparing for re-use is greyed with no figure (no EU total: 8 Member States do not report it). The share burnt without energy recovery and the share "not in the figures" (with its explanation) are under the pyramid. The pyramid comes back in the closing panel.
2. **How much waste do we generate?** Waste per person by country: an introduction, not linked to a level of the waste hierarchy (levels between countries are not a ranking of prevention, findings §1 bullet 14).
3. **Can the economy grow without more waste? (prevention over time).** Decoupling; the Prevention level of the hero's waste hierarchy links here.
4. **Are we recycling enough? (recycling).** Recycling rates against the 2025 targets.
5. **Back to the waste hierarchy.** A short closing panel: recycling is only halfway up the waste hierarchy, prevention comes first. No new facts.
6. **Methodological note** and **How I did this**, at the end.

- **Section titles are questions** (e.g. "How much do we throw away?"), worded by the ux-copywriter.
- **Treatment data across the waste hierarchy** comes from findings §4 (data-scientist): each level of the pyramid shows its EU27 figure where there is one.
- Every chart invites the reader to find their own country and compare it with the EU27.
- **Distance to target shows all 8 rows** at once (a trial with two rows and a "show all" button was rejected).
- **Postponed deadlines are not marked in the chart.** Texts about the chart must not call the countries below the target "failing": where relevant, say that some postponed the deadline (findings §3; method notes §4).
- **Each chart has its own country search**; there is no single search for the whole page.

## 3. Key messages per section

Approved on 15 November 2026 (ux-copywriter's wording; figures are filled from the data, see section 4). Final texts are in `data/lookups/dashboard_texts.json` and the chart lookups.

| Section | Key message | From findings | Caveat to keep | What to notice or try |
|---|---|---|---|---|
| Hero | On average, each of us in the EU generates {eu_kg} kg of municipal waste a year; follow it down the waste hierarchy | §1 bullet 1; §4 bullets 1–2 and 7 | "Not in the figures" shown on its own; re-use greyed, no figure | The levels of the waste hierarchy, then find your country |
| How much waste do we generate? | In {year}, the EU generated about {eu_mt} million tonnes of municipal waste, about {eu_kg} kg per person. The key message answers the title's question; no comparison between countries (it would need an explanation of the countries left out) | §1 bullets 1, 2 and 12 | Countries count differently, also in the same year (§1 bullets 4–5 and 13) | Is your country above or below the EU27 bar? |
| Can the economy grow without more waste? | Mostly yes: the EU economy grew much faster than its waste; in {n_absolute} countries waste fell while the economy grew | §2 bullets 1–2 | Counting changes (§1 bullets 4–6, 10–11; §2 bullet 6); Irish GDP (§2 bullet 5) | Search for the Netherlands; a country against the grey EU27 lines |
| Are we recycling enough? | Ahead on packaging, still short on municipal waste and plastic | §3 municipal bullet 1, packaging bullets 1–2 | Not "failing": two years left, postponements (§3; §5); Poland's change in method (§4) | Your country across 8 rows; the plastic row |
| Back to the waste hierarchy | Recycling is only halfway up the waste hierarchy; generating less waste comes first, and there little has changed | §1 bullet 1; §4 bullet 1 | None (no new facts) | Back to the top |

## 4. Voice, tone and wording

- **Voice and tone**: a curious, friendly guide. Talk to "you" and about "we/our waste". Direct, warm, a little playful; never preachy, never guilt-tripping. Never call a country "failing", "bad" or "lagging": say "below the 2025 target", "postponed its deadline". When the findings give no cause, say "the data does not say why".
- **"Level", not "step"**: the levels of the waste hierarchy are a ranking of options, not steps in a sequence; no step numbers in section labels.
- **Writing rules**: headlines up to ~10 words; section titles are questions; key messages one sentence; ledes two lines at most; notes 1–2 sentences. Reading age about 12; no acronyms except EU, EU27, GDP. UK number style (7,142; 47.9 %). Distances to targets are "points above/below the target", never "pp".
- **"Waste hierarchy", not "waste ladder"**: use the Waste Framework Directive's own name, explained as "from best to worst for the environment".
- **"Generate", not "make"**: the texts use "generate" (waste generated), for consistency with the Commission's early warning reports.
- **Figures come from the data, not from the text**: wherever a text shows a figure that comes from the data (hero, waste hierarchy, section headers, closing panel), the lookup holds a placeholder (e.g. `{eu_kg}`) that the dashboard fills from the processed files (`dashboard/src/lib/keyFigures.js`), so the figures follow every new download. Each one must still be a finding.
- **"How I did this"** describes the project (Eurostat API, Python pipeline, D3 and React, Claude Code and the agents), not waste facts; it is checked against the README, not the findings.
- **Glossary**:

| Term | Plain-language explanation |
|---|---|
| Municipal waste | The waste from our homes, plus similar waste from shops, offices and public buildings. |
| Waste hierarchy | How EU law ranks what to do with waste, from best to worst for the environment: prevent it, prepare it for re-use, recycle it, recover energy from it, and only then dispose of it. |
| Prevention | Not generating the waste in the first place. |
| Preparing for re-use | Checking, cleaning or repairing things so they can be used again. |
| Recycling | Turning waste into new materials, including composting food and garden waste. |
| Other recovery | Burning waste to make energy. |
| Disposal | Landfill, or burning waste without using the energy. |
| Not in the figures | Waste counted when it was generated but in no treatment figure; the data does not say where it went. |
| Recycling rate | The share of waste generated that is recycled, in %. |
| 2025 target | The recycling rate EU law asks each country to reach by 2025. |
| Points (above/below the target) | The gap between a rate and its target: 50 % against a 55 % target is 5 points below. |
| Postponed deadline | Some countries were legally allowed to reach a target later than 2025. |
| Decoupling | When the economy grows faster than waste. |
| GDP per person | The size of a country's economy divided by its people, without inflation. |
| EU27 | The 27 EU countries together. |

## 5. Visual identity

"Le Journal" (15 November 2026; replaces "Loop", which reviewers found too close to Claude's default style): a white newspaper page with black rules, condensed sans headlines over a reading serif, one colour family per meaning, and charts labelled directly instead of boxed with legends. No institutional brand, no tinted panels, no shadows, no chips. Built on the `rebrand` branch for review.

- **Palette** (WCAG AA on white: text 4.5:1, graphics 3:1; CSS tokens on `:root` in `dashboard/src/index.css`, the same hex values in the chart constants):
  - Page: white `#ffffff`; ink `#1a1a1a` (text, rules, baselines, buttons); muted ink `#5c5c5c` (secondary text, axes, notes, sources); grid `#e5e5e5`; hairlines `#d9d9d9`; input border `#767676`.
  - Waste (orange, everywhere): light `#fa9f5c` for bar fills, always with a 2 px `#b2511a` end cap at the value end (the light fill alone is 2.1:1); `#e36f25` for lines and small marks (3.2:1); `#b2511a` for waste text (5.1:1).
  - Economy (GDP): steel blue `#2563a8` (6.1:1).
  - EU27: neutral slate `#4f6d8a` for the bar and its label (5.4:1), instead of a very dark tone, which read as negative; EU27 reference lines behind a country: grey `#8a8a8a`.
  - Distance to target: d3 RdYlBu, unchanged (red–orange below target, blue target met).
  - No highlight colour: hover, selection and focus use ink (a level filled in ink with white text, a 2 px ink focus outline). The pale mint is gone.
- **Typography (Google Fonts)**: Barlow Semi Condensed (400–700) for headlines, key messages, section labels, interface, hover cards and all chart text; Literata (400, optical sizes) for ledes, the hero sentence, notes and the method text; bold run-in leads inside serif text are in Barlow. Section labels in capitals. Sizes, line heights and spacing are tokens in `index.css`. Arrows (↓ ↑) use a system font, as Barlow has none.
- **Shapes**: square corners everywhere (pyramid, bars, hover cards, search boxes), except buttons, which are rounded. Sections are separated by rules: a heavy rule at the top of the page and of the closing panel, a thin ink rule above each section, hairlines inside. Flags in circular crops (flag-icons).
- **Waste-hierarchy motif**: a flat inverted pyramid of stacked trapezoids, best option at the top. Levels covered by a section are white with an ink outline and an arrow, and fill with ink (white text) on hover; levels without a section are light grey `#f2f2f2` with muted text. The EU figures in the levels come from the data (findings §4). A 40 px version sits next to each section label, with the section's level filled in ink.
- **Layout**: hero in one column (label, headline, lede with the EU kg per person and the landfill share in bold Barlow, findings §1 bullet 1 and §4, and a button). Then a first section, "The waste hierarchy": the pyramid with the EU figures on the left and, beside each level, its explanation and a link to its section if it has one (on mobile the levels are listed under the pyramid); under it, the share burnt without energy recovery and the share "not in the figures" with its explanation. Each section: rule, icon and label, question title, key message, lede, "try this" hint marked by a short ink rule, then the chart at full width with no box, the country note, "About this chart" and the source lines. Closing panel between rules, with the pyramid. Method note and "How I did this" in two columns on desktop (heading left, serif text right). A slot for a wordmark is foreseen above the hero once a name is chosen.
- **Charts**: direct labels instead of legends where possible (line ends and the 2011 = 100 line in the decoupling chart; the legend only on small screens); bars with square ends; decoupling lines 3 px; hover cards square with an ink border and 28 px flags; square search boxes. The recycling targets chart keeps its design (colours, marks, layout, label sizes and colours) and changes only its font; its search box, caption and hover card follow the page.
- **Small screens**: one column; the beeswarm puts row labels above the rows, the decoupling chart drops line-end labels and shows its legend, the bar chart narrows its label column.
- **Motion**: only a short fade when the selected country changes and colour transitions on hover; none with `prefers-reduced-motion`.

## 6. Needs a finding

Figures or facts the communication would need that are not in `findings.md` yet. Each is calculated (or checked by the fact-checker) and added to `findings.md` before any text uses it.

| Requested by | What is needed | Status |
|---|---|---|
| data-storyteller | **Treatment of municipal waste across the hierarchy.** Question: what happens to the EU's municipal waste? Figure: shares of municipal waste generated that are prepared for re-use, recycled (material), composted and digested, incinerated with energy recovery, incinerated without, and landfilled, in % (each / generated). Scope: EU27 and each Member State, 2023, and the EU27 trend since 2011. Likely source: `env_wasmun` (`wst_oper` codes such as `PRP_REU`, `RCY_M`, `RCY_C_D`, `RCV_E`, `DSP_I`, `DSP_L_OTH`). Used for: the greyed levels of the waste hierarchy in the hero. Caveats: RCY sometimes includes PRP_REU (method notes §2); breaks in series; treatment can differ from generation (temporary storage). | Done: findings §4 (treatment) |
| data-storyteller | **Waste per person per day.** EU27 and each Member State, 2023, = kg per person per year / 365, for a human-scale headline. Source: findings §1 (kg per person). | Done: findings §1, last bullet |
| data-storyteller | **Trend of the EU27 municipal recycling rate** since 2011 (or 2020, given the break). | On hold |
| data-storyteller | **Decoupling class per Member State** (absolute, relative, none), 2023. | On hold |
| data-storyteller | **Irish GDP**: confirm that GDP per person overstates the Irish economy (multinationals), and the +23 % in 2015 in the dashboard note. | Done: confirmed, findings §2 (+23.5 % in 2015, CSO and Central Bank of Ireland); Irish note corrected |

## 7. Open questions

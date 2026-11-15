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

The dashboard follows the waste hierarchy from top to bottom: the reader learns the hierarchy first, then sees the steps the data covers, in the hierarchy's order. Approved on 15 November 2026.

1. **Hero: the waste hierarchy.** A five-step ladder (prevention, preparing for re-use, recycling, other recovery, disposal) frames the whole dashboard. Each step shows the EU27 figure from the data where there is one (findings §4); steps with a section are links, the others are greyed. Prevention shows no figure; preparing for re-use is greyed with no figure (no EU total: 8 Member States do not report it). "Not in the figures" (waste in no treatment figure) is shown under the waste hierarchy.
2. **How much waste do we generate?** Waste per person by country: an introduction, not linked to a step of the waste hierarchy (levels between countries are not a ranking of prevention, findings §1 bullet 14).
3. **Can the economy grow without more waste? (prevention over time).** Decoupling; the Prevention step of the hero's waste hierarchy links here.
4. **Are we recycling enough? (recycling).** Recycling rates against the 2025 targets.
5. **Back to the waste hierarchy.** A short closing panel: recycling is only halfway up the waste hierarchy, prevention comes first. No new facts.
6. **Methodological note** and **How I did this**, at the end.

- **Section titles are questions** (e.g. "How much do we throw away?"), worded by the ux-copywriter.
- **Treatment data will fill the greyed steps.** How municipal waste is treated across the hierarchy (recycling, composting, preparing for re-use, energy recovery, landfill) will be added as findings by a data scientist agent; until then those steps stay greyed. See section 6.
- Every chart invites the reader to find their own country and compare it with the EU27.
- **Distance to target shows all 8 rows** at once (a trial with two rows and a "show all" button was rejected).
- **Postponed deadlines are not marked in the chart.** Texts about the chart must not call the countries below the target "failing": where relevant, say that some postponed the deadline (findings §3; method notes §4).
- **Each chart has its own country search**; there is no single search for the whole page.

## 3. Key messages per section

Approved on 15 November 2026 (ux-copywriter's wording; figures are filled from the data, see section 4). Final texts are in `data/lookups/dashboard_texts.json` and the chart lookups.

| Section | Key message | From findings | Caveat to keep | What to notice or try |
|---|---|---|---|---|
| Hero | On average, each of us in the EU generates {eu_kg} kg of municipal waste a year; follow it down the waste hierarchy | §1 bullet 1; §4 bullets 1–2 and 7 | "Not in the figures" shown on its own; re-use greyed, no figure | The ladder steps, then find your country |
| How much waste do we generate? | Where you live makes a big difference: waste generation per person in {max_country} is {ratio} times that of {min_country} (among Member States without a change in definition) | §1 bullets 1, 2 and 12 | Countries count differently, also in the same year (§1 bullets 4–5 and 13) | Is your country above or below the EU27 bar? |
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

Proposed by the brand-designer ("Loop": warm paper background, deep green-black ink, one soft mint highlight, rounded shapes; no institutional navy or report grey). Approved so far (15 November 2026):

- **Chart colours**, each with one meaning across the dashboard (all at least 3:1 against the page for graphics):
  - Waste: orange `#d96a2b` (bars, waste line); `#b2511a` for waste-coloured text.
  - Economy (GDP): blue `#3b5bdb`.
  - EU27: ink `#1d2b2a` (bar, diamond, bold label); EU27 reference lines behind a country: grey `#838b88`.
  - Distance to target: d3 RdYlBu kept (red–orange below target, blue target met).
- **Hierarchy steps without data** are shown in grey.
- **Fonts (Google Fonts)**: Bricolage Grotesque (700, 800) for headlines; Inter (400–600, tabular numbers) for text, interface and charts.
- **Rest of the identity, built for review (15 November 2026)**, as proposed by the brand-designer:
  - Page: warm paper background `#fbf8f3`, ink `#1d2b2a`, muted ink `#55625f`, tint `#eef4f0` (hero and end matter), highlight `#dcefe3`; CSS tokens on `:root` in `dashboard/src/index.css`.
  - Hero on a tint panel: eyebrow, headline, lede, "start exploring" button, and the waste hierarchy as a large inverted pyramid of stacked trapezoids, each step narrower than the one above (steps with a section are white links that turn mint on hover; the others are greyed; no arrow). Under it: the share burnt without energy recovery (also disposal) and the share "not in the figures". Key-number cards wait for the copywriter's texts.
  - Sections: small pyramid icon with the section's step in mint, eyebrow, title, lede and "try this" chip (pale mint) (from `dashboard_texts.json`); the chart in a white card; notes folded under "About this chart" (the decoupling note of the selected country stays visible); sources under the card.
  - Closing panel with the pyramid; methodological note and "how I did this" on tint panels.
  - Charts: warm grid `#e6e1d8`; ink baseline and target ticks; 3 px rounded lines with a short fade when the country changes; beeswarm circles with a thin ink outline, a soft track per row and white halos on labels; rounder hover cards with 32 px flags; pill search boxes with a mint focus ring.
  - Small screens: one column; the beeswarm puts row labels above the rows, the decoupling chart drops line-end labels, the bar chart narrows its label column.
  - Respects `prefers-reduced-motion`.


- Identity in one sentence:
- Palette (colour, role, contrast):
- Typography:
- Waste-hierarchy motif:
- Layout (hero, section; desktop and mobile):
- Chart styling:
- CSS tokens:

## 6. Needs a finding

Figures or facts the communication would need that are not in `findings.md` yet. Each is calculated (or checked by the fact-checker) and added to `findings.md` before any text uses it.

| Requested by | What is needed | Status |
|---|---|---|
| data-storyteller | **Treatment of municipal waste across the hierarchy.** Question: what happens to the EU's municipal waste? Figure: shares of municipal waste generated that are prepared for re-use, recycled (material), composted and digested, incinerated with energy recovery, incinerated without, and landfilled, in % (each / generated). Scope: EU27 and each Member State, 2023, and the EU27 trend since 2011. Likely source: `env_wasmun` (`wst_oper` codes such as `PRP_REU`, `RCY_M`, `RCY_C_D`, `RCV_E`, `DSP_I`, `DSP_L_OTH`). Used for: the greyed steps of the hero ladder. Caveats: RCY sometimes includes PRP_REU (method notes §2); breaks in series; treatment can differ from generation (temporary storage). | Done: findings §4 (treatment) |
| data-storyteller | **Waste per person per day.** EU27 and each Member State, 2023, = kg per person per year / 365, for a human-scale headline. Source: findings §1 (kg per person). | Done: findings §1, last bullet |
| data-storyteller | **Trend of the EU27 municipal recycling rate** since 2011 (or 2020, given the break). | On hold |
| data-storyteller | **Decoupling class per Member State** (absolute, relative, none), 2023. | On hold |
| data-storyteller | **Irish GDP**: confirm that GDP per person overstates the Irish economy (multinationals), and the +23 % in 2015 in the dashboard note. | Done: confirmed, findings §2 (+23.5 % in 2015, CSO and Central Bank of Ireland); Irish note corrected |

## 7. Open questions

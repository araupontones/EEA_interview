# Decision log

Every decision taken on the way, newest first: data, dashboard and project organisation. One entry per decision, with the reason and where it is applied.

For data decisions, the full explanation and its consequences are in [method_notes.md](method_notes.md), which describes the data as it stands now; this log records when and why each decision was taken. Open questions still to decide are in [method_notes.md, section 7](method_notes.md#7-open-points).

## 15 November 2026

**The waste hierarchy gets its own section; no country comparison in "How much waste do we generate?".**
- Decision: the pyramid leaves the hero and becomes the first section, "The waste hierarchy": the pyramid with the EU figures, each level's explanation next to it (visible, not on hover), a link to the section of each covered level, and under it the share burnt without energy recovery and the share "not in the figures" with its explanation visible (this settles the open "Not in the figures ⓘ" task). The hero keeps label, title, lede and button, in one column; the button leads to the new section. The closing panel keeps its pyramid. The key message of "How much waste do we generate?" drops the Denmark/Romania comparison: "In {year}, the EU generated about {eu_mt} million tonnes of municipal waste, about {eu_kg} kg per person." (findings §1 bullet 1; new placeholder `{eu_mt}` in `lib/keyFigures.js`, from `mw_tt`).
- Why: the hero felt overcrowded, and the level explanations were hidden in hover tooltips that most people miss and phones do not show. The comparison needed an explanation (it leaves out countries with a change in definition, so it does not name the country with the longest bar); the user preferred to avoid it altogether.
- Applied in: `scripts/lookups/create_dashboard_texts.py` (`SECTIONS["waste-hierarchy"]`, new; `SECTIONS["municipal-waste"]`), `sections/waste_hierarchy/WasteHierarchySection.jsx` (new), `components/HierarchyMotif.jsx`, `sections/hero/Hero.jsx`, `App.jsx`, `index.css`, `lib/keyFigures.js`; [communication.md](communication.md) sections 2, 3 and 5.

**Key messages answer their section's question; hero lede in one paragraph.**
- Decision: "How much waste do we generate?" now answers with the amount first: "In {year}, the EU generated about {eu_kg} kg per person, but waste generation per person in {max_country} was {ratio} times that of {min_country}." (option A of the storyteller and copywriter); the lede keeps only the definition of municipal waste. The recycling key message stays as it is (the "Not yet:" versions sounded critical and did not acknowledge progress); decoupling and closing unchanged. The hero lede is the user's own text, one paragraph with the EU kg and landfill figures in bold Barlow (the separate key-figure sentence is dropped). The "2011 level (100)" label in the decoupling chart moves up to the 117 level, and section texts run to 85 % of the chart width.
- Why: the old key message answered "do countries differ?", not "how much?"; the decoupling section ("Mostly yes: …") was the model.
- Applied in: `scripts/lookups/create_dashboard_texts.py` (`SECTIONS["municipal-waste"]`, `HERO["lede"]` as text/figure parts), `sections/hero/Hero.jsx`, `index.css`, `DecouplingLineChart.jsx`; [communication.md](communication.md) section 3.

**Rebrand built: "Le Journal" identity applied on the `rebrand` branch.**
- Decision: the brand designer's full spec is applied, with the user's choices: bars in light orange `#fa9f5c` with a dark orange end cap (option 1 of 3); GDP in steel blue `#2563a8`; the mint highlight replaced by ink; the EU27 bar in a neutral slate blue-grey `#4f6d8a` instead of near-black, which read as negative (the GDP blue is not reused, so blue keeps meaning "economy"); the recycling targets chart changes only its font, while its search box, caption and hover card follow the new style like the other charts. The hero key-number cards become one sentence with the figures set large (`hero.key_sentence`, same wording as the cards). The bar chart hint now says "the EU27 bar" instead of "the dark EU27 bar".
- Why: reviewers found the previous look close to Claude's default style; see the entry below for the direction.
- Applied in: `dashboard/src/index.css`, `components/HierarchyMotif.jsx`, `components/Section.jsx`, the hero, closing, section and end-matter components, `WastePerCapitaBarChart.jsx`, `DecouplingLineChart.jsx`; `scripts/lookups/create_dashboard_texts.py`; [communication.md](communication.md) section 5.

**Rebrand direction: editorial layout on white, Barlow Semi Condensed + Literata.**
- Decision: a hybrid of the brand designer's directions A ("Le Journal": thin rules, no boxed cards, notes on the charts instead of legends) and C's fonts, on a white page (no dark sections for now; may be tested later). Barlow Semi Condensed for headlines and chart labels, Literata for paragraphs. Square corners everywhere except buttons, which stay rounded. The waste-hierarchy pyramid stays flat (outlined trapezoids, no drawn 3D version). Section labels stay in capitals, with the small pyramid icon. The hero key-number cards are first tested as one sentence with large figures (they may be dropped). The bars stay all coloured; the designer proposes a lighter orange that keeps 3:1 contrast against white (#FA9F5C alone is 2.1:1). The pale mint highlight and the GDP blue are open to review. The recycling targets chart changes only its font. No wordmark yet (name to be decided), no "guess first", no dark mode, no projector variant.
- Why: three reviewers found the current look close to Claude's default style (cream page, mint, display font over Inter, rounded cards, pills); the user likes Pablo Robles's typography and Les Décodeurs' editorial style, and prefers a white page with sans headlines and serif text.
- Applied in: to be specified by the brand designer and applied on a `rebrand` branch; nothing reaches `main` until the user approves the screenshots. Then [communication.md](communication.md) section 5.

**Back to the Denmark / Romania ratio, worded about waste generation, not people.** (Replaces the range decided just before.)
- Decision: the hero card and the key message compare waste generation per person, not people: "Waste generation per person in {max_country} is {ratio} times that of {min_country}" (2023: Denmark / Romania = 2.5, among Member States without a change in definition). The texts do not say that "countries count it differently".
- Why: the user found that saying "countries count it differently" in the headline undermines the credibility of the whole dashboard; comparing generation rather than people keeps it neutral. The caveat on definitions stays in the notes under the charts and in the method note.
- Applied in: `scripts/lookups/create_dashboard_texts.py`, `dashboard/src/lib/keyFigures.js`; [communication.md](communication.md) section 3; [findings.md](findings.md) §1 bullet 12.

**Differences between countries shown as a range, not a ratio.** (Replaces the Denmark / Romania ratio decided earlier today.)
- Decision: the key message of "How much waste do we generate?" and the second hero card show the range of waste per person from the lowest to the highest Member State, naming both (2023: 305 kg in Romania to 782 kg in Austria), "partly because countries count it differently". Option A of the storyteller and copywriter.
- Why: "people in Denmark generate 2.5 times as much as people in Romania" read as a reproach to one country's people; a range describes the spread without a verdict, and gives the reason in the same sentence (findings §1 bullets 2, 13–14).
- Applied in: `scripts/lookups/create_dashboard_texts.py`, `dashboard/src/lib/keyFigures.js` (new placeholders `{low_kg}`, `{high_kg}`, `{low_country}`, `{high_country}`; the ratio placeholders are removed); [communication.md](communication.md) section 3; [findings.md](findings.md) §1 bullet 12.

**Section eyebrows without step numbers.**
- Decision: "Step 1 · Prevention, over time" and "Step 3 · Recycling" become "Prevention, over time" and "Recycling".
- Why: the levels of the waste hierarchy are a ranking of options, not steps in a sequence. The same applies to the other texts: hero eyebrow "Waste in the EU, from best to worst", closing title "Recycling is only halfway up the waste hierarchy", and "level" instead of "step" in the method notes.
- Applied in: `scripts/lookups/create_dashboard_texts.py`; [communication.md](communication.md) sections 2–4 (new wording rule).

**Highlight colour: pale mint instead of yellow.**
- Decision: the highlight `#ffd84d` (yellow) becomes `#dcefe3` (pale mint) for the "Try this" hints, the hover on the hierarchy steps, the step highlighted in the section icon and the search focus ring. Ink text on it: 12.2:1.
- Why: the yellow was too aggressive; mint is calmer and ties in with the green tint of the hero.
- Applied in: `dashboard/src/index.css` (`--color-highlight`), `components/HierarchyMotif.jsx`; [communication.md](communication.md) section 5.

**"How much waste do we generate?" is an introduction, not the Prevention step.**
- Decision: the section has no eyebrow, no hierarchy icon and no prevention sentence; its lede is the definition of municipal waste and the EU figure. The Prevention step of the hero's waste hierarchy now links to the decoupling section, which keeps "Step 1 · Prevention, over time". The hero button leads to the first section of the page.
- Why: levels between countries are not a ranking of prevention effort (findings §1 bullet 14); the section introduces how much waste we generate.
- Applied in: `scripts/lookups/create_dashboard_texts.py`, `sections/hero/Hero.jsx`; [communication.md](communication.md) section 2.

**Waste hierarchy drawn as an inverted pyramid; disposal shows only landfill.**
- Decision: the steps are stacked trapezoids (each one narrower than the one above), not rounded pills, and the orange loop arrow is removed, so the shape reads as an inverted pyramid (hero, closing panel and the small section icon). The disposal step shows only "{landfill} % landfill"; the share burnt without energy recovery moves under the pyramid ("Also disposal: …"), next to "Not in the figures".
- Applied in: `components/HierarchyMotif.jsx`, `scripts/lookups/create_dashboard_texts.py` (`hierarchy.burnt`); [communication.md](communication.md) section 5.

**Prevention stays linked to waste per person and decoupling, with framing.**
- Decision: the fact-checker confirmed that waste generated per person is the indicator used to track prevention (WFD Art. 9(3); Eurostat cei_pc031; EEA 2025) and that decoupling is the aim of prevention programmes (WFD Art. 29), but that waste generated is the result of prevention, not prevention itself, and that levels between countries are not a ranking of prevention effort. Both sections keep the "Prevention" eyebrow; the waste-per-person section's lede now says "Waste we avoid can't be counted, so we look at how much we generate: if prevention works, this falls over time."
- Applied in: [findings.md](findings.md) §1 bullet 14 and §2 bullet 7; [method_notes.md](method_notes.md) §2 (hierarchy mapping); `scripts/lookups/create_dashboard_texts.py`.

**"Waste hierarchy", not "waste ladder"; a simpler hierarchy in the hero.**
- Decision: the Waste Framework Directive's name is used everywhere, explained as "how the EU ranks what to do with waste, from best to worst for the environment" (copywriter). In the hero, Prevention shows only its name, Preparing for re-use is greyed with no figure (no EU total: 8 Member States, including some of the largest, do not report it, so any EU figure would be incomplete), and no step shows "Chart coming soon". The hero lede starts "On average".
- Applied in: `scripts/lookups/create_dashboard_texts.py`, `components/HierarchyMotif.jsx`; [communication.md](communication.md) sections 2–4.

**Ratio between countries: only Member States without a change in definition (data-scientist, option A).**
- Decision: the hero card and the key message compare the Member States with the most and least waste per person among those without a break year in `decoupling_notes.json` (2023: Denmark / Romania = 2.5), not Austria / Romania (2.6), because Austria's level includes its 2020 change in definition. Findings §1 bullet 2 was wrong ("around 2.5 times" between groups of three countries; the group averages give 2.2) and was corrected. New findings: §1 bullet 12 (the ratio) and bullet 13 (comparing countries in one year needs care); the definition of municipal waste is in method notes §2.
- Applied in: `dashboard/src/lib/keyFigures.js`; [findings.md](findings.md) §1; [method_notes.md](method_notes.md) §2.

**Fact-check fixes applied.**
- Closing panel no longer says the EU "is close to its targets" (it beats the packaging target but is short for municipal waste and plastic); Irish and Estonian notes corrected; method notes separate the five countries that widened their definition from Estonia and Slovenia; "adjusted for inflation"; decoupling lede "has grown more than waste since 2011"; "burnt without energy"; "every row where it has data"; "How I did this" describes the agents accurately; distance-to-target texts use the year of the targets data.

**Dashboard texts applied (ux-copywriter, approved with changes).**
- Decision: hero "Where does our waste go?", with the yearly figure per person in the lede (not the daily one); question titles; plain-language notes and hover cards ("points below the target", not "pp"); "generate" instead of "make" everywhere (as in the early warning reports). The ladder shows the EU27 figure of every step from the data, with "Chart coming soon" on the steps without a chart. Figures in the texts are placeholders filled from the processed data (`lib/keyFigures.js`), so they follow new downloads. "How I did this" describes the project (API, Python pipeline, D3 and React, Claude Code and agents), not findings. The data-scientist added the decoupling jumps as findings (§1 bullets 10–11, §2 bullet 6), so the country notes keep their figures; Luxembourg's note now says GDP "stayed about the same" before its change.
- Applied in: `scripts/lookups/create_dashboard_texts.py`, `create_decoupling_notes.py`, `create_municipal_waste_notes.py`, `dashboard/src/lib/keyFigures.js`, the section components; [communication.md](communication.md) sections 2–4.

**Visual identity "Loop" built for review.**
- Decision: the brand-designer's identity is applied in full for the user to review: CSS tokens, warm page, hero with the hierarchy pyramid, section headers with a small pyramid icon, chart cards, notes folded under "About this chart", closing panel, restyled charts and hover cards, small-screen layouts. Page texts (hero, ladder, section headings, labels) now come from a new lookup, `dashboard_texts.json`, with the current titles until the copywriter's texts are approved.
- Applied in: `dashboard/src/index.css`, `components/HierarchyMotif.jsx`, `components/Section.jsx`, `sections/hero/Hero.jsx`, `sections/closing/ClosingPanel.jsx`, the three charts; `scripts/lookups/create_dashboard_texts.py`; [communication.md](communication.md) section 5.

**Poland 2023 is a documented break in method (data-scientist).**
- Decision: from 2023 Poland's treatment data are reported directly by companies instead of partly estimated (Eurostat country notes; flag `b` on treatment, recycling and landfill). Poland's 2023 rates are not compared with earlier years.
- Applied in: [findings.md](findings.md) sections 3–5, [method_notes.md](method_notes.md) sections 2 and 7. The count in method notes section 2 was also corrected (40 of 550 country-years without a recycling rate, all outside the EU).

**Distance-to-target chart: hover text in a card.**
- Decision: hovering a circle shows a small card (flag, country, waste category, recycling rate and distance to the 2025 target) instead of a text label on the chart; it opens above the circle (below it in the first row) and stays inside the chart.
- Why: the label clashed with circles, lines and row labels and was hard to read; the card matches the bar chart's hover card.
- Applied in: `DistanceToTargetScatter.jsx` (`HoverCard`), `dashboard/src/index.css` (`.hover-card-small`).

**Irish GDP: claim confirmed, real GDP per person kept for all countries.**
- Decision: the data-scientist confirmed that Irish GDP per person overstates the growth of the Irish economy (our data: +23.5 % in 2015, EU27 +2.2 %; cause from the Irish Central Statistics Office and the Central Bank of Ireland, cited in findings §2). Real GDP per person stays the measure for all countries, Ireland included; modified GNI (GNI*) exists only for Ireland, so it cannot be compared across Member States. The Irish note under the decoupling chart now uses the checked figure (23.5 %, not "23 %") and names the source.
- Applied in: [findings.md](findings.md) section 2, [method_notes.md](method_notes.md) section 6, `scripts/lookups/create_decoupling_notes.py`.

**Distance-to-target chart: back to all 8 rows; postponed countries not marked.** (Replaces the two-row trial and the hollow circles decided earlier today.)
- Decision: the chart shows all 8 rows, with no "show all" button. The countries that postponed a target are drawn like all others; no `postponed_2025` flag.
- Consequence: texts must not call countries below the target "failing" where they postponed the deadline (method notes §4).
- Applied in: `DistanceToTargetScatter.jsx`, [method_notes.md](method_notes.md) section 4, [communication.md](communication.md) section 2.

**No single country search for the whole page; fonts from Google Fonts.**
- Decision: each chart keeps its own search. Fonts: Bricolage Grotesque for headlines, Inter for text and charts, loaded from Google Fonts.
- Applied in: `dashboard/src/index.css`; [communication.md](communication.md) section 5.

**Decoupling class per country on hold; Irish GDP to be confirmed by the data-scientist.**
- Applied in: [communication.md](communication.md) section 6.

**Treatment of municipal waste across the hierarchy, and waste per person per day (data-scientist).**
- Decisions: shares are of waste **generated**, not treated (as the recycling rate, the WFD Art. 11 target and the landfill target), with the remainder kept visible as `unaccounted_pct`. Hierarchy mapping: preparing for re-use = `PRP_REU`; recycling = `RCY_M` + `RCY_C_D` (composting and digestion count as recycling; preparing for re-use kept apart, so it is never counted twice); other recovery = `RCV_E`; disposal = `DSP_I` + `DSP_L_OTH`; prevention has no share. The EU27 preparing-for-re-use share stays empty (8 Member States do not report it). Missing EU27 2023 disposal totals (Latvia has no figure) are estimated with Eurostat's previous-year method, flagged `estimated`, and the rule stops once Eurostat publishes them. Waste per person per day = kg per year / 365, stored as `mw_pc_day` (two decimals) in `municipal_waste.json`.
- Why: comparable with the targets; nothing double counted; the dashboard reads the figures from files.
- Applied in: `scripts/interim/env_wasmun.py`, `scripts/processed/municipal_waste_treatment.py` → `data/processed/municipal_waste_treatment.json`, `scripts/processed/municipal_waste.py`; [findings.md](findings.md) sections 1 and 4 (caveats are now section 5); [method_notes.md](method_notes.md) section 2.

**Dashboard colours: waste orange, GDP blue, EU27 ink.**
- Decision: country bars and the waste line `#d96a2b` (labels `#b2511a`), GDP line `#3b5bdb`, EU27 ink `#1d2b2a` in all charts (bar, diamond), EU27 reference lines `#838b88`. Replaces the blue bars `#5d92f5`, the EU27 navy `#003494` and the earlier dark grey `#333333`, the waste line `#e07b39` and the reference grey `#bdbdbd`.
- Why: one meaning per colour across the dashboard, a less institutional look, and three of the old colours failed the WCAG 3:1 contrast for graphics (`#e07b39` 2.97, `#5d92f5` 3.05 on white and 2.97 on the page, `#bdbdbd` 1.88).
- Applied in: `WastePerCapitaBarChart.jsx`, `DecouplingLineChart.jsx`, `DistanceToTargetScatter.jsx`; [communication.md](communication.md) section 5.

**Distance-to-target chart: trial with two rows by default.** (Replaces "all 8 rows" taken earlier today.)
- Decision: municipal waste and plastic packaging are shown first; a "Show all materials" button opens the other six. If the trial does not work, back to all 8 rows.
- Applied in: `DistanceToTargetScatter.jsx` (`DEFAULT_ROWS`). The button labels are in the component for now and move to a lookup with the copywriter's texts.

**No COVID-19 explanation in the dashboard.**
- Decision: the EU27 note under the decoupling chart no longer mentions COVID-19 or its cause.
- Why: not supported by the findings.
- Applied in: `scripts/lookups/create_decoupling_notes.py`.

**A data-scientist agent owns the analytical pipeline.**
- Decision: `.claude/agents/data-scientist.md` is responsible for download, raw, lookups, interim and processed data, and turns "Needs a finding" requests into findings and method notes. First tasks: treatment of municipal waste across the hierarchy, and waste per person per day. The trend of the recycling rate is on hold.
- Applied in: `.claude/agents/data-scientist.md`, [communication.md](communication.md) section 6.

**Distance-to-target chart: all 8 rows, postponed countries as hollow circles.**
- Decision: the chart keeps all 8 rows at once. In the municipal waste row, the 8 Member States that postponed the 2025 target are hollow circles, with a legend entry "Deadline postponed" and a hover label (at least 50 % by 2025). The flag comes from a new pipeline lookup. Packaging is not marked until we know which materials each country postponed.
- Why: a postponed deadline is legal, so missing 55 % in 2023 must not read as a failure.
- Applied in: [communication.md](communication.md) section 2; to do in [todo.md](todo.md).

**Storyline: the dashboard follows the waste hierarchy.**
- Decision: hero with a five-step hierarchy ladder; steps without data greyed ("not in this dashboard yet"), not hidden; then waste per person and decoupling (prevention), distance to target (recycling), a closing panel back to the ladder. Section titles are questions.
- Treatment data across the hierarchy will be added as findings by a data scientist agent, to fill the greyed steps. "Needs a finding" requests from the storyteller and copywriter must say the question, figure, scope, likely source, use and caveats.
- Why: teaches the hierarchy first and is honest about what the data covers; question titles invite the reader in.
- Applied in: [communication.md](communication.md) sections 2 and 6; `.claude/agents/data-storyteller.md`, `ux-copywriter.md`.

**Communication has its own document, separate from the findings.**
- Decision: `docs/communication.md` holds how the dashboard communicates, as it stands now (audience, storyline, key messages, voice and glossary, visual identity, "Needs a finding" requests). `findings.md` stays the only source of facts; key messages point to findings and never restate figures; final texts stay in the lookups; this log records when and why.
- Why: keeps facts and communication apart, so a figure is changed in one place only, and gives the storyteller, copywriter and designer one shared brief.
- Applied in: [communication.md](communication.md), the four agents, `CLAUDE.md`, `README.md`.

**Findings-only rule for every dashboard text.**
- Decision: all agents (and the main session when writing dashboard texts) use only facts in `docs/findings.md`: no general knowledge, no outside sources, no assumed causes, no new figures. A missing figure is a "Needs a finding" request: calculated and added to the findings first, if agreed. The fact-checker marks claims that are true in the data but not in the findings as "not in findings". Only exception: the order and names of the waste hierarchy. The fact-checker may use outside sources to verify the data and the findings (cited with URLs); corrections go into the findings first.
- Why: the dashboard simplifies for the public; every message must still be traceable to a checked finding.
- Applied in: the four files in `.claude/agents/`, `CLAUDE.md`.

**Four agents for the dashboard's content and design.**
- Decision: `.claude/agents/` holds `data-storyteller`, `ux-copywriter`, `brand-designer` and `fact-checker`. They only propose; changes are applied after approval. The dashboard gets its own visual identity (not an institutional brand), and its texts are in English only.
- Why: the dashboard is for a general public that reads little; it should explain the waste hierarchy and the circular economy through key messages and charts people can play with, without losing accuracy (hence the fact-checker).
- Applied in: `.claude/agents/`, `CLAUDE.md`.

**Every chart shows its data source and download date.**
- Decision: a source line under each chart names the Eurostat datasets it uses (linked to the Eurostat data browser), the date Eurostat last updated each one and the date we downloaded it. Built by `scripts/lookups/create_data_sources.py` from the raw catalog, so the dates follow each new download.
- Why: readers can trace every figure to its source and see how recent it is; figures change when Eurostat revises past years.
- The distance-to-target chart also names the legal acts that set the targets (Waste Framework Directive, Regulation (EU) 2025/40), linked to EUR-Lex and read from `recycling_targets.json`, so they always match the targets shown.
- Applied in: `create_data_sources.py` → `data/lookups/data_sources.json`, `dashboard/src/components/ChartSource.jsx`, the three chart sections.

**Notes under the charts use the full width of the chart.**
- Decision: the notes are no longer limited to 75 characters per line.
- Why: they looked detached from the chart at half its width.
- Applied in: `dashboard/src/index.css` (`.chart-note`).

**Decoupling chart: a search box selects the geography, with the EU27 as grey reference.**
- Decision: a search box like the one of the distance-to-target chart selects one geography; the EU27 is shown by default. When a Member State is selected, its waste and GDP lines are coloured and the EU27 lines stay behind them in grey, labelled "EU27 waste per person" and "EU27 GDP per person". Fixed y axis for all geographies (80 to 210), dashed line at 100, vertical line on the break year. No hover card. Caption and labels come from `decoupling_notes.json`.
- Why: one country at a time keeps the chart readable (two lines per country); the EU27 reference shows at once whether a country does better or worse than the EU.
- Applied in: `dashboard/src/sections/decoupling/DecouplingLineChart.jsx`, `scripts/lookups/create_decoupling_notes.py`.

**Decoupling notes: a country note only where the cause of a jump is documented.**
- Decision: country notes for the breaks with a jump of 10 % or more whose cause is in the Eurostat annex: Estonia 2014, Slovenia 2013, Ireland 2014 added; Luxembourg's note made precise (2016, +34 %) and Luxembourg added to the break note. Jumps without a documented cause (Romania 2011, Finland 2022, Latvia 2015) get no note and become an open point. Small breaks (< 10 %) get no note.
- Why: a note must explain the jump, not guess at it.
- Applied in: `create_decoupling_notes.py`, [method_notes.md, section 6](method_notes.md#6-municipal-waste-decoupling).

**Decoupling chart: the break note is shown only with the EU27.**
- Decision: the note on the countries that changed their definition is shown when the EU27 is selected; a selected country shows its own note instead.
- Why: the EU27 total includes those changes; for a country, its own note already explains its break.
- Applied in: `DecouplingLineChart.jsx`, `create_decoupling_notes.py`.

**Correction: Luxembourg's 2016 break is large.**
- Earlier today Luxembourg was left out of the break marker and note because "its effect is small". That used its net change since 2011 (+7.8 %); the jump in 2016 itself is +34 %. Luxembourg is now in the break note.

**The breaks in series are explained under the decoupling chart, not in the bar chart.**
- Decision: the † marker and the break note are removed from the municipal waste bar chart. The note moves to the decoupling chart as `break_note`, shown for every country, next to the country notes and the break-year marker.
- Why: the bar chart shows one year (2023) and compares countries, not years; the decoupling chart compares years, where the breaks change the reading.
- Applied in: `scripts/lookups/create_municipal_waste_notes.py`, `scripts/lookups/create_decoupling_notes.py`, `WastePerCapitaBarChart.jsx`, [method_notes.md, section 6](method_notes.md#6-municipal-waste-decoupling).

**Municipal waste bar chart: a card on hover, with the country's flag.**
- Decision: hovering a row dims the other bars and shows a card with the flag in a circle (top left), the country name, waste per person (kg) and waste generated (thousand tonnes). The card labels and units come from `data/lookups/municipal_waste_notes.json`.
- Why: the bars show only waste per person; the card adds the total without crowding the chart.
- Applied in: `WastePerCapitaBarChart.jsx`, `scripts/lookups/create_municipal_waste_notes.py`.

**Flags come from the flag-icons npm package, mapped through a lookup.**
- Decision: the flag code of each geography is in `data/lookups/geo_flags.json` (built by `scripts/lookups/create_geo_flags.py`); the images are the square SVG flags of `flag-icons` (MIT, version 7.6.0 pinned), and only the 28 flags used are bundled (`dashboard/src/lib/flags.js`).
- Why: Eurostat codes are not always ISO codes (Greece is `EL`, the EU27 total uses the EU flag), so the mapping is data and belongs in the pipeline. A pinned package, rather than scraping flags from a website, keeps the images versioned, licensed and available offline.
- Applied in: `create_geo_flags.py`, `dashboard/src/lib/flags.js`, `dashboard/package.json`.

**Municipal waste bar chart: horizontal bars, sorted from highest to lowest.**
- Decision: one row per Member State, from the highest waste per person to the lowest, for the latest year with data for all 27 Member States (2023), computed in the chart so it moves on when a complete new year is published.
- Why: country names stay readable, the ranking is visible at once, and the layout matches the rows of the distance-to-target chart.
- Applied in: `dashboard/src/sections/municipal_waste/WastePerCapitaBarChart.jsx`.

**Municipal waste bar chart: the EU27 is a bar in its own colour.**
- Decision: the EU27 is one more bar, in its ranked position, in dark grey (`#333333`) with a bold label.
- Why: the EU27 value can be read and ranked like the countries; dark grey is the EU27 colour in the distance-to-target chart too.
- Applied in: `WastePerCapitaBarChart.jsx`.

**Municipal waste bar chart: breaks in series get a marker and a note.** (Replaced the same day: see "The breaks in series are explained under the decoupling chart".)
- Decision: Czechia (2017), Belgium, Austria and Slovakia (2020) have a † after their name, explained in a note under the chart. Luxembourg (2016) is not marked, as its effect is small.
- Why: their figures rose because of a wider definition, not more waste; readers comparing with earlier years or other sources need to know.
- Applied in: `scripts/lookups/create_municipal_waste_notes.py` → `data/lookups/municipal_waste_notes.json`; [method_notes.md, section 6](method_notes.md#6-municipal-waste-decoupling).

**Findings are kept in `docs/findings.md`.**
- Decision: one file with the most relevant findings of the analysis (municipal waste per person, decoupling, distance to target), with figures, kept up to date when the data or the method changes.
- Why: a single summary of results to draw on for the dashboard texts and presentations.
- Applied in: [findings.md](findings.md), `CLAUDE.md`, `README.md`.

**The `docs/` folder is the project notebook.**
- Decision: `method_notes.md` and `todo.md` moved to `docs/`; `dashboard_notes/` removed; this decision log added.
- Why: one place for all project notes, not only notes about the dashboard.
- Applied in: `CLAUDE.md`, `README.md`, and the references in `scripts/interim/env_waspacr.py`, `scripts/lookups/create_decoupling_notes.py` and `dashboard/src/sections/method_note/MethodNoteSection.jsx`.

**Open data questions are listed only in the method notes (section 7).**
- Decision: `todo.md` holds only build tasks and links to the method notes for open data questions. When a decision leads to work, the task is added to `todo.md`.
- Why: the two lists overlapped and had drifted apart.
- Applied in: [method_notes.md, section 7](method_notes.md#7-open-points), [todo.md](todo.md).

**Rates: share or % in raw and interim data, % with one decimal in processed data and the dashboard.**
- Decision: raw and interim tables keep the unit of the source (e.g. the municipal recycling rate as a share from 0 to 1), stated in the script docstring. Processed scripts convert rates to % with one decimal, so the dashboard always shows %.
- Why: interim tables stay close to the source; the dashboard uses one unit for all rates.
- Applied in: `CLAUDE.md` and `README.md` (conventions), [method_notes.md](method_notes.md) sections 2 and 3. Already done in `scripts/processed/recycling_distance_to_target.py`.

**The year column stays `time` in the interim tables.**
- Decision: not renamed; the processed files already use `year`.
- Why: it does not affect any output.

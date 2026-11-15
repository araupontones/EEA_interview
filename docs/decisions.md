# Decision log

Every decision taken on the way, newest first: data, dashboard and project organisation. One entry per decision, with the reason and where it is applied.

For data decisions, the full explanation and its consequences are in [method_notes.md](method_notes.md), which describes the data as it stands now; this log records when and why each decision was taken. Open questions still to decide are in [method_notes.md, section 7](method_notes.md#7-open-points).

## 15 November 2026

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

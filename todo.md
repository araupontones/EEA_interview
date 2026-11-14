# To do

## 1. Next: dashboard charts (D3 and React, in `dashboard/`)

- [ ] **Municipal waste bar chart** (`dashboard/src/sections/municipal_waste/WastePerCapitaBarChart.jsx`): distribution of municipal waste per person (kg) between the 27 EU Member States, with the EU27 as reference.
  - Data: `municipal_waste.json` (`mw_pc`); latest year with data for all 27 countries is 2023 (2024 has 26).
  - Decide: sort order, EU27 as a bar or a reference line, and how to note the breaks in series (Czechia 2017; Belgium, Austria, Slovakia 2020).
- [ ] **Decoupling line chart** (`dashboard/src/sections/decoupling/DecouplingLineChart.jsx`): municipal waste per person and real GDP per person, both indexed to 2011 = 100 (prototype in `notebooks/python/07_explore_municipal_waste.ipynb`).
  - Data: `municipal_waste_decoupling.json`, names from `geo_eu27.json`.
  - A dropdown with the countries (EU27 first, then the 27 Member States by name) to explore the data by country; EU27 selected by default.
  - Fixed y axis, the same for every country, so countries can be compared fairly (no zoom in or out when the selection changes): from the lowest to the highest index of all countries, rounded out to the nearest 10 (80 to 210 with the current data). Dashed reference line at 100.
  - A note under the chart that changes with the selected country: the general note for all countries, and a country note where the data needs care, with a marker on the break year. Texts and break years are in `data/lookups/decoupling_notes.json` (built by `scripts/lookups/create_decoupling_notes.py`): read them from there, do not write them in the dashboard code.

## 2. Rest of the dashboard

- [ ] Texts: hero (title, subtitle, brief explanation), the text of each section, the methodological note and "How I did this".
- [ ] Fonts and text sizes for all charts (now temporary classes in `dashboard/src/index.css`).
- [ ] Distance-to-target chart: add a note for Cyprus steel packaging, which is empty in the data (published rate 221.5 %).
- [ ] Mark the Member States that postponed the 2025 targets ("deadline postponed") instead of showing them as failing.
- [ ] Publish: on GitHub, Settings → Pages → Source: "GitHub Actions"; check the first deployment.

## Open points (from dashboard_notes/method_notes.md)

- [ ] Decide whether the municipal recycling rate uses RCY, RCY_M + RCY_C_D, or RCY_M + RCY_C_D + PRP_REU.
- [ ] Check the municipal recycling rate against the official Eurostat rate for a few countries.
- [ ] Decide how to handle breaks in series in municipal waste per person (note, index from the break year, or a `break_year` column), and check the breaks not yet reviewed (Estonia, Ireland, Poland, Portugal, Slovenia, Greece, Sweden, France).
- [ ] Confirm with the reporters the packaging rates above 100 % (Slovenia, Poland).
- [ ] Find which packaging materials each of the 7 Member States postponed, and decide whether to add a `postponed_2025` flag to the lookups.

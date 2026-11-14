# To do

## 1. Next: explore the municipal waste data for the dashboard

- [ ] Explore the processed municipal waste data (`data/processed/municipal_waste.json` and `municipal_waste_decoupling.json`) in a notebook (`notebooks/python/07_explore_municipal_waste.ipynb`) to decide the best way to present it in the dashboard.
  - Idea so far: first the distribution of waste per person between EU countries (bar chart), then the EU27 series over time (y axis from 0) to show that waste per person has stayed almost constant while real GDP grew (decoupling).
  - Breaks in series (Czechia 2017; Belgium, Austria, Slovakia 2020; see method notes section 6) and the 8 Member States that postponed the 2025 municipal waste target.
  - Decide whether `EU27_2020` is shown as a point or line, or as a reference line.
- [ ] Adjust `scripts/processed/municipal_waste.py` and `municipal_waste_decoupling.py` to the chosen charts, if needed.

## 2. Dashboard (D3 and React)

- [ ] Build the dashboard with D3 and React, reading the JSON files in `data/processed/`:
  - `recycling_distance_to_target.json`: recycling rates and distance to the 2025 target, municipal and packaging waste, 2023.
  - `municipal_waste.json`: municipal waste generated per person (kg) and in total (thousand tonnes), per country and year, 2010–2024.
  - `municipal_waste_decoupling.json`: municipal waste and real GDP per person, indexed to 2011 = 100 (decoupling).
- [ ] Rates on a scale from 0 to 105 %. Add a chart note for Cyprus steel packaging, which is empty in the data (published rate 221.5 %).
- [ ] Mark the Member States that postponed the 2025 targets ("deadline postponed") instead of showing them as failing.
- [ ] Decoupling chart: one line chart with two lines, municipal waste per person and real GDP per person, both indexed to 2011 = 100 (prototype in `notebooks/python/07_explore_municipal_waste.ipynb`).
  - A dropdown with the countries (EU27 first, then the 27 Member States by name, from `data/lookups/geo_eu27.json`) to explore the data by country; EU27 selected by default.
  - Fixed y axis, the same for every country, so countries can be compared fairly (no zoom in or out when the selection changes): from the lowest to the highest index of all countries, rounded out to the nearest 10 (80 to 210 with the current data). Dashed reference line at 100.
- [ ] Show a note under the decoupling chart that changes with the selected country:
  - a general note for all countries: how to read the index and what decoupling means (2011 = 100; GDP line above the waste line = decoupling);
  - a country note where the data needs care, plus a marker on the break year: Czechia (break 2017), Belgium, Austria, Slovakia (definition change 2020), Ireland (GDP inflated by multinational companies' accounting), EU27 (2020–2021 affected by COVID-19 and the definition changes);
  - the note texts and break years are in `data/lookups/decoupling_notes.json` (built by `scripts/lookups/create_decoupling_notes.py`): read them from there, do not write them in the dashboard code.

## Open points (from dashboard_notes/method_notes.md)

- [ ] Decide whether the municipal recycling rate uses RCY, RCY_M + RCY_C_D, or RCY_M + RCY_C_D + PRP_REU.
- [ ] Check the municipal recycling rate against the official Eurostat rate for a few countries.
- [ ] Decide how to handle breaks in series in municipal waste per person (note, index from the break year, or a `break_year` column), and check the breaks not yet reviewed (Estonia, Ireland, Poland, Portugal, Slovenia, Greece, Sweden, France).
- [ ] Confirm with the reporters the packaging rates above 100 % (Slovenia, Poland).
- [ ] Find which packaging materials each of the 7 Member States postponed, and decide whether to add a `postponed_2025` flag to the lookups.

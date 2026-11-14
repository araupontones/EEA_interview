# To do

## 1. Next: processed data for municipal waste

- [ ] Write `scripts/processed/municipal_waste.py`, which builds the processed municipal waste table from `data/interim/env_wasmun.parquet` and saves it as `data/processed/municipal_waste.json` (see the conventions in the README).
  - Indicators available: waste generated per person (kg) and in total (thousand tonnes), recycled (thousand tonnes), recycling rate. All years 2010–2024.
  - Recycling rate in % with one decimal, as in `recycling_distance_to_target.json` (the interim rate is a share from 0 to 1).
  - Year as a whole number (`year`), not text (`time`).
  - Keep `EU27_2020` so it can be used as a reference in the charts.
  - Add the script to `STEPS` in `scripts/run_pipeline.py`, and document the decisions in `dashboard_notes/method_notes.md`.

## 2. Explore the municipal waste data for the dashboard

- [ ] Explore the processed municipal waste data in a notebook (`notebooks/python/07_explore_municipal_waste.ipynb`) to decide the best way to present it in the dashboard.
  - Trends over time (e.g. waste per person, recycling rate, 2010–2024), country comparisons, distance to the 2025 target (55 %).
  - The break in series in 2020 (new calculation rules) and the 8 Member States that postponed the 2025 target.
  - Decide whether `EU27_2020` is shown as a point or line, or as a reference line.
- [ ] Adjust `scripts/processed/municipal_waste.py` to the chosen charts, if needed.

## 3. Dashboard (D3 and React)

- [ ] Build the dashboard with D3 and React, reading the JSON files in `data/processed/`:
  - `recycling_distance_to_target.json`: recycling rates and distance to the 2025 target, municipal and packaging waste, 2023.
  - `municipal_waste.json`: municipal waste indicators over time (from step 1).
- [ ] Rates on a scale from 0 to 105 %. Add a chart note for Cyprus steel packaging, which is empty in the data (published rate 221.5 %).
- [ ] Mark the Member States that postponed the 2025 targets ("deadline postponed") instead of showing them as failing.

## Open points (from dashboard_notes/method_notes.md)

- [ ] Decide whether the municipal recycling rate uses RCY, RCY_M + RCY_C_D, or RCY_M + RCY_C_D + PRP_REU.
- [ ] Check the municipal recycling rate against the official Eurostat rate for a few countries.
- [ ] Confirm the break in series in 2020 in the Eurostat metadata.
- [ ] Confirm with the reporters the packaging rates above 100 % (Slovenia, Poland).
- [ ] Find which packaging materials each of the 7 Member States postponed, and decide whether to add a `postponed_2025` flag to the lookups.

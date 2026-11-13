# To do

## Next: JSON files for the D3/React dashboard

- [ ] **Scatter plot of recycling rates**: create the JSON file with one point per country.
  - Sources: `data/interim/env_wasmun.parquet` (municipal waste recycling rate) and `data/interim/env_waspacr.parquet` (packaging recycling rates, 2023).
  - Use the same unit for all rates (%). The municipal rate is a share from 0 to 1 and the packaging rates are already in %.
  - Use the same year for both axes (packaging is 2023 only).
  - Decide whether `EU27_2020` is a point on the chart or a reference line.
- [ ] **Line chart of municipal waste per person over time**: create the JSON file with one line per country, 2010–2024.
  - Source: `data/interim/env_wasmun.parquet`, `municipal_waste_gen_pc` (kg per person).
  - Year as a whole number, not text.
  - Decide whether to include `EU27_2020` as a reference line.

## Open points (from dashboard_notes/method_notes.md)

- [ ] Decide whether the municipal recycling rate uses RCY, RCY_M + RCY_C_D, or RCY_M + RCY_C_D + PRP_REU.
- [ ] Check the municipal recycling rate against the official Eurostat rate for a few countries.
- [ ] Confirm the break in series in 2020 in the Eurostat metadata.

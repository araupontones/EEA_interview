# Method notes

Decisions taken when building the indicator tables, and what they mean for the analysis and the dashboard.
Last updated: 13 November 2026.

## 1. General decisions (all sources)

| Decision | Consequence |
|---|---|
| Data is downloaded from the Eurostat Statistics API for countries plus the EU-level totals of each dataset (always `EU27_2020`; some datasets also have EU28, euro area or EFTA totals), for 2010 to 2026 only. | No regional data. The EU27 figure is Eurostat's own total, so it does not need to be calculated, but totals must be removed before summing or averaging countries, or they are counted twice. Years before 2010 are not available without changing the download defaults in `src/apiEurostat/download_eurostat.py`. |
| Data is stored in layers: `data/raw` (downloads, never edited), `data/interim` (indicators from one source), `data/processed` (final country-year table for the dashboard, still to build). | Every figure in the dashboard can be traced back to one raw file. Each layer can be rebuilt by running its scripts. |
| Each raw download overwrites the previous one. `data/catalog/raw_sources.csv` records the Eurostat release date (`source_updated`) and download time. | Figures can change after a new download, because Eurostat revises past years. Check the catalog to see which release the dashboard uses. |
| Interim tables keep all geographies in the source: countries, including non-EU countries (e.g. IS, NO, CH, candidate countries), and the EU-level totals. | Filtering to EU27 countries is done later with `data/lookups/geo_EU27.json`, which contains only the 27 countries, not `EU27_2020`. |
| Missing values are kept as empty values, not filled or set to zero. | Gaps stay visible. Averages and totals must handle empty values explicitly. |
| The year column is still called `time` and stored as text in the interim tables. | It must be renamed to `year` and converted to a whole number before merging the sources. |

## 2. Municipal waste (env_wasmun)

Script: `scripts/interim/env_wasmun.py`. Output: `data/interim/env_wasmun.parquet`, one row per country and year, 2010 to 2024.

### Indicators

| Indicator | Definition | Unit |
|---|---|---|
| `municipal_waste_gen_pc` | Waste generated (GEN) | kg per person |
| `municipal_waste_gen_total` | Waste generated (GEN) | thousand tonnes |
| `municipal_waste_rcy_total` | Recycling (RCY) | thousand tonnes |
| `municipal_waste_rcy_rate` | Recycling / waste generated, both in thousand tonnes | share, 0 to 1 |

### Decisions and consequences

**Recycling is measured with the RCY code.**
RCY covers material recycling (RCY_M) and composting and digestion (RCY_C_D). It is not material recycling only.
- The rate is higher than a rate based on material recycling only, especially in countries that compost a large share of bio-waste.
- RCY sometimes also includes preparing for reuse (PRP_REU). Checked for EU27, 2020 to 2024 (allowing up to 3 thousand tonnes for rounding, as Eurostat publishes whole thousand tonnes):
  - 91 of 134 country-years: RCY = RCY_M + RCY_C_D.
  - 43 of 134 country-years: RCY = RCY_M + RCY_C_D + PRP_REU. This applies to AT, BE, FR and IE in every year, to DE in 2020 to 2022, and to BG, DK, EL, FI, LT, LV, SE and SK in some years. The number grows over time, from 6 countries in 2020 to 11 in 2024.
  - No other differences.
- Effect on the rate: including preparing for reuse adds a median of 0.5 percentage points, and at most 2.7 points (Latvia 2024). Small, but it means the rate is not calculated the same way for all countries and years, and a country's rate can rise only because it started including preparing for reuse (e.g. Latvia from 2023, Bulgaria in 2024).
- The rate is therefore close to, but not guaranteed to match, the official Eurostat municipal waste recycling rate. Compare a few countries with the official rate before publishing.

**The rate is calculated from tonnes, not from kg per person.**
Both give the same ratio. Tonnes are used because recycling per person is not needed.

**Recycling is joined with a left join.**
Country-years with waste generated but no recycling figure are kept, with an empty rate. 75 of 570 country-years have no rate.

**Waste per person and total waste are joined with an inner join.**
A country-year is dropped if one of the two is missing.

**The rate is a share (0 to 1), not a percentage.**
Multiply by 100 for display. The packaging rates (section 3) are already in %, so the two must be aligned before they appear side by side.

**Possible break in series.**
New calculation rules for the municipal waste targets apply from reference year 2020. Trends across 2020 should be read with care. Check the Eurostat metadata for countries with a break flag.

## 3. Packaging waste recycling rates (env_waspacr)

Script: `scripts/interim/env_waspacr.py`. Output: `data/interim/env_waspacr.parquet`, one row per country and packaging type, 2023 only.

### Decisions and consequences

**Only the rate under the 2025-target calculation method (`RT_TGT2025`) is used. The 2008-target method (`RT_T2008`) is dropped.**
- `RT_TGT2025` measures recycling where waste enters the final recycling operation, after sorting losses are removed (Directive (EU) 2018/852, Implementing Decision (EU) 2019/665). It is the only method that can be compared with the 2025 and 2030 targets (packaging overall 65% and 70%, plastic 50% and 55%).
- It is also the only series with full coverage: all countries, 2010 to 2024. `RT_T2008` has only 2 to 45 values a year, for a few countries.
- Where both exist, the new method usually gives lower rates: on average 7.4 percentage points lower for plastic, 4.3 points for paper and cardboard, and 1.9 points for glass. Using `RT_T2008` would make countries look closer to the targets than they are.
- The two methods are never mixed in one column.
- Values for 2010 to 2019 in `RT_TGT2025` were probably calculated under the old rules, since the new rules apply from reference year 2020. This is to be confirmed in the Eurostat metadata. If confirmed, trends from 2010 contain a break in 2020 and should start in 2020 or show the break.

**Only 2023 is kept.**
- The table gives a snapshot of where countries stand against the 2025 targets, not a trend.
- After merging with other sources, all years other than 2023 will have no packaging rates. Keep all years if trends are needed.

**All packaging types are kept, including the total (`Packaging`, W1501).**
- Aluminium and steel are parts of metallic packaging. Do not add them to metallic packaging, and do not add the packaging types up to the total.
- `Other packaging` is often 0.0. It should not be read as a recycling rate of 0%.

**The table is in long format (one row per country and packaging type).**
It must be turned into one column per packaging type (e.g. `packaging_rcy_rate_plastic`) before it can be merged into the country-year table.

**Missing rates are kept.**
36 of 270 rows have no rate in 2023. Bulgaria, Croatia, Hungary and Poland have no rates at all for 2023 under this method.

**Values are in %.**
Unlike the municipal waste rate, which is a share (0 to 1).

## 4. Open points

- Check `municipal_waste_rcy_rate` against the official Eurostat municipal waste recycling rate for a few countries.
- Confirm in the Eurostat metadata the break in series in 2020 for both sources.
- Decide one unit for all rates (% recommended).
- Decide whether packaging should keep all years, or only the latest year.

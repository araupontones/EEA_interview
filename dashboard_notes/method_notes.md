# Method notes

Decisions taken when building the indicator tables, and what they mean for the analysis and the dashboard.
Last updated: 14 November 2026.

## 1. General decisions (all sources)

| Decision | Consequence |
|---|---|
| Data is downloaded from the Eurostat Statistics API for countries plus the EU-level totals of each dataset (always `EU27_2020`; some datasets also have EU28, euro area or EFTA totals), for 2010 to 2026 only. | No regional data. The EU27 figure is Eurostat's own total, so it does not need to be calculated, but totals must be removed before summing or averaging countries, or they are counted twice. Years before 2010 are not available without changing the download defaults in `src/eurostat_api/download_eurostat.py`. |
| Data is stored in layers: `data/raw` (downloads, never edited), `data/interim` (indicators from one source), `data/processed` (final country-year table for the dashboard, still to build). | Every figure in the dashboard can be traced back to one raw file. Each layer can be rebuilt by running its scripts. |
| Each raw download overwrites the previous one. `data/catalog/raw_sources.csv` records the Eurostat release date (`source_updated`) and download time. | Figures can change after a new download, because Eurostat revises past years. Check the catalog to see which release the dashboard uses. |
| Interim tables keep all geographies in the source: countries, including non-EU countries (e.g. IS, NO, CH, candidate countries), and the EU-level totals. | Filtering to EU27 countries is done later with `data/lookups/geo_eu27.json`, which contains only the 27 countries, not `EU27_2020`. |
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
37 of 279 rows have no rate in 2023: 36 are empty in the source, and 1 (Cyprus, steel packaging) is set to empty by the data validation below. Bulgaria, Croatia, Hungary and Poland have no rates at all for 2023 under this method.

**Values are in %.**
Unlike the municipal waste rate, which is a share (0 to 1).

### Data validation

The data validation is at the end of `scripts/interim/env_waspacr.py` (function `validate`). Each correction is printed when the script runs.

**Cyprus, steel packaging: the rate is set to empty for the visualisation.**
- Eurostat reports a recycling rate of 221.5 % for Cyprus steel packaging in 2023. This is the published figure: it is also the figure used in the Commission's early warning assessment for Cyprus. It is not treated as an error. The rate has been above 190 % in every year since 2017, with a peak of 369.1 % in 2020 (2024: 230.4 %).
- The rate is set to empty so that it does not distort the charts: the dashboard shows recycling rates on a scale from 0 to 105 %, and a value of 221.5 % would not fit on it.
- The value is set to empty only while it is above 200 %. If Eurostat publishes a revised figure of 200 % or below, it is kept automatically.
- Consequence: Cyprus is not shown for steel packaging and has no distance to the steel packaging target in the dashboard. The published figure (221.5 %) should be mentioned in a note to the chart. The Cypriot rate for metallic packaging (105.8 %) is left as it is; it is above 100 % for the same reason, since steel is part of metallic packaging.

**Other rates above 100 % are kept, but should be read with care.**
In 2023, six other rates are above 100 %:

| Country | Packaging type | Rate 2023 (%) |
|---|---|---|
| CY | Metallic packaging | 105.8 |
| SI | Glass packaging | 112.0 |
| PL | Steel packaging | 101.7 |
| SI | Aluminium packaging | 101.0 |
| SI | Metallic packaging | 100.7 |
| SI | Steel packaging | 100.6 |

- Except for Cyprus metallic packaging (see above), these are close to 100 %. They can come from packaging waste brought in from other countries and recycled there, from timing differences between when packaging is placed on the market and when it is recycled, or from estimates in the data. They are not clearly errors, so they are not changed.
- They overstate the distance to target. Slovenia appears 42 percentage points above the glass target, and 51 points above the aluminium target.
- They should be flagged in the QC log and confirmed with the reporters (Slovenia, Poland).

## 4. Recycling targets

Script: `scripts/lookups/create_recycling_targets.py`. Output: `data/lookups/recycling_targets.json`, one record per waste category in the combined recycling table (`df_appended` in `scripts/processed/recycling_distance_to_target.py`).

### Targets and sources

Targets are recycling rates in %, in the same format as the data. Values checked against the legal texts.

| Waste category | 2025 | 2030 | Source |
|---|---|---|---|
| Municipal waste | 55 | 60 | Waste Framework Directive 2008/98/EC, Art. 11(2)(c) and (d), as amended by Directive (EU) 2018/851 (preparing for re-use and recycling) |
| Packaging (all) | 65 | 70 | Packaging and Packaging Waste Regulation (EU) 2025/40, Art. 52 |
| Plastic packaging | 50 | 55 | Regulation (EU) 2025/40, Art. 52 |
| Wooden packaging | 25 | 30 | Regulation (EU) 2025/40, Art. 52 |
| Steel packaging | 70 | 80 | Regulation (EU) 2025/40, Art. 52 (target for ferrous metals) |
| Aluminium packaging | 50 | 60 | Regulation (EU) 2025/40, Art. 52 |
| Glass packaging | 70 | 75 | Regulation (EU) 2025/40, Art. 52 |
| Paper and cardboard packaging | 75 | 85 | Regulation (EU) 2025/40, Art. 52 |
| Metallic packaging | none | none | No EU target (only ferrous metals and aluminium have targets) |
| Other packaging | none | none | No EU target |

Legal texts:
- Waste Framework Directive, consolidated text: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02008L0098-20240218
- Regulation (EU) 2025/40: https://eur-lex.europa.eu/eli/reg/2025/40/oj/eng

### Decisions and consequences

**Steel packaging is compared with the ferrous metals target.**
Eurostat reports steel packaging; the legal target is set for ferrous metals. They are treated as the same category.

**Metallic packaging and Other packaging are kept with empty targets.**
Every category in the data has a row in the lookup, so a merge on `waste_name` never drops data. These two categories cannot be assessed against a target.

**The packaging rates use the 2025-target calculation method (`RT_TGT2025`, section 3).**
This is the method the targets are measured against. The 2023 data shows the distance to the 2025 targets two years before the deadline, not whether the target was met.

### Member States that postponed the 2025 targets

The legislation lets Member States postpone the 2025 deadlines by up to five years, under conditions. A Member State that postpones the 2025 target is not in breach if it misses the target in 2025. A dashboard that compares every country with the 2025 target would therefore overstate the number of countries failing it.

**Municipal waste (Waste Framework Directive, Art. 11(3)).**
Only Member States that prepared for re-use and recycled less than 20 %, or landfilled more than 60 %, of their municipal waste in 2013 could postpone. They must still reach at least 50 % by 2025 and submit an implementation plan. 11 Member States fulfilled the conditions; 8 notified the Commission that they postpone the 2025 target:

| Code | Country |
|---|---|
| EL | Greece |
| HR | Croatia |
| LT | Lithuania |
| HU | Hungary |
| MT | Malta |
| PL | Poland |
| RO | Romania |
| SK | Slovakia |

**Packaging, material-specific targets (Directive 94/62/EC, Art. 6(6); continued in Regulation (EU) 2025/40).**
All 27 Member States could postpone. The deviation is limited to 15 percentage points from one target, or split between two targets. 7 Member States notified a postponement of the 2025 material-specific targets:

| Code | Country |
|---|---|
| CZ | Czechia |
| EL | Greece |
| HR | Croatia |
| LU | Luxembourg |
| MT | Malta |
| PT | Portugal |
| SE | Sweden |

The postponement applies to material-specific targets only, not to the target for all packaging (65 %). The source does not say which materials each Member State postponed.

In total 12 Member States postponed at least one target; Greece, Croatia and Malta postponed both.

Source for the lists: European Court of Auditors, Special Report 23/2025 "Municipal waste management", paragraph 31 and footnotes 11 and 12 (https://www.eca.europa.eu/ECAPublications/SR-2025-23/SR-2025-23_EN.pdf). The Commission's 2023 early warning report (COM(2023) 304) found 23 Member States at risk of missing at least one 2025 target, so not every Member State at risk used the option to postpone.

Consequences for the dashboard:
- For these countries, show the 2025 comparison with a note ("deadline postponed"), not as a failure.
- For municipal waste, these 8 countries can also be compared with their minimum of 50 % for 2025.
- For packaging, the material-level flag cannot be set until we know which materials each country postponed.

## 5. Open points

- Check `municipal_waste_rcy_rate` against the official Eurostat municipal waste recycling rate for a few countries.
- Confirm in the Eurostat metadata the break in series in 2020 for both sources.
- Decide whether packaging should keep all years, or only the latest year.
- Find which packaging materials each of the 7 Member States postponed (Commission notifications or implementation plans).
- Check in the legal texts the conditions for postponement (Waste Framework Directive Art. 11(3), Directive 94/62/EC Art. 6(6)) and whether postponements notified under Directive 94/62/EC carry over unchanged under Regulation (EU) 2025/40.
- Confirm with the reporters the packaging rates above 100 % (Slovenia glass, aluminium, steel and metallic, Poland steel), and decide whether to flag them in the dashboard.
- Decide whether to add a `postponed_2025` flag per country to the lookups, so the dashboard can mark these countries automatically.

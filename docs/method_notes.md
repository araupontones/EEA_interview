# Method notes

Decisions taken when building the indicator tables, and what they mean for the analysis and the dashboard.
Last updated: 15 November 2026.

## 1. General decisions (all sources)

| Decision | Consequence |
|---|---|
| Data is downloaded from the Eurostat Statistics API for countries plus the EU-level totals of each dataset (always `EU27_2020`; some datasets also have EU28, euro area or EFTA totals), for 2010 to 2026 only. | No regional data. The EU27 figure is Eurostat's own total, so it does not need to be calculated, but totals must be removed before summing or averaging countries, or they are counted twice. Years before 2010 are not available without changing the download defaults in `src/eurostat_api/download_eurostat.py`. |
| Data is stored in layers: `data/raw` (downloads, never edited), `data/interim` (indicators from one source), `data/processed` (final tables for the dashboard, one JSON file per topic: `recycling_distance_to_target.json`, `municipal_waste.json`, `municipal_waste_decoupling.json`). | Every figure in the dashboard can be traced back to one raw file. Each layer can be rebuilt by running its scripts. |
| Each raw download overwrites the previous one. `data/catalog/raw_sources.csv` records the Eurostat release date (`source_updated`) and download time. | Figures can change after a new download, because Eurostat revises past years. Check the catalog to see which release the dashboard uses. |
| Raw and interim tables keep all geographies in the source: countries, including non-EU countries (e.g. IS, NO, CH, candidate countries), and the EU-level and euro area totals. | Interim data can be reused for other comparisons (e.g. with non-EU countries) without downloading again. |
| Processed tables keep only the 27 EU Member States and the EU27 total (`EU27_2020`), with the same rule in every processed script (`keep_eu27()` in `src/geo`, based on `data/lookups/geo_eu27.json`). `run_pipeline.py` fails if a processed file has any other geography. | The dashboard shows only EU countries. The EU total always has the same code, `EU27_2020`, in all processed files; its display name is "EU27" in `geo_eu27.json`. Non-EU countries (AL, BA, CH, GE, IS, ME, MK, NO, RS, TR, XK) are not in the dashboard. |
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

**The rate is a share (0 to 1) in the interim data, and in % in the processed data.**
The interim table keeps the share. The processed scripts multiply it by 100 and round to one decimal (as in `recycling_distance_to_target.json`), so the dashboard always shows rates in % with one decimal, the same unit as the packaging rates (section 3).

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
37 of 279 rows have no rate in 2023: 36 are empty in the source, and 1 (Cyprus, steel packaging) is set to empty by the data validation below. Bulgaria, Czechia and Hungary have no rates at all for 2023 under this method.

**Values are in %.**
Unlike the interim municipal waste rate, which is a share (0 to 1) until the processed scripts convert it.

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

## 5. GDP per person (nama_10_pc)

Script: `scripts/interim/nama_10_pc.py`. Output: `data/interim/nama_10_pc.parquet`, one row per country and year, 2010 to 2025.

**Only real GDP per person is kept (`gdp_pc`).**
- `na_item` B1GQ (GDP at market prices), `unit` CLV20_EUR_HAB (chain linked volumes, euro per person at 2020 prices).
- Real GDP, not current prices: the change over time then shows growth of the economy, not inflation. In current prices, EU27 GDP per person rose by 60 % from 2010 to 2024; in real terms, by 19 %. Using current prices would overstate decoupling.
- All geographies are kept, including `EU27_2020` and the euro area totals (EA12 to EA21).
- The dataset was downloaded again on 14 November 2026. The earlier download had no EU-level totals.

## 6. Municipal waste decoupling

Script: `scripts/processed/municipal_waste_decoupling.py`. Output: `data/processed/municipal_waste_decoupling.json`, one record per country and year, 2010 to 2024.

**Decoupling is measured in real terms: waste per person against real GDP per person.**
- GDP is in chain linked volumes (euro at 2020 prices, section 5), so its change shows growth of the economy, not inflation. In current prices, GDP would grow much faster and decoupling would look stronger than it is.
- Both series are per person, so population growth does not affect the comparison.

### How decoupling is estimated

1. For each country, both series are turned into an index with the base year 2011 = 100:
   - `mw_pc_index = mw_pc / mw_pc in 2011 × 100`
   - `gdp_pc_index = gdp_pc / gdp_pc in 2011 × 100`
2. The two indices are compared in the same year (e.g. 2023). An index of 110 means 10 % higher than in 2011.
3. The result is classified as:

| Result | Condition | Meaning |
|---|---|---|
| Absolute decoupling | GDP index above 100 and waste index at or below 100 | The economy grew while waste per person stayed the same or fell. |
| Relative decoupling | Waste index above 100, but below the GDP index | Waste per person grew, but more slowly than the economy. |
| No decoupling | Waste index at or above the GDP index | Waste per person grew as fast as the economy, or faster. |

Indexing puts both series on one axis (no chart with two y-axes) and shows the change, not the level. The classification is not stored in the data yet; it can be calculated from the two index columns.

**The base year is 2011, not 2010.**
2011 is the first year with municipal waste data for all 27 EU countries: Denmark has no figure for 2010. With 2010 as the base, Denmark would have no index. The base year is set once (`BASE_YEAR`) in the script.

**Only country-years present in both sources are kept (inner join).**
- All 27 Member States and `EU27_2020` have both waste and GDP data, so no EU country is lost in the join.
- Non-EU countries are dropped (section 1).
- Missing values within a kept country-year stay empty.

### Breaks in series in waste per person

Several countries changed the definition of municipal waste after 2011, mostly to include waste from businesses that is similar to household waste (the definition in Directive (EU) 2018/851). Their waste per person jumps in the year of the change, although the amount of waste did not change. Across a break, the waste index does not measure decoupling.

The five EU countries whose definition widened to include waste from businesses:

| Country | Year | What changed (Eurostat country notes) | Effect | Before the break |
|---|---|---|---|---|
| Czechia | 2017 | Until 2016 only waste collected by municipalities was reported; from 2017 also waste from LoW chapter 20 from enterprises and waste from citizens collected outside the municipal system. | +44 % from 2016 to 2017 (339 to 489 kg; +45 % in total amounts) | 2016: waste index 105.9, GDP index 109.1, relative decoupling |
| Belgium | 2020 | Municipal waste reported as defined in Directive (EU) 2018/851 (household and similar waste from businesses). Not flagged as a break in the Eurostat data. | +75 % from 2019 to 2020 (416 to 729 kg) | 2019: waste index 91.4, GDP index 106.9, absolute decoupling |
| Austria | 2020 | Municipal waste from all sources other than households (commerce and industry) added. | +42 % from 2019 to 2020 (588 to 834 kg) | 2019: waste index 102.6, GDP index 105.4, relative decoupling |
| Luxembourg | 2016 | Definition newly based on LoW codes, so it includes more waste from non-household sources; before, municipal waste was the waste under the responsibility of the public sector. Eurostat gives +37 % in waste generated. | +34 % from 2015 to 2016 (607 to 815 kg) | 2015: waste index 91.1, GDP index 100.4, absolute decoupling |
| Slovakia | 2020 | New national definition of municipal waste, also covering waste from other sources (from the Waste Information System). Not flagged as a break in the Eurostat data. | +14 % from 2019 to 2020 | 2019: waste index 135.4, GDP index 121.9, no decoupling |

- Belgium, Austria, Czechia and Luxembourg show "no decoupling" only because of the change in definition: before it, all four were decoupled.
- Slovakia's waste per person was already rising faster than GDP before 2020 (+35 % from 2011 to 2019, against +22 % for GDP). The country notes give no change in method for those years, so for Slovakia the lack of decoupling is real, and the 2020 change makes it look larger.
- Other breaks and jumps, reviewed on 15 November 2026 (year-on-year change in waste per person; causes from the Eurostat annex "Country specific notes on municipal waste", section "Municipal waste generated"):

| Country | Year | Change | Cause (Eurostat annex) | Dashboard note |
|---|---|---|---|---|
| Estonia | 2014 | +22 % (293 to 357 kg) | Packaging waste included from 2014 (not until 2013); also more mixed municipal waste and more separate collection in bigger towns. Before the break (2013): waste index 97.3, GDP index 106.3. | Yes |
| Slovenia | 2013 | +14 % (362 to 414 kg) | Waste from special waste collectors included from 2013, not in earlier years. | Yes |
| Ireland | 2014 | no 2013 figure | Improved method to estimate unmanaged household waste. Ireland also has no figure for 2015. | Yes, in the Irish note |
| Romania | 2011 | +17 % | Nothing documented for 2011 (the annex mentions a change in method from 2010). | No |
| Finland | 2022, 2023 | +17 %, +10 % | Nothing documented. | No |
| Latvia | 2015 | +11 % | Nothing documented for waste generated. | No |
| Poland 2013 and 2014, Portugal 2015, Greece 2020, Sweden 2020 and 2024, France 2024, Ireland 2020 | | below 10 % (Poland -6 % and -8 %, Sweden 2024 +9 %, others under 5 %) | Break flags; small effect on the trend. | No |

  Country notes are written only where the annex documents the cause. The jumps without a documented cause stay without a note (open point, section 7).
- The EU27 total includes these changes: its waste per person rose from 505 to 521 kg in 2020, partly because of them. The EU27 rise since 2011 (+2.8 %) therefore overstates the real rise in waste, and decoupling in the EU is probably stronger than the index shows.

**These notes are shown in the dashboard.** `scripts/lookups/create_decoupling_notes.py` writes `data/lookups/decoupling_notes.json`: a general note on how to read the chart, and a note for the EU27, Czechia, Belgium, Austria, Slovakia, Luxembourg, Estonia, Slovenia and Ireland, with the break year where there is one (all except the EU27). The dashboard shows the note of the selected country under the chart and marks the break year with a vertical line. When this section changes, update the texts in that script.

**The breaks are explained under the decoupling chart, not under the municipal waste bar chart.** The decoupling chart compares years, so a break changes what it shows; the bar chart compares countries in one year (2023), so it has no note on breaks. `create_decoupling_notes.py` also writes a `break_note`, shown under the decoupling chart when the EU27 is selected (the EU27 total includes these changes; a selected country has its own note): Luxembourg (from 2016), Czechia (from 2017) and Belgium, Austria and Slovakia (from 2020) widened their definition, which raised their waste per person by 14 % to 75 % in the year of the change. The list of countries is `DEFINITION_CHANGES` in that script; their break years come from the country notes.

Sources: Eurostat metadata for env_wasmun (https://ec.europa.eu/eurostat/cache/metadata/en/env_wasmun_esms.htm) and its annex "Country specific notes on municipal waste"; break flags (`b`) from the Eurostat API. The flags are not kept in our raw download.

**Results (2011 to 2023 unless stated).**
- EU27: from 2011 to 2024, waste per person rose by 2.8 % and real GDP per person by 16.8 % (relative decoupling).
- In 2023, 13 EU countries show absolute decoupling, 9 relative decoupling, and 5 no decoupling: Austria, Belgium, Czechia, Luxembourg and Slovakia. For all of these except Slovakia, the result comes from a change in definition (see above), so they should not be presented as not decoupled without a note.

## 7. Open points

The single list of open data questions. Each item points to the section that explains it. When a decision leads to work (a script, a flag, a chart change), add that task to [todo.md](todo.md), and remove the item here once it is decided and recorded in its section.

Municipal waste (section 2, section 6):
- [ ] Decide whether the municipal recycling rate uses RCY, RCY_M + RCY_C_D, or RCY_M + RCY_C_D + PRP_REU (section 2).
- [ ] Check the municipal recycling rate against the official Eurostat rate for a few countries (section 2).
- [ ] Confirm in the Eurostat metadata the break in series in 2020, for municipal waste and packaging (sections 2 and 3).
- [ ] Ask the reporters about the jumps in waste per person without a documented cause: Romania 2011 (+17 %), Finland 2022 and 2023 (+17 %, +10 %), Latvia 2015 (+11 %) (section 6).

Packaging (section 3):
- [ ] Decide whether packaging keeps all years, or only the latest year.
- [ ] Confirm with the reporters the rates above 100 % (Slovenia glass, aluminium, steel and metallic; Poland steel), and decide whether to flag them in the dashboard.

Targets and postponements (section 4):
- [ ] Find which packaging materials each of the 7 Member States postponed (Commission notifications or implementation plans).
- [ ] Check in the legal texts the conditions for postponement (Waste Framework Directive Art. 11(3), Directive 94/62/EC Art. 6(6)), and whether postponements notified under Directive 94/62/EC carry over unchanged under Regulation (EU) 2025/40.
- [ ] Decide whether to add a `postponed_2025` flag per country to the lookups, so the dashboard can mark these countries automatically.

Data download (section 1):
- [ ] Consider keeping the Eurostat flags (`b` break, `e` estimate, `p` provisional) in the raw download, so breaks can be found in the data rather than in the metadata.

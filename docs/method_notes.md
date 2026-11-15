# Method notes

Decisions taken when building the indicator tables, and what they mean for the analysis and the dashboard.
Last updated: 15 November 2026.

## 1. General decisions (all sources)

| Decision | Consequence |
|---|---|
| Data is downloaded from the Eurostat Statistics API for countries plus the EU-level totals of each dataset (always `EU27_2020`; some datasets also have EU28, euro area or EFTA totals), for 2010 to 2026 only. | No regional data. The EU27 figure is Eurostat's own total, so it does not need to be calculated, but totals must be removed before summing or averaging countries, or they are counted twice. Years before 2010 are not available without changing the download defaults in `src/eurostat_api/download_eurostat.py`. |
| Data is stored in layers: `data/raw` (downloads, never edited), `data/interim` (indicators from one source), `data/processed` (final tables for the dashboard, one JSON file per topic: `recycling_distance_to_target.json`, `municipal_waste.json`, `municipal_waste_decoupling.json`, `municipal_waste_treatment.json`). | Every figure in the dashboard can be traced back to one raw file. Each layer can be rebuilt by running its scripts. |
| Each raw download overwrites the previous one. `data/catalog/raw_sources.csv` records the Eurostat release date (`source_updated`) and download time. | Figures can change after a new download, because Eurostat revises past years. Check the catalog to see which release the dashboard uses. |
| Raw and interim tables keep all geographies in the source: countries, including non-EU countries (e.g. IS, NO, CH, candidate countries), and the EU-level and euro area totals. | Interim data can be reused for other comparisons (e.g. with non-EU countries) without downloading again. |
| Processed tables keep only the 27 EU Member States and the EU27 total (`EU27_2020`), with the same rule in every processed script (`keep_eu27()` in `src/geo`, based on `data/lookups/geo_eu27.json`). `run_pipeline.py` fails if a processed file has any other geography. | The dashboard shows only EU countries. The EU total always has the same code, `EU27_2020`, in all processed files; its display name is "EU27" in `geo_eu27.json`. Non-EU countries (AL, BA, CH, GE, IS, ME, MK, NO, RS, TR, XK) are not in the dashboard. |
| Missing values are kept as empty values, not filled or set to zero. | Gaps stay visible. Averages and totals must handle empty values explicitly. |
| The year column is still called `time` and stored as text in the interim tables. | It must be renamed to `year` and converted to a whole number before merging the sources. |

## 2. Municipal waste (env_wasmun)

Script: `scripts/interim/env_wasmun.py`. Output: `data/interim/env_wasmun.parquet`, one row per country and year, 2010 to 2024.

### Definition of municipal waste

Waste Framework Directive (2008/98/EC), Art. 3(2b), inserted by Directive (EU) 2018/851 (https://eur-lex.europa.eu/eli/dir/2018/851/oj):

> "'municipal waste' means: (a) mixed waste and separately collected waste from households, including paper and cardboard, glass, metals, plastics, bio-waste, wood, textiles, packaging, waste electrical and electronic equipment, waste batteries and accumulators, and bulky waste, including mattresses and furniture; (b) mixed waste and separately collected waste from other sources, where such waste is similar in nature and composition to waste from households; Municipal waste does not include waste from production, agriculture, forestry, fishing, septic tanks and sewage network and treatment, including sewage sludge, end-of-life vehicles or construction and demolition waste. This definition is without prejudice to the allocation of responsibilities for waste management between public and private actors"

Recital 10 of Directive (EU) 2018/851 gives examples of the "other sources": "retail, administration, education, health services, accommodation and food services, and other services and activities", and adds that "Member States are to ensure that waste from large commerce and industry which is not similar to waste from households is not included in the scope of municipal waste".

Eurostat env_wasmun metadata (https://ec.europa.eu/eurostat/cache/metadata/en/env_wasmun_esms.htm, last update 31 March 2026):
- Section 3.4: "The definition of municipal waste is regulated in article 3 (2b) and in recital 10 the Directive (EU) 2018/851 amending Directive 2008/98/EC on waste." and "This definition is not completely identical with the definition used before the Directive (EU) 2018/851 taking effect. Therefore between 2019 and 2022 several countries adapted there data collection system to the new definition. In cases where this lead to breaks in series, these are marked with the footnote 'b'." (The text that follows in section 3.4, "household and similar waste collected by or on behalf of municipal authorities", is the old definition, given for comparison.)
- Section 6.1: "From reference year 2020 on municipal waste generation and recyling are covered by the Directive (EU) 2018/851".
- Section 15.1 (geographical comparability): "The concept of municipal waste includes different waste streams in different municipalities. Especially, the extent to which waste generated by offices and small businesses are included differs from municipality to municipality. Thus, different levels of municipal waste generation can reflect different coverage of the generation of waste, but also differences in the organisation of municipal waste management."

Consequence: the metadata does not state that all Member States now apply the definition in the same way, so levels in one year are not fully comparable between countries (findings, section 1). The countries that widened their definition after 2011 are listed in section 6 ("Breaks in series in waste per person").

**Ratio between the highest and lowest waste per person.** Computed for 2023 among the Member States with no `break_year` in `data/lookups/decoupling_notes.json` (19 of 27; leaves out CZ, BE, AT, SK, LU, EE, SI, IE): Denmark 759 kg / Romania 305 kg = 2.5. Across all 27 the ratio is 2.6 (Austria / Romania), but Austria's level includes its 2020 widening of the definition. Romania (undocumented +17 % jump in 2011, no break year) stays in. The dashboard computes the ratio the same way from the data.

### Indicators

| Indicator | Definition | Unit |
|---|---|---|
| `municipal_waste_gen_pc` | Waste generated (GEN) | kg per person |
| `municipal_waste_gen_total` | Waste generated (GEN) | thousand tonnes |
| `municipal_waste_rcy_total` | Recycling (RCY) | thousand tonnes |
| `municipal_waste_rcy_rate` | Recycling / waste generated, both in thousand tonnes | share, 0 to 1 |
| `municipal_waste_trt_total` | Waste treatment, all operations (TRT) | thousand tonnes |
| `municipal_waste_prp_reu_total` | Preparing for re-use (PRP_REU) | thousand tonnes |
| `municipal_waste_rcy_m_total` | Recycling, material (RCY_M) | thousand tonnes |
| `municipal_waste_rcy_c_d_total` | Recycling, composting and digestion (RCY_C_D) | thousand tonnes |
| `municipal_waste_rcv_e_total` | Energy recovery, incineration with energy recovery (RCV_E, R1) | thousand tonnes |
| `municipal_waste_dsp_i_total` | Incineration without energy recovery (DSP_I, D10) | thousand tonnes |
| `municipal_waste_dsp_l_total` | Landfill and other disposal (DSP_L_OTH, D1-D7, D12) | thousand tonnes |
| `municipal_waste_eu27_estimated` | True where an EU27 treatment value was estimated by the data validation | true / false |

`DSP_I_RCV_E` (all incineration) is not kept: it equals `RCV_E` + `DSP_I` in every EU country-year (checked, 2010 to 2024).

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
Country-years with waste generated but no recycling figure are kept, with an empty rate. In the interim table (`env_wasmun.parquet`: 39 geographies, i.e. 38 countries and the EU27, 2010 to 2024; one row per geography and year, 585 rows), 550 country-years have waste generated, and 40 of them have no recycling rate. All 40 are outside the EU: Türkiye and North Macedonia (9 each), Montenegro and Albania (7 each), Bosnia and Herzegovina and Kosovo (4 each). The EU27 and the 27 Member States have a rate in every year with waste generated.

**Waste per person and total waste are joined with an inner join.**
A country-year is dropped if one of the two is missing.

**The rate is a share (0 to 1) in the interim data, and in % in the processed data.**
The interim table keeps the share. The processed scripts multiply it by 100 and round to one decimal (as in `recycling_distance_to_target.json`), so the dashboard always shows rates in % with one decimal, the same unit as the packaging rates (section 3).

**Possible break in series.**
New calculation rules for the municipal waste targets apply from reference year 2020. Trends across 2020 should be read with care. Check the Eurostat metadata for countries with a break flag.

### Treatment across the waste hierarchy

Processed script: `scripts/processed/municipal_waste_treatment.py`. Output: `data/processed/municipal_waste_treatment.json`, one record per country and year, 2010 to 2024 (EU27 and 27 Member States; 416 records, as country-years without waste generated are dropped).

**How each operation maps to a step of the waste hierarchy** (Waste Framework Directive 2008/98/EC, Art. 4):

| Hierarchy step | Eurostat operations | Column(s) |
|---|---|---|
| 1. Prevention | None: prevented waste is not generated, so it has no share. Waste per person (`municipal_waste.json`) is the indicator used to track prevention over time (WFD Art. 9(3); Eurostat cei_pc031; EEA 2025, see findings §1): it measures the result of prevention, not prevention itself, and levels between countries are not a ranking of prevention effort. | none |
| 2. Preparing for re-use | `PRP_REU` (checking, cleaning or repairing) | `prep_reuse_pct` |
| 3. Recycling | `RCY_M` (material recycling) + `RCY_C_D` (composting and digestion) | `recycling_material_pct`, `recycling_compost_pct`, `recycling_pct` (sum) |
| 4. Other recovery | `RCV_E` (incineration with energy recovery, R1) | `energy_recovery_pct` |
| 5. Disposal | `DSP_I` (incineration without energy recovery, D10) + `DSP_L_OTH` (landfill and other disposal, D1-D7, D12) | `incineration_pct`, `landfill_pct`, `disposal_pct` (sum) |

Composting and digestion count as recycling, as in the Waste Framework Directive and in Eurostat's recycling category. Backfilling, the other "other recovery" operation, is not reported for municipal waste.

**Shares are of waste generated, not of waste treated.**
- Every share is the operation divided by municipal waste generated (`GEN`), both in thousand tonnes, in % with one decimal.
- Why: the recycling rate in the dashboard, the official Eurostat rates, the municipal recycling target (Waste Framework Directive, Art. 11(2)) and the 2035 landfill target (at most 10 % of municipal waste generated, Landfill Directive 1999/31/EC, Art. 5(5), as amended by Directive (EU) 2018/850) are all shares of waste generated. With the same denominator, the recycling step of the ladder matches the recycling chart (except for preparing for re-use, below), and the landfill step can be read against the landfill target. Shares of waste treated would always add up to 100 %, but they would raise every share in the countries where much of the waste generated is not in the treatment figures (Bulgaria, Poland, Cyprus), and would not match the recycling rate.
- Consequence: the shares do not always add up to 100 %. The remainder is kept in its own column, `unaccounted_pct` = 100 - (preparing for re-use + recycling + other recovery + disposal), so it stays visible instead of being spread over the operations. `treated_pct` gives all waste treated (`TRT`) as a share of generated.
- `landfill_pct` is the landfill share as reported in env_wasmun. It is not calculated with the specific rules of the landfill target (e.g. for residues of other treatments sent to landfill), so it is close to, but not the same as, a landfill target rate.

**Preparing for re-use is never counted twice.**
- Recycling is built from `RCY_M` + `RCY_C_D`, never from `RCY`, because `RCY` includes `PRP_REU` for some countries and years (see "Recycling is measured with the RCY code" above). Preparing for re-use is its own column.
- Consequence: `recycling_pct` is up to 2.5 points lower than the recycling rate in `recycling_distance_to_target.json` for the countries whose `RCY` includes preparing for re-use (EU27 2023: 47.7 % against 47.9 %). `prep_reuse_pct` + `recycling_pct` is the closest to the municipal target measure (preparing for re-use and recycling).
- Where `PRP_REU` is reported but `RCY` = `RCY_M` + `RCY_C_D` (e.g. Cyprus, Malta, Slovenia in 2023), the data cannot show whether preparing for re-use is inside `RCY_M`. The amounts are at most 2 thousand tonnes, so the effect is negligible.
- How the official sources define it: Eurostat's cei_wm011 uses `RCY`, and its metadata says that since Implementing Decision (EU) 2019/1004 "preparing for re-use is also included in recycling" (cei_wm011 metadata, section 4.1); the dataset description still lists only material recycling, composting and anaerobic digestion. The EEA's indicator "Waste recycling in Europe" defines municipal recycling as "material recycling and composting/anaerobic digestion" (source env_wasmun), with no mention of preparing for re-use. The municipal target (WFD Art. 11(2)(c)) covers preparing for re-use and recycling together.
- Decision (15 November 2026): the hierarchy chart follows the EEA definition (`recycling_pct` = `RCY_M` + `RCY_C_D`, EU 2023 47.7 %, the EEA's published figure). The targets chart follows cei_wm011 (`municipal_waste_rcy_rate` = `RCY` / `GEN`, EU 2023 47.9 %, checked against the Eurostat values), the closest published measure to the target. Consequence: the gap between the two charts is preparing for re-use only (0.2 points for the EU in 2023); the 5.0 % "not in the figures" share includes the small amount prepared for re-use, as it has no EU figure.

**Preparing for re-use is missing for the EU27 and for 8 Member States.**
- The category was added in 2019; before, it was part of recycling (env_wasmun metadata, section 3.4). Most countries report it from 2020; France from 2016.
- Eurostat publishes no EU27 total for it, so `prep_reuse_pct` is empty for the EU27 in every year. It is not calculated from the countries, because 8 Member States do not report it in 2023: Germany, Estonia, Spain, Croatia, Italy, the Netherlands, Poland and Portugal.
- The 19 Member States that report it prepared 476 thousand tonnes for re-use in 2023, 0.2 % of EU27 waste generated. The highest shares are Latvia (2.5 %) and Belgium (1.4 %).
- Where it is missing, `unaccounted_pct` may include it.

**Why treatment differs from generation.**
The env_wasmun metadata (section 15.4) lists: estimates for the population not covered by collection, weight losses (e.g. by drying), waste going through two or more treatment steps (double counts), exports and imports, and time lags between generation and treatment (temporary storage). From 2020, recycling is also measured under the new calculation rules (Directive (EU) 2018/851), which leave out sorting losses. The data does not show which of these applies to each country.

In 2023 (`unaccounted_pct`):
- Within 1 point of zero in 12 Member States.
- More than 10 % of waste generated is in no operation in 7: Bulgaria (35.9 %), Poland (21.5 %), Cyprus (20.4 %), Estonia (18.9 %), Slovenia (17.5 %), Italy (14.1 %) and Croatia (10.6 %).
- Negative in Portugal (-5.4 %): more waste treated than generated, in every year since 2020.
- EU27: 5.0 %, against 2.0 % to 3.2 % from 2011 to 2022. Most of the rise from 2022 (+4.8 million tonnes not accounted for) comes from Poland (+2.9 million tonnes), Italy (+1.1) and Bulgaria (+0.5).

**Breaks in series in the treatment shares.**
- **Poland, 2023**: waste generated stayed the same (13.4 million tonnes), but waste treated fell from 13.4 to 10.6 million tonnes and recycling (`RCY`) from 5.5 to 3.7 million tonnes. Poland's recycling rate fell from 40.9 % (2022) to 27.6 % (2023), and 21.5 % of its waste generated is in no operation, against 0 % in every earlier year.
  - **Cause: a change in method, documented by Eurostat.** The env_wasmun annex "Country specific notes on municipal waste" (version of 1 April 2026), Poland, sections "General" and "Municipal waste treatment": "Until 2022, municipal waste treatment data was partially estimated. From 2023, the data on municipal waste management processes are reported in the M-09 directly by companies, excluding the estimate. The change in the methodology for calculating recycling rate caused a difference between waste generation and treatment of 20%." Section "Municipal waste recycled": "The change in the methodology for calculating recycling rate caused a drop in municipal waste recycling by 41% in 2023." (https://ec.europa.eu/eurostat/cache/metadata/Annexes/env_wasmun_esms_an_Country_specific_notes_on_MW.docx). So the fall reflects the end of the estimates, not a change in waste management; 2023 is not comparable with earlier years.
  - **Flags** (Eurostat API, env_wasmun, geo=PL, unit=THS_T, data updated 15 October 2026): 2023 is flagged `b` (break in time series) for waste treated (`TRT`), recycling (`RCY`, `RCY_M`, `RCY_C_D`) and landfill (`DSP_L_OTH`). Waste generated (`GEN`), energy recovery (`RCV_E`) and incineration without energy recovery (`DSP_I`) are not flagged. No value for 2021 to 2024 is flagged as estimated (`e`) or provisional (`p`). Our raw download does not keep the flags.
  - Statistics Poland gives the same 2023 amounts (recycling 2.1 million tonnes, composting or digestion 1.6 million tonnes, landfill 4.1 million tonnes; GUS, "Ochrona środowiska 2024", chapter on waste), but no note on the change in method was found there.
  - Consequences: Poland's recycling rate in the distance-to-target chart (27.6 % in 2023) cannot be compared with its earlier rates, and the EU27 totals for treatment and recycling include the break. In 2024 (no flag), Poland's waste treated is 11.8 million tonnes for 14.2 million tonnes generated, so the gap remains under the new method.
- **Bulgaria, from 2020**: the share not accounted for moves between -7 % and 40 % from year to year (0.1 % to 0.3 % before 2020), and landfill swings (1,903, 892 and 1,695 thousand tonnes in 2020, 2021 and 2022). Bulgaria's shares should be read with care.
- Other year-on-year changes of 10 points or more in a share, mostly before 2017: Estonia 2012 to 2014, Latvia 2011 and 2019, Lithuania 2011 and 2016, Malta 2015 and 2016, Slovenia 2011 to 2016. The 2020 change in calculation rules (section 2 above) and the changes in the definition of municipal waste (section 6) also apply.
- The EU27 series changes gradually: from 2011 to 2024, no share moves by more than 2.4 points from one year to the next (disposal as a whole: at most 3.2 points, in 2012), and all the larger moves (2012 to 2017) follow the long-term trend: less landfill and incineration without energy recovery, more recycling and energy recovery. The exception is the share not accounted for in 2023 (+2.1 points, mostly Poland's change in method, above).

**Latvia 2023: incineration without energy recovery and landfill are missing**, so Latvia has no disposal share and no remainder in 2023. Eurostat therefore publishes no EU27 total for these two operations in 2023. The interim data validation estimates them (below), and `estimated` is true for the EU27 in 2023.

### Data validation

The data validation is at the end of `scripts/interim/env_wasmun.py` (function `validate`). Each estimate is printed when the script runs.

**EU27 totals missing for a treatment operation are estimated as the sum of the Member States.**
- Eurostat publishes no EU27 total for an operation in a year when a Member State has no figure. In the current release this is the case in 2023 for incineration without energy recovery (`DSP_I`) and landfill (`DSP_L_OTH`), because Latvia has none.
- The missing EU27 value is estimated as the sum of the 27 Member States, with each missing Member State at its previous-year value. This is how Eurostat estimates missing countries in its EU aggregates (env_wasmun metadata, section 18.5). In years with all Member States, the sum of the countries matches the published EU27 total within 3 thousand tonnes.
- 2023 estimates: landfill 49,235 thousand tonnes (Latvia at its 2022 value, 380), incineration without energy recovery 1,116 thousand tonnes (Latvia at 0).
- Effect: small. Latvia's waste treated minus its recycling and energy recovery in 2023 is 305 thousand tonnes, 75 less than the 2022 value used; the difference changes the EU27 landfill share by less than 0.1 point.
- The rule only fills an empty EU27 value, so it stops applying when Eurostat publishes one. It is not applied to preparing for re-use (see above). The Latvian rows stay empty.

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
- **Decision (15 November 2026): the distance-to-target chart does not mark the countries that postponed a target.** All countries are drawn the same way against the 2025 target, and there is no `postponed_2025` flag in the lookups. Hollow circles for the 8 Member States that postponed the municipal waste target were considered and rejected by the user.
- Consequence: in the chart, these countries look as if they miss the 2025 target, although a postponed deadline is legal. Texts about the chart must not call them failing: where a text speaks of countries below the 2025 target, it should say that some postponed the deadline (findings, section 3).
- For municipal waste, these 8 countries must still reach at least 50 % by 2025.
- For packaging, we do not know which materials each country postponed.

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
| Slovakia | 2020 | New national definition of municipal waste, also covering waste from other sources (from the Waste Information System). Not flagged as a break in the Eurostat data. | +14 % from 2019 to 2020 (421 to 478 kg) | 2019: waste index 135.4, GDP index 121.9, no decoupling |

- Belgium, Austria, Czechia and Luxembourg show "no decoupling" only because of the change in definition: before it, all four were decoupled.
- Slovakia's waste per person was already rising faster than GDP before 2020 (+35 % from 2011 to 2019, against +22 % for GDP). The country notes give no change in method for those years, so for Slovakia the lack of decoupling is real, and the 2020 change makes it look larger.
- Other breaks and jumps, reviewed on 15 November 2026 (year-on-year change in waste per person; causes from the Eurostat annex "Country specific notes on municipal waste", section "Municipal waste generated"):

| Country | Year | Change | Cause (Eurostat annex) | Dashboard note |
|---|---|---|---|---|
| Estonia | 2014 | +22 % (293 to 357 kg) | Packaging waste included from 2014 (not until 2013); also more mixed municipal waste and more separate collection in bigger towns. Before the break (2013): waste index 97.3, GDP index 106.3. | Yes |
| Slovenia | 2013 | +14 % (362 to 414 kg) | Waste from special waste collectors included from 2013, not in earlier years. Before the break (2012): waste index 87.2, GDP index 96.9 (both fell, so no decoupling class applies). | Yes |
| Ireland | 2014 | no 2013 figure | "The break in time series for 2014 (Generation) data is because of an improved methodology for estimating unmanaged household waste." Ireland also has no figure for 2015; the annex does not explain the missing years. 2012: 585 kg, 2014: 562 kg. | Yes, in the Irish note |
| Romania | 2011 | +17 % | Nothing documented for 2011 (the annex mentions a change in method from 2010). | No |
| Finland | 2022, 2023 | +17 %, +10 % | Nothing documented. | No |
| Latvia | 2015 | +11 % | Nothing documented for waste generated. | No |
| Poland 2013 and 2014, Portugal 2015, Greece 2020, Sweden 2020 and 2024, France 2024, Ireland 2020 | | below 10 % (Poland -6 % and -8 %, Sweden 2024 +9 %, others under 5 %) | Break flags; small effect on the trend. | No |

  Country notes are written only where the annex documents the cause. The jumps without a documented cause stay without a note (open point, section 7).
- The EU27 total includes these changes: its waste per person rose from 505 to 521 kg in 2020, partly because of them. The EU27 rise since 2011 (+2.8 %) therefore overstates the real rise in waste, and decoupling in the EU is probably stronger than the index shows.

**These notes are shown in the dashboard.** `scripts/lookups/create_decoupling_notes.py` writes `data/lookups/decoupling_notes.json`: a general note on how to read the chart, and a note for the EU27, Czechia, Belgium, Austria, Slovakia, Luxembourg, Estonia, Slovenia and Ireland, with the break year where there is one (all except the EU27). The dashboard shows the note of the selected country under the chart and marks the break year with a vertical line. When this section changes, update the texts in that script.

**The breaks are explained under the decoupling chart, not under the municipal waste bar chart.** The decoupling chart compares years, so a break changes what it shows; the bar chart compares countries in one year (2023), so it has no note on breaks. `create_decoupling_notes.py` also writes a `break_note`, shown under the decoupling chart when the EU27 is selected (the EU27 total includes these changes; a selected country has its own note): Luxembourg (from 2016), Czechia (from 2017) and Belgium, Austria and Slovakia (from 2020) widened their definition, which raised their waste per person by 14 % to 75 % in the year of the change. The list of countries is `DEFINITION_CHANGES` in that script; their break years come from the country notes.

Sources: Eurostat metadata for env_wasmun (https://ec.europa.eu/eurostat/cache/metadata/en/env_wasmun_esms.htm) and its annex "Country specific notes on municipal waste"; break flags (`b`) from the Eurostat API. The flags are not kept in our raw download.

**Irish GDP per person overstates the Irish economy.** Ireland's real GDP per person rose by 23.5 % from 2014 to 2015 (EU27: +2.2 %) and its GDP index reaches 197 in 2023 (EU27: 116). The CSO attributes the 2015 jump to multinational companies relocating their balance sheets, mostly intellectual property, to Ireland (https://www.cso.ie/en/methods/nationalaccounts/din/nie2017faq/). Ireland's decoupling therefore looks stronger than it is; the waste index is not affected. The CSO publishes modified GNI (GNI*), "GNI less the impact of re-domiciled companies and the depreciation of categories of foreign-owned domestic capital assets" such as intellectual property, as an indicator that "excludes globalisation effects". GNI* exists only for Ireland, so it cannot replace GDP in a comparison of all Member States; we keep real GDP per person for all countries and explain the issue in the Irish note.

**Results (2011 to 2023 unless stated).**
- EU27: from 2011 to 2024, waste per person rose by 2.8 % and real GDP per person by 16.8 % (relative decoupling).
- In 2023, 13 EU countries show absolute decoupling, 9 relative decoupling, and 5 no decoupling: Austria, Belgium, Czechia, Luxembourg and Slovakia. For all of these except Slovakia, the result comes from a change in definition (see above), so they should not be presented as not decoupled without a note.

## 7. Open points

The single list of open data questions. Each item points to the section that explains it. When a decision leads to work (a script, a flag, a chart change), add that task to [todo.md](todo.md), and remove the item here once it is decided and recorded in its section.

Municipal waste (section 2, section 6):
- [ ] Confirm in the Eurostat metadata the break in series in 2020, for municipal waste and packaging (sections 2 and 3).
- [ ] Ask the reporters about the jumps in waste per person without a documented cause: Romania 2011 (+17 %), Finland 2022 and 2023 (+17 %, +10 %), Latvia 2015 (+11 %) (section 6).
- [ ] Ask about the gaps between waste generated and waste treated above 10 % in 2023 (Bulgaria, Cyprus, Estonia, Slovenia, Italy, Croatia; Poland's gap is explained by the 2023 change in method) and Bulgaria's unstable treatment series since 2020 (section 2, treatment).

Packaging (section 3):
- [ ] Decide whether packaging keeps all years, or only the latest year.
- [ ] Confirm with the reporters the rates above 100 % (Slovenia glass, aluminium, steel and metallic; Poland steel), and decide whether to flag them in the dashboard.

Targets and postponements (section 4):
- [ ] Find which packaging materials each of the 7 Member States postponed (Commission notifications or implementation plans).
- [ ] Check in the legal texts the conditions for postponement (Waste Framework Directive Art. 11(3), Directive 94/62/EC Art. 6(6)), and whether postponements notified under Directive 94/62/EC carry over unchanged under Regulation (EU) 2025/40.

Data download (section 1):
- [ ] Consider keeping the Eurostat flags (`b` break, `e` estimate, `p` provisional) in the raw download, so breaks can be found in the data rather than in the metadata.

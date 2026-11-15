# Findings

The most relevant findings of the analysis so far: municipal waste per person, decoupling from economic growth, and the distance to the 2025 recycling targets. Figures are for 2023 (the latest year with data for all 27 Member States) unless stated, from the Eurostat release in `data/catalog/raw_sources.csv`. How each figure is built, and its limits, is in [method_notes.md](method_notes.md).

Last updated: 15 November 2026. Update this file when the data or the method changes.

## 1. Municipal waste per person

- **The EU generates about 510 kg of municipal waste per person** (2023; 513 kg in 2024). The level has hardly changed since 2011 (499 kg): +2.2 % in 13 years. In total, about 229 million tonnes in 2023.
- **Large differences between countries.** Austria (782 kg), Denmark (759 kg) and Luxembourg (718 kg) generate around 2.5 times as much per person as Romania (305 kg), Poland (367 kg) and Estonia (373 kg). The median Member State is at 489 kg; 12 Member States are above the EU figure.
- **Since 2011, waste per person fell in 13 Member States and rose in 14.** The largest falls are in the Netherlands (-18 %), Sweden (-14 %) and Denmark (-12 %).
- **The largest rises come from changes in definition, not from more waste.** Czechia (+68 %), Slovakia (+52 %), Belgium (+51 %) and Austria (+37 %) widened their definition of municipal waste (Czechia in 2017, the others in 2020) to include similar waste from businesses. Only Slovakia was already rising before the change. Comparisons over time for these countries need a note.
- **Luxembourg also widened its definition, in 2016.** Its waste per person jumped by 34 % in one year (607 to 815 kg) when it started to define municipal waste by waste codes, including more waste from sources other than households. Its net rise since 2011 is only +7.8 %, because waste per person was falling before the change.
- **Two more countries count more waste because of a change in what is included.** Estonia added packaging waste in 2014 (+22 % in one year) and Slovenia added waste from special waste collectors in 2013 (+14 %). Their rises since 2011 (+24 % and +25 %) are partly due to these changes.
- **Three large jumps have no documented cause**: Romania 2011 (+17 %), Finland 2022 (+17 %, then +10 % in 2023) and Latvia 2015 (+11 %). They should be checked with the reporters before they are read as real changes.
- **The EU figure includes the same changes.** EU waste per person rose from 505 to 521 kg in 2020 and peaked at 534 kg in 2021, partly because of the new definitions. The real rise since 2011 is probably smaller than the +2.2 % shown.

## 2. Decoupling from economic growth

Waste per person compared with real GDP per person, both indexed to 2011 = 100.

- **In the EU, waste per person is decoupled from economic growth in relative terms.** From 2011 to 2023, real GDP per person rose by 15.6 % and waste per person by 2.2 % (2024: +16.8 % and +2.8 %). Because of the breaks in series, decoupling in the EU is probably stronger than the index shows.
- **13 Member States show absolute decoupling**: the economy grew while waste per person fell. The clearest cases are Ireland (GDP index 197, waste 96), Malta (157 and 97), Bulgaria (146 and 97), and the Netherlands (113 and 82), which has the largest fall in waste.
- **9 show relative decoupling**: waste per person grew, but more slowly than the economy. Examples: Lithuania (GDP index 159, waste 101), Romania (156 and 118), Poland (149 and 115).
- **5 show no decoupling: Czechia, Belgium, Austria, Slovakia and Luxembourg.** For four of them the result comes from a change in definition: before the break, Belgium and Luxembourg showed absolute decoupling, and Czechia and Austria relative decoupling. **Slovakia is the only Member State where the lack of decoupling is real**: its waste per person rose faster than GDP before its 2020 change (+35 % against +22 % from 2011 to 2019).
- Ireland's GDP growth is partly due to the accounts of multinational companies, so its decoupling looks stronger than it is. (General knowledge about Irish GDP; not checked in this project's data.)

## 3. Distance to the 2025 recycling targets

Recycling rates in 2023, two years before the 2025 deadline, compared with the 2025 targets. Rates are calculated under the 2025-target methods. A negative distance means the country is below the target.

### Municipal waste (target: 55 %)

- **The EU recycles 47.9 % of its municipal waste, 7.1 points below the 2025 target.**
- **Only 6 Member States reach 55 %:** Germany (68.7 %), Austria (62.8 %), Slovenia (59.8 %), the Netherlands (57.9 %), Luxembourg (56.5 %) and Belgium (55.8 %).
- 3 more are within 5 points: Italy (50.8 %), Latvia (50.6 %) and Slovakia (50.3 %).
- **6 Member States recycle less than 30 %:** Romania (12.4 %), Cyprus (15.8 %), Bulgaria (16.7 %), Greece and Malta (17.4 %), and Poland (27.6 %).
- **Postponements.** 8 Member States postponed the 2025 municipal target and must reach at least 50 % by 2025. In 2023, only Slovakia (50.3 %) was above 50 %; Lithuania was close (49.3 %). The other six (Greece, Croatia, Hungary, Malta, Poland, Romania) were below 37 %. 13 Member States that did not postpone were below 55 %, including Bulgaria and Cyprus, which are below 20 %.

### Packaging (target for all packaging: 65 %)

24 Member States have rates for 2023. Bulgaria, Czechia and Hungary have none under the 2025-target method.

- **The EU recycles 67.4 % of its packaging waste, 2.4 points above the 2025 target.** 11 of 24 Member States reach it, and 8 more are within 5 points.
- **Plastic is the main gap.** The EU recycles 41.6 % of plastic packaging, 8.4 points below the 50 % target. Only 5 of 24 Member States reach it: Belgium, Germany, Latvia, Slovenia and Slovakia. Denmark (22.7 %), France (25.7 %) and Austria (26.9 %) are more than 20 points below.
- **The other materials are mostly on track.** Paper and cardboard: 19 of 24 Member States reach the target (EU 87.0 %). Steel: 17 of 23 (EU 84.9 %). Wood: 17 of 24 (EU 37.7 %). Aluminium: 16 of 24 (EU 56.0 %). Glass: 13 of 24 (EU 74.9 %), with 6 more within 5 points.
- **Leaders and laggards.** Belgium, Germany, Slovenia and Slovakia reach all seven packaging targets. Belgium, Germany and Slovenia also reach the municipal target: they are the only Member States on track for all eight targets. Romania and Malta miss all seven packaging targets, and Greece misses six.
- Some postponements apply. 7 Member States (Czechia, Greece, Croatia, Luxembourg, Malta, Portugal, Sweden) postponed some material-specific targets, but not the target for all packaging. Which materials each postponed is not known yet, so their misses on materials cannot yet be read as failures.

## 4. Caveats for all findings

- **Breaks in series** affect municipal waste per person and decoupling for Czechia, Belgium, Austria, Slovakia, Luxembourg, Estonia and Slovenia, and the EU figure. The other flagged breaks have small effects (under 10 %). Jumps in Romania, Finland and Latvia have no documented cause (method notes, section 6).
- **The municipal recycling rate** includes composting and, for some countries and years, preparing for reuse. It is close to, but not yet checked against, the official Eurostat rate (method notes, section 2).
- **Some packaging rates are above 100 %** (Slovenia, Poland) and overstate the distance to target. The Cyprus steel rate (221.5 %) is left out of the assessment (method notes, section 3).
- **2023 is a snapshot, not the 2025 result.** Countries below the target in 2023 still had two years to reach it, and postponements change what counts as a failure (method notes, section 4).

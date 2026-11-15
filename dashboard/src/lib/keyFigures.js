// Figures shown inside the page texts (hero, waste hierarchy, section headers, closing panel).
//
// The texts in data/lookups/dashboard_texts.json contain placeholders such as "{eu_kg}"; the
// values are computed here from the processed data files, so they follow every new download.
// Each figure is also a finding in docs/findings.md. fill() replaces the placeholders.
import { greatest, least, max } from "d3-array";

import {
  EU27_TOTAL,
  decouplingNotes,
  geoNames,
  municipalWaste,
  municipalWasteDecoupling,
  municipalWasteTreatment,
  recyclingDistanceToTarget,
} from "../data.js";

const BASE_YEAR = 2011; // base year of the decoupling index and of the trends
const MEMBER_STATES = Object.keys(geoNames).filter((geo) => geo !== EU27_TOTAL);

const pct = (v) => (v == null ? "–" : v.toLocaleString("en-GB", { minimumFractionDigits: 1, maximumFractionDigits: 1 }));
const whole = (v) => (v == null ? "–" : Math.round(v).toLocaleString("en-GB"));

// latest year with waste per person for all 27 Member States
const countByYear = new Map();
for (const d of municipalWaste) {
  if (d.geo !== EU27_TOTAL && d.mw_pc != null) countByYear.set(d.year, (countByYear.get(d.year) ?? 0) + 1);
}
const YEAR = max([...countByYear].filter(([, n]) => n === MEMBER_STATES.length), ([y]) => y);

const row = (rows, geo, year) => rows.find((d) => d.geo === geo && d.year === year);

// waste per person
const wasteYear = municipalWaste.filter((d) => d.year === YEAR && d.mw_pc != null);
const euKg = row(municipalWaste, EU27_TOTAL, YEAR)?.mw_pc;
// EU total generated, from thousand tonnes (mw_tt) to million tonnes, whole number
const euMt = row(municipalWaste, EU27_TOTAL, YEAR)?.mw_tt;
const countries = wasteYear.filter((d) => d.geo !== EU27_TOTAL);
// Ratio of the most to the least waste per person, among Member States without a change in
// definition or a break in waste per person (the geographies with a break_year in
// decoupling_notes.json), so the ratio does not rest on a change in counting (findings §1
// bullet 12).
const BREAK_GEOS = new Set(
  decouplingNotes.country_notes.filter((n) => n.break_year != null).map((n) => n.geo),
);
const comparable = countries.filter((d) => !BREAK_GEOS.has(d.geo));
const most = greatest(comparable, (d) => d.mw_pc);
const least_ = least(comparable, (d) => d.mw_pc);

// decoupling
const euDecoupling = row(municipalWasteDecoupling, EU27_TOTAL, YEAR);
const absolute = municipalWasteDecoupling.filter(
  (d) => d.year === YEAR && d.geo !== EU27_TOTAL && d.gdp_pc_index > 100 && d.mw_pc_index <= 100,
);

// treatment across the hierarchy (EU27)
const euTreatment = row(municipalWasteTreatment, EU27_TOTAL, YEAR) ?? {};
const euTreatmentBase = row(municipalWasteTreatment, EU27_TOTAL, BASE_YEAR) ?? {};

// recycling targets: plastic packaging
const plastic = recyclingDistanceToTarget.filter(
  (d) => d.waste_name === "Plastic packaging" && d.geo !== EU27_TOTAL && d.distance_to_target != null,
);
const targetYear = max(recyclingDistanceToTarget, (d) => Number(d.time));

export const KEY_FIGURES = {
  year: String(YEAR),
  eu_kg: whole(euKg),
  eu_mt: whole(euMt == null ? null : euMt / 1000),
  max_country: geoNames[most?.geo],
  min_country: geoNames[least_?.geo],
  ratio: pct(most && least_ ? most.mw_pc / least_.mw_pc : null),
  n_above: String(countries.filter((d) => d.mw_pc > euKg).length),
  gdp_growth: pct(euDecoupling ? euDecoupling.gdp_pc_index - 100 : null),
  waste_growth: pct(euDecoupling ? euDecoupling.mw_pc_index - 100 : null),
  n_absolute: String(absolute.length),
  recycling: pct(euTreatment.recycling_pct),
  energy_recovery: pct(euTreatment.energy_recovery_pct),
  landfill: pct(euTreatment.landfill_pct),
  landfill_2011: pct(euTreatmentBase.landfill_pct),
  incineration: pct(euTreatment.incineration_pct),
  unaccounted: pct(euTreatment.unaccounted_pct),
  plastic_met: String(plastic.filter((d) => d.distance_to_target >= 0).length),
  plastic_n: String(plastic.length),
  target_year: String(targetYear),
};

// Replace "{name}" placeholders with values (KEY_FIGURES by default, plus any extra values).
export function fill(text, extra = {}) {
  if (text == null) return text;
  const values = { ...KEY_FIGURES, ...extra };
  return text.replace(/\{(\w+)\}/g, (match, key) => (values[key] != null ? values[key] : match));
}

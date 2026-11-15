// Line chart of municipal waste per person and real GDP per person, both indexed to 2011 = 100,
// for one geography chosen with a search box (the EU27 by default).
//
// The chosen geography has two coloured lines (waste, GDP). When a Member State is chosen, the
// EU27 lines stay behind it in grey, for comparison. The y axis is fixed, the same for every
// geography (lowest to highest index of all geographies, rounded out to 10), so the chart does
// not zoom in or out when the selection changes. A dashed line marks 100 (the 2011 level).
// Where the chosen geography has a break in series, a vertical line marks the break year.
//
// Under the chart: the general note, the country note of the chosen geography (if any) and,
// for the EU27, the note on the Member States that changed their definition. All texts, labels
// and break years come from data/lookups/decoupling_notes.json.
//
// The search box works like the one of the distance-to-target chart: type a name, pick it from
// the suggestions. D3 computes the scales, ticks and line paths; React renders the SVG.
import { extent, group, max, min } from "d3-array";
import { scaleLinear } from "d3-scale";
import { line } from "d3-shape";
import { useMemo, useState } from "react";

import { EU27_TOTAL, decouplingNotes, geoNames, municipalWasteDecoupling } from "../../data.js";

const MARGIN = { top: 28, right: 160, bottom: 30, left: 44 };
const HEIGHT = 420;
const Y_STEP = 10; // the y axis is rounded out to a multiple of this
const MIN_PX_PER_YEAR_LABEL = 44; // below this, label every second year
const LABEL_GAP = 14; // px, minimum vertical distance between two line-end labels

const SERIES = [
  { key: "mw_pc_index", color: "#e07b39" },
  { key: "gdp_pc_index", color: "#003494" },
];
const REFERENCE_COLOR = "#bdbdbd";
const GRID = "#e5e5e5";
const BASE_LINE = { stroke: "#333333", strokeWidth: 1, strokeDasharray: "4 4" };
const BREAK_COLOR = "#757575";

const { labels } = decouplingNotes;

// --- data preparation (runs once) -------------------------------------------------------

// rows of each geography, by year
const ROWS_BY_GEO = Object.fromEntries(
  [...group(municipalWasteDecoupling, (d) => d.geo)].map(([geo, rows]) => [
    geo,
    [...rows].sort((a, b) => a.year - b.year),
  ]),
);

const YEARS = extent(municipalWasteDecoupling, (d) => d.year);

// Fixed y domain: all indexes of all geographies, rounded out to Y_STEP.
const ALL_INDEXES = municipalWasteDecoupling.flatMap((d) => [d.mw_pc_index, d.gdp_pc_index]);
const Y_DOMAIN = [
  Math.floor(min(ALL_INDEXES) / Y_STEP) * Y_STEP,
  Math.ceil(max(ALL_INDEXES) / Y_STEP) * Y_STEP,
];

const NOTES_BY_GEO = Object.fromEntries(decouplingNotes.country_notes.map((n) => [n.geo, n]));

// Search options: the EU27 first, then the Member States by name.
const OPTIONS = [
  { geo: EU27_TOTAL, name: geoNames[EU27_TOTAL] },
  ...Object.keys(ROWS_BY_GEO)
    .filter((geo) => geo !== EU27_TOTAL)
    .map((geo) => ({ geo, name: geoNames[geo] ?? geo }))
    .sort((a, b) => a.name.localeCompare(b.name)),
];
const GEO_BY_NAME = Object.fromEntries(OPTIONS.map((o) => [o.name.toLowerCase(), o.geo]));

// Last point with a value of a series, for the line-end label.
const lastPoint = (rows, key) => [...rows].reverse().find((d) => d[key] != null);

// Spread labels vertically so that no two are closer than LABEL_GAP (keeps their order).
function spreadLabels(items) {
  const sorted = [...items].sort((a, b) => a.y - b.y).map((d) => ({ ...d, labelY: d.y }));
  for (let i = 1; i < sorted.length; i += 1) {
    sorted[i].labelY = Math.max(sorted[i].y, sorted[i - 1].labelY + LABEL_GAP);
  }
  return sorted;
}

// --- chart -------------------------------------------------------------------------------

export default function DecouplingLineChart({ width }) {
  const [selected, setSelected] = useState(EU27_TOTAL);
  const [searchQuery, setSearchQuery] = useState("");

  const boundsWidth = width - MARGIN.left - MARGIN.right;
  const boundsHeight = HEIGHT - MARGIN.top - MARGIN.bottom;

  const xScale = useMemo(
    () => scaleLinear().domain(YEARS).range([0, boundsWidth]),
    [boundsWidth],
  );
  const yScale = useMemo(
    () => scaleLinear().domain(Y_DOMAIN).range([boundsHeight, 0]),
    [boundsHeight],
  );

  // one label per year, or every second year when the chart is narrow
  const yearStep = boundsWidth / (YEARS[1] - YEARS[0]) < MIN_PX_PER_YEAR_LABEL ? 2 : 1;
  const xTicks = [];
  for (let year = YEARS[0]; year <= YEARS[1]; year += yearStep) xTicks.push(year);

  // line path of one series; gaps where a value is missing (e.g. Ireland 2013 and 2015)
  const pathOf = (rows, key) =>
    line()
      .defined((d) => d[key] != null)
      .x((d) => xScale(d.year))
      .y((d) => yScale(d[key]))(rows);

  const rows = ROWS_BY_GEO[selected];
  const isEU = selected === EU27_TOTAL;
  const note = NOTES_BY_GEO[selected];
  const name = geoNames[selected] ?? selected;

  // Typing an exact name (or picking a suggestion) selects it; clearing the box goes back to
  // the EU27. Anything else keeps the current selection.
  const onSearch = (value) => {
    setSearchQuery(value);
    const query = value.trim().toLowerCase();
    if (!query) setSelected(EU27_TOTAL);
    else if (GEO_BY_NAME[query]) setSelected(GEO_BY_NAME[query]);
  };

  // line-end labels: the chosen geography, plus the EU27 reference when a country is chosen
  const endLabels = spreadLabels([
    ...SERIES.map(({ key, color }) => {
      const d = lastPoint(rows, key);
      return { key, text: labels[key], color, y: yScale(d[key]), x: xScale(d.year), bold: true };
    }),
    ...(isEU
      ? []
      : SERIES.map(({ key }) => {
          const d = lastPoint(ROWS_BY_GEO[EU27_TOTAL], key);
          return {
            key: `reference-${key}`,
            text: labels[`reference_${key}`],
            color: REFERENCE_COLOR,
            y: yScale(d[key]),
            x: xScale(d.year),
            bold: false,
          };
        })),
  ]);

  return (
    <figure className="line-chart">
      <div className="chart-controls">
        <input
          type="search"
          list="decoupling-countries"
          placeholder="Search a country..."
          value={searchQuery}
          onChange={(e) => onSearch(e.target.value)}
          aria-label="Search a country"
        />
        <datalist id="decoupling-countries">
          {OPTIONS.map((o) => (
            <option key={o.geo} value={o.name} />
          ))}
        </datalist>

        <Legend showReference={!isEU} />
      </div>

      <figcaption className="chart-caption">{decouplingNotes.caption.replace("{name}", name)}</figcaption>

      <svg width={width} height={HEIGHT} role="img" aria-label={decouplingNotes.caption.replace("{name}", name)}>
        <g transform={`translate(${MARGIN.left},${MARGIN.top})`}>
          {/* horizontal grid with index labels */}
          {yScale.ticks(Y_DOMAIN[1] - Y_DOMAIN[0] > 100 ? 7 : 10).map((v) => (
            <g key={`y-${v}`}>
              <line x1={0} x2={boundsWidth} y1={yScale(v)} y2={yScale(v)} stroke={GRID} />
              <text x={-8} y={yScale(v)} textAnchor="end" dominantBaseline="middle" className="chart-axis">
                {v}
              </text>
            </g>
          ))}

          {/* year labels */}
          {xTicks.map((year) => (
            <text key={`x-${year}`} x={xScale(year)} y={boundsHeight + 20} textAnchor="middle" className="chart-axis">
              {year}
            </text>
          ))}

          {/* 2011 = 100 */}
          <line x1={0} x2={boundsWidth} y1={yScale(100)} y2={yScale(100)} {...BASE_LINE} />

          {/* break in series of the chosen geography */}
          {note?.break_year != null && (
            <g>
              <line
                x1={xScale(note.break_year)}
                x2={xScale(note.break_year)}
                y1={0}
                y2={boundsHeight}
                stroke={BREAK_COLOR}
                strokeWidth={1.5}
              />
              <text x={xScale(note.break_year)} y={-10} textAnchor="middle" className="chart-axis">
                {labels.break_year} ({note.break_year})
              </text>
            </g>
          )}

          {/* EU27 reference lines (only when a Member State is chosen) */}
          {!isEU &&
            SERIES.map(({ key }) => (
              <path
                key={`reference-${key}`}
                d={pathOf(ROWS_BY_GEO[EU27_TOTAL], key)}
                fill="none"
                stroke={REFERENCE_COLOR}
                strokeWidth={2}
              />
            ))}

          {/* lines of the chosen geography; a point with no value on either side (e.g. Ireland
              2014) cannot be joined by a line, so it is drawn as a dot */}
          {SERIES.map(({ key, color }) => (
            <g key={key}>
              <path d={pathOf(rows, key)} fill="none" stroke={color} strokeWidth={2.5} />
              {rows
                .filter((d, i) => d[key] != null && rows[i - 1]?.[key] == null && rows[i + 1]?.[key] == null)
                .map((d) => (
                  <circle key={d.year} cx={xScale(d.year)} cy={yScale(d[key])} r={3.5} fill={color} />
                ))}
            </g>
          ))}

          {/* line-end labels */}
          {endLabels.map((l) => (
            <text
              key={`label-${l.key}`}
              x={l.x + 8}
              y={l.labelY}
              dominantBaseline="middle"
              className={l.bold ? "chart-label-strong" : "chart-label"}
              style={{ fill: l.color }}
            >
              {l.text}
            </text>
          ))}
        </g>
      </svg>

      <p className="chart-note">{decouplingNotes.general_note}</p>
      {note && (
        <p className="chart-note">
          <strong>{name}:</strong> {note.note}
        </p>
      )}
      {isEU && <p className="chart-note">{decouplingNotes.break_note}</p>}
    </figure>
  );
}

// Legend: the two series, the EU27 reference (when shown), the 2011 = 100 line.
function Legend({ showReference }) {
  const items = [
    ...SERIES.map(({ key, color }) => ({ key, text: labels[key], line: { stroke: color, strokeWidth: 2.5 } })),
    ...(showReference
      ? [{ key: "reference", text: labels.reference, line: { stroke: REFERENCE_COLOR, strokeWidth: 2 } }]
      : []),
    { key: "base", text: labels.base_year, line: BASE_LINE },
  ];
  return (
    <div className="line-legend" role="list" aria-label="Legend">
      {items.map((item) => (
        <span key={item.key} className="line-legend-item" role="listitem">
          <svg width={24} height={10} aria-hidden="true">
            <line x1={0} x2={24} y1={5} y2={5} {...item.line} />
          </svg>
          {item.text}
        </span>
      ))}
    </div>
  );
}

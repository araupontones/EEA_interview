// Horizontal bar chart of municipal waste per person (kg) by EU Member State.
//
// One bar per Member State, sorted from the highest to the lowest value, for the latest year
// with data for all 27 Member States (computed from the data, so it moves on when Eurostat
// publishes a complete new year). The EU27 is one more bar, in its ranked position, in dark
// grey (the same colour as the EU27 marker in the distance-to-target chart). Each bar ends with
// its value. Caption, note and the labels of the hover card come from
// data/lookups/municipal_waste_notes.json. The chart compares countries in one year, so the
// breaks in series are explained under the decoupling chart, not here.
//
// Hovering a row (label, bar or value) dims the other bars and shows a card with the country's
// flag (in a circle, top left), its name, waste per person and total waste generated.
//
// D3 computes the scales and ticks; React renders the SVG.
import { max, rollup } from "d3-array";
import { scaleBand, scaleLinear } from "d3-scale";
import { useMemo, useRef, useState } from "react";

import {
  EU27_TOTAL,
  geoNames,
  municipalWaste,
  municipalWasteNotes,
} from "../../data.js";
import { flagUrl } from "../../lib/flags.js";

const MARGIN = { top: 24, right: 48, bottom: 8, left: 120 };
const ROW_HEIGHT = 22;
const TICK_COUNT = 5;

const COUNTRY_COLOR = "#5d92f5";
const EU_COLOR = "#003494";
const GRID = "#e5e5e5";
const CARD_WIDTH = 280; // px, also set in index.css (.hover-card)
const CARD_OFFSET = 14; // px between the pointer and the card
const DIMMED_OPACITY = 0.35; // other bars while a row is hovered
const BASELINE = { stroke: "#000000", strokeWidth: 2 }; // grid line at x = 0
const BAR_RADIUS = 5; // px, radius of the rounded right end of the bars

// Bar from x = 0 to x = width, at y with height h, with only the right-hand corners rounded
// (the left end sits on the baseline). The radius shrinks for bars too short or thin for it.
function barPath(width, y, h, radius) {
  const r = Math.max(0, Math.min(radius, h / 2, width));
  return [
    `M0,${y}`,
    `H${width - r}`,
    `A${r},${r} 0 0 1 ${width},${y + r}`,
    `V${y + h - r}`,
    `A${r},${r} 0 0 1 ${width - r},${y + h}`,
    "H0",
    "Z",
  ].join(" ");
}

// --- data preparation (runs once) -------------------------------------------------------

const MEMBER_STATE_COUNT = Object.keys(geoNames).filter(
  (geo) => geo !== EU27_TOTAL,
).length;

// Latest year with a value for every Member State.
const COUNTRIES_PER_YEAR = rollup(
  municipalWaste.filter((d) => d.geo !== EU27_TOTAL && d.mw_pc != null),
  (rows) => rows.length,
  (d) => d.year,
);
const YEAR = max(
  [...COUNTRIES_PER_YEAR].filter(([, count]) => count === MEMBER_STATE_COUNT),
  ([year]) => year,
);

// One bar per geography, highest value first.
const BARS = municipalWaste
  .filter((d) => d.year === YEAR && d.mw_pc != null)
  .map((d) => ({
    geo: d.geo,
    name: geoNames[d.geo] ?? d.geo,
    value: d.mw_pc,
    total: d.mw_tt,
    isEU: d.geo === EU27_TOTAL,
  }))
  .sort((a, b) => b.value - a.value);

const CAPTION = municipalWasteNotes.caption.replace("{year}", YEAR);

// Numbers in UK style: comma for thousands, no decimals (e.g. 7,334).
const formatNumber = (v) =>
  v == null ? "–" : v.toLocaleString("en-GB", { maximumFractionDigits: 0 });

// --- chart -------------------------------------------------------------------------------

export default function WastePerCapitaBarChart({ width }) {
  const containerRef = useRef(null);
  const [hovered, setHovered] = useState(null); // { bar, x, y }: x, y = pointer in the container
  const height = MARGIN.top + BARS.length * ROW_HEIGHT + MARGIN.bottom;
  const boundsWidth = width - MARGIN.left - MARGIN.right;
  const boundsHeight = height - MARGIN.top - MARGIN.bottom;

  const xScale = useMemo(
    () =>
      scaleLinear()
        .domain([0, max(BARS, (d) => d.value)])
        .range([0, boundsWidth])
        .nice(TICK_COUNT),
    [boundsWidth],
  );
  const yScale = useMemo(
    () =>
      scaleBand()
        .domain(BARS.map((d) => d.geo))
        .range([0, boundsHeight])
        .padding(0.2),
    [boundsHeight],
  );

  // Pointer position relative to the chart container (where the card is positioned).
  const onPointerMove = (bar) => (e) => {
    const box = containerRef.current.getBoundingClientRect();
    setHovered({ bar, x: e.clientX - box.left, y: e.clientY - box.top });
  };

  return (
    <figure className="bar-chart">
      <figcaption className="chart-caption">{CAPTION}</figcaption>

      <div ref={containerRef} className="chart-hover-area">
        <svg width={width} height={height} role="img" aria-label={CAPTION}>
          <g transform={`translate(${MARGIN.left},${MARGIN.top})`}>
            {/* vertical grid with kg labels */}
            {xScale.ticks(TICK_COUNT).map((v) => (
              <g key={`grid-${v}`}>
                <line
                  x1={xScale(v)}
                  x2={xScale(v)}
                  y1={0}
                  y2={boundsHeight}
                  stroke={GRID}
                />
                <text
                  x={xScale(v)}
                  y={-8}
                  textAnchor="middle"
                  className="chart-axis"
                >
                  {v}
                </text>
              </g>
            ))}

            {/* one bar per geography: country label, bar, value */}
            {BARS.map((d) => {
              const y = yScale(d.geo) ?? 0;
              const yMid = y + yScale.bandwidth() / 2;
              const barEnd = xScale(d.value);
              const dimmed = hovered !== null && hovered.bar.geo !== d.geo;
              return (
                <g
                  key={d.geo}
                  style={{
                    opacity: dimmed ? DIMMED_OPACITY : 1,
                    cursor: "default",
                  }}
                  onPointerMove={onPointerMove(d)}
                  onPointerLeave={() => setHovered(null)}
                >
                  {/* invisible rectangle over the whole row, so the row is easy to hover */}
                  <rect
                    x={-MARGIN.left}
                    y={y - (yScale.step() - yScale.bandwidth()) / 2}
                    width={width}
                    height={yScale.step()}
                    fill="transparent"
                  />
                  <text
                    x={-8}
                    y={yMid}
                    textAnchor="end"
                    dominantBaseline="middle"
                    className={
                      d.isEU
                        ? "chart-row-label chart-label-eu"
                        : "chart-row-label"
                    }
                  >
                    {d.name}
                  </text>
                  <path
                    d={barPath(barEnd, y, yScale.bandwidth(), BAR_RADIUS)}
                    fill={d.isEU ? EU_COLOR : COUNTRY_COLOR}
                  />
                  <text
                    x={barEnd + 4}
                    y={yMid}
                    dominantBaseline="middle"
                    className={
                      d.isEU ? "chart-label chart-label-eu" : "chart-label"
                    }
                  >
                    {d.value.toFixed(0)}
                  </text>
                </g>
              );
            })}

            {/* baseline at x = 0, drawn after the bars so they do not cover it */}
            <line
              x1={xScale(0)}
              x2={xScale(0)}
              y1={0}
              y2={boundsHeight}
              {...BASELINE}
            />
          </g>
        </svg>

        {hovered && <HoverCard {...hovered} containerWidth={width} />}
      </div>

      <p className="chart-note">{municipalWasteNotes.general_note}</p>
    </figure>
  );
}

// Card shown next to the pointer: flag in a circle and country name, then the values.
// It opens to the left of the pointer when there is no room on the right.
function HoverCard({ bar, x, y, containerWidth }) {
  const { card } = municipalWasteNotes;
  const flag = flagUrl(bar.geo);
  const left =
    x + CARD_OFFSET + CARD_WIDTH > containerWidth
      ? x - CARD_OFFSET - CARD_WIDTH
      : x + CARD_OFFSET;

  return (
    <div
      className="hover-card"
      style={{ left, top: y + CARD_OFFSET }}
      role="tooltip"
    >
      <div className="hover-card-header">
        {flag && <img className="flag-circle" src={flag} alt="" />}
        <span className="hover-card-title">{bar.name}</span>
      </div>
      <dl className="hover-card-values">
        <dt>{card.mw_pc.label}</dt>
        <dd>
          {formatNumber(bar.value)} {card.mw_pc.unit}
        </dd>
        <dt>{card.mw_tt.label}</dt>
        <dd>
          {formatNumber(bar.total)} {card.mw_tt.unit}
        </dd>
      </dl>
    </div>
  );
}

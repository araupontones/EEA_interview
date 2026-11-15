// Beeswarm of recycling rates by waste category, coloured by the distance to the 2025 target.
//
// One row per waste category with a 2025 target; one circle per country (x = recycling rate,
// small vertical jitter to avoid overlaps). Colour = distance to target, with a break at the
// target: countries below it use the red-to-yellow end of the RdYlBu palette, countries that met
// it use the blue end only, so blue always means "target met". Darker = further from the target,
// capped at ±COLOR_CAP percentage points. A vertical tick marks each row's target.
// The EU27 is a dark grey diamond (same area as the circles) and is not coloured by distance.
// Each row labels the country with the lowest and the highest rate (geo code, bold).
// Hover a circle to highlight that country in every row; search a country by name.
//
// Adapted from https://www.react-graph-gallery.com/example/beeswarm-interactive-search
// (without its annotations). D3 computes scales and extremes; React renders the SVG.
import { greatest, least } from "d3-array";
import { scaleBand, scaleLinear, scaleSequential } from "d3-scale";
// Colour scale for the distance to target: red below the target, blue above
// (readable with red-green colour blindness, unlike red-green scales).
import { interpolateRdYlBu } from "d3-scale-chromatic";
import { symbol, symbolDiamond2 } from "d3-shape";
import { useMemo, useState } from "react";

import {
  dashboardTexts,
  EU27_TOTAL,
  geoNames,
  recyclingDistanceToTarget,
  recyclingTargets,
} from "../../data.js";
import { flagUrl } from "../../lib/flags.js";
import { fill } from "../../lib/keyFigures.js";

const MARGIN = { top: 30, right: 30, bottom: 20, left: 210 };
const ROW_HEIGHT = 64;
const NARROW = 560; // px: below this width, row labels go above the rows
const MARGIN_NARROW = { top: 30, right: 16, bottom: 20, left: 12 };
const ROW_HEIGHT_NARROW = 80;
const RADIUS = 6;
const X_MAX = 115; // recycling rates above 100 % exist (e.g. Slovenia, glass: 112 %)
const GRID_VALUES = [0, 25, 50, 75, 100];
const MIN_LABEL_SPACE = 70; // px left of a circle needed for a label; less: label goes above
const TARGET_TICK_SHARE = 0.6; // height of the target tick, as a share of the row band (~30 px)

// Colour scale capped at ±COLOR_CAP percentage points: countries further from their target get
// the strongest colour, so the colours separate the countries close to their target better.
// Half of the countries are within 12 points of their target.
const COLOR_CAP = 25;

// Parts of the RdYlBu palette (0 = dark red, 0.5 = pale yellow, 1 = dark blue) used on each side
// of the target. "Below" stops before the palest yellow, which is hard to see on the background.
const BELOW_TARGET_RANGE = [0, 0.42]; // far below -> just below: dark red -> light yellow-orange
const TARGET_MET_RANGE = [0.62, 1]; // just above -> far above: light blue -> dark blue

const EU_COLOR = "#1d2b2a"; // EU27 = ink (dashboard identity)
const GRID = "#e6e1d8";

// Colour of a country from its distance to the target (percentage points).
const sliceOf = ([from, to]) => (t) => interpolateRdYlBu(from + (to - from) * t);
const belowTargetColor = scaleSequential(sliceOf(BELOW_TARGET_RANGE))
  .domain([-COLOR_CAP, 0])
  .clamp(true);
const targetMetColor = scaleSequential(sliceOf(TARGET_MET_RANGE))
  .domain([0, COLOR_CAP])
  .clamp(true);
const distanceColor = (distance) =>
  distance < 0 ? belowTargetColor(distance) : targetMetColor(distance);

// EU27 marker: a diamond with the same area as a country circle, centred on (0, 0).
const EU_DIAMOND = symbol(symbolDiamond2, Math.PI * RADIUS * RADIUS)();

// --- data preparation (runs once) -------------------------------------------------------

const TARGETS = Object.fromEntries(
  recyclingTargets
    .filter((t) => t.target_2025 != null)
    .map((t) => [t.waste_name, t]),
);

// Rows: municipal waste, all packaging, then the materials from the highest 2025 target to the
// lowest (2030 target to break ties). Categories without a target are left out.
const ROWS = Object.values(TARGETS)
  .sort((a, b) => {
    const first = ["Municipal waste", "Packaging"];
    const ia = first.indexOf(a.waste_name);
    const ib = first.indexOf(b.waste_name);
    if (ia !== -1 || ib !== -1)
      return (ia === -1 ? 99 : ia) - (ib === -1 ? 99 : ib);
    return b.target_2025 - a.target_2025 || b.target_2030 - a.target_2030;
  })
  .map((t) => t.waste_name);

// Stable pseudo-random number in [0, 1) from a string, so the jitter is the same on every load.
function hash01(text) {
  let h = 2166136261;
  for (let i = 0; i < text.length; i += 1) {
    h ^= text.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0) / 4294967296;
}

// One record per country and waste category with a rate and a target.
const CIRCLES = recyclingDistanceToTarget
  .filter(
    (d) =>
      TARGETS[d.waste_name] && d.value != null && d.distance_to_target != null,
  )
  .map((d) => ({
    ...d,
    name: geoNames[d.geo] ?? d.geo,
    isEU: d.geo === EU27_TOTAL,
    jitter: hash01(`${d.geo}-${d.waste_name}`) - 0.5,
  }));

// Lowest and highest rate per row, among countries only (the EU27 is not labelled).
const EXTREMES = ROWS.flatMap((row) => {
  const countries = CIRCLES.filter((d) => d.waste_name === row && !d.isEU);
  return [
    { ...least(countries, (d) => d.value), side: "min" },
    { ...greatest(countries, (d) => d.value), side: "max" },
  ];
});

// Country names for the search suggestions.
const COUNTRY_NAMES = [
  ...new Set(CIRCLES.filter((d) => !d.isEU).map((d) => d.name)),
].sort();

const CARD_WIDTH = 220; // px, hover card (also .hover-card-small in index.css)
const CARD_GAP = 12; // px between the circle and the card

// texts of this chart (data/lookups/dashboard_texts.json)
const TEXTS = dashboardTexts.distance_to_target;


// --- chart -------------------------------------------------------------------------------

export default function DistanceToTargetScatter({ width }) {
  const [hovered, setHovered] = useState(null); // { geo, waste_name }
  const [searchQuery, setSearchQuery] = useState("");

  const narrow = width < NARROW;
  const margin = narrow ? MARGIN_NARROW : MARGIN;
  const rowHeight = narrow ? ROW_HEIGHT_NARROW : ROW_HEIGHT;
  const height = margin.top + ROWS.length * rowHeight + margin.bottom;
  const boundsWidth = width - margin.left - margin.right;
  const boundsHeight = height - margin.top - margin.bottom;

  const xScale = useMemo(
    () => scaleLinear().domain([0, X_MAX]).range([0, boundsWidth]),
    [boundsWidth],
  );
  const yScale = useMemo(
    () => scaleBand().domain(ROWS).range([0, boundsHeight]).padding(0.2),
    [boundsHeight],
  );
  const rowCenter = (row) => (yScale(row) ?? 0) + yScale.bandwidth() / 2;
  const cy = (d) =>
    rowCenter(d.waste_name) + d.jitter * yScale.bandwidth() * 0.8;

  // countries matching the search (by name)
  const matchedGeos = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();
    if (!query) return new Set();
    return new Set(
      CIRCLES.filter((d) => d.name.toLowerCase().includes(query)).map(
        (d) => d.geo,
      ),
    );
  }, [searchQuery]);

  const isInteracting = hovered !== null || matchedGeos.size > 0;

  // One mark per record: a circle coloured by distance for countries, a diamond for the EU27.
  // highlight = dark outline (hovered or searched).
  const mark = (d, { highlight = false, ...props } = {}) => {
    const x = xScale(d.value);
    const y = cy(d);
    const outline = highlight
      ? { stroke: "#1d2b2a", strokeWidth: 2 }
      : { stroke: "#1d2b2a", strokeOpacity: 0.6, strokeWidth: 1 }; // ink outline: light colours keep a 3:1 edge
    return d.isEU ? (
      <path d={EU_DIAMOND} transform={`translate(${x},${y})`} fill={EU_COLOR} {...outline} {...props} />
    ) : (
      <circle cx={x} cy={y} r={RADIUS} fill={distanceColor(d.distance_to_target)} {...outline} {...props} />
    );
  };

  // Layer 1: all marks (dimmed while hovering or searching)
  const allCircles = CIRCLES.map((d) => (
    <g key={`${d.waste_name}-${d.geo}`}>
      {mark(d, {
        onMouseEnter: () => setHovered({ geo: d.geo, waste_name: d.waste_name }),
        onMouseLeave: () => setHovered(null),
        style: { cursor: "pointer" },
      })}
    </g>
  ));

  // the hovered record (for the hover card)
  const hoveredRecord = hovered
    ? CIRCLES.find((d) => d.geo === hovered.geo && d.waste_name === hovered.waste_name)
    : null;

  // Layer 2: the hovered country in every row, with a label on the hovered circle
  const highlightedCircles = hovered
    ? CIRCLES.filter((d) => d.geo === hovered.geo).map((d) => (
        <g key={`hovered-${d.waste_name}`} style={{ pointerEvents: "none" }}>
          {mark(d, { highlight: true })}
        </g>
      ))
    : null;

  // Layer 3: searched countries in every row, labelled in the first row
  const searchedCircles = CIRCLES.filter((d) => matchedGeos.has(d.geo)).map(
    (d) => (
      <g
        key={`searched-${d.waste_name}-${d.geo}`}
        style={{ pointerEvents: "none" }}
      >
        {mark(d, { highlight: true })}
        {d.waste_name === ROWS[0] && (
          <text
            x={xScale(d.value)}
            y={cy(d) - 12}
            textAnchor="middle"
            className="chart-label-strong"
          >
            {d.name}
          </text>
        )}
      </g>
    ),
  );

  return (
    <div className="beeswarm">
      <div className="chart-controls">
        <input
          type="search"
          list="distance-to-target-countries"
          placeholder={dashboardTexts.ui.search_placeholder}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          aria-label={dashboardTexts.ui.search_aria}
        />
        <datalist id="distance-to-target-countries">
          {COUNTRY_NAMES.map((name) => (
            <option key={name} value={name} />
          ))}
        </datalist>

        {/* legend above the chart, right-aligned in the same row as the search box */}
        <Legend cap={COLOR_CAP} />
      </div>

      <p className="chart-caption">{fill(TEXTS.caption)}</p>
      <div className="chart-hover-area">
        <svg
          width={width}
          height={height}
          role="img"
          aria-label={fill(TEXTS.aria_label)}
        >
          <g transform={`translate(${margin.left},${margin.top})`}>
            {/* vertical grid with % labels */}
            {GRID_VALUES.map((v) => (
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
                  y={-10}
                  textAnchor="middle"
                  className="chart-axis"
                >
                  {v}%
                </text>
              </g>
            ))}

            {/* per row: line from lowest to highest rate, 2025 target tick, row label */}
            {ROWS.map((row) => {
              const values = CIRCLES.filter((d) => d.waste_name === row).map(
                (d) => d.value,
              );
              const y = rowCenter(row);
              const target = TARGETS[row].target_2025;
              const half = (yScale.bandwidth() * TARGET_TICK_SHARE) / 2;
              return (
                <g key={`row-${row}`}>
                  <line
                    x1={xScale(Math.min(...values))}
                    x2={xScale(Math.max(...values))}
                    y1={y}
                    y2={y}
                    stroke="#e6e1d8"
                    strokeWidth={4}
                    strokeLinecap="round"
                  />
                  <line
                    x1={xScale(target)}
                    x2={xScale(target)}
                    y1={y - half}
                    y2={y + half}
                    stroke="#1d2b2a"
                    strokeWidth={2.5}
                  />
                  <text
                    x={narrow ? 0 : -10}
                    y={narrow ? (yScale(row) ?? 0) - 6 : y}
                    textAnchor={narrow ? "start" : "end"}
                    dominantBaseline={narrow ? "auto" : "middle"}
                    className="chart-row-label"
                  >
                    {row}
                  </text>
                </g>
              );
            })}

            {/* Layer 1 */}
            <g
              style={{
                opacity: isInteracting ? 0.3 : 1,
                filter: isInteracting ? "saturate(0.3)" : "none",
              }}
            >
              {allCircles}
            </g>

            {/* lowest and highest rate per row (only when not interacting) */}
            {!isInteracting &&
              EXTREMES.map((d) => {
                const x = xScale(d.value);
                // lowest: label left of the circle, or above it if it would run into the row labels
                const above = d.side === "min" && x < MIN_LABEL_SPACE;
                return (
                  <text
                    key={`extreme-${d.waste_name}-${d.side}`}
                    x={
                      above
                        ? x
                        : x + (d.side === "min" ? -RADIUS - 4 : RADIUS + 4)
                    }
                    y={above ? cy(d) - RADIUS - 4 : cy(d)}
                    textAnchor={
                      above ? "start" : d.side === "min" ? "end" : "start"
                    }
                    dominantBaseline={above ? "auto" : "middle"}
                    className="chart-label-extreme chart-label-halo"
                    style={{ pointerEvents: "none" }}
                  >
                    {d.geo}
                  </text>
                );
              })}

            {/* Layer 2 and 3 */}
            {highlightedCircles}
            {searchedCircles}
          </g>
        </svg>

        {/* hover card: next to the hovered circle, above it (below it in the first row) */}
        {hoveredRecord && (
          <HoverCard
            d={hoveredRecord}
            x={margin.left + xScale(hoveredRecord.value)}
            y={margin.top + cy(hoveredRecord)}
            below={hoveredRecord.waste_name === ROWS[0]}
            containerWidth={width}
          />
        )}
      </div>

      <details className="chart-details">
        <summary>{dashboardTexts.ui.about_chart}</summary>
        {TEXTS.notes.map((note) => (
          <p key={note} className="chart-note">
            {note}
          </p>
        ))}
      </details>
    </div>
  );
}

// Plain wording of the distance to the target, e.g. "42.6 points below the 2025 target of 55 %".
function distanceText(d) {
  const target = TARGETS[d.waste_name]?.target_2025;
  const values = { distance: Math.abs(d.distance_to_target).toFixed(1), target: target ?? "" };
  if (d.distance_to_target > 0) return fill(TEXTS.hover.above, values);
  if (d.distance_to_target < 0) return fill(TEXTS.hover.below, values);
  return fill(TEXTS.hover.on, values);
}

// Card with the flag, country name, waste category, recycling rate and distance to target.
function HoverCard({ d, x, y, below, containerWidth }) {
  const flag = flagUrl(d.geo);
  const left = Math.min(Math.max(x - CARD_WIDTH / 2, 0), containerWidth - CARD_WIDTH);
  const style = below
    ? { left, top: y + RADIUS + CARD_GAP }
    : { left, top: y - RADIUS - CARD_GAP, transform: "translateY(-100%)" };
  return (
    <div className="hover-card hover-card-small" style={style} role="tooltip">
      <div className="hover-card-header">
        {flag && <img className="flag-circle" src={flag} alt="" />}
        <span className="hover-card-title">{d.name}</span>
      </div>
      <div className="hover-card-sub">{d.waste_name}</div>
      <div className="hover-card-main">{fill(TEXTS.hover.rate, { value: d.value.toFixed(1) })}</div>
      <div className="hover-card-sub">{distanceText(d)}</div>
    </div>
  );
}

// Legend: the two colour scales (below target, target met), the target tick and the EU27 symbol.
function Legend({ cap }) {
  const stops = [0, 0.25, 0.5, 0.75, 1];
  const barWidth = 140; // width of each of the two bars
  const gap = 6; // gap between the bars: the break at the target
  const metX = barWidth + gap;
  const otherX = 2 * barWidth + gap + 40; // start of the target and EU27 entries
  return (
    <svg
      viewBox={`0 0 ${otherX + 160} 64`}
      width={otherX + 160}
      style={{ maxWidth: "100%", height: "auto" }}
      className="chart-legend"
      role="img"
      aria-label="Legend"
    >
      <defs>
        <linearGradient id="below-target-gradient">
          {stops.map((t) => (
            <stop key={t} offset={`${t * 100}%`} stopColor={belowTargetColor(-cap + t * cap)} />
          ))}
        </linearGradient>
        <linearGradient id="target-met-gradient">
          {stops.map((t) => (
            <stop key={t} offset={`${t * 100}%`} stopColor={targetMetColor(t * cap)} />
          ))}
        </linearGradient>
      </defs>

      <text x={0} y={12} className="chart-axis">
        {TEXTS.legend.below}
      </text>
      <text x={metX + barWidth} y={12} textAnchor="end" className="chart-axis">
        {TEXTS.legend.met}
      </text>
      <rect x={0} y={20} width={barWidth} height={10} fill="url(#below-target-gradient)" />
      <rect x={metX} y={20} width={barWidth} height={10} fill="url(#target-met-gradient)" />
      <text x={0} y={44} className="chart-axis">
        ≤ −{cap}
      </text>
      <text x={barWidth + gap / 2} y={44} textAnchor="middle" className="chart-axis">
        0
      </text>
      <text x={metX + barWidth} y={44} textAnchor="end" className="chart-axis">
        ≥ +{cap}
      </text>
      <text x={0} y={60} className="chart-axis">
        {TEXTS.legend.axis}
      </text>

      <line x1={otherX} x2={otherX} y1={18} y2={34} stroke="#1d2b2a" strokeWidth={2.5} />
      <text x={otherX + 8} y={30} className="chart-axis">
        {TEXTS.legend.target}
      </text>

      <path d={EU_DIAMOND} transform={`translate(${otherX + 110},26)`} fill={EU_COLOR} />
      <text x={otherX + 122} y={30} className="chart-axis">
        {TEXTS.legend.eu}
      </text>
    </svg>
  );
}

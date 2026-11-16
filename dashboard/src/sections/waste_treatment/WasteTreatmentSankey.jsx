// Sankey of what happens to the municipal waste generated per person, for one geography chosen
// with a search box (the EU27 by default), in the latest year with data for all 27 Member States.
//
// Left: one node, the waste generated (kg per person a year). Right: the levels of the waste
// hierarchy in a fixed order, best to worst (preparing for re-use, recycling, other recovery,
// disposal), then "not in the figures". Recycling and disposal each receive two bands
// (material recycling and composting and digestion; burnt without energy recovery and
// landfill). Prevention is never a node: prevented waste is not generated.
//
// Colours follow the RdYlBu scale of the distance-to-target chart (decision 16 Nov 2026): blue
// for re-use and recycling, pale yellow for energy recovery, red for disposal; "not in the
// figures" is hatched grey, outside the scale. The source node is waste orange.
//
// Missing values are never drawn as zero: a level without a figure (null in the data) keeps its
// slot as an empty dashed box labelled "Not reported" ("No EU figure" for re-use in the EU27).
// A negative "not in the figures" (more treated than generated, e.g. Portugal) gets no band.
//
// Data: municipal_waste_treatment.json (*_kg_pc and *_pct columns); texts:
// dashboard_texts.json (waste_treatment). d3-sankey computes the layout; React renders it.
import { group } from "d3-array";
import { sankey, sankeyJustify, sankeyLinkHorizontal } from "d3-sankey";
import { useMemo, useState } from "react";

import { EU27_TOTAL, dashboardTexts, geoNames, municipalWasteTreatment } from "../../data.js";
import { flagUrl } from "../../lib/flags.js";
import { KEY_FIGURES, fill } from "../../lib/keyFigures.js";

const TEXTS = dashboardTexts.waste_treatment;
const YEAR = Number(KEY_FIGURES.year);

const MARGIN = { top: 12, right: 250, bottom: 12, left: 150 };
const HEIGHT = 460;
const NARROW = 560; // px: below this width, shorter labels (no bands) and the source label on top
const MARGIN_NARROW = { top: 64, right: 132, bottom: 12, left: 4 };
const HEIGHT_NARROW = 480;
const NODE_WIDTH = 16;
const NODE_PADDING = 22;
const MISSING_SLOT = 10; // px, height of the dashed box of a level without a figure
const LINE = 17; // px, line height of the labels on the right
const LINK_OPACITY = 0.7;
const FADE_OPACITY = 0.12;
// levels whose label also shows the share of the waste generated (user, 16 Nov 2026)
const SHARE_LEVELS = ["recycling", "energy_recovery", "disposal"];
const CARD_WIDTH = 300; // px, also set in index.css (.hover-card-sankey)

const INK = "#1a1a1a";
const MUTED = "#5c5c5c";
const SOURCE_COLOR = "#e36f25"; // waste orange
const HATCH_COLOR = "#8a8a8a";

// Levels on the right, best to worst. key: node id; bands: [column prefix, colour], top to
// bottom; total: the column of the level total (kg per person: `${total}_kg_pc`).
const LEVELS = [
  { key: "prep_reuse", total: "prep_reuse", bands: [["prep_reuse", "#313695"]] },
  {
    key: "recycling",
    total: "recycling",
    bands: [
      ["recycling_material", "#4575b4"],
      ["recycling_compost", "#74add1"],
    ],
  },
  { key: "energy_recovery", total: "energy_recovery", bands: [["energy_recovery", "#fee090"]] },
  {
    key: "disposal",
    total: "disposal",
    bands: [
      ["incineration", "#d73027"],
      ["landfill", "#a50026"],
    ],
  },
  { key: "unaccounted", total: "unaccounted", bands: [["unaccounted", "url(#sankey-hatch)"]] },
];

// --- data preparation (runs once) -------------------------------------------------------

const ROW_BY_GEO = Object.fromEntries(
  [...group(municipalWasteTreatment.filter((d) => d.year === YEAR), (d) => d.geo)].map(
    ([geo, rows]) => [geo, rows[0]],
  ),
);

// Search options: the EU27 first, then the Member States by name.
const OPTIONS = [
  { geo: EU27_TOTAL, name: geoNames[EU27_TOTAL] },
  ...Object.keys(ROW_BY_GEO)
    .filter((geo) => geo !== EU27_TOTAL)
    .map((geo) => ({ geo, name: geoNames[geo] ?? geo }))
    .sort((a, b) => a.name.localeCompare(b.name)),
];
const GEO_BY_NAME = Object.fromEntries(OPTIONS.map((o) => [o.name.toLowerCase(), o.geo]));

const fmt = (v, digits) =>
  v.toLocaleString("en-GB", { minimumFractionDigits: digits, maximumFractionDigits: digits });
// labels: whole kg, one decimal under 10 kg so small flows don't read as 0
const kgLabel = (v) => fmt(v, Math.abs(v) < 10 ? 1 : 0);

// Layout input for one geography: nodes and links in a fixed order. A band with no value
// (null) or a value of 0 or less gets no link.
function sankeyInput(row) {
  const nodes = [{ id: "source" }, ...LEVELS.map((l) => ({ id: l.key }))];
  const links = LEVELS.flatMap((level) =>
    level.bands
      .map(([band, color]) => ({ source: "source", target: level.key, band, color, value: row[`${band}_kg_pc`] }))
      .filter((l) => l.value != null && l.value > 0),
  );
  return { nodes, links };
}

// Spread label blocks vertically so they don't overlap (keeps their order), within [0, maxY].
function spreadLabels(items, maxY) {
  const out = items.map((d) => ({ ...d, top: Math.max(0, d.y - d.height / 2) }));
  for (let i = 1; i < out.length; i += 1) {
    out[i].top = Math.max(out[i].top, out[i - 1].top + out[i - 1].height + 4);
  }
  const overflow = out.length ? out[out.length - 1].top + out[out.length - 1].height - maxY : 0;
  if (overflow > 0) {
    for (let i = out.length - 1; i >= 0; i -= 1) {
      const limit = i === out.length - 1 ? maxY - out[i].height : out[i + 1].top - out[i].height - 4;
      out[i].top = Math.min(out[i].top, limit);
    }
  }
  return out;
}

// --- chart -------------------------------------------------------------------------------

export default function WasteTreatmentSankey({ width }) {
  const [selected, setSelected] = useState(EU27_TOTAL);
  const [searchQuery, setSearchQuery] = useState("");
  const [hovered, setHovered] = useState(null); // level key

  const narrow = width < NARROW;
  const margin = narrow ? MARGIN_NARROW : MARGIN;
  const height = narrow ? HEIGHT_NARROW : HEIGHT;
  const boundsWidth = width - margin.left - margin.right;
  const boundsHeight = height - margin.top - margin.bottom;

  const row = ROW_BY_GEO[selected];
  const isEU = selected === EU27_TOTAL;
  const name = geoNames[selected] ?? selected;

  const layout = useMemo(() => {
    const generator = sankey()
      .nodeId((d) => d.id)
      .nodeAlign(sankeyJustify)
      .nodeWidth(NODE_WIDTH)
      .nodePadding(NODE_PADDING)
      .nodeSort(null)
      .linkSort(null)
      .iterations(0)
      .extent([
        [0, 0],
        [boundsWidth, boundsHeight],
      ]);
    // d3-sankey changes the objects it receives: give it fresh copies on each render
    return generator(sankeyInput(row));
  }, [row, boundsWidth, boundsHeight]);

  const nodeById = Object.fromEntries(layout.nodes.map((n) => [n.id, n]));
  const source = nodeById.source;

  // value of a column (kg per person or %), null if missing
  const value = (column, unit = "kg_pc") => row[`${column}_${unit}`] ?? null;

  // What a level shows: "value", "missing" (null: dashed box) or "none" (0 or less: no band).
  const levelState = (level) => {
    const v = value(level.total);
    if (v == null) return "missing";
    return v > 0 ? "value" : "none";
  };
  const missingText = (level) =>
    isEU && level.key === "prep_reuse" ? TEXTS.no_eu_figure : TEXTS.missing;

  // label blocks on the right, one per level
  const labels = spreadLabels(
    LEVELS.map((level) => {
      const node = nodeById[level.key];
      const state = levelState(level);
      // wide screens: name and value, the level's one-line definition, then its bands (if two)
      const showBands = !narrow && state === "value" && level.bands.length > 1;
      const lines = narrow ? 2 : 2 + (showBands ? level.bands.length : 0);
      return {
        level,
        state,
        showBands,
        y: (node.y0 + node.y1) / 2,
        nodeY: (node.y0 + node.y1) / 2,
        height: lines * LINE,
      };
    }),
    boundsHeight,
  );

  // Typing an exact name (or picking a suggestion) selects it; clearing the box goes back to
  // the EU27. Anything else keeps the current selection.
  const onSearch = (text) => {
    setSearchQuery(text);
    const query = text.trim().toLowerCase();
    if (!query) setSelected(EU27_TOTAL);
    else if (GEO_BY_NAME[query]) setSelected(GEO_BY_NAME[query]);
  };

  const hoverProps = (key) => ({
    onPointerEnter: () => setHovered(key),
    onPointerLeave: () => setHovered(null),
    onClick: () => setHovered((h) => (h === key ? null : key)),
  });

  const caption = fill(TEXTS.caption, { name });
  const countryNote = TEXTS.country_notes[selected];
  const reuseNote = isEU
    ? TEXTS.notes.reuse_missing_eu
    : value("prep_reuse") == null
      ? fill(TEXTS.notes.reuse_missing_country, { name })
      : null;
  const hoveredLevel = LEVELS.find((l) => l.key === hovered);

  return (
    <figure className="sankey-chart">
      <div className="chart-controls">
        <input
          type="search"
          list="waste-treatment-countries"
          placeholder={dashboardTexts.ui.search_placeholder}
          value={searchQuery}
          onChange={(e) => onSearch(e.target.value)}
          aria-label={dashboardTexts.ui.search_aria}
        />
        <datalist id="waste-treatment-countries">
          {OPTIONS.map((o) => (
            <option key={o.geo} value={o.name} />
          ))}
        </datalist>
      </div>

      <figcaption className="chart-caption">{caption}</figcaption>

      <div className="chart-hover-area">
        <svg width={width} height={height} role="img" aria-label={fill(TEXTS.aria_label, { name })}>
          <defs>
            <pattern id="sankey-hatch" width={6} height={6} patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
              <rect width={6} height={6} fill="#ffffff" />
              <line x1={0} y1={0} x2={0} y2={6} stroke={HATCH_COLOR} strokeWidth={2} />
            </pattern>
          </defs>

          <g transform={`translate(${margin.left},${margin.top})`} key={selected} className="fade-in">
            {/* bands */}
            {layout.links.map((link) => (
              <path
                key={link.band}
                d={sankeyLinkHorizontal()(link)}
                fill="none"
                stroke={link.color}
                strokeWidth={Math.max(1, link.width)}
                strokeOpacity={hovered && hovered !== link.target.id ? FADE_OPACITY : LINK_OPACITY}
                className="sankey-link"
                {...hoverProps(link.target.id)}
              />
            ))}

            {/* source node and its label */}
            <rect x={source.x0} y={source.y0} width={NODE_WIDTH} height={source.y1 - source.y0} fill={SOURCE_COLOR} />
            <SourceLabel node={source} kg={value("mw")} narrow={narrow} />

            {/* level nodes */}
            {LEVELS.map((level) => {
              const node = nodeById[level.key];
              const state = levelState(level);
              const mid = (node.y0 + node.y1) / 2;
              if (state === "missing" || state === "none") {
                return (
                  <rect
                    key={level.key}
                    x={node.x0}
                    y={mid - MISSING_SLOT / 2}
                    width={NODE_WIDTH}
                    height={MISSING_SLOT}
                    fill="#ffffff"
                    stroke={state === "missing" ? "#767676" : "#d9d9d9"}
                    strokeDasharray="3 2"
                    tabIndex={0}
                    onFocus={() => setHovered(level.key)}
                    onBlur={() => setHovered(null)}
                    {...hoverProps(level.key)}
                  />
                );
              }
              return (
                <g key={level.key}>
                  {level.bands.map(([band, color]) => {
                    const link = layout.links.find((l) => l.band === band);
                    if (!link) return null;
                    return (
                      <rect
                        key={band}
                        x={node.x0}
                        y={link.y1 - link.width / 2}
                        width={NODE_WIDTH}
                        height={Math.max(1, link.width)}
                        fill={color}
                      />
                    );
                  })}
                  <rect
                    x={node.x0}
                    y={node.y0}
                    width={NODE_WIDTH}
                    height={Math.max(1, node.y1 - node.y0)}
                    fill="none"
                    stroke={INK}
                    strokeOpacity={hovered === level.key ? 1 : 0.6}
                    tabIndex={0}
                    aria-label={`${TEXTS.levels[level.key]}: ${kgLabel(value(level.total))} kg`}
                    onFocus={() => setHovered(level.key)}
                    onBlur={() => setHovered(null)}
                    style={{ pointerEvents: "all" }}
                    {...hoverProps(level.key)}
                  />
                </g>
              );
            })}

            {/* labels on the right */}
            {labels.map((l) => (
              <LevelLabel
                key={l.level.key}
                label={l}
                x={boundsWidth + 8}
                nodeX={boundsWidth}
                value={value}
                missingText={missingText(l.level)}
                narrow={narrow}
                faded={hovered && hovered !== l.level.key}
              />
            ))}
          </g>
        </svg>

        {hoveredLevel && (
          <HoverCard
            level={hoveredLevel}
            state={levelState(hoveredLevel)}
            missingText={missingText(hoveredLevel)}
            value={value}
            geo={selected}
            name={name}
            narrow={narrow}
            x={margin.left + boundsWidth - NODE_WIDTH}
            y={margin.top + (nodeById[hoveredLevel.key].y0 + nodeById[hoveredLevel.key].y1) / 2}
            height={height}
          />
        )}
      </div>

      {countryNote && <p className="chart-note">{fill(countryNote)}</p>}

      <details className="chart-details">
        <summary>{dashboardTexts.ui.about_chart}</summary>
        <p className="chart-note">{fill(TEXTS.about, { name })}</p>
        <p className="chart-note">{TEXTS.notes.not_accounted}</p>
        {reuseNote && <p className="chart-note">{reuseNote}</p>}
        <p className="chart-note">{fill(TEXTS.notes.two_recycling)}</p>
      </details>

      <details className="chart-details">
        <summary>{TEXTS.table.show}</summary>
        <DataTable value={value} missingText={missingText} name={name} />
      </details>
    </figure>
  );
}

// "Waste generated" and the kg per person, left of the source node (above it on small screens).
function SourceLabel({ node, kg, narrow }) {
  const value = kg == null ? TEXTS.missing : fill(TEXTS.value, { kg: kgLabel(kg) });
  if (narrow) {
    return (
      // in the top margin, above every band
      <text x={node.x0} y={-40} className="sankey-label">
        <tspan className="sankey-source-name">{TEXTS.source}</tspan>
        <tspan x={node.x0} dy={22} className="sankey-source-value">
          {value}
        </tspan>
      </text>
    );
  }
  const mid = (node.y0 + node.y1) / 2;
  return (
    <text x={node.x0 - 10} y={mid - 10} textAnchor="end" className="sankey-label">
      <tspan className="sankey-source-name">{TEXTS.source}</tspan>
      <tspan x={node.x0 - 10} dy={28} className="sankey-source-value">
        {value}
      </tspan>
    </text>
  );
}

// Name and kg of a level, with its one-line definition and its bands below on wide screens (on
// small screens the definition is in the tap card); a short leader line when the label had to
// move away from its node.
function LevelLabel({ label, x, nodeX, value, missingText, narrow, faded }) {
  const { level, state, showBands, top, nodeY } = label;
  const total = value(level.total);
  const share = value(level.total, "pct");
  const valueText =
    state === "missing"
      ? missingText
      : state === "value"
        ? SHARE_LEVELS.includes(level.key) && share != null
          ? fill(TEXTS.value_share, { kg: kgLabel(total), share: fmt(share, 1) })
          : fill(TEXTS.value, { kg: kgLabel(total) })
        : "";
  const firstY = top + LINE * 0.75;
  const moved = Math.abs(top + LINE / 2 - nodeY) > 6;

  return (
    <g opacity={faded ? 0.45 : 1} className="sankey-level-label">
      {moved && <line x1={nodeX + 2} x2={x - 2} y1={nodeY} y2={top + LINE / 2} stroke="#d9d9d9" />}
      <text x={x} y={firstY} className="sankey-label">
        <tspan className={state === "value" ? "sankey-name" : "sankey-name is-muted"}>{TEXTS.levels[level.key]}</tspan>
        {narrow ? (
          <tspan x={x} dy={LINE} className={state === "value" ? "sankey-value" : "sankey-sub"}>
            {valueText}
          </tspan>
        ) : (
          <tspan dx={6} className={state === "value" ? "sankey-value" : "sankey-sub"}>
            {valueText}
          </tspan>
        )}
        {!narrow && (
          <tspan x={x} y={firstY + LINE} className="sankey-note">
            {TEXTS.level_notes[level.key]}
          </tspan>
        )}
        {showBands &&
          level.bands.map(([band], i) => {
            const v = value(band);
            const text = v != null ? `${TEXTS.bands[band]} ${kgLabel(v)} kg` : TEXTS.bands[band];
            return (
              <tspan key={band} x={x} y={firstY + LINE * (i + 2)} className="sankey-sub">
                {text}
              </tspan>
            );
          })}
      </text>
    </g>
  );
}

// Card of a level: flag and geography, level name, kg per person and % of waste generated, and
// one row per band. On small screens it sits under the chart.
function HoverCard({ level, state, missingText, value, geo, name, narrow, x, y, height }) {
  const flag = flagUrl(geo);
  const kg = value(level.total);
  const share = value(level.total, "pct");
  const style = narrow
    ? { position: "static", marginTop: 8 }
    : { left: Math.max(0, x - CARD_WIDTH - 16), top: Math.min(Math.max(0, y - 60), height - 160) };

  return (
    <div className="hover-card hover-card-sankey" style={style} role="status">
      <div className="hover-card-header">
        {flag && <img className="flag-circle" src={flag} alt="" />}
        <span className="hover-card-title">{name}</span>
      </div>
      <div className="hover-card-sub">{TEXTS.levels[level.key]}</div>
      <p className="hover-card-explain">
        {TEXTS.level_hover[level.key]}
        {geo === EU27_TOTAL && level.key === "unaccounted" && ` ${TEXTS.level_hover.unaccounted_eu}`}
      </p>
      {state === "missing" ? (
        <div className="hover-card-main">{missingText}</div>
      ) : (
        <>
          <div className="hover-card-main">{fill(TEXTS.hover.kg, { kg: fmt(kg, 1) })}</div>
          <div className="hover-card-sub">{fill(TEXTS.hover.share, { share: fmt(share, 1) })}</div>
          {level.bands.length > 1 && (
            <dl className="hover-card-values">
              {level.bands.map(([band]) => (
                <BandRow key={band} band={band} value={value} />
              ))}
            </dl>
          )}
        </>
      )}
    </div>
  );
}

function BandRow({ band, value }) {
  const v = value(band);
  return (
    <>
      <dt>{TEXTS.bands[band]}</dt>
      <dd>{v == null ? TEXTS.missing : `${fmt(v, 1)} kg`}</dd>
    </>
  );
}

// The same figures as a table: one row per band, grouped by level.
function DataTable({ value, missingText, name }) {
  const [hLevel, hBand, hKg, hPct] = TEXTS.table.headers;
  const cell = (v) => (v == null ? null : fmt(v, 1));
  return (
    <table className="chart-table">
      <caption className="visually-hidden">{fill(TEXTS.caption, { name })}</caption>
      <thead>
        <tr>
          <th scope="col">{hLevel}</th>
          <th scope="col">{hBand}</th>
          <th scope="col">{hKg}</th>
          <th scope="col">{hPct}</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">{TEXTS.source}</th>
          <td />
          <td>{cell(value("mw"))}</td>
          <td>100.0</td>
        </tr>
        {LEVELS.flatMap((level) =>
          level.bands.map(([band], i) => {
            const kg = value(band);
            const pct = value(band, "pct");
            return (
              <tr key={band}>
                {i === 0 && (
                  <th scope="row" rowSpan={level.bands.length}>
                    {TEXTS.levels[level.key]}
                  </th>
                )}
                <td>{level.bands.length > 1 || level.key === "energy_recovery" ? TEXTS.bands[band] : ""}</td>
                <td>{kg == null ? missingText(level) : cell(kg)}</td>
                <td>{pct == null ? missingText(level) : cell(pct)}</td>
              </tr>
            );
          }),
        )}
      </tbody>
    </table>
  );
}

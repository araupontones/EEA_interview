// The waste hierarchy as an inverted pyramid: five stacked trapezoids from the best option
// (prevention, widest, at the top) to the worst (disposal, narrowest, at the bottom); each step's
// bottom edge is as wide as the top edge of the next one. Step names, links, figures and notes
// come from data/lookups/dashboard_texts.json (hierarchy); figures are filled from the data
// (lib/keyFigures.js).
//
// size="large" (hero, closing panel): each step shows its name and its EU27 figure; a step
// covered by a section is a link to it and lights up on hover; steps without a section are
// greyed; steps without an EU figure show only their name. Under the pyramid: the share burnt
// without energy recovery (also disposal) and the share "not in the figures". Hovering a step
// shows its explanation.
// size="small" (section headings): a 40 px icon without labels; the step of the section
// (highlight) is filled in ink.
//
// Steps without data in the dashboard are never highlighted (communication.md, section 5).
import { dashboardTexts } from "../data.js";
import { fill } from "../lib/keyFigures.js";

const {
  steps,
  burnt: BURNT,
  not_accounted: NOT_ACCOUNTED,
  not_accounted_note: NOT_ACCOUNTED_NOTE,
} = dashboardTexts.hierarchy;
const TITLE = fill(dashboardTexts.hierarchy.title);

const COLORS = {
  ink: "#1a1a1a",
  covered: "#ffffff",
  uncovered: "#f2f2f2",
  iconCovered: "#d9d9d9",
  iconUncovered: "#ececec",
};

const NARROWING = 0.12; // each step is this share of the top width narrower than the one above

// Trapezoid of step i in a pyramid of the given width: top edge, bottom edge, height.
// Returns an SVG path with square corners.
function trapezoid(i, width, stepHeight, gap) {
  const top = width * (1 - i * NARROWING);
  const bottom = width * (1 - (i + 1) * NARROWING);
  const y = i * (stepHeight + gap);
  const xTop = (width - top) / 2;
  const xBottom = (width - bottom) / 2;
  return {
    d: `M ${xTop} ${y} H ${xTop + top} L ${xBottom + bottom} ${y + stepHeight} H ${xBottom} Z`,
    y,
    mid: width / 2,
  };
}

export default function HierarchyMotif({ size = "large", highlight = null, ...options }) {
  return size === "small" ? <SmallMotif highlight={highlight} /> : <LargeMotif {...options} />;
}

// LARGE: level height and gap in the hero-sized pyramid; the waste-hierarchy section passes
// taller levels so its explanations fit next to each level (fixed = drawn at 1:1, not scaled).
export const LARGE = { width: 360, stepHeight: 58, gap: 4 };

function LargeMotif({ stepHeight = LARGE.stepHeight, gap = LARGE.gap, notes = true, fixed = false }) {
  const width = LARGE.width;
  const height = steps.length * (stepHeight + gap) - gap;

  return (
    <div className="hierarchy-large">
      <svg
        className="hierarchy-motif"
        viewBox={`0 0 ${width} ${height}`}
        width={fixed ? width : "100%"}
        height={fixed ? height : undefined}
        role="list"
        aria-label={TITLE}
      >
        {steps.map((step, i) => {
          const { d, y, mid } = trapezoid(i, width, stepHeight, gap);
          const covered = step.section != null;
          const value = fill(step.value);
          const content = (
            <g className={covered ? "hierarchy-step hierarchy-step-covered" : "hierarchy-step hierarchy-step-uncovered"}>
              <title>{step.explanation}</title>
              <path
                d={d}
                fill={covered ? COLORS.covered : COLORS.uncovered}
                stroke={covered ? COLORS.ink : "none"}
                strokeWidth={1.5}
                strokeLinejoin="miter"
              />
              <text
                x={mid}
                y={y + (value ? stepHeight / 2 - 9 : stepHeight / 2)}
                textAnchor="middle"
                dominantBaseline="middle"
                className="hierarchy-name"
              >
                {step.name}
                {covered && (
                  <tspan className="arrow" aria-hidden="true" dx="4">
                    {"↓︎"}
                  </tspan>
                )}
              </text>
              {value && (
                <text
                  x={mid}
                  y={y + stepHeight / 2 + 13}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  className="hierarchy-value"
                >
                  {value}
                </text>
              )}
            </g>
          );
          return (
            <g key={step.key} role="listitem">
              {covered ? (
                <a href={`#${step.section}`} aria-label={step.name}>
                  {content}
                </a>
              ) : (
                content
              )}
            </g>
          );
        })}
      </svg>
      {notes && BURNT && <p className="hierarchy-not-accounted">{fill(BURNT)}</p>}
      {notes && (
        <p className="hierarchy-not-accounted" title={NOT_ACCOUNTED_NOTE}>
          {fill(NOT_ACCOUNTED)} <span className="hierarchy-info">ⓘ</span>
        </p>
      )}
    </div>
  );
}

function SmallMotif({ highlight }) {
  const width = 40;
  const stepHeight = 5;
  const gap = 1;
  const height = steps.length * (stepHeight + gap) - gap;
  const name = steps.find((s) => s.key === highlight)?.name;
  return (
    <svg
      className="hierarchy-icon"
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      role="img"
      aria-label={name ? `${TITLE}: ${name}` : TITLE}
    >
      {steps.map((step, i) => {
        const isHighlight = step.key === highlight;
        return (
          <path
            key={step.key}
            d={trapezoid(i, width, stepHeight, gap).d}
            fill={isHighlight ? COLORS.ink : step.section ? COLORS.iconCovered : COLORS.iconUncovered}
          />
        );
      })}
    </svg>
  );
}

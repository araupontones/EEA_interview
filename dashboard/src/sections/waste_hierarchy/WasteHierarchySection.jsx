// The waste hierarchy: introduction after the hero. The pyramid with the EU figures on the left;
// next to each level, its explanation and, for levels with their own section, a link to it.
// Under it: the share burnt without energy recovery and the share "not in the figures", with
// its explanation visible. Texts from data/lookups/dashboard_texts.json (hierarchy,
// sections["waste-hierarchy"]); figures filled from the data (lib/keyFigures.js).
import HierarchyMotif, { LARGE } from "../../components/HierarchyMotif.jsx";
import Section from "../../components/Section.jsx";
import { dashboardTexts } from "../../data.js";
import { fill } from "../../lib/keyFigures.js";

const { steps, burnt, not_accounted: notAccounted, not_accounted_note: notAccountedNote } =
  dashboardTexts.hierarchy;
const SEE_ALSO = dashboardTexts.sections["waste-hierarchy"].see_also;

const STEP_HEIGHT = 76; // px: taller levels than in the closing panel, so two lines fit beside
const GAP = 6;

export default function WasteHierarchySection() {
  return (
    <Section id="waste-hierarchy">
      <div
        className="hierarchy-explained"
        style={{ "--level-height": `${STEP_HEIGHT}px`, "--level-gap": `${GAP}px` }}
      >
        <HierarchyMotif size="large" stepHeight={STEP_HEIGHT} gap={GAP} notes={false} fixed />
        <ol className="hierarchy-levels" style={{ width: undefined }}>
          {steps.map((step) => {
            const target = step.section && dashboardTexts.sections[step.section];
            return (
              <li key={step.key} className={step.section ? "level level-covered" : "level"}>
                <span className="level-name">
                  {step.name}
                  {step.value && <> · {fill(step.value)}</>}
                </span>
                <span className="level-explanation">{step.explanation}</span>
                {target && (
                  <a className="level-link" href={`#${step.section}`}>
                    {SEE_ALSO.replace("{title}", target.title)}
                  </a>
                )}
              </li>
            );
          })}
        </ol>
      </div>
      <div className="hierarchy-notes" style={{ maxWidth: `${LARGE.width * 2}px` }}>
        {burnt && <p className="chart-note">{fill(burnt)}.</p>}
        <p className="chart-note">
          <strong>{fill(notAccounted)}.</strong> {notAccountedNote}
        </p>
      </div>
    </Section>
  );
}

// Closing panel: back to the waste hierarchy after the charts. No new facts.
// Texts come from data/lookups/dashboard_texts.json (closing); figures from lib/keyFigures.js.
import HierarchyMotif from "../../components/HierarchyMotif.jsx";
import { dashboardTexts } from "../../data.js";
import { fill } from "../../lib/keyFigures.js";

const { closing } = dashboardTexts;

export default function ClosingPanel() {
  return (
    <section id="closing" className="closing">
      <div className="closing-text">
        <span className="eyebrow">{closing.eyebrow}</span>
        <h2>{closing.title}</h2>
        <p className="lede">{fill(closing.text)}</p>
        <a className="cta" href="#top">
          {closing.cta} <span aria-hidden="true">↑</span>
        </a>
      </div>
      <div className="closing-motif">
        <HierarchyMotif size="large" />
      </div>
    </section>
  );
}

// Shared wrapper for every section: anchor id, header (small hierarchy icon, eyebrow, question
// title, key message, lede and "try this" hint) and the section content. Texts come from
// data/lookups/dashboard_texts.json (sections[id]); figures in braces are filled from the data
// (lib/keyFigures.js). The hierarchy step of the section is highlighted in the icon.
import { dashboardTexts } from "../data.js";
import { fill } from "../lib/keyFigures.js";
import HierarchyMotif from "./HierarchyMotif.jsx";

export default function Section({ id, className = "", children }) {
  const texts = dashboardTexts.sections[id] ?? {};
  return (
    <section id={id} className={`section ${className}`.trim()}>
      <header className="section-header">
        <div className="eyebrow-row">
          {texts.step && <HierarchyMotif size="small" highlight={texts.step} />}
          {texts.eyebrow && <span className="eyebrow">{texts.eyebrow}</span>}
        </div>
        <h2>{texts.title}</h2>
        {texts.key_message && <p className="key-message">{fill(texts.key_message)}</p>}
        {texts.lede && <p className="lede">{fill(texts.lede)}</p>}
        {texts.try && <p className="try-hint">{fill(texts.try)}</p>}
      </header>
      {children}
    </section>
  );
}

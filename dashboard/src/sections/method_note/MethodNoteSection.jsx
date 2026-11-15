// Methodological note: plain-language summary of sources, definitions and caveats
// (docs/method_notes.md, docs/findings.md). Texts from data/lookups/dashboard_texts.json.
import Section from "../../components/Section.jsx";
import { dashboardTexts } from "../../data.js";

export default function MethodNoteSection() {
  return (
    <Section id="method-note" className="section-end">
      <div className="end-body">
        {dashboardTexts.method_note.map((p) => (
          <p key={p.lead} className="end-paragraph">
            <strong>{p.lead}</strong> {p.text}
          </p>
        ))}
      </div>
    </Section>
  );
}

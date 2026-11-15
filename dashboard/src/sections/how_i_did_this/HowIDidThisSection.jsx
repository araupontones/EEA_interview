// How I did this: the data pipeline, tools and the AI agents used to build the project.
// Texts from data/lookups/dashboard_texts.json (how_i_did_this, how_i_did_this_links).
import Section from "../../components/Section.jsx";
import { dashboardTexts } from "../../data.js";

const links = dashboardTexts.how_i_did_this_links;

export default function HowIDidThisSection() {
  return (
    <Section id="how-i-did-this" className="section-end">
      {dashboardTexts.how_i_did_this.map((p) => (
        <p key={p.lead} className="end-paragraph">
          <strong>{p.lead}</strong> {p.text}
        </p>
      ))}
      <p className="end-paragraph end-links">
        {links.map((link, i) => (
          <span key={link.url}>
            {i > 0 && " · "}
            <a href={link.url} target="_blank" rel="noreferrer">
              {link.text}
            </a>
          </span>
        ))}
      </p>
    </Section>
  );
}

// Hero: eyebrow, headline, lede, a link to the first section and three key-number cards, next
// to the waste hierarchy (large, interactive). Texts come from data/lookups/dashboard_texts.json
// (hero, hierarchy); figures are filled from the data (lib/keyFigures.js).
import HierarchyMotif from "../../components/HierarchyMotif.jsx";
import { dashboardTexts } from "../../data.js";
import { fill } from "../../lib/keyFigures.js";

const { hero, hierarchy } = dashboardTexts;
// the button leads to the first section of the page (the first one in dashboard_texts.sections)
const FIRST_SECTION = Object.keys(dashboardTexts.sections)[0];

export default function Hero() {
  return (
    <header className="hero" id="top">
      <div className="hero-text">
        <span className="eyebrow">{hero.eyebrow}</span>
        <h1>{hero.title}</h1>
        <p className="lede">{fill(hero.lede)}</p>
        {FIRST_SECTION && (
          <a className="cta" href={`#${FIRST_SECTION}`}>
            {hero.cta} <span aria-hidden="true">↓</span>
          </a>
        )}
        <ul className="hero-cards">
          {hero.cards.map((card) => (
            <li key={card.value} className="hero-card">
              <span className="hero-card-value">{fill(card.value)}</span>
              <span className="hero-card-label">{fill(card.label)}</span>
            </li>
          ))}
        </ul>
      </div>
      <div className="hero-motif">
        <p className="hero-motif-title">{fill(hierarchy.title)}</p>
        <p className="hero-motif-intro">{hierarchy.intro}</p>
        <HierarchyMotif size="large" />
      </div>
    </header>
  );
}

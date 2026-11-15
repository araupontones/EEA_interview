// Hero: eyebrow, headline, lede (with its key figures in bold), byline and a link to the first section
// (the waste hierarchy). Texts come from data/lookups/dashboard_texts.json (hero); figures are filled from the data (lib/keyFigures.js).
import { dashboardTexts } from "../../data.js";
import { fill } from "../../lib/keyFigures.js";

const { hero } = dashboardTexts;
// the button leads to the first section of the page (the first one in dashboard_texts.sections)
const FIRST_SECTION = Object.keys(dashboardTexts.sections)[0];

export default function Hero() {
  return (
    <header className="hero" id="top">
      <div className="hero-text">
        <span className="eyebrow">{hero.eyebrow}</span>
        <h1>{hero.title}</h1>
        <p className="lede">
          {hero.lede.map((part, i) =>
            part.figure ? (
              <strong key={i} className="hero-figure">
                {fill(part.figure)}
              </strong>
            ) : (
              <span key={i}>{fill(part.text)}</span>
            ),
          )}
        </p>
        {hero.byline && (
          <div className="byline">
            <p>
              By{" "}
              <a href={hero.byline.url} target="_blank" rel="noreferrer">
                {hero.byline.author}
              </a>{" "}
              · {hero.byline.date}
            </p>
            <p className="byline-data">{fill(hero.byline.data_note)}</p>
          </div>
        )}
        {FIRST_SECTION && (
          <a className="cta" href={`#${FIRST_SECTION}`}>
            {hero.cta} <span className="arrow" aria-hidden="true">{"↓︎"}</span>
          </a>
        )}
      </div>
    </header>
  );
}

// Source lines shown under a chart: the Eurostat datasets it uses (linked to the Eurostat data
// browser), when Eurostat last updated them and when they were downloaded; and, for charts that
// show the recycling targets, the legal acts that set them (linked to EUR-Lex).
// Texts and dates come from data/lookups/data_sources.json (scripts/lookups/create_data_sources.py);
// `chart` is the chart id used there (e.g. "decoupling").
import { dataSources } from "../data.js";

export default function ChartSource({ chart }) {
  const source = dataSources[chart];
  if (!source) return null;

  return (
    <div className="chart-source">
      <p>
        {source.prefix}:{" "}
        {source.datasets.map((d, i) => (
          <span key={d.code}>
            {i > 0 && "; "}
            <a href={d.url} target="_blank" rel="noreferrer">
              {d.label}
            </a>{" "}
            {d.text}
          </span>
        ))}
        .
      </p>
      {source.targets && (
        <p>
          {source.targets.prefix}:{" "}
          {source.targets.acts.map((act, i) => (
            <span key={act.label}>
              {i > 0 && "; "}
              <a href={act.url} target="_blank" rel="noreferrer">
                {act.label}
              </a>
            </span>
          ))}
          .
        </p>
      )}
    </div>
  );
}

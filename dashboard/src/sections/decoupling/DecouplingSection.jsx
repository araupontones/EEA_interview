// Decoupling: municipal waste and real GDP per person, indexed to 2011 = 100, with a
// country search box and the notes under the chart.
// Data: municipalWasteDecoupling (data/processed/municipal_waste_decoupling.json),
//       decouplingNotes (data/lookups/decoupling_notes.json), geoNames.
import ChartSource from "../../components/ChartSource.jsx";
import Section from "../../components/Section.jsx";
import { useContainerWidth } from "../../lib/useContainerWidth.js";
import DecouplingLineChart from "./DecouplingLineChart.jsx";

export default function DecouplingSection() {
  const [ref, width] = useContainerWidth();

  return (
    <Section id="decoupling">
      <div className="chart-panel" ref={ref}>{width > 0 && <DecouplingLineChart width={width} />}</div>
      <ChartSource chart="decoupling" />
    </Section>
  );
}

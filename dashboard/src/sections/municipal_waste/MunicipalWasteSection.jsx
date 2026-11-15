// Municipal waste generation: distribution of municipal waste per person between the
// 27 EU Member States, with the EU27 as reference.
// Data: municipalWaste (data/processed/municipal_waste.json),
//       municipalWasteNotes (data/lookups/municipal_waste_notes.json), geoNames.
import ChartSource from "../../components/ChartSource.jsx";
import Section from "../../components/Section.jsx";
import { useContainerWidth } from "../../lib/useContainerWidth.js";
import WastePerCapitaBarChart from "./WastePerCapitaBarChart.jsx";

export default function MunicipalWasteSection() {
  const [ref, width] = useContainerWidth();

  return (
    <Section id="municipal-waste">
      <div className="chart-panel" ref={ref}>{width > 0 && <WastePerCapitaBarChart width={width} />}</div>
      <ChartSource chart="municipal_waste" />
    </Section>
  );
}

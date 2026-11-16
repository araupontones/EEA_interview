// Where the waste generated per person ends up: a sankey from the waste generated to the levels
// of the waste hierarchy, with a country search box, notes and a table version.
// Data: municipalWasteTreatment (data/processed/municipal_waste_treatment.json); texts:
// dashboardTexts.waste_treatment and dashboardTexts.sections["waste-treatment"].
import ChartSource from "../../components/ChartSource.jsx";
import Section from "../../components/Section.jsx";
import { useContainerWidth } from "../../lib/useContainerWidth.js";
import WasteTreatmentSankey from "./WasteTreatmentSankey.jsx";

export default function WasteTreatmentSection() {
  const [ref, width] = useContainerWidth();

  return (
    <Section id="waste-treatment">
      <div className="chart-panel" ref={ref}>{width > 0 && <WasteTreatmentSankey width={width} />}</div>
      <ChartSource chart="waste_treatment" />
    </Section>
  );
}

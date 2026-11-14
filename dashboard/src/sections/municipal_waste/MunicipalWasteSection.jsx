// Municipal waste generation: distribution of municipal waste per person between the
// 27 EU Member States, with the EU27 as reference.
// Data: municipalWaste (data/processed/municipal_waste.json).
import ChartPlaceholder from "../../components/ChartPlaceholder.jsx";
import Section from "../../components/Section.jsx";

export default function MunicipalWasteSection() {
  return (
    <Section id="municipal-waste" title="Municipal waste generation">
      <p>To do: text.</p>
      <ChartPlaceholder label="Bar chart: municipal waste per person by country (WastePerCapitaBarChart)" />
    </Section>
  );
}

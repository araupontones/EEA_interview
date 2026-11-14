// Decoupling: municipal waste and real GDP per person, indexed to 2011 = 100, with a
// country dropdown and the notes under the chart.
// Data: municipalWasteDecoupling (data/processed/municipal_waste_decoupling.json),
//       decouplingNotes (data/lookups/decoupling_notes.json), geoNames.
import ChartPlaceholder from "../../components/ChartPlaceholder.jsx";
import Section from "../../components/Section.jsx";

export default function DecouplingSection() {
  return (
    <Section id="decoupling" title="Decoupling">
      <p>To do: text and country dropdown.</p>
      <ChartPlaceholder label="Line chart: waste and GDP indexes, 2011 = 100 (DecouplingLineChart)" />
      <p>To do: notes under the chart.</p>
    </Section>
  );
}

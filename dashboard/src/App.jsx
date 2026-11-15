// The dashboard page: the sections in reading order. Each section lives in its own folder
// in src/sections/, with its chart next to it.
import ClosingPanel from "./sections/closing/ClosingPanel.jsx";
import DecouplingSection from "./sections/decoupling/DecouplingSection.jsx";
import DistanceToTargetSection from "./sections/distance_to_target/DistanceToTargetSection.jsx";
import Hero from "./sections/hero/Hero.jsx";
import HowIDidThisSection from "./sections/how_i_did_this/HowIDidThisSection.jsx";
import MethodNoteSection from "./sections/method_note/MethodNoteSection.jsx";
import MunicipalWasteSection from "./sections/municipal_waste/MunicipalWasteSection.jsx";
import WasteHierarchySection from "./sections/waste_hierarchy/WasteHierarchySection.jsx";

export default function App() {
  return (
    <main>
      <Hero />
      <WasteHierarchySection />
      <MunicipalWasteSection />
      <DecouplingSection />
      <DistanceToTargetSection />
      <ClosingPanel />
      <MethodNoteSection />
      <HowIDidThisSection />
    </main>
  );
}

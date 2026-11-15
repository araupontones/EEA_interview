// Distance to target: recycling rates against the 2025 targets.
// Data: recyclingDistanceToTarget (data/processed/recycling_distance_to_target.json),
//       recyclingTargets (data/lookups/recycling_targets.json), geoNames.
import ChartSource from "../../components/ChartSource.jsx";
import Section from "../../components/Section.jsx";
import { useContainerWidth } from "../../lib/useContainerWidth.js";
import DistanceToTargetScatter from "./DistanceToTargetScatter.jsx";

export default function DistanceToTargetSection() {
  const [ref, width] = useContainerWidth();

  return (
    <Section id="distance-to-target">
      <div className="chart-card" ref={ref}>{width > 0 && <DistanceToTargetScatter width={width} />}</div>
      <ChartSource chart="distance_to_target" />
    </Section>
  );
}

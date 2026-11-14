// The only module that loads data. Every chart imports its data from here.
//
// The JSON files are written by the Python pipeline (scripts/run_pipeline.py) in the
// repository's data/ folder. Vite bundles them into the app at build time ("@data" is an
// alias for data/, set in vite.config.js), so the published dashboard always matches the
// data in the commit it was built from. Column names are documented in the scripts that
// write each file and in the README.
//
// If the data grows to several MB, switch to fetch() from dashboard/public/data/ here;
// the charts do not need to change.

// processed data: the 27 EU Member States and EU27_2020 only
import municipalWaste from "@data/processed/municipal_waste.json";
import municipalWasteDecoupling from "@data/processed/municipal_waste_decoupling.json";
import recyclingDistanceToTarget from "@data/processed/recycling_distance_to_target.json";

// lookups
import decouplingNotes from "@data/lookups/decoupling_notes.json";
import geoNames from "@data/lookups/geo_eu27.json";
import recyclingTargets from "@data/lookups/recycling_targets.json";

export const EU27_TOTAL = "EU27_2020";

export {
  decouplingNotes,
  geoNames,
  municipalWaste,
  municipalWasteDecoupling,
  recyclingDistanceToTarget,
  recyclingTargets,
};

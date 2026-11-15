// Flag images for the geographies in the dashboard (the 27 Member States and the EU27).
//
// The images are the square (1x1) SVG flags of the flag-icons npm package (MIT licence,
// version pinned in package.json). The geography -> flag code mapping comes from
// data/lookups/geo_flags.json (built by scripts/lookups/create_geo_flags.py), so Eurostat
// codes that differ from ISO codes (EL -> gr, EU27_2020 -> eu) are handled in the pipeline.
//
// Only the flags listed in the pattern below are bundled, not the 271 flags of the package.
// The pattern must be a literal, so it repeats the flag codes of geo_flags.json; if a code is
// missing here, flagUrl() returns null and a warning is printed in the browser console.
import { geoFlags } from "../data.js";

const FILES = import.meta.glob(
  "../../node_modules/flag-icons/flags/1x1/{at,be,bg,cy,cz,de,dk,ee,es,eu,fi,fr,gr,hr,hu,ie,it,lt,lu,lv,mt,nl,pl,pt,ro,se,si,sk}.svg",
  { eager: true, query: "?url", import: "default" },
);

const URLS = Object.fromEntries(
  Object.entries(FILES).map(([path, url]) => [path.split("/").pop().replace(".svg", ""), url]),
);

const missing = Object.entries(geoFlags).filter(([, code]) => !URLS[code]);
if (missing.length > 0) {
  console.warn("flags.js: no flag image for", Object.fromEntries(missing));
}

// URL of the flag of a geography code (e.g. "AT", "EU27_2020"), or null if there is none.
export function flagUrl(geo) {
  return URLS[geoFlags[geo]] ?? null;
}

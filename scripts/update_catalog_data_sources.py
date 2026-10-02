import json
import logging
from pathlib import Path
import pandas as pd

log = logging.getLogger(__name__)

RAW = Path("data/raw")
CATALOG = Path("data/catalog/raw_sources.csv")

def build_raw_catalog() -> pd.DataFrame:
    rows = []
    for folder in sorted(p for p in RAW.iterdir() if p.is_dir()):
        meta_path = folder / "metadata.json"
        lookup_path = folder / "lookup.json"

        if not meta_path.exists():
            log.warning("%s: no metadata.json, folder is incomplete", folder.name)
            rows.append({"source_code": folder.name, "status": "incomplete"})
            continue

        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)

        lookups = {}
        if lookup_path.exists():
            with open(lookup_path, encoding="utf-8") as f:
                lookups = json.load(f)

        rows.append({
            "source_code": folder.name,
            "label": meta.get("label"),
            "retrieved_at": meta.get("retrieved_at"),
            "source_updated": meta.get("updated"),
            "n_rows": meta.get("n_rows"),
            "n_dims": len(lookups),
            "dims": ", ".join(lookups),
            "status": "complete",

        })

    catalog = pd.DataFrame(rows)
    #CATALOG.parent.mkdir(parents=True, exist_ok=True)
    catalog.to_csv(CATALOG, index=False, encoding="utf-8")
    log.info("Catalog written: %d sources -> %s", len(catalog), CATALOG)
    return catalog

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    build_raw_catalog()
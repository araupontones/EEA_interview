"""
Update the catalog of raw data sources: one row per dataset folder in data/raw.

For each folder, reads metadata.json and lookup.json and records the dataset label,
when it was downloaded, when Eurostat last updated it, and its dimensions.
A folder without metadata.json is listed with status "incomplete".

Input:  data/raw/<dataset code>/metadata.json and lookup.json
Output: data/catalog/raw_sources.csv (overwritten on each run)

Run from anywhere, after downloading new data:
    .venv/Scripts/python scripts/raw/update_catalog_data_sources.py
"""

import json
import logging
from pathlib import Path
import pandas as pd
import pyarrow.parquet as pq

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]  # scripts/raw -> project root
RAW = ROOT / "data/raw"
CATALOG = ROOT / "data/catalog/raw_sources.csv"

def build_raw_catalog() -> pd.DataFrame:
    rows = []
    for folder in sorted(p for p in RAW.iterdir() if p.is_dir()):
        meta_path = folder / "metadata.json"
        lookup_path = folder / "lookup.json"
        data_path = folder / "df.parquet"

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

        # Number of rows, read from the parquet file's metadata (the data itself is not loaded)
        n_rows = pq.ParquetFile(data_path).metadata.num_rows if data_path.exists() else None

        rows.append({
            "source_code": folder.name,
            "label": meta.get("label"),
            "retrieved_at": meta.get("retrieved_at"),
            "source_updated": meta.get("updated"),
            "n_rows": n_rows,
            "n_dims": len(lookups),
            "dims": ", ".join(lookups),
            "status": "complete",

        })

    catalog = pd.DataFrame(rows)
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    catalog.to_csv(CATALOG, index=False, encoding="utf-8")
    log.info("Catalog written: %d sources -> %s", len(catalog), CATALOG)
    return catalog

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    build_raw_catalog()
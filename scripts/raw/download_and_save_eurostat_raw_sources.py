"""
Download the latest version of every Eurostat dataset in DATASET_CODES and save it in data/raw.

For each dataset, the data is downloaded from the Eurostat Statistics API (years 2010-2026,
countries plus EU-level totals such as EU27_2020) and saved in data/raw/<dataset code>/:
    df.parquet      the data, one row per observation
    lookup.json     code-to-label mapping for each dimension
    metadata.json   dataset label, last Eurostat update and download time
Existing files are overwritten.

If one dataset fails, the error is logged and the script continues with the next one.
It ends with exit code 1 if any dataset failed.

Run from anywhere:
    .venv/Scripts/python scripts/raw/download_and_save_eurostat_raw_sources.py

To add a dataset, add its Eurostat code to DATASET_CODES.
The download logic is in src/apiEurostat/ (pipeline.process).
"""

import logging
import sys
from apiEurostat.pipeline import process

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
                    )
log = logging.getLogger(__name__)

DATASET_CODES = [
    "env_wasmun",
    "env_wasobl",
    "env_waspacr",
    "env_wasflow",
    "env_waseleeos",
    "env_wasgen",
    "nama_10_pc",
    "demo_gind",
]

def main() -> int:
    failed = []
    for datasetCode in DATASET_CODES:
        try:
            process(datasetCode)
        except Exception:
            log.exception("%s failed", datasetCode)
            failed.append(datasetCode)
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
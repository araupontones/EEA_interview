# scripts/download_and_save_eurostat_raw_sources.py
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
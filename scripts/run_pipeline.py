"""
Rebuild all the data, running every script in the right order.

Steps (each script reads the outputs of the steps before it):
    1. raw        download_eurostat.py (only with --download), update_raw_catalog.py
    2. lookups    create_geo_eu27.py, create_recycling_targets.py
    3. interim    env_wasmun.py, env_waspacr.py
    4. processed  recycling_distance_to_target.py

By default the Eurostat download is skipped and the pipeline rebuilds everything from the
raw files already in data/raw. Use --download to fetch the latest Eurostat release first.
A new download can change the figures, because Eurostat revises past years.

The pipeline stops at the first script that fails.

Run from anywhere:
    .venv/Scripts/python scripts/run_pipeline.py
    .venv/Scripts/python scripts/run_pipeline.py --download
"""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent

DOWNLOAD = "raw/download_eurostat.py"
STEPS = [
    "raw/update_raw_catalog.py",
    "lookups/create_geo_eu27.py",
    "lookups/create_recycling_targets.py",
    "interim/env_wasmun.py",
    "interim/env_waspacr.py",
    "processed/recycling_distance_to_target.py",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild all the data.")
    parser.add_argument("--download", action="store_true",
                        help="download the latest data from Eurostat first")
    args = parser.parse_args()

    steps = ([DOWNLOAD] if args.download else []) + STEPS
    for i, step in enumerate(steps, start=1):
        print(f"\n[{i}/{len(steps)}] {step}", flush=True)
        result = subprocess.run([sys.executable, str(SCRIPTS / step)])
        if result.returncode != 0:
            print(f"\nFAILED: {step} (exit code {result.returncode}). Later steps were not run.")
            return 1

    print("\nPipeline finished.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

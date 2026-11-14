"""
Project paths, defined once and imported everywhere.

Usage:
    from paths import DIR_INTERIM, raw_dir, interim_file

    df = pd.read_parquet(interim_file("env_wasmun"))

All paths are absolute, so scripts and notebooks work from any working directory.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # src/paths -> project root

DATA = ROOT / "data"
DIR_RAW = DATA / "raw"
DIR_INTERIM = DATA / "interim"
DIR_PROCESSED = DATA / "processed"
DIR_LOOKUPS = DATA / "lookups"
DIR_CATALOG = DATA / "catalog"


def raw_dir(source: str) -> Path:
    """Folder of one raw Eurostat dataset, e.g. data/raw/env_wasmun."""
    return DIR_RAW / source


def interim_file(source: str) -> Path:
    """Interim parquet file of one dataset, e.g. data/interim/env_wasmun.parquet."""
    return DIR_INTERIM / f"{source}.parquet"

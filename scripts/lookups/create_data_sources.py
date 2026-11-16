"""
Create the source lines shown under each chart of the dashboard.

Every chart names the Eurostat datasets it uses, when Eurostat last updated each one, and
when we downloaded it. The dates come from the raw catalog, so they change automatically
after a new download (run_pipeline.py --download).

Charts that compare data with the EU recycling targets also name the legal acts that set
the targets, read from data/lookups/recycling_targets.json (so they always match the
targets in the chart), with a link to each act in EUR-Lex.

Which datasets each chart uses is set in CHARTS below. When a chart starts using another
dataset, add it there and run the pipeline. Do not edit the JSON by hand.

Output: one record per chart (key = chart id used in the dashboard):
    prefix      text before the list of datasets ("Source: Eurostat")
    datasets    one record per dataset used by the chart:
        code        Eurostat dataset code
        label       dataset name (shown as a link)
        url         page of the dataset in the Eurostat data browser
        text        text after the name: code, update date and download date
    targets     only for charts in CHARTS_WITH_TARGETS:
        prefix      text before the list of legal acts ("Targets")
        acts        one record per legal act: label, url

Input:  data/catalog/raw_sources.csv (built by scripts/raw/update_raw_catalog.py)
        data/lookups/recycling_targets.json (built by create_recycling_targets.py)
Output: data/lookups/data_sources.json (overwritten on each run)

Run from anywhere:
    .venv/Scripts/python scripts/lookups/create_data_sources.py
"""

import json

import pandas as pd

from paths import DIR_CATALOG, DIR_LOOKUPS

INPUT = DIR_CATALOG / "raw_sources.csv"
INPUT_TARGETS = DIR_LOOKUPS / "recycling_targets.json"
OUTPUT = DIR_LOOKUPS / "data_sources.json"

PREFIX = "Source: Eurostat"
URL = "https://ec.europa.eu/eurostat/databrowser/view/{code}/default/table"

# chart id (used in the dashboard) -> Eurostat datasets it shows
CHARTS = {
    "municipal_waste": ["env_wasmun"],
    "decoupling": ["env_wasmun", "nama_10_pc"],
    "distance_to_target": ["env_wasmun", "env_waspacr"],
    "waste_treatment": ["env_wasmun"],
}

# charts that show the recycling targets
CHARTS_WITH_TARGETS = ["distance_to_target"]
TARGETS_PREFIX = "Targets"

# EUR-Lex page of each legal act in recycling_targets.json (legal_basis -> url)
LEGAL_ACT_URLS = {
    "Waste Framework Directive 2008/98/EC (as amended by Directive (EU) 2018/851)":
        "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02008L0098-20240218",
    "Packaging and Packaging Waste Regulation (EU) 2025/40":
        "https://eur-lex.europa.eu/eli/reg/2025/40/oj/eng",
}


def target_acts():
    """Legal acts that set the 2025 targets, in the order of recycling_targets.json."""
    with open(INPUT_TARGETS, encoding="utf-8") as f:
        targets = json.load(f)
    acts = list(dict.fromkeys(t["legal_basis"] for t in targets if t["target_2025"] is not None))
    missing = [a for a in acts if a not in LEGAL_ACT_URLS]
    if missing:
        raise ValueError(f"no EUR-Lex link in LEGAL_ACT_URLS for: {missing}")
    return [{"label": act, "url": LEGAL_ACT_URLS[act]} for act in acts]


def format_date(timestamp):
    """'2026-10-15T11:00:00+0200' -> '15 October 2026' (date in the timestamp's own zone)."""
    return f"{pd.Timestamp(timestamp).day} {pd.Timestamp(timestamp):%B %Y}"


def main():
    catalog = pd.read_csv(INPUT).set_index("source_code")

    missing = sorted({c for codes in CHARTS.values() for c in codes} - set(catalog.index))
    if missing:
        raise ValueError(f"datasets not in {INPUT.name} (download them first): {missing}")

    def dataset(code):
        row = catalog.loc[code]
        return {
            "code": code,
            "label": row["label"],
            "url": URL.format(code=code),
            "text": (
                f"({code}), updated by Eurostat on {format_date(row['source_updated'])}, "
                f"downloaded on {format_date(row['retrieved_at'])}"
            ),
        }

    sources = {
        chart: {"prefix": PREFIX, "datasets": [dataset(code) for code in codes]}
        for chart, codes in CHARTS.items()
    }
    for chart in CHARTS_WITH_TARGETS:
        sources[chart]["targets"] = {"prefix": TARGETS_PREFIX, "acts": target_acts()}

    DIR_LOOKUPS.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(sources, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"saved the data sources of {len(sources)} charts to {OUTPUT}")


if __name__ == "__main__":
    main()

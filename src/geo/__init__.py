"""
Geographies covered by the processed data: the 27 EU Member States and the EU27 total.

Usage:
    from geo import keep_eu27

    df = keep_eu27(df)   # keeps the 27 Member States and EU27_2020, drops all other geographies

The codes and display names come from data/lookups/geo_eu27.json (built by
scripts/lookups/create_geo_eu27.py), which has the 27 Member States and EU27_2020.
Raw and interim data keep all geographies; the filter is applied only in the processed step.
"""

import json

from paths import DIR_LOOKUPS

EU27_TOTAL = "EU27_2020"  # Eurostat code for the EU27 total (from 2020)


def geo_names() -> dict[str, str]:
    """Return {code: display name} for the 27 Member States and EU27_2020."""
    with open(DIR_LOOKUPS / "geo_eu27.json", encoding="utf-8") as f:
        return json.load(f)


def eu27_geos() -> list[str]:
    """Return the geographies kept in the processed data: the 27 Member States and EU27_2020."""
    return list(geo_names())


def eu27_countries() -> list[str]:
    """Return the codes of the 27 EU Member States only (without EU27_2020)."""
    return [g for g in eu27_geos() if g != EU27_TOTAL]


def keep_eu27(df, col="geo"):
    """Return df with only the 27 Member States and EU27_2020 in column `col`."""
    return df.loc[df[col].isin(eu27_geos())].reset_index(drop=True)

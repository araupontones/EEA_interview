# EEA interview
This project was created to explore data used in the Waste Data Reporting (WDR) cycle of the EEA. The objective is to understand the full data cycle of the WDR.

## Download the latest Eurostat data

Raw data is downloaded from the [Eurostat Statistics API](https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-detailed-guidelines/api-statistics) and saved in `data/raw/<datasetCode>/`:

| File | Content |
|------|---------|
| `df.parquet` | The data, one row per observation |
| `lookup.json` | Code-to-label mapping for each dimension (e.g. `wst_oper`: `GEN` → `Waste generated`) |
| `metadata.json` | Dataset label, source, last Eurostat update and download time |

Each download overwrites the files that are already there.

### Update all datasets

From the project root:

```
.venv/Scripts/python scripts/raw/download_and_save_eurostat_raw_sources.py
```

This downloads every dataset in `DATASET_CODES` in [scripts/raw/download_and_save_eurostat_raw_sources.py](scripts/raw/download_and_save_eurostat_raw_sources.py). If a dataset fails, the error is logged, the script continues with the next one, and it ends with exit code 1. To add a dataset, add its Eurostat code to that list.

### Update one dataset

```
.venv/Scripts/python -c "from apiEurostat.pipeline import process; process('env_wasmun')"
```

### Notes

- Only years 2010 to 2026 are downloaded, for countries plus the EU-level totals Eurostat publishes for each dataset (always `EU27_2020`; some datasets also have EU28, euro area or EFTA totals). To change this, edit the defaults of `download_eurostat()` in [src/apiEurostat/download_eurostat.py](src/apiEurostat/download_eurostat.py).
- The `apiEurostat` package is installed into `.venv` in editable mode. If the import fails, reinstall it with `.venv/Scripts/python -m pip install -e .`
- How the code is organised:
  - `download_eurostat.py` calls the API.
  - `transform_reponse.py` builds the dataframe and lookups and saves the files.
  - `pipeline.py` runs both steps for one dataset.
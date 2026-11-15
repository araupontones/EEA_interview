# EEA waste data

This project explores the data used in the EEA's Waste Data Reporting (WDR) cycle and covers the full data cycle: it downloads Eurostat waste datasets, builds indicators, checks them, and calculates each country's distance to the EU recycling targets. The outputs feed a dashboard.

The project notebook is the [docs/](docs/) folder:
- **Method notes**: what each indicator means, decisions taken and their consequences, and the open data questions are in [docs/method_notes.md](docs/method_notes.md). Read it before using the data.
- **Decision log**: every decision taken on the way (data, dashboard, project organisation), dated, newest first, in [docs/decisions.md](docs/decisions.md).
- **Findings**: the most relevant results of the analysis, in [docs/findings.md](docs/findings.md).
- **Next tasks**: [docs/todo.md](docs/todo.md).

## Quick start

Requires Python 3.10 or later (developed with 3.14) and git. Commands are for Windows; on macOS or Linux, replace `.venv/Scripts/python` with `.venv/bin/python`.

```
# 1. Create the project environment (once)
python -m venv .venv

# 2. Install the dependencies and the project's own packages (once, and after pulling new packages)
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m pip install -e .

# 3. Build all the data. The first time, download the raw data too (it is not in git).
.venv/Scripts/python scripts/run_pipeline.py --download
```

After the first run, rebuild everything from the raw files already downloaded with:

```
.venv/Scripts/python scripts/run_pipeline.py
```

Only use `--download` when you want the latest Eurostat release. A new download can change the figures, because Eurostat revises past years.

Always use the project environment (`.venv`). Install new packages with `.venv/Scripts/python -m pip install <package>` and add them to `requirements.txt`; never install them globally.

## Project structure

```
data/
  raw/<dataset code>/   Eurostat downloads, never edited (parquet files not in git)
  catalog/              raw_sources.csv: which Eurostat release each raw dataset is
  lookups/              reference tables: EU27 countries, recycling targets
  interim/              indicators from one source, one file per Eurostat dataset
  processed/            final tables for the dashboard
scripts/
  run_pipeline.py       runs every script below in the right order
  raw/                  download data, update the catalog
  lookups/              build the lookup tables
  interim/              build indicators from one raw dataset
  processed/            combine interim tables into dashboard tables
src/
  paths/                all project paths (ROOT, DIR_RAW, DIR_INTERIM, ...)
  geo/                  geographies of the processed data (keep_eu27)
  eurostat_api/         download and save Eurostat datasets
  cleaning/             helpers to profile and check raw tables (used in notebooks)
notebooks/python/       exploration; each script was first developed in a notebook
dashboard/              React + D3 dashboard (Vite app), published on GitHub Pages
  src/data.js           the only file that loads data (from data/processed and data/lookups)
.github/workflows/      deploy-dashboard.yml: builds and publishes the dashboard
docs/                   project notebook: method notes, decision log, findings, to do
background/             reference documents
```

## The pipeline

The data moves through four layers: `raw` → `lookups` → `interim` → `processed`. Each script reads the outputs of the scripts before it, so `run_pipeline.py` runs them in this order:

| Step | Script | Input | Output |
|---|---|---|---|
| 1 | [scripts/raw/download_eurostat.py](scripts/raw/download_eurostat.py) (only with `--download`) | Eurostat API | `data/raw/<code>/` |
| 2 | [scripts/raw/update_raw_catalog.py](scripts/raw/update_raw_catalog.py) | `data/raw/` | `data/catalog/raw_sources.csv` |
| 3 | [scripts/lookups/create_geo_eu27.py](scripts/lookups/create_geo_eu27.py) | `data/raw/demo_gind/` | `data/lookups/geo_eu27.json` |
| 4 | [scripts/lookups/create_geo_flags.py](scripts/lookups/create_geo_flags.py) | `geo_eu27.json` | `data/lookups/geo_flags.json` |
| 5 | [scripts/lookups/create_recycling_targets.py](scripts/lookups/create_recycling_targets.py) | targets written in the script | `data/lookups/recycling_targets.json` |
| 6 | [scripts/lookups/create_decoupling_notes.py](scripts/lookups/create_decoupling_notes.py) | notes written in the script, `geo_eu27.json` | `data/lookups/decoupling_notes.json` |
| 7 | [scripts/lookups/create_municipal_waste_notes.py](scripts/lookups/create_municipal_waste_notes.py) | notes written in the script | `data/lookups/municipal_waste_notes.json` |
| 8 | [scripts/lookups/create_data_sources.py](scripts/lookups/create_data_sources.py) | `data/catalog/raw_sources.csv`, `recycling_targets.json` | `data/lookups/data_sources.json` |
| 9 | [scripts/interim/env_wasmun.py](scripts/interim/env_wasmun.py) | `data/raw/env_wasmun/` | `data/interim/env_wasmun.parquet` |
| 10 | [scripts/interim/env_waspacr.py](scripts/interim/env_waspacr.py) | `data/raw/env_waspacr/` | `data/interim/env_waspacr.parquet` |
| 11 | [scripts/interim/nama_10_pc.py](scripts/interim/nama_10_pc.py) | `data/raw/nama_10_pc/` | `data/interim/nama_10_pc.parquet` |
| 12 | [scripts/processed/recycling_distance_to_target.py](scripts/processed/recycling_distance_to_target.py) | interim files, `recycling_targets.json` | `data/processed/recycling_distance_to_target.json` |
| 13 | [scripts/processed/municipal_waste.py](scripts/processed/municipal_waste.py) | `data/interim/env_wasmun.parquet` | `data/processed/municipal_waste.json` |
| 14 | [scripts/processed/municipal_waste_decoupling.py](scripts/processed/municipal_waste_decoupling.py) | `env_wasmun.parquet`, `nama_10_pc.parquet` | `data/processed/municipal_waste_decoupling.json` |

The pipeline stops at the first script that fails. Every script can also be run on its own, from any folder, e.g. `.venv/Scripts/python scripts/interim/env_wasmun.py`. Each script's docstring states its input, output and decisions.

### Outputs

| File | Content |
|---|---|
| `data/raw/<code>/df.parquet` | Eurostat data, one row per observation |
| `data/raw/<code>/lookup.json` | Code-to-label mapping for each dimension (e.g. `wst_oper`: `GEN` → `Waste generated`) |
| `data/raw/<code>/metadata.json` | Dataset label, last Eurostat update and download time |
| `data/catalog/raw_sources.csv` | One row per raw dataset: label, Eurostat release date, download time, dimensions |
| `data/lookups/geo_eu27.json` | The geographies in the processed data: the 27 EU Member States and the EU27 total, code → display name (e.g. `"BE": "Belgium"`, `"EU27_2020": "EU27"`) |
| `data/lookups/geo_flags.json` | Flag code of each geography in the processed data, for the flags in the dashboard (`"AT": "at"`; Greece `EL` → `gr`, `EU27_2020` → `eu`) |
| `data/lookups/recycling_targets.json` | 2025 and 2030 recycling targets (%) per waste category, with legal basis |
| `data/lookups/decoupling_notes.json` | Texts of the decoupling chart: caption, legend labels, a general note, a note on the countries that changed their definition of municipal waste (shown with the EU27), and country notes with the year of a break in series |
| `data/lookups/municipal_waste_notes.json` | Texts of the municipal waste bar chart: caption, labels of the hover card, general note |
| `data/lookups/data_sources.json` | Source lines under each chart: the Eurostat datasets it uses, with link, Eurostat update date and download date; for the distance-to-target chart, also the legal acts that set the targets (from `recycling_targets.json`) |
| `data/interim/env_wasmun.parquet` | Municipal waste generated (kg per person, tonnes), recycled (tonnes) and recycling rate, per country and year |
| `data/interim/env_waspacr.parquet` | Packaging recycling rates (%) per country and packaging type, 2023 |
| `data/interim/nama_10_pc.parquet` | Real GDP per person (euro, 2020 prices) per country and year, 2010–2025 |
| `data/processed/recycling_distance_to_target.json` | Recycling rate (%) and distance to the 2025 target (percentage points) per country and waste category, 2023 |
| `data/processed/municipal_waste.json` | Municipal waste generated per person (kg) and in total (thousand tonnes), per country and year, 2010–2024 |
| `data/processed/municipal_waste_decoupling.json` | Municipal waste and real GDP per person, and both indexed to 2011 = 100, per country and year, 2010–2024 |

Raw and interim tables keep all geographies in the source (EU and non-EU countries, EU and euro area totals). Processed tables keep only the 27 EU Member States and the `EU27_2020` total, filtered with `keep_eu27()` from the `geo` package; `run_pipeline.py` checks this at the end. The dashboard can show names instead of codes with `data/lookups/geo_eu27.json`. See the method notes for the full list of decisions.

## The dashboard

A React app in `dashboard/`, built with [Vite](https://vite.dev/) and published on GitHub Pages. D3 does the maths (scales, line paths, axis ticks) and React renders the SVG. Use only D3's maths modules (`d3-array`, `d3-scale`, `d3-shape`), not `d3-selection`, which edits the page directly and conflicts with React.

Requires Node.js (developed with Node 26). From the `dashboard/` folder:

```
npm install        # once, and after pulling new dependencies
npm run dev        # local preview with live reload: open the address it prints
npm run build      # build the site into dashboard/dist/ (what GitHub Pages serves)
npm run preview    # preview the built site
```

**Structure.** The page is a sequence of sections, in this order, set in [dashboard/src/App.jsx](dashboard/src/App.jsx). Each section has its own folder in `dashboard/src/sections/`, with its chart next to it, so each can be worked on separately:

| Section | Folder | Chart |
|---|---|---|
| Hero: title, subtitle, brief explanation | `hero/` | |
| Municipal waste generation | `municipal_waste/` | `WastePerCapitaBarChart.jsx`: waste per person by country |
| Decoupling | `decoupling/` | `DecouplingLineChart.jsx`: waste and GDP indexes, 2011 = 100 |
| Distance to target | `distance_to_target/` | `DistanceToTargetScatter.jsx`: recycling rates against the 2025 targets |
| Methodological note | `method_note/` | |
| How I did this | `how_i_did_this/` | |

Shared pieces are in `dashboard/src/components/` (`Section.jsx`: heading and anchor of each section). Folder names are lower case with `_`, as in the rest of the project; React component files use PascalCase (`DecouplingSection.jsx`), the React convention.

**Data sources.** Every chart ends with a source line (`components/ChartSource.jsx`): the Eurostat datasets it uses, linked to the Eurostat data browser, with the date Eurostat last updated them and the date they were downloaded; charts that show the recycling targets also name the legal acts that set them, linked to EUR-Lex. The texts come from `data/lookups/data_sources.json`; the datasets of each chart are set in `CHARTS` in [scripts/lookups/create_data_sources.py](scripts/lookups/create_data_sources.py), and the dates come from the raw catalog, so they update after each download. A new chart needs an entry there.

**Flags.** Country and EU flags come from the [flag-icons](https://github.com/lipis/flag-icons) npm package (MIT licence, version pinned in `package.json`), not from the web. [dashboard/src/lib/flags.js](dashboard/src/lib/flags.js) maps a geography code to its flag with `data/lookups/geo_flags.json` and bundles only the 28 flags used; `flagUrl("AT")` returns the image to show.

**Data.** The dashboard reads the JSON files in `data/processed/` and `data/lookups/` directly, with no copy: [dashboard/src/data.js](dashboard/src/data.js) imports them (`@data` is an alias for `data/`, set in [dashboard/vite.config.js](dashboard/vite.config.js)), and Vite bundles them into the app when it builds. `data.js` is the only file that loads data; charts import from it. To update the data in the dashboard: run the pipeline, commit the JSON files and push.

The processed files are the dashboard's data contract: renaming a column or a file breaks the dashboard, so change `data.js` and the charts at the same time.

**Publishing.** Every push to `main` that changes `dashboard/`, `data/processed/` or `data/lookups/` runs [.github/workflows/deploy-dashboard.yml](.github/workflows/deploy-dashboard.yml), which builds the app and publishes it on GitHub Pages. It can also be started by hand from the Actions tab. The built files (`dashboard/dist/`) and `node_modules/` are not committed. One-time setup on GitHub: Settings → Pages → Source: **GitHub Actions**. The site is served at `https://<user>.github.io/EEA_interview/` (set as `base` in `vite.config.js`); GitHub Pages is public, whatever the visibility of the repository.

## Common tasks

### Use project paths in a script or notebook

Never write paths by hand or relative to the working directory. Import them:

```python
from paths import DIR_LOOKUPS, raw_dir, interim_file

df = pd.read_parquet(interim_file("env_wasmun"))      # data/interim/env_wasmun.parquet
df_raw = pd.read_parquet(raw_dir("env_wasmun") / "df.parquet")
```

The paths are absolute, so code works from any folder, including notebooks and the VS Code Interactive Window. To add a new folder, add it once in [src/paths/__init__.py](src/paths/__init__.py).

### Keep only the EU27 in processed data

Every processed script filters its data with the same rule:

```python
from geo import keep_eu27

df = keep_eu27(df)   # the 27 Member States and EU27_2020; all other geographies dropped
```

The list of geographies comes from `data/lookups/geo_eu27.json` ([src/geo/__init__.py](src/geo/__init__.py)). To change it, edit [scripts/lookups/create_geo_eu27.py](scripts/lookups/create_geo_eu27.py), never the JSON file.

### Download or update Eurostat data

- All datasets: `.venv/Scripts/python scripts/raw/download_eurostat.py`, then `scripts/raw/update_raw_catalog.py` (or `run_pipeline.py --download`, which runs both and rebuilds everything).
- One dataset: `.venv/Scripts/python -c "from eurostat_api.pipeline import process; process('env_wasmun')"`
- To add a dataset, add its Eurostat code to `DATASET_CODES` in [scripts/raw/download_eurostat.py](scripts/raw/download_eurostat.py).
- If one dataset fails, the error is logged, the script continues with the next one, and it ends with exit code 1.
- Only years 2010 to 2026 are downloaded, for countries plus the EU-level totals Eurostat publishes for each dataset. To change this, edit the defaults of `download_eurostat()` in [src/eurostat_api/download_eurostat.py](src/eurostat_api/download_eurostat.py).
- How the package is organised: `download_eurostat.py` calls the API, `transform_response.py` builds the dataframe and lookups and saves the files, `pipeline.py` runs both for one dataset.

### Add a new indicator source

1. Download the dataset (add its code to `DATASET_CODES`).
2. Explore it in a new notebook, `notebooks/python/NN_<topic>.ipynb`.
3. Write `scripts/interim/<eurostat code>.py`, using an existing interim script as a template, and save to `interim_file("<eurostat code>")`.
4. Add the script to `STEPS` in [scripts/run_pipeline.py](scripts/run_pipeline.py), in the right layer.
5. Record the decisions in [docs/method_notes.md](docs/method_notes.md), and log them in [docs/decisions.md](docs/decisions.md).

### Change a recycling target

Edit `TARGETS` in [scripts/lookups/create_recycling_targets.py](scripts/lookups/create_recycling_targets.py), run the pipeline, and update the targets table in the method notes.

### Adjust a value in the source data

Data validation is done at the end of each interim script, in a section marked `DATA VALIDATION` (see [scripts/interim/env_waspacr.py](scripts/interim/env_waspacr.py)). Each rule:
- explains the issue in a comment,
- only applies while the issue is still in the Eurostat data (e.g. a threshold, not a fixed country-year), so a revised figure is kept automatically,
- prints a line every time it changes a value,
- is documented in the method notes.

Never edit files in `data/raw`.

## Conventions

| What | Convention | Example |
|---|---|---|
| File and folder names | lower case, words separated by `_` | `geo_eu27.json` |
| Interim scripts and files | named after the Eurostat dataset code | `env_wasmun.py` → `env_wasmun.parquet` |
| Other scripts | named after what they create; lookups start with `create_` | `create_recycling_targets.py` → `recycling_targets.json` |
| Processed files | topic first, then the content | `recycling_distance_to_target.json` |
| Notebooks | two-digit number, then the topic | `04_create_mw_pc.ipynb` |
| Script docstring | what it does, input, output, how to run | see any script |
| Paths | always from the `paths` package | `from paths import DIR_INTERIM` |
| Formats | parquet for raw and interim data; JSON for lookups and dashboard files | |
| Waste category labels | sentence case, as in Eurostat | `Municipal waste`, `Plastic packaging` |
| Rates | in raw and interim data, as in the source (share 0–1 or %, stated in the docstring); in the processed files and the dashboard, % with one decimal; distances in percentage points | `0.681` (interim) → `68.1` (processed) |

Notebooks are for exploration. Anything the dashboard uses must be produced by a script in `scripts/` and listed in `run_pipeline.py`.

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'paths'` (or `eurostat_api`) | Run `.venv/Scripts/python -m pip install -e .`. In the VS Code Interactive Window or a notebook, check the kernel is `.venv` and restart it. |
| `FileNotFoundError` for a file in `data/raw` | The raw parquet files are not in git. Run `scripts/run_pipeline.py --download`. |
| `FileNotFoundError` for an interim or lookup file | Run `scripts/run_pipeline.py`, which builds the files in the right order. |
| `time` becomes a number when reading a JSON file | Read it with `pd.read_json(path, dtype={"time": str})`. |
| Figures differ from a colleague's | Compare `source_updated` in `data/catalog/raw_sources.csv`: you may have different Eurostat releases. |

# Project: Waste in the EU

Explores the data of the EEA's Waste Data Reporting (WDR) cycle: downloads Eurostat waste datasets, builds indicators, checks them, and calculates each country's distance to the EU recycling targets. The processed data feeds a dashboard to be built with D3 and React.

- [README.md](README.md): setup, pipeline, outputs, conventions, common tasks. The team's guide; keep it up to date when scripts, outputs or conventions change.
- [docs/](docs/): the project notebook.
  - [docs/method_notes.md](docs/method_notes.md): how the data is built as it stands now: every data decision and its consequence, the recycling targets and their legal sources, data validation, and the open data questions (section 7, the only list of them).
  - [docs/decisions.md](docs/decisions.md): dated log of every decision taken (data, dashboard, project organisation), newest first. Add an entry each time the user takes a decision; for data decisions, also update the method notes and link to the section.
  - [docs/communication.md](docs/communication.md): how the dashboard communicates, as it stands now: audience, storyline, key messages per section (pointing to findings, never restating figures), voice and glossary, visual identity, "Needs a finding" requests. Written from the agents' proposals after the user approves; final texts stay in the lookups.
  - [docs/findings.md](docs/findings.md): the most relevant findings of the analysis, with figures. Every time the analysis produces a new finding (in a notebook, a script or a conversation), add it here in the right section, with its figures and caveats. Update existing findings when the data or the method changes.
  - [docs/todo.md](docs/todo.md): next build tasks. Remove items once done.

## Python

- Use the project virtual environment at `.venv/`
- Install packages with `.venv/Scripts/python -m pip install <pkg>`
  and add them to `requirements.txt` (UTF-8). Never install globally.
- The project's own packages (`paths`, `eurostat_api`, in `src/`) are installed in editable mode. After adding a package under `src/`, run `.venv/Scripts/python -m pip install -e .`

## Git

- Never add Claude as co-author in commits: no `Co-Authored-By` lines or other Claude attribution in commit messages or PR descriptions.

## Dashboard

- React + D3 app in `dashboard/` (Vite), published on GitHub Pages by `.github/workflows/deploy-dashboard.yml` on push to `main`. Commands run from `dashboard/`: `npm install`, `npm run dev`, `npm run build`.
- D3 does the maths, React renders: use `d3-array`, `d3-scale`, `d3-shape` to compute scales, paths and ticks, and render them as JSX. Never use `d3-selection` or edit the DOM directly.
- Data is loaded only in `dashboard/src/data.js`, by importing the JSON files from `data/processed/` and `data/lookups/` (`@data` alias). No copies of the data in `dashboard/`.
- The processed JSON files are the dashboard's data contract: when renaming a column or file in a processed script, update `data.js` and the charts in the same change.
- Texts shown in the dashboard (notes, captions) come from data files built by the pipeline (e.g. `data/lookups/decoupling_notes.json`), not from the React code.
- Every chart ends with its source line (`<ChartSource chart="..." />`): add each new chart and its Eurostat datasets to `CHARTS` in `scripts/lookups/create_data_sources.py`.
- Before committing dashboard changes, run `npm run build` and check it passes.

## Pipeline

Layers: `data/raw` → `data/lookups` → `data/interim` → `data/processed`, with one folder of scripts per layer in `scripts/`.

- Rebuild everything: `.venv/Scripts/python scripts/run_pipeline.py` (add `--download` to fetch new Eurostat data; don't download unless asked, as it changes the figures).
- Every new script must be added to `STEPS` in `scripts/run_pipeline.py`, in the right layer.
- After changing a script, run it (or the pipeline) and check the output.

## Conventions

- Paths: always import them from the `paths` package (`from paths import DIR_INTERIM, interim_file, raw_dir`). Never hard-code paths or use paths relative to the working directory.
- Names: lower case with `_`. Interim scripts and files are named after the Eurostat dataset code (`env_wasmun.py` → `env_wasmun.parquet`); other scripts after what they create; lookups start with `create_`; processed files are `<topic>_<content>.json`; notebooks are `NN_<topic>.ipynb`.
- Every script starts with a docstring: what it does, input, output, how to run.
- Scripts in `scripts/processed/` use `# %%` cells, so they can be run in the VS Code Interactive Window.
- Formats: parquet for raw and interim data; JSON (records, readable, `null` for empty values) for lookups and processed files.
- Data: rates in raw and interim data may be a share (0 to 1) or in %, as in the source (state which in the docstring); in processed files and the dashboard, rates are in % with one decimal (convert in the processed script). Distances in percentage points (value - target); waste category labels in sentence case (`Municipal waste`); keep missing values empty, never fill them with zero.
- Raw and interim tables keep all geographies. Processed tables keep only the 27 EU Member States and `EU27_2020`: filter with `keep_eu27()` from the `geo` package in every processed script. `data/lookups/geo_eu27.json` is generated by `scripts/lookups/create_geo_eu27.py`; never edit it by hand.
- Never edit files in `data/raw`. Adjust source values only in the `DATA VALIDATION` section at the end of an interim script: explain the issue in a comment, make the rule stop applying if Eurostat revises the value (e.g. a threshold), print each change, and document it in the method notes.
- Notebooks are for exploration only. Anything the dashboard uses must come from a script.

## Agents (`.claude/agents/`)

For the dashboard's content and design, aimed at a general public that reads little and should learn about the waste hierarchy and the circular economy. The four communication and checking agents only propose; the main session applies what the user approves.

**Findings-only rule (all agents, and the main session when writing dashboard texts):** `docs/findings.md` is the only source of facts. No general knowledge, outside sources or assumed causes; no new figures (averages, shares, rankings, conversions) — a missing figure is a "Needs a finding" request, calculated and added to the findings first if the user agrees. The only exception is the order and names of the waste hierarchy. The fact-checker may use outside sources (Eurostat metadata, official indicators, legal texts, Commission reports) to verify the data and the findings; what it finds goes into the findings first, never straight into a text.

- `data-storyteller`: storyline, one key message per section, what each chart should make people notice.
- `ux-copywriter`: every visible text, in plain English, with where it goes (lookup script and key, or component).
- `brand-designer`: the dashboard's own visual identity (not an institutional brand) and the design of each element.
- `data-scientist`: owns the analytical pipeline (download, raw, lookups, interim, processed) and turns "Needs a finding" requests into data, findings and method notes. Unlike the other four, it edits files (not `dashboard/`, `docs/communication.md` or `docs/decisions.md`).
- `fact-checker`: verifies every figure and claim in proposed texts against the processed data, `docs/findings.md` and `docs/method_notes.md`.

Usual order: data-storyteller → ux-copywriter → fact-checker; brand-designer in parallel. Approved proposals go into `docs/communication.md` (and the final texts into the lookups), and each decision is logged in `docs/decisions.md`. Dashboard texts are in English only.


# Decision log

Every decision taken on the way, newest first: data, dashboard and project organisation. One entry per decision, with the reason and where it is applied.

For data decisions, the full explanation and its consequences are in [method_notes.md](method_notes.md), which describes the data as it stands now; this log records when and why each decision was taken. Open questions still to decide are in [method_notes.md, section 7](method_notes.md#7-open-points).

## 15 November 2026

**Findings are kept in `docs/findings.md`.**
- Decision: one file with the most relevant findings of the analysis (municipal waste per person, decoupling, distance to target), with figures, kept up to date when the data or the method changes.
- Why: a single summary of results to draw on for the dashboard texts and presentations.
- Applied in: [findings.md](findings.md), `CLAUDE.md`, `README.md`.

**The `docs/` folder is the project notebook.**
- Decision: `method_notes.md` and `todo.md` moved to `docs/`; `dashboard_notes/` removed; this decision log added.
- Why: one place for all project notes, not only notes about the dashboard.
- Applied in: `CLAUDE.md`, `README.md`, and the references in `scripts/interim/env_waspacr.py`, `scripts/lookups/create_decoupling_notes.py` and `dashboard/src/sections/method_note/MethodNoteSection.jsx`.

**Open data questions are listed only in the method notes (section 7).**
- Decision: `todo.md` holds only build tasks and links to the method notes for open data questions. When a decision leads to work, the task is added to `todo.md`.
- Why: the two lists overlapped and had drifted apart.
- Applied in: [method_notes.md, section 7](method_notes.md#7-open-points), [todo.md](todo.md).

**Rates: share or % in raw and interim data, % with one decimal in processed data and the dashboard.**
- Decision: raw and interim tables keep the unit of the source (e.g. the municipal recycling rate as a share from 0 to 1), stated in the script docstring. Processed scripts convert rates to % with one decimal, so the dashboard always shows %.
- Why: interim tables stay close to the source; the dashboard uses one unit for all rates.
- Applied in: `CLAUDE.md` and `README.md` (conventions), [method_notes.md](method_notes.md) sections 2 and 3. Already done in `scripts/processed/recycling_distance_to_target.py`.

**The year column stays `time` in the interim tables.**
- Decision: not renamed; the processed files already use `year`.
- Why: it does not affect any output.

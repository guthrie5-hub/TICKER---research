# Adobe Project 1 — linked FCFF valuation

## Decision question

Should a fund initiate Adobe (ADBE), place it on watch/defer, or not initiate, using a dated valuation range and stated conditions?

Current working call: **Initiate.** This is an educational working draft, not investment advice or a final committee recommendation.

## What is in this folder

- `adobe_project1.py` — final working linked FY2026E–FY2030E statements, FCFF DCF, cases, WACC-growth grid, reverse DCF, and articulation checks. Standard library only.
- `adobe_ev_comps.py` — dated EV/revenue and reported-GAAP-P/E peer calculator. Standard library only.
- `adobe_project1_sources.md` — source locators, basis definitions, peer policy, and full assumption challenge record.
- `adobe_project1_memo.md` — working committee memo and conditional action.
- `visible_output.md` — results visible without running code.
- `project-1.md`, `adobe_proforma_research.md`, `adobe_proforma.py`, `dcf.py`, and `peer_valuation.py` — earlier lab evidence retained for history; not the final linked Project 1 system.
- `proforma.py` — ABG known-answer training model.
- `visible_output.md` — saved results from the current local run.
- `validation_record.md` — checks completed and remaining readiness gaps.
- `project_readiness.md` — the short readiness submission cover record.
- `project_audit.py` and `project-submission-manifest-template.csv` — mechanical manifest audit and working manifest.

## Run commands

## Cold-run setup and commands

The model itself requires a regular installation of **Python 3.10 or newer** and no third-party packages. Do not rely on this student's local `.uv` folder: it is not part of a fresh repository checkout.

From the repository root, first enter the folder containing this README and the Python files. If you are already in that folder, skip this command:

```sh
cd fin43900-fall2026-work
```

Check that Python is available:

```sh
python3 --version
```

If that command does not print a Python version, install Python locally, reopen Terminal, and start again. Then run the current Project 1 system:

```sh
python3 adobe_project1.py
python3 adobe_ev_comps.py
```

The model uses no installed packages. It prints the FY2025 opening reconciliation, five projected statements, articulation checks, FCFF enterprise-to-equity bridge, WACC/growth grid, cases, and reverse DCF. `adobe_ev_comps.py` prints the two separately defined peer methods; it never averages them.

The course-supplied manifest audit separately requires pandas. Only after the two model commands work, create an audit environment:

```sh
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python project_audit.py project-submission-manifest-template.csv
```

## Evidence boundary and remaining completion items

The current system is an FCFF enterprise-value model driven by its own linked pro-forma. It does not make the final project complete: the student must still do and record the AI-off locked prediction, README-only cold run, actual partner challenge, source-opening checks, repository-access confirmation, manifest freeze, and three recorded videos with corrected transcripts. Do not represent those events as completed until they happened.

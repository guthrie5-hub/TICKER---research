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

Run the current Project 1 system:

```sh
./.uv/bin/python3.13 adobe_project1.py
./.uv/bin/python3.13 adobe_ev_comps.py
```

The model uses no installed packages. It prints the FY2025 opening reconciliation, five projected statements, articulation checks, FCFF enterprise-to-equity bridge, WACC/growth grid, cases, and reverse DCF. `adobe_ev_comps.py` prints the two separately defined peer methods; it never averages them.

The course-supplied manifest audit requires pandas. A project-local virtual environment contains it:

```sh
./.venv/bin/python project_audit.py project-submission-manifest-template.csv
```

To recreate that audit environment:

```sh
./.tools/uv/uv venv .venv --python ./.uv/bin/python3.13
./.tools/uv/uv pip install --python ./.venv/bin/python -r requirements.txt
```

## Evidence boundary and remaining completion items

The current system is an FCFF enterprise-value model driven by its own linked pro-forma. It does not make the final project complete: the student must still do and record the AI-off locked prediction, README-only cold run, actual partner challenge, source-opening checks, repository-access confirmation, manifest freeze, and three recorded videos with corrected transcripts. Do not represent those events as completed until they happened.

# Adobe Project 1 — working draft

## Decision question

Should a fund initiate Adobe (ADBE), place it on watch/defer, or not initiate, using a dated valuation range and stated conditions?

Current draft call: **Watch—defer.** This is not a final committee recommendation.

## What is in this folder

- `project-1.md` — company research, source log, early peer-P/E comparison, and draft call.
- `adobe_proforma_research.md` — FY2023–FY2025 history, assumptions, sources, and sensitivity record.
- `adobe_proforma.py` — Adobe five-year FCFE pro-forma draft with balance and cash checks.
- `dcf.py` — standalone FCFF DCF, WACC-growth grid, and reverse DCF.
- `peer_valuation.py` — peer P/E calculator.
- `proforma.py` — ABG known-answer training model.
- `visible_output.md` — saved results from the current local run.
- `validation_record.md` — checks completed and remaining readiness gaps.
- `project_readiness.md` — the short readiness submission cover record.
- `project_audit.py` and `project-submission-manifest-template.csv` — mechanical manifest audit and working manifest.

## Run commands

The company scripts use the existing local Python command:

```sh
./.uv/bin/python3.13 adobe_proforma.py
./.uv/bin/python3.13 dcf.py
./.uv/bin/python3.13 peer_valuation.py
./.uv/bin/python3.13 proforma.py
```

The course-supplied manifest audit requires pandas. A project-local virtual environment contains it:

```sh
./.venv/bin/python project_audit.py project-submission-manifest-template.csv
```

To recreate that audit environment:

```sh
./.tools/uv/uv venv .venv --python ./.uv/bin/python3.13
./.tools/uv/uv pip install --python ./.venv/bin/python -r requirements.txt
```

## Important current limitation

This folder is **not yet a final Project 1 system**. `adobe_proforma.py` is an FCFE draft and labels working-capital, financing, debt-repayment, and buyback inputs as placeholders; it therefore withholds value per share. `dcf.py` is a separate FCFF model rather than an FCFF valuation driven by the pro-forma. The two should not yet be presented as one fully linked, same-date valuation system.

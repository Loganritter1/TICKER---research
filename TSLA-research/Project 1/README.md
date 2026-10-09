# Tesla Corporate Finance Application

> Educational project for FIN 43900. This repository is not investment advice.

## Decision

This project supports a buy-side investment committee deciding whether to **initiate, watch/defer, or not initiate** a position in Tesla, Inc. (`TSLA`). The fund currently holds no position. The final recommendation will be a conditional valuation range with monitoring and reversal triggers, not a single target price.

## Current build status

The repository contains prior lab work on Tesla sources, comparable companies, a five-year pro forma, and sensitivity analysis. It is now being consolidated into the final required architecture:

- a five-year, linked three-statement projection;
- an FCFF DCF using WACC and a stated terminal convention;
- an enterprise-value-to-equity-value-to-per-share bridge;
- an enterprise-value and an equity-value comparable multiple;
- low/base/high and downside cases, sensitivity, and reverse-DCF evidence; and
- reproducible validation, AI-use, and submission records.

The final valuation date, currency, share-count basis, and explicit exclusions will be stated in the final decision memo and source ledger before the valuation is run.

## Repository map

| Location | Purpose |
|---|---|
| `tesla_proforma.py` | Existing lab-stage Tesla forecast model; to be refactored into the final FCFF engine. |
| `tesla_fcff.py` | Final-project FCFF/WACC engine, currently in input-reconciliation stage. |
| `tsla_ev_comps.py` | Qualified GM EV/revenue and P/E reference calculations using September 30 market prices. |
| `tsla_pe_comps.py` | Existing lab-stage equity-multiple reference calculation. |
| `asbury_pe_comps.py` | Training-case comparable-company calculator. |
| `lab06.md`–`lab11.md` | Prior lab evidence and working notes. |
| `sources.md` | Initial Tesla source list. |
| `docs/` | Final evidence, validation, decision, and recording records. |
| `output/` | Committed visible executed output for a grader who does not run code. |
| `tests/` | Final automated and reproducible validation checks. |

## Run status

Run the current FCFF engine from this folder with:

```powershell
python tesla_fcff.py
```

Run the reproducible validation suite with:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

The current root-level scripts are lab-stage artifacts and are not the final integrated application. The FCFF engine's dated WACC and market-price inputs will be finalized only after their September 30, 2026 evidence is reconciled in the source ledger.

## Evidence and limitations

Material facts, assumptions, transformations, source dates, and exclusions are tracked in [`docs/source-ledger.md`](docs/source-ledger.md). The current limitations and validation plan are recorded in [`docs/validation-and-ai-use.md`](docs/validation-and-ai-use.md).

## Academic-integrity note

The final project will disclose the AI tools used and retain independent source checks. The required Locked Changed-Input prediction is reserved for the student to author, without AI assistance, before the associated model run.

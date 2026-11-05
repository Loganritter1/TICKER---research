# Tesla Corporate Finance Application

> Educational project for FIN 43900. This repository is not investment advice.

## Decision

This project supports a buy-side investment committee deciding whether to **initiate, watch/defer, or not initiate** a position in Tesla, Inc. (`TSLA`). The fund currently holds no position. The frozen September 30, 2026 conclusion is to **not initiate at the reference price and retain TSLA on the watch list**. It is a conditional valuation range with monitoring and reversal triggers, not a single target price.

## Current build status

The final-project folder contains a frozen, locally runnable analysis with:

- a five-year, linked three-statement projection;
- an FCFF DCF using WACC and a stated terminal convention;
- an enterprise-value-to-equity-value-to-per-share bridge;
- an enterprise-value and an equity-value comparable multiple;
- low/base/high and downside cases, sensitivity, and reverse-DCF evidence; and
- reproducible validation, AI-use, and submission records; and
- a bounded driver panel that lets a teammate explore scenarios without changing the locked accounting engine or source inputs.

The valuation date is September 30, 2026; amounts are USD millions except per-share values and percentages; and the consistent share convention is 3,528 million FY2025 diluted weighted-average shares. The explicit bridge exclusions and valuation limitations are recorded in `docs/source-ledger.md` and `docs/freeze-2026-09-30.md`.

## Repository map

| Location | Purpose |
|---|---|
| `tesla_fcff.py` | Frozen final-project FCFF/WACC engine, linked three-statement forecast, DCF, and enterprise-to-equity bridge. |
| `tsla_ev_comps.py` | Qualified GM EV/revenue and P/E reference calculations using September 30 market prices. |
| `app.py` | Semi-adjustable Streamlit workbench with bounded driver controls and a visible checks panel. |
| `docs/` | Final evidence, validation, decision, and recording records. |
| `output/` | Frozen visible executed output for a grader who does not run code. |
| `tests/` | Final automated and reproducible validation checks. |

## Run status

Launch the semi-adjustable workbench from this folder with:

```powershell
python -m streamlit run app.py
```

The workbench exposes bounded FY2027 operating drivers, WACC, terminal growth,
and operating-cash treatment. It includes a base-case reset, five-year outputs,
bridge, sensitivity table, and failing-loudly check panel. The accounting engine
and dated source inputs remain locked in `tesla_fcff.py`.

For the required failure demonstration, select **Diagnostic: inject invalid
terminal value**. The locked engine rejects terminal growth equal to WACC; clear
the diagnostic or select **Reset to frozen base case** to recover.

Run the current FCFF engine from this folder with:

```powershell
python tesla_fcff.py
```

Run the reproducible validation suite with:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

The root-level lab scripts are supporting workpapers only; the final integrated application is self-contained in this folder. The dated WACC and market-price inputs were frozen and independently reconciled in `docs/freeze-2026-09-30.md`.

## Evidence and limitations

Material facts, assumptions, transformations, source dates, and exclusions are tracked in [`docs/source-ledger.md`](docs/source-ledger.md). The assumption challenges and one-at-a-time pro-forma sensitivity results are in [`docs/assumption-challenge-record.md`](docs/assumption-challenge-record.md). The current limitations and validation results are recorded in [`docs/validation-and-ai-use.md`](docs/validation-and-ai-use.md).

## Academic-integrity note

The project discloses AI tools used and retains independent source checks. The Locked Changed-Input prediction was authored by the student without AI assistance before the associated run.

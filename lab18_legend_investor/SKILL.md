---
name: legend-investor
description: Analyze a public company with Buffett-style business-quality checks from the last five SEC EDGAR 10-Ks; use when a ticker needs reproducible computed evidence and a short judgment memo.
---

# Legend Investor

Run `edgar_buffett.py` for the requested ticker using the student's SEC-compliant User-Agent (their name and email). The script, not the model, computes every figure and Buffett check. It prints only 10-K evidence from the last five fiscal years in USD millions, including the XBRL tag used.

Use the report as the exclusive numeric source for a short Buffett-style Markdown memo. Judge business quality only, never price. Select **own the business**, **watch it**, or **pass**; explain the conclusion using only values and results the script printed. If a required value or check is `not found` or `not known`, say that the evidence does not support that portion of the judgment. Save the memo as `memos/<TICKER>_buffett_memo.md` beside the app.

Do not estimate, replace missing values, or use FAskills or paid data. SEC requires a User-Agent identifying the requester; ask the student for it if it has not been supplied, and do not save it in project files.

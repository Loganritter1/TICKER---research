# Lab 20 — Project 2 Readiness

> Education only; not investment advice. This Lab 20 record reports the current state of the project and does not claim final Project 2 approval.

## 1. Partner cold-run note

| Field | Record |
|---|---|
| Repository tested | `https://github.com/Loganritter1/Project-2` |
| Partner platform | macOS terminal |
| README command on first run | `python -m streamlit run ".\\lab13 files\\app.py"` |
| First failure | `Error: Invalid value: File does not exist: .\\lab13 files\\app.py` |
| Why it failed | The README used a Windows-only path with backslashes. |
| Time first failure observed | 2:30 PM |
| Elapsed time to first failure | _Partner should add the elapsed duration if available._ |
| Result location on first run | No app result; Streamlit stopped at the missing-file error. |

## 2. Fix pushed and partner rerun

| Field | Record |
|---|---|
| Fix | README command changed to `python -m streamlit run "lab13 files/app.py"`. |
| Fix commit | `c32d7e5` — `Use cross-platform app path in README` |
| Partner rerun | Successful: the app opened in the partner's local browser after `git pull`. |
| Result location | Streamlit localhost page in the partner's browser. |
| Time successful rerun observed | 2:40 PM |
| Elapsed time to successful result | _Partner should add the elapsed duration if available._ |

## 3. Locked Changed-Input Record — AI closed

**Status: pending student AI-closed work.** Before running a new, untested changed-input scenario, the student must write the prediction below in their own words, commit and push this file, and only then run the scenario.

| Required item | Student record |
|---|---|
| Load-bearing input | _To complete with AI closed._ |
| Old value and units | _To complete with AI closed._ |
| New value and units | _To complete with AI closed._ |
| Expected direction of decision numbers | _To complete with AI closed._ |
| Expected effect on the decision | _To complete with AI closed._ |
| Pre-run commit hash and GitHub link | _Add after committing and pushing the prediction, before the run._ |
| Before output | _To complete after the pre-run commit._ |
| After output | _To complete after the run._ |
| What happened and why | _To complete after the run._ |

### Example format only — do not submit this as the AI-closed prediction

Replace this example with your own AI-closed writing before the pre-run commit:

| Required item | Example of the format |
|---|---|
| Load-bearing input | `Expected annual return estimate for [asset name]` |
| Old value and units | `[old value]% per year` |
| New value and units | `[new value]% per year` |
| Expected direction of decision numbers | `I expect [allocation / expected return / volatility] to [increase or decrease] because [my reasoning].` |
| Expected effect on the decision | `I expect the mandate verdict and recommendation to [stay the same / change] because [my reasoning].` |

### AI-assisted draft — not a valid Locked Changed-Input prediction

The app does not use an earnings control, so this draft treats “earnings” as an expected annual return estimate:

| Required item | Draft record |
|---|---|
| Load-bearing input | Expected annual return estimate |
| Old value and units | 10% per year |
| New value and units | 8% per year |
| Expected direction of decision numbers | I expect portfolio return to decrease. |
| Expected effect on the decision | I expect the mandate verdict and decision to stay the same because I do not expect the change to alter the allocation. |

## 4. Decision line

**Pilot the constrained portfolio process; do not adopt until final mandate terms, the point-in-time signal, and stress evidence are complete.**

## 5. Reflection

The cold run found a problem that was not visible on the developer's Windows machine: the README used a Windows-only path and failed on macOS. The app became reproducible only after the README was corrected and the partner reran it.

After the changed-input evidence is frozen, I will not change the data, mandate thresholds, allocation-grid size, or decision rule without documenting the change and rerunning the affected evidence.

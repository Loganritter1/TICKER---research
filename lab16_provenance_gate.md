# Lab 16 — Provenance Gate

## Decision question

On 31 March 2026, what did the training data actually show, based only on
information published by that date?

The accompanying program is [asof.py](asof.py). Run it from this folder with:

```powershell
python asof.py
```

The table and decision date are editable inputs at the top of the program.

## Point-in-time filter

I applied the required rules in order:

| Step | Rows removed | Reason |
|---|---|---|
| Missing ticker | 11 | The row cannot be assigned to a company. |
| Exact duplicate | 7 | It repeats row 6. |
| Published after 31 March | 3, 8, 10 | Those values were not public on the decision date. |
| Superseded revision | 2 | AAA February row 4 is a newer available publication. |

The resulting as-of panel contains rows **1, 4, 5, 6, 9, and 12**.

## Signals and proof

| Ticker | As-of signal | Naive signal |
|---|---:|---:|
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

I also checked the later decision date of 15 April 2026. At that date, the
as-of signals equal the naive signals for every ticker because all of the
training-table publications are then available.

## Revision logic

The revision rule uses a `(ticker, month)` key. For each such pair, the code
keeps the row with the latest publication date. AAA's February value therefore
uses row 4 (103.0, published 25 March), rather than row 2 (104.0, published
10 March). The point-in-time AAA signal is `(103 / 101 - 1) * 100 = +1.98%`.

## Reflection

The measured month describes when the activity happened; the publication date
describes when a trader could have seen the number. Look-ahead bias occurs when
a historical calculation uses a release or revision that arrived later.

For AAA, the naive result uses March's 109.0 index value, but that value was
published on 10 April and was unavailable on 31 March. Treating +5.83% as a
31 March signal would overstate what a backtest could have known. Rule 3 keeps
future releases out of the decision, while rule 4 makes sure the latest
available revision—not an obsolete value—is used.

## AI-use note

OpenAI Codex assisted with drafting and checking the standard-library Python
program. I ran the program, checked the required outputs, and can explain the
revision-selection logic.

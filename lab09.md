# Lab 09 — Pro-Forma Build: the Engine and the Known Answer

> Educational exercise only; not investment advice.

## Question

What are five years of a company's statements worth, built from assumptions I can defend, and how do I know the statements are right?

This workpaper builds a five-year (2026–2030) three-statement pro-forma for Asbury Automotive Group (ABG) in USD millions. The associated implementation is [proforma.py](proforma.py).

## Assumptions and opening balances

The model uses the Lab 09 ABG case assumptions: 1.8% annual organic revenue growth; 17.05% gross margin; SG&A as 66.5%, 65.5%, 64.5%, 64.5%, and 64.5% of gross profit; $120.0 annual non-cash impairment; $250.0 annual capital spending; 25.5% tax rate; $150.0 annual debt repayment and share buyback; 10.0% cost of equity; and 2.5% terminal growth.

History-based ratios are calculated directly in the code from the supplied FY2025 figures:

- Depreciation / opening PP&E = 82.4 / 3,070.4
- Inventory days = 2,135.8 / (17,999.0 − 3,071.7) × 365
- Floor plan / inventory = 2,027.0 / 2,135.8

The FY2025 opening balance sheet is revenue 17,999.0; inventory 2,135.8; PP&E 3,070.4; other assets 6,371.6; cash 40.4; floor plan 2,027.0; term debt 3,572.0; other liabilities 2,127.5; and equity 3,891.7.

## Build order

For each year, the model calculates the income statement using opening PP&E and opening debt balances for depreciation and interest. It then calculates balance-sheet accounts other than cash, FCFE, and cash last. If preliminary cash falls below the $25.0 minimum, the model draws the revolver (up to its $850.0 limit); when excess cash exists, it repays the revolver first.

FCFE is net income plus depreciation and impairment, less capital spending, inventory growth, other working-capital growth, and term-debt repayment, plus the change in floor-plan funding. Terminal value uses `(2030 FCFE + 2030 debt repayment) × (1 + g) / (ke − g)`.

## Known-answer validation

Running `python TSLA-research\proforma.py` produced the following results, matching the case answer to one decimal:

| Line | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | 18,323.0 | 19,678.3 |
| Operating income | 844.2 | 971.4 |
| Net income | 413.6 | 527.5 |
| Free cash flow to equity | 211.4 | 342.3 |
| Cash, year end | 101.8 | 719.8 |
| Assets − liabilities − equity | 0.0 | 0.0 |

The equity value is $5,237.3 million, the share of value after 2030 is 79.8%, and value per share is **$291.75** using 17.951349 million shares outstanding.

## Broken-balance test

I temporarily replaced computed FY2026 cash with the $40.4 opening cash. The program refused the model with:

```text
AssertionError: FY2026E balance-sheet gap: -61.4
```

The correct cash formula was restored afterward. The −61.4 gap is the FY2026 change in cash with the sign reversed, which shows why cash must be computed last rather than assumed.

## Floor plan

Floor-plan debt is inventory financing provided by manufacturer finance arms and banks. It rises with inventory; interest uses the opening balance. In this model, the change in floor-plan funding is inside FCFE because it finances operating inventory. Removing the line would require cash to fund the inventory directly and creates the large cash shortfall described in the case video.

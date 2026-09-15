# Lab 07 — Comparable-Company Policy and Implied Range

## P/E in plain language

Price-to-earnings (P/E) is a share price divided by earnings per share (EPS). Price per share is the market's current price for one common share. Diluted EPS is the period's GAAP profit available to common shareholders divided by diluted weighted-average shares; it includes the potential dilution from instruments such as options. A P/E multiple says how many dollars investors currently pay for one dollar of that year's earnings.

P/E makes earnings comparable on a per-share basis, so it can compare companies with very different sizes. It adds a market-based cross-check to a DCF: the DCF asks what the company's own forecast cash flows are worth, while P/E asks what investors are paying for similar companies' earnings. It does not replace the DCF.

A comparison is most useful when the companies have similar operations, accounting and earnings definitions, cyclicality, capital needs, leverage-related risk, growth prospects, and geography. It is misleading with negative or very small earnings, one-time gains or losses, materially different growth or risk, or inconsistent accounting. A lower P/E is not automatically better: it may reflect weaker expected growth, lower margins, greater risk, temporary earnings strength, or a less comparable business.

Question investigated: *What would Asbury's share be worth if the market assigned it the P/E multiples of comparable franchised vehicle retailers?*

## Peer policy before calculation

Franchised vehicle retail and service/parts matter more than a broad “automotive” label because they describe how revenue and earnings are made. Asbury sells new and used vehicles through franchised dealerships and also earns recurring service/parts and finance-and-insurance income. A manufacturer, supplier, rental company, or online marketplace can share the label “automotive” but have a different earnings model.

| Candidate | Decision | Business rationale |
|---|---|---|
| AutoNation (AN) | Use | Like Asbury, it is a large franchised dealership retailer with new/used-vehicle retail, service/parts, and F&I activity. Differences in brand mix, local markets, scale, and acquisition strategy still require interpretation. |
| Group 1 Automotive (GPI) | Qualified use | It also operates franchised dealerships with the core retail and service/parts activities, making it a relevant comparison. Qualify it for its different geographic footprint, brand mix, and international exposure, which can affect growth, margins, and the P/E investors assign. |

These decisions were made from operating fit, not from whether a peer's multiple makes Asbury look cheaper or more expensive.

## Frozen case calculation and interpretation

The calculator in `asbury_pe_comps.py` uses December 31, 2024 closing prices paired with subsequently reported FY2024 GAAP diluted EPS, as specified in the training case. It uses only P/E; cash and debt are not bridged into this equity per-share comparison.

Run from the repository folder:

```powershell
python TSLA-research\asbury_pe_comps.py
```

Using full-precision inputs, AN's P/E is 10.037825x and GPI's is 11.450149x. The two-peer median is 10.743987x. Applied to Asbury's $21.50 EPS, the implied range is $215.81 to $246.18 and the median-implied price is $231.00.

Before reading the leave-one-out output, the prediction was that removing GPI would lower the estimate: GPI has the higher P/E. The result is the one-peer AN reference estimate of $215.81, a $15.18 decrease from the two-peer median-implied estimate. With only one peer, there is no peer distribution from which to form a range; it is a reference estimate, not a range.

The result does not prove that Asbury is fairly valued. It is conditional on the peer policy and on the market's pricing of each peer's earnings. Different growth prospects, risk, earnings quality, or business mix can justify different multiples.

# Lab 08 — Deal Evidence and Valuation Triangulation: Tesla (TSLA)

> Educational exercise only; not investment advice.

## Reopen and explain

I reran the saved Asbury training calculator before changing cases:

```powershell
python TSLA-research\asbury_pe_comps.py
```

The Asbury two-peer median-implied Tesla price was $231.00. For each peer, divide its closing price by its annual GAAP diluted EPS to calculate its P/E multiple, then multiply that multiple by Tesla’s annual GAAP diluted EPS. Take the median of the two implied per-share prices. Do not add cash or subtract debt, since P/E is already an equity per-share valuation metric.

## Define / discover

**Target:** Tesla, Inc. (NASDAQ: TSLA)  
**Week 3 valuation date / comparison date:** September 10, 2026  
**Currency and share basis:** USD per common share; FY2025 GAAP diluted EPS for every company.

Tesla designs, manufactures, sells, and leases fully electric vehicles and energy generation/storage systems, and sells increasingly software-enabled services; it generally sells directly to customers. [Tesla 2025 Form 10-K, Item 1, p. 4](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm). Its FY2025 reported GAAP diluted EPS was **$1.08**, so P/E is mechanically usable. [Tesla 2025 Form 10-K, Consolidated Statements of Operations, p. 50](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm)

Focused research question: *Which listed operating company both manufactures and sells vehicles and had positive FY2025 GAAP diluted earnings public by September 10, 2026, while being sufficiently close to Tesla's EV/manufacturing economics to provide a clearly qualified P/E reference?*

## Peer policy written before candidate selection

I require a listed operating company whose principal economics include designing/building/selling vehicles and bearing vehicle-manufacturing, warranty, supply-chain, and demand risk. I prefer companies with material EV technology or battery exposure and positive, full-year GAAP diluted EPS available by the comparison date. I qualify rather than treat as fully interchangeable companies with a different propulsion mix, distribution model, financing arm, scale, geography, or material non-vehicle earnings. I exclude manufacturers without positive annual GAAP EPS from a P/E calculation; I retain them in the evidence table because their business fit still informs the limitation. I exclude manufacturers, suppliers, dealers, marketplaces, and software firms whose economics do not meet this policy.

**Rejection evidence set before searching:** a candidate would be rejected if its 10-K showed it was chiefly a dealer/supplier/marketplace instead of a vehicle manufacturer, if its annual EPS was nonpositive, or if its earnings were not public by September 10, 2026.

**AI process note:** I sent Tesla, the September 10, 2026 comparison date, and my unchanged peer policy independently to Codex and Google Antigravity. Antigravity identified GM and Rivian as candidates. I treated those suggestions as leads only; I opened the SEC sources and made the qualify/use decision for GM and the P/E exclusion decision for Rivian myself.

## Candidate evidence and my decisions

| Candidate | Decision | Primary-source business evidence | Important difference from Tesla | FY2025 reported diluted EPS; fiscal period; publication date | Decision reason |
|---|---|---|---|---|---|
| General Motors (NYSE: GM) | **Qualify / use** | GM says it designs, builds and sells trucks, crossovers, cars and parts, plus software-enabled services and subscriptions; it also provides financing through GM Financial. [2025 Form 10-K, Item 1, p. 4](https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm) | GM has an ICE-heavy multi-brand portfolio, dealer distribution and GM Financial; Tesla is direct-to-consumer and has energy generation/storage. GM also took large EV-realignment charges. | **$3.27**, year ended Dec. 31, 2025; released Jan. 27, 2026. [GM FY2025 results release](https://www.sec.gov/Archives/edgar/data/1467858/000146785826000011/gmq42025pressreleaseandfin.htm); [10-K Note 21, p. 100](https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm) | It meets the manufacturer policy and has positive annual GAAP diluted EPS, but the differences are material. I use it only as a one-peer qualified reference, not a peer range. |
| Rivian Automotive (NASDAQ: RIVN) | **Exclude from P/E** | Rivian reports Automotive and Software and Services segments; its consumer products include the R1T pickup and R1S SUV, and it has commercial vans. [2025 Form 10-K, Item 1, pp. 5–8](https://www.sec.gov/Archives/edgar/data/1874178/000187417826000008/rivn-20251231.htm) | Rivian is far smaller, still scaling production, lacks Tesla's energy business, and is loss-making; Amazon commercial vans are also a distinct customer concentration/mix issue. | **$(3.07)** diluted loss per share, year ended Dec. 31, 2025; 10-K filed Feb. 12, 2026. [2025 Form 10-K, Note 17, p. 106](https://www.sec.gov/Archives/edgar/data/1874178/000187417826000008/rivn-20251231.htm); [SEC filing index](https://www.sec.gov/Archives/edgar/data/1874178/000187417826000008/0001874178-26-000008-index.htm) | It meets the vehicle/EV operating-fit screen but fails the positive-EPS requirement. Price ÷ a negative annual EPS is not a meaningful P/E, so it is not entered in the calculator. |

No policy revision was made after reviewing candidates.

## Implement: inputs and result

| Company | Sep. 10, 2026 close | Annual reported diluted EPS | Fiscal year-end | EPS publication date | Source locator |
|---|---:|---:|---|---|---|
| Tesla | $363.56 | $1.08 | Dec. 31, 2025 | Jan. 29, 2026 | [Nasdaq historical data page](https://www.nasdaq.com/market-activity/stocks/tsla/historical) (opened); date-specific close cross-checked at [FinanceCharts](https://www.financecharts.com/stocks/TSLA/summary/price); [Tesla 10-K, p. 50](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm) |
| GM | $86.12 | $3.27 | Dec. 31, 2025 | Jan. 27, 2026 | [Nasdaq historical data page](https://www.nasdaq.com/market-activity/stocks/gm/historical) (opened); date-specific close cross-checked at [FinanceCharts](https://www.financecharts.com/stocks/GM/summary/price); [GM 10-K Note 21, p. 100](https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm) |
| Rivian (excluded) | $16.05 | $(3.07) | Dec. 31, 2025 | Feb. 12, 2026 | [Nasdaq historical data page](https://www.nasdaq.com/market-activity/stocks/rivn/historical) (opened); date-specific close cross-checked at [FinanceCharts](https://www.financecharts.com/stocks/RIVN/summary/price); [Rivian 10-K Note 17, p. 106](https://www.sec.gov/Archives/edgar/data/1874178/000187417826000008/rivn-20251231.htm) |

The annual reported EPS inputs are GAAP diluted EPS, not adjusted EPS. GM's $10.60 adjusted EPS was not used. All price and EPS values are USD per share and were public by the comparison date.

Run:

```powershell
python TSLA-research\tsla_pe_comps.py
```

Output: GM P/E = **26.336391x** and the one-qualified-peer reference estimate for Tesla is **$28.44** (26.336391 × $1.08). This is a reference estimate, not a range, because there is only one admitted peer.

## Validate

Hand check: $86.12 ÷ $3.27 = **26.336391x**, which matches the calculator. I predicted that removing GM would leave no usable peer because Rivian was excluded before the calculation. The calculator result is therefore **no estimate**, not a lower or higher valuation. I did not add Rivian or remove GM to change the result.

## Evolve: triangulation and skeptical review

| Method | Tesla result and date | Main assumption or limitation |
|---|---|---|
| Week 3 DCF | **$25.14–$29.47/share** sensitivity range; base **$26.99**. Inputs are the saved Tesla DCF. | Explicit FCFF growth (11%, 8%, 6%, 5%, 4%), 16.1% WACC, and 2%–4% terminal growth. The Week 3 market-price input of $367.81 was documented as Sept. 10 but the historical close is actually $367.81 on Sept. 9; this is a date-label mismatch in the earlier workpaper, not an input silently reused here. |
| Peer P/E | **$28.44/share** GM reference, using Sep. 10, 2026 prices and FY2025 GAAP diluted EPS. | One qualified peer only; GM's legacy ICE mix, dealer channel, financing arm, and special EV-realignment charges make the P/E a weak comparability reference. Rivian's negative EPS prevents P/E use. |

**Provisional call:** **watch/defer; do not initiate at the Sep. 10 close of $363.56.** Both the modeled DCF range and the qualified-peer reference use current reported operating earnings and cluster near $25–$29, but neither captures a separately evidenced value for Tesla's autonomy/AI optionality. I therefore withhold a broad peer range rather than average two methods or claim that $28.44 is a complete intrinsic value.

What could most easily change my mind: source-backed, repeatable evidence that Tesla's autonomy/software or energy earnings are material and durable, or a new DCF that explicitly and plausibly models those cash flows. A sustained recovery in automotive margins and FCFF would also change the DCF side.

**Second AI partner used:** Google Antigravity. I summarized its response below and checked the criticism against my sources.

**Google Antigravity criticism (summary):** The weakest assumption is treating GM's FY2025 GAAP P/E of 26.34x as a clean, ongoing automotive-earnings multiple for Tesla. GM's $3.27 GAAP diluted EPS included major EV-realignment charges, so the multiple may be distorted. Antigravity also noted that GM's ICE-heavy, dealer-distributed business with GM Financial differs materially from Tesla's direct-sales EV, energy-storage, and software-enabled model. The September 10, 2026 share prices are also being compared with FY2025 annual earnings, even though later 2026 filings were available.

**Question it asked:** If Tesla's energy-storage business and net cash are supported separately, and the DCF assumptions are revisited, does Tesla's core automotive business still fail the required return hurdle?

**My judgment: Accept in part.** I accept that GM's FY2025 EV-realignment charges and its different operating model weaken the GM comparison. This supports retaining GM only as one qualified P/E reference rather than treating it as a fully comparable peer or presenting a peer range. I reject changing the Lab 08 calculation to GM's adjusted EPS because the lab specifically requires annual reported diluted EPS and says to keep reported and adjusted earnings separate. I leave the price-versus-FY2025 timing concern unresolved: FY2025 annual EPS was public by the September 10 comparison date, so it meets the stated lab rule, but subsequent 2026 filings could change the economic interpretation. I would need source-supported evidence of Tesla's energy and autonomy cash flows, plus a documented revised DCF, before changing my watch/defer decision.

## Reflect

GM adds a market-based check on the value investors place on annual vehicle-manufacturing earnings, while Rivian confirms that a closer EV operating model can still be unusable for P/E when annual GAAP EPS is negative. The peer comparison corroborates rather than replaces the DCF because both methods, under their stated operating-earnings assumptions, are near $25–$29 per share. Their sharp difference from the market price is explainable only in part by business differences; it may reflect expectations for growth and optionality, but this work does not quantify them.

I therefore **watch/defer** and withhold a two-peer range. The defensible P/E reference is $28.44 and the saved DCF sensitivity range is $25.14–$29.47, not a mechanically averaged target. At the September 10, 2026 closing price of $363.56, I do not have sufficient source-supported operating evidence to initiate a position because that price is far above both the DCF sensitivity range and the one-qualified-peer P/E reference. I would reconsider after documented, economically meaningful autonomy/software or energy cash flows, or after evidence of durable automotive margin and FCFF improvement. My answer to the skeptical question is: I do not yet have a source-supported forecast that converts optionality into enough incremental cash flow; without it, it should not be treated as established valuation support.

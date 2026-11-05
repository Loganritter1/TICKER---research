"""Generate the three final Project 1 PDFs from frozen project records."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


DOCS = Path(__file__).resolve().parent / "docs"
NAVY = colors.HexColor("#12304A")
BLUE = colors.HexColor("#1F6E8C")
PALE = colors.HexColor("#EAF2F6")
GRAY = colors.HexColor("#5B6570")


def styles():
    base = getSampleStyleSheet()
    base.add(ParagraphStyle(name="TitleCustom", parent=base["Title"], fontName="Helvetica-Bold", fontSize=19, leading=23, textColor=NAVY, spaceAfter=8))
    base.add(ParagraphStyle(name="Subtitle", parent=base["Normal"], fontSize=9, leading=12, textColor=GRAY, spaceAfter=14))
    base.add(ParagraphStyle(name="H1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=NAVY, spaceBefore=7, spaceAfter=5))
    base.add(ParagraphStyle(name="BodyCustom", parent=base["BodyText"], fontSize=8.8, leading=11.5, spaceAfter=5))
    base.add(ParagraphStyle(name="Small", parent=base["BodyText"], fontSize=7.3, leading=9.1, spaceAfter=2))
    base.add(ParagraphStyle(name="Callout", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=NAVY, borderColor=BLUE, borderWidth=0.6, borderPadding=7, backColor=PALE, spaceAfter=8))
    base.add(ParagraphStyle(name="Footer", parent=base["Normal"], fontSize=7, textColor=GRAY, alignment=TA_CENTER))
    return base


S = styles()


def p(text, style="BodyCustom"):
    return Paragraph(text, S[style])


def table(rows, widths, small=True):
    data = [[p(cell, "Small" if small else "BodyCustom") for cell in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#B9C8D2")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F6F9FB")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#B9C8D2"))
    canvas.line(0.65 * inch, 0.55 * inch, 7.85 * inch, 0.55 * inch)
    canvas.setFillColor(GRAY)
    canvas.setFont("Helvetica", 7)
    canvas.drawCentredString(4.25 * inch, 0.37 * inch, f"FIN 43900 Project 1 | Educational use only | Page {doc.page}")
    canvas.restoreState()


def build(path, story):
    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=0.65 * inch, rightMargin=0.65 * inch, topMargin=0.58 * inch, bottomMargin=0.7 * inch)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def research_evolution():
    story = [p("Research Evolution", "TitleCustom"), p("Project 1 | Frozen record supporting the final recommendation", "Subtitle")]
    story += [p("Edition A status", "H1"), p("This record preserves the research evolution without revising or relabeling later work as the original Edition A. It documents Edition B and the evidence supporting its final architecture.")]
    story += [p("Edition B decision question", "H1"), p("Should a buy-side investment committee with no current Tesla position initiate, watch/defer, or not initiate TSLA at September 30, 2026, based on a valuation range with explicit conditions and reversal triggers?", "Callout")]
    story += [p("A-to-B evolution", "H1")]
    story.append(table([
        ["Area", "Edition B conclusion", "Evidence / reason"],
        ["Decision", "Do not initiate at $354.81; retain TSLA on a watch list.", "Frozen DCF and qualified GM references are far below the market reference."],
        ["Data", "Dated closes cross-checked; risk-free rate corrected to 5.29%; bridge uses FY2025 filed cash, investments, debt, and leases.", "Federal Reserve H.15 and Tesla 2025 Form 10-K reconciliation."],
        ["Model", "Five-year linked FCFF/WACC DCF, EV-to-equity bridge, sensitivity, reverse DCF, and operating-cash-reserve sensitivity.", "Replaces lab-stage FCFE work with an enterprise-value framework."],
        ["Uncertainty", "Terminal value is 99.0% of EV; GM is a qualified one-peer reference; reported liquidity may not all be excess cash.", "These limitations prevent a point-price conclusion."],
    ], [1.0*inch, 2.75*inch, 2.8*inch]))
    story += [p("What changed and why", "H1"), p("The final system moves the work from disconnected lab-stage valuation toward a linked FCFF/WACC engine that begins with a five-year three-statement projection and ends with a stated enterprise-to-equity bridge. The dated-input review corrected the preliminary 5.26% risk-free rate to 5.29%, resulting in a 14.46% WACC and $21.21 base DCF value per diluted share."), p("The recommendation is conditional rather than a claim that the market is wrong. At the frozen explicit cash flows, matching the market reference requires approximately 14.06% terminal growth, near the 14.46% WACC and outside a credible perpetuity assumption. GM is used as corroboration only: its ICE-heavy mix, dealer model, and GM Financial business make it an imperfect economic comparable."), p("AI-use evolution", "H1"), p("Codex supported project structuring, code assistance, research leads, and explanatory drafting. The dated risk-free-rate result was independently checked against the Federal Reserve H.15 series and corrected before the model was rerun. No AI-generated judgment was accepted without source evidence; the locked changed-input prediction was authored by the student without AI assistance.")]
    build(DOCS / "research-evolution.pdf", story)


def decision_memo():
    story = [p("Investment Committee Decision Memo", "TitleCustom"), p("Tesla, Inc. (TSLA) | Valuation date: September 30, 2026 | USD millions except per-share data", "Subtitle")]
    story += [p("Recommendation and committee ask", "H1"), p("DO NOT INITIATE at the September 30 reference price; retain TSLA on a watch list. The committee is asked to decline an initial position until a refreshed, independently reconciled model supports a materially different conclusion.", "Callout")]
    story += [p("Decision context", "H1"), p("Target: Tesla common stock. The fund has no position. The analysis uses FY2026E-FY2030E explicit forecasts, a perpetuity-growth terminal value, and 3.528bn FY2025 diluted weighted-average shares consistently across methods. Automotive, energy, and services are forecast. The bridge adds reported cash and short-term investments, deducts debt and finance leases, and does not separately value future products, optionality, or unmodeled capital claims.")]
    story += [p("Valuation evidence", "H1")]
    story.append(table([
        ["Method / measure", "Result", "Interpretation"],
        ["Base FCFF DCF", "$21.21 / diluted share", "EV $39,158.52m; equity value $74,841.52m; WACC 14.46%; terminal growth 3.0%."],
        ["DCF sensitivity", "$19.02-$24.34 / share", "15.5% / 2.0% through 13.5% / 4.0% WACC-growth combinations."],
        ["GM EV / revenue reference", "$20.38 / share", "Qualified one-peer operating reference; not mechanically averaged."],
        ["GM GAAP P/E reference", "$25.43 / share", "Qualified equity-value reference using FY2025 GAAP EPS."],
        ["Market reference", "$354.81 / share", "September 30 regular close; used for comparison and reverse DCF."],
    ], [1.55*inch, 1.35*inch, 3.65*inch]))
    story += [p("Range, assumptions, and limitations", "H1"), p("The frozen valuation range is $19.02-$25.43 per diluted share. The FY2026-FY2027 capex profile produces negative FCFF of $8,781.8m and $1,770.9m before FCFF turns positive in FY2028. Terminal value is 99.0% of base enterprise value. Retaining $10bn as operating cash lowers the DCF result to $18.38 per share. A reverse DCF requires roughly 14.06% terminal growth to reach the market reference, holding explicit cash flows and WACC constant."), p("The range is sensitive to beta, ERP, cost of debt, terminal-growth, and operating-cash policy. GM is not a close economic peer because of its ICE-heavy mix, dealer model, and GM Financial business. These methods corroborate direction but do not establish a stand-alone price target.")]
    story += [p("Reversal conditions and monitoring", "H1"), p("Reconsider after independently reconciling dated WACC, close, shares, and bridge inputs; observing sustained positive FCFF and capex efficiency above the base forecast; evidence of durable automotive gross-margin expansion; or a revised case supporting value nearer the market price without terminal growth near WACC. Monitor quarterly automotive, energy, and services revenue; gross margin; capex; liquidity; debt and leases; diluted shares; and updated guidance."), p("This is a FIN 43900 course-project valuation and not investment advice.", "Small")]
    build(DOCS / "decision-memo.pdf", story)


def validation():
    story = [p("Validation and AI-Use Record", "TitleCustom"), p("Tesla, Inc. (TSLA) | Frozen Project 1 record | October 2026", "Subtitle")]
    story += [p("AI-use disclosure", "H1"), p("Codex was used for project structuring, code assistance, research leads, and explanatory support. Its output was treated as a lead or draft only. A preliminary 5.26% risk-free rate was checked against the official Federal Reserve H.15 series, corrected to 5.29%, and rerun through the model. The disposition is qualified and corrected; AI-generated judgment was not accepted without cited evidence.")]
    story += [p("Validation register", "H1")]
    story.append(table([
        ["Check", "Pass criterion / result", "Evidence"],
        ["Known-answer reconciliation", "EV $39,158.52m; equity $74,841.52m; $21.21/share within stated rounding tolerance. PASS.", "test_known_answer_base_case"],
        ["Source / definition", "Dated prices cross-checked; Treasury rate checked against official Fed series; cash, investments, debt, leases, and shares reconciled. PASS.", "freeze-2026-09-30.md"],
        ["Three-statement articulation", "All forecast-year balance-sheet gaps equal $0.00m; cash flow ties to cash. PASS.", "test_three_statement_articulation_and_bridge"],
        ["DCF monotonicity", "Value falls when WACC rises and rises when terminal growth rises. PASS.", "test_dcf_monotonicity"],
        ["Bridge and liquidity", "Base bridge and $10bn operating-cash-reserve sensitivity reconcile. PASS.", "Bridge test and freeze record"],
        ["Peer consistency", "Pre-existing policy, matching definitions, and GM qualification reviewed. PASS.", "lab08.md and tsla_ev_comps.py"],
        ["Highest-risk failure", "Terminal growth at WACC raises ValueError. PASS.", "test_highest_risk_terminal_value_failure_fails_loudly"],
        ["Cold run", "python tesla_fcff.py and six-test suite complete without third-party packages for the engine. PASS.", "Run recorded October 8, 2026"],
    ], [1.4*inch, 3.55*inch, 1.6*inch]))
    story += [p("Locked changed-input record", "H1")]
    story.append(table([
        ["Field", "Student-authored record"],
        ["Pre-run commitment", "October 6, 2026, 7:02 PM; pre-run commit 6b732cd (7:06 PM EDT)."],
        ["Exact change", "FY2027 automotive revenue growth increased from 4% to 6%; all other independent assumptions unchanged."],
        ["AI-off prediction", "FY2027 FCFF will increase. The watch/defer decision will likely not change because a small driver change cannot close the valuation-market gap."],
        ["Actual result", "FY2027 FCFF increased from negative $1,770.89m to negative $1,763.49m (+$7.40m). DCF value increased from $21.21 to $21.47 per share (+$0.25)."],
        ["Reconciliation", "Direction matched. Higher FCFF was partly offset by operating working-capital needs; the decision did not change."],
    ], [1.45*inch, 5.1*inch]))
    story += [p("Limits and reproducibility", "H1"), p("The valuation remains dependent on WACC, terminal growth, cash classification, and a weighted-average share-count convention. Run the engine with python tesla_fcff.py and validation with python -m unittest discover -s tests -p \"test_*.py\" -v. The semi-adjustable workbench is launched with python -m streamlit run app.py.")]
    build(DOCS / "validation-and-ai-use.pdf", story)


if __name__ == "__main__":
    research_evolution()
    decision_memo()
    validation()
    print("Generated three Project 1 submission PDFs in docs/.")

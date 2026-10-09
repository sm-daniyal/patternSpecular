"""Compile the 17-slide Pattern Specular Walkthrough Presentation Deck (PDF).

Designed for engineering leaders, AI researchers, and hiring managers.
Highlights AI-native software engineering, multi-agent debate, empirical statistical gating,
and sovereign multi-jurisdiction compliance.

Typography & Design Tokens:
- Widescreen 16:9 layout (1152 x 648 pt)
- Editorial Display: Georgia / Georgia-Bold
- Modern Technical Sans: Segoe UI / Segoe UI-Bold
- Rosewood Palette: #b83a58 (Rosewood), #1e1317 (Charcoal), #6b5e62 (Slate Muted), #fbf9f9 (Canvas)
- Clean math rendering: HTML entities & italicized mathematical notations (p < 0.05, k >= 3)
"""

import os
from pathlib import Path

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.colors import HexColor, transparent
from reportlab.lib.pagesizes import landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

DECK_DIR = Path(__file__).resolve().parent
ASSETS_DIR = DECK_DIR / "assets"
OUTPUT_PDF = DECK_DIR / "pattern-specular-deck.pdf"

PAGE_WIDTH = 1152
PAGE_HEIGHT = 648

# Register system TrueType fonts for editorial publication-grade typography
FONT_SERIF = "Helvetica"
FONT_SERIF_BOLD = "Helvetica-Bold"
FONT_SANS = "Helvetica"
FONT_SANS_BOLD = "Helvetica-Bold"
FONT_SANS_ITALIC = "Helvetica-Oblique"

try:
    pdfmetrics.registerFont(TTFont("Georgia", "C:/Windows/Fonts/georgia.ttf"))
    pdfmetrics.registerFont(TTFont("Georgia-Bold", "C:/Windows/Fonts/georgiab.ttf"))
    pdfmetrics.registerFont(TTFont("Georgia-Italic", "C:/Windows/Fonts/georgiai.ttf"))
    FONT_SERIF = "Georgia"
    FONT_SERIF_BOLD = "Georgia-Bold"
except Exception:
    pass

try:
    pdfmetrics.registerFont(TTFont("SegoeUI", "C:/Windows/Fonts/segoeui.ttf"))
    pdfmetrics.registerFont(TTFont("SegoeUI-Bold", "C:/Windows/Fonts/segoeuib.ttf"))
    pdfmetrics.registerFont(TTFont("SegoeUI-Italic", "C:/Windows/Fonts/segoeuii.ttf"))
    FONT_SANS = "SegoeUI"
    FONT_SANS_BOLD = "SegoeUI-Bold"
    FONT_SANS_ITALIC = "SegoeUI-Italic"
except Exception:
    pass

# Rosewood Executive Palette
COLOR_ROSEWOOD = HexColor("#b83a58")
COLOR_ROSEWOOD_DARK = HexColor("#8e243d")
COLOR_ROSEWOOD_LIGHT = HexColor("#fdf2f4")
COLOR_ROSEWOOD_BORDER = HexColor("#f2d6dc")
COLOR_CHARCOAL = HexColor("#1e1317")
COLOR_MUTED = HexColor("#625559")
COLOR_CANVAS = HexColor("#fbf9f9")
COLOR_CARD = HexColor("#ffffff")
COLOR_BORDER = HexColor("#e8dfdf")
COLOR_TAG_BG = HexColor("#f4eeee")
COLOR_ACCENT_GREEN = HexColor("#1b7340")

styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    "DeckTitle",
    parent=styles["Heading1"],
    fontSize=26,
    leading=32,
    textColor=COLOR_CHARCOAL,
    fontName=FONT_SERIF_BOLD,
    spaceAfter=4,
)

style_section_kicker = ParagraphStyle(
    "SectionKicker",
    parent=styles["Normal"],
    fontSize=10,
    leading=12,
    textColor=COLOR_ROSEWOOD,
    fontName=FONT_SANS_BOLD,
    textTransform="uppercase",
    spaceAfter=2,
)

style_subtitle = ParagraphStyle(
    "DeckSubtitle",
    parent=styles["Normal"],
    fontSize=13,
    leading=18,
    textColor=COLOR_MUTED,
    fontName=FONT_SANS,
    spaceAfter=12,
)

style_body = ParagraphStyle(
    "DeckBody",
    parent=styles["Normal"],
    fontSize=11,
    leading=16,
    textColor=COLOR_CHARCOAL,
    fontName=FONT_SANS,
)

style_body_muted = ParagraphStyle(
    "DeckBodyMuted",
    parent=styles["Normal"],
    fontSize=10,
    leading=14.5,
    textColor=COLOR_MUTED,
    fontName=FONT_SANS,
)

style_card_title = ParagraphStyle(
    "CardHeader",
    parent=styles["Normal"],
    fontSize=12.5,
    leading=16,
    textColor=COLOR_ROSEWOOD,
    fontName=FONT_SANS_BOLD,
    spaceAfter=4,
)

style_card_title_dark = ParagraphStyle(
    "CardHeaderDark",
    parent=styles["Normal"],
    fontSize=12.5,
    leading=16,
    textColor=COLOR_CHARCOAL,
    fontName=FONT_SANS_BOLD,
    spaceAfter=4,
)

style_bullet = ParagraphStyle(
    "DeckBullet",
    parent=styles["Normal"],
    fontSize=10.5,
    leading=15.5,
    textColor=COLOR_CHARCOAL,
    fontName=FONT_SANS,
    leftIndent=10,
    spaceAfter=4,
)

style_footer = ParagraphStyle(
    "DeckFooter",
    parent=styles["Normal"],
    fontSize=8.5,
    leading=10,
    textColor=COLOR_MUTED,
    fontName=FONT_SANS,
)


def make_card(content_flowables, bg=COLOR_CARD, border=COLOR_BORDER, padding=12):
    t = Table([[content_flowables]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.75, border),
                ("TOPPADDING", (0, 0), (-1, -1), padding),
                ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
                ("LEFTPADDING", (0, 0), (-1, -1), padding),
                ("RIGHTPADDING", (0, 0), (-1, -1), padding),
            ]
        )
    )
    return t


def header_block(kicker_text, title_text, subtitle_text=""):
    elements = [
        Paragraph(kicker_text.upper(), style_section_kicker),
        Paragraph(title_text, style_title),
    ]
    if subtitle_text:
        elements.append(Paragraph(subtitle_text, style_subtitle))
    else:
        elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", thickness=1, color=COLOR_ROSEWOOD_BORDER, spaceAfter=14))
    return elements


def footer_block(slide_num, tag="Pattern Specular · AI-Native Talent Bias Analysis"):
    t = Table(
        [
            [
                Paragraph(f"<b>{tag}</b> · Syed Daniyal (sm-daniyal)", style_footer),
                Paragraph(f"{slide_num:02d} / 17", ParagraphStyle("RightFooter", parent=style_footer, alignment=2, fontName=FONT_SANS_BOLD)),
            ]
        ],
        colWidths=[820, 252],
    )
    t.setStyle(
        TableStyle(
            [
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return [
        Spacer(1, 8),
        HRFlowable(width="100%", thickness=0.5, color=COLOR_BORDER, spaceAfter=3),
        t,
    ]


def generate_qr_drawing(url, size=110):
    d = Drawing(size, size)
    qr = QrCodeWidget(url)
    qr.barWidth = size
    qr.barHeight = size
    qr.qrVersion = 3
    d.add(qr)
    return d


def build_deck():
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=40,
        rightMargin=40,
        topMargin=32,
        bottomMargin=20,
    )
    story = []

    # ====================================================
    # SLIDE 01: Title Slide
    # ====================================================
    story.append(Spacer(1, 35))
    login_img_path = ASSETS_DIR / "01-login-screen.png"
    login_img = None
    if login_img_path.exists():
        login_img = Image(str(login_img_path), width=490, height=275)

    title_left = [
        Paragraph("PATTERN SPECULAR", ParagraphStyle("BrandKicker", fontSize=12, fontName=FONT_SANS_BOLD, textColor=COLOR_ROSEWOOD, spaceAfter=8)),
        Paragraph("The Pattern Specular", ParagraphStyle("BigTitle", fontSize=40, leading=46, fontName=FONT_SERIF_BOLD, textColor=COLOR_CHARCOAL, spaceAfter=10)),
        HRFlowable(width="80%", thickness=2, color=COLOR_ROSEWOOD, spaceAfter=14),
        Paragraph("A Longitudinal Bias-Pattern Analysis Platform for Talent Writing", ParagraphStyle("BigSub", fontSize=16, leading=22, fontName=FONT_SANS_BOLD, textColor=COLOR_ROSEWOOD, spaceAfter=16)),
        Paragraph(
            "<i>\"Surfaces unconscious bias tendencies in a manager's own writing, anchored by statutory citations and mathematical proof, so they can decide what to change.\"</i>",
            ParagraphStyle("CalloutQuote", fontSize=13.5, leading=20, textColor=COLOR_CHARCOAL, fontName=FONT_SERIF, spaceAfter=22),
        ),
        Paragraph("<b>Engineering Portfolio Showcase:</b> Applied AI Systems &amp; AI-Native Architecture<br/><b>Author:</b> Syed Daniyal (sm-daniyal) · <b>Stack:</b> Google Gemini 2.5/3.5 · React 19 · FastAPI · Neon PostgreSQL", style_body_muted),
    ]

    t1 = Table([[title_left, login_img if login_img else Paragraph("", style_body)]], colWidths=[570, 502])
    t1.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(t1)
    story.extend(footer_block(1, "The Pattern Specular · Architecture Showcase"))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 02: About the Author
    # ====================================================
    story.extend(header_block("About the Author", "Syed Daniyal (sm-daniyal)", "Applied AI & AI-Native Systems Developer"))

    bio_left = [
        Paragraph("<b>Engineering Profile</b>", style_card_title),
        Paragraph("• <b>AI-Native Architecture:</b> LLM multi-agent debate topologies, schema-first structured outputs with Instructor, prompt calibration, and deterministic AST verification.", style_bullet),
        Paragraph("• <b>Modern Full-Stack Systems:</b> React 19 concurrent client, TanStack Router/Query, FastAPI asynchronous I/O, and Neon Serverless PostgreSQL with SQLAlchemy 2.0.", style_bullet),
        Paragraph("• <b>Statistical Data Science:</b> Finite-sample exact inference (two-tailed Fisher's exact test, <i>p</i> &lt; 0.05), and differential privacy guarantees (<i>k</i> &ge; 3 anonymity).", style_bullet),
        Paragraph("• <b>Multi-Jurisdictional Compliance:</b> India (Code on Wages 2019, RPwD Act 2016), Singapore (TAFEP), US (Title VII, ADEA), and UK (Equality Act 2010).", style_bullet),
        Spacer(1, 6),
        Paragraph("<b>Contact &amp; Code:</b> github.com/sm-daniyal/patternSpecular · India", style_body_muted),
    ]

    bio_right = [
        Paragraph("<b>The Project Genesis: Why Build Pattern Specular?</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("Unconscious bias training in corporate settings suffers from an acute feedback void: managers attend mandatory seminars, but <b>zero real-time systems assist the actual documents they write</b> — Job Descriptions, Performance Reviews, and Promotion Write-ups.", style_body),
        Spacer(1, 6),
        Paragraph("Conventional linting tools either rely on dumb keyword matching (high false positives) or generic LLM rewrites that erase the author's authentic voice. Surveillance DEI tools spy on managers, triggering resentment.", style_body),
        Spacer(1, 6),
        Paragraph("<b>The AI-Native Solution:</b> Pattern Specular acts as a personal, sovereign mirror. It operates in strict manager privacy, combines sub-10ms deterministic lemmatizers with high-reasoning Gemini models, and only highlights recurring habits once mathematically proven across time.", style_body),
    ]

    t_bio = Table([[make_card(bio_left, padding=16), make_card(bio_right, padding=16)]], colWidths=[530, 542])
    story.append(t_bio)
    story.extend(footer_block(2))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 03: Deck Contents & Flow
    # ====================================================
    story.extend(header_block("Contents", "What's in this Deck", "Structured across Product Design, Applied AI Engineering, and Production Learnings"))

    col1 = [
        Paragraph("<b>THE PRODUCT</b>", style_card_title),
        Spacer(1, 6),
        Paragraph("<b>04</b> Motivation: Where Training Stops, This Begins", style_bullet),
        Paragraph("<b>05</b> What It Does: Evidence In, Decision Theirs", style_bullet),
        Paragraph("<b>06</b> Writing Tools: JD Studio &amp; Feedback Checkpoint", style_bullet),
        Paragraph("<b>07</b> Seeing Patterns: Longitudinal Trend Analysis", style_bullet),
        Paragraph("<b>08</b> The HR View: Firm Trends &amp; <i>k</i> &ge; 3 Privacy", style_bullet),
    ]
    col2 = [
        Paragraph("<b>THE ENGINEERING</b>", style_card_title),
        Spacer(1, 6),
        Paragraph("<b>09</b> The 7-Stage Bias Detection Hybrid Pipeline", style_bullet),
        Paragraph("<b>10</b> LLM as a Judge: Multi-Agent Confidence Gating", style_bullet),
        Paragraph("<b>11</b> Research Grounding: 5 Landmark ML Papers", style_bullet),
        Paragraph("<b>12</b> Self-Growth: Autonomous 4-Agent Debate Loop", style_bullet),
        Paragraph("<b>13</b> Architecture Topology: Decoupled Cloud-Native", style_bullet),
        Paragraph("<b>14</b> Schema Foundations: Privacy &amp; Audit Trail", style_bullet),
    ]
    col3 = [
        Paragraph("<b>WRAP-UP &amp; FUTURE</b>", style_card_title),
        Spacer(1, 6),
        Paragraph("<b>15</b> Version 2 Roadmap: Multimodal &amp; RAG", style_bullet),
        Paragraph("<b>16</b> Production Engineering Reflections", style_bullet),
        Paragraph("<b>17</b> Repository &amp; Developer Contact", style_bullet),
    ]

    t_contents = Table([[make_card(col1, padding=14), make_card(col2, padding=14), make_card(col3, padding=14)]], colWidths=[350, 370, 350])
    story.append(t_contents)
    story.extend(footer_block(3))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 04: Motivation
    # ====================================================
    story.extend(header_block("Motivation", "Where bias training stops, this begins.", "The invisible gap between theoretical awareness and real managerial writing"))

    m1 = [
        Paragraph("<b>01 · The Critical Training Void</b>", style_card_title_dark),
        Spacer(1, 3),
        Paragraph("Managers routinely complete annual fair-hiring and unconscious bias modules. Yet nothing audits or coaches the job descriptions, interview assessments, and promotion cases they actually submit. The training is theoretical; the writing is where hiring and compensation decisions are codified.", style_body),
    ]
    m2 = [
        Paragraph("<b>02 · Bias in Writing is an Aggregate Pattern</b>", style_card_title_dark),
        Spacer(1, 3),
        Paragraph("In isolation, describing one candidate as <i>'supportive and polite'</i> or another as an <i>'aggressive go-getter'</i> reads as completely unremarkable. Tendencies only emerge as statistically verifiable patterns when observed across <b>dozens of evaluations over multiple quarters</b> — which nobody reviews.", style_body),
    ]
    m3 = [
        Paragraph("<b>03 · The Pattern Specular Response</b>", style_card_title_dark),
        Spacer(1, 3),
        Paragraph("Pattern Specular catches statutory infractions as they are drafted, benchmarks candidate feedback against objective criteria, and surfaces longitudinal tendencies across time using Fisher's exact test (<i>p</i> &lt; 0.05) — <b>acting as an authentic mirror, never a punitive scoreboard</b>.", style_body),
    ]

    t_mot = Table([[make_card(m1, padding=14)], [Spacer(1, 8)], [make_card(m2, padding=14)], [Spacer(1, 8)], [make_card(m3, padding=14)]], colWidths=[1072])
    story.append(t_mot)
    story.extend(footer_block(4))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 05: What It Does — Core Invariants
    # ====================================================
    story.extend(header_block("What It Does", "Evidence in, decision theirs.", "A calibrated personal mirror for writers, preserving 100% human agency"))

    callout_s5 = [
        Paragraph("<b>A flag</b> is a specific span of writing marked as potentially biased, accompanied by a plain-language explanation and a statutory citation. The manager retains complete authority on whether to accept, revise, or dismiss.", ParagraphStyle("CalloutP", fontSize=12, fontName=FONT_SERIF, textColor=COLOR_CHARCOAL)),
    ]
    story.append(make_card(callout_s5, bg=COLOR_ROSEWOOD_LIGHT, border=COLOR_ROSEWOOD_BORDER, padding=10))
    story.append(Spacer(1, 10))

    w_left = [
        Paragraph("<b>Core Capabilities</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• <b>Every Flag is Cited:</b> Cites labor legislation (India Code on Wages 2019, RPwD Act 2016; Singapore TAFEP; US Title VII; UK Equality Act) or peer-reviewed research. Uncited flags are dropped.", style_bullet),
        Paragraph("• <b>Statutory Criteria Drift Check:</b> Verifies whether feedback drifts into personality critiques while ignoring objective job criteria.", style_bullet),
        Paragraph("• <b>Statistically Significant Habits:</b> Only patterns clearing Fisher's Exact Test (<i>p</i> &lt; 0.05) are surfaced. A single flag is never called a pattern.", style_bullet),
        Paragraph("• <b>Firm Aggregates Only:</b> HR accesses high-level trends; managers' individual drafts are structurally hidden.", style_bullet),
    ]

    w_right = [
        Paragraph("<b>Non-Negotiable Design Invariants</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• <b>Mirror, Not Judge:</b> Shows recurring patterns; never scores, grades, or penalizes the manager.", style_bullet),
        Paragraph("• <b>Private by Architecture:</b> HR cannot read any manager's writing; the database has no query path there.", style_bullet),
        Paragraph("• <b>Non-Blocking:</b> Every flag is dismissible with one click; workflow submission is never blocked.", style_bullet),
        Paragraph("• <b>Always Grounded:</b> Academic research or regulatory guidance backs every recommendation.", style_bullet),
        Paragraph("• <b>Not a Chatbot · Not a Hiring Gate:</b> Pure applied-AI assistance leaving full decision authority with the user.", style_bullet),
    ]

    t_s5 = Table([[make_card(w_left, padding=14), make_card(w_right, padding=14)]], colWidths=[530, 542])
    story.append(t_s5)
    story.extend(footer_block(5))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 06: Manager Surfaces — Three Writing Tools
    # ====================================================
    story.extend(header_block("Product · Manager", "Three writing tools, one bias-detection pipeline underneath.", "Dual-pass detection: sub-10ms lemma matcher + asynchronous Gemini contextual pass"))

    img_jd_path = ASSETS_DIR / "06-jd-studio-hero.png"
    img_jd = Image(str(img_jd_path), width=620, height=348) if img_jd_path.exists() else Paragraph("", style_body)

    desc_tools = [
        Paragraph("<b>1 · Instant Flags on Known Phrasing</b>", style_card_title),
        Paragraph("Established statutory terms caught the moment they are typed via fast in-memory lemmatization — zero LLM overhead.", style_bullet),
        Spacer(1, 4),
        Paragraph("<b>2 · Contextual LLM Pass on Pause</b>", style_card_title),
        Paragraph("When the manager pauses typing, Google Gemini evaluates the broader sentence context, catching coded proxies and genuine occupational exceptions (GDOR).", style_bullet),
        Spacer(1, 4),
        Paragraph("<b>3 · Evidence &amp; Suggested Rewrites</b>", style_card_title),
        Paragraph("Every flag displays the flagged phrase, statutory justification, and 2–3 one-click neutral alternatives (`motivated`, `driven`).", style_bullet),
        Spacer(1, 6),
        Paragraph("<b>The Three Surfaces:</b><br/>• <b>JD Studio:</b> Flags exclusionary terms in job ads.<br/>• <b>Feedback Checkpoint:</b> Checks review text against original JD criteria.<br/>• <b>Promotion Writeup:</b> Checks cases against 360 peer feedback.", style_body_muted),
    ]

    t_s6 = Table([[img_jd, make_card(desc_tools, padding=14)]], colWidths=[630, 442])
    story.append(t_s6)
    story.extend(footer_block(6))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 07: Manager Surfaces — Longitudinal Dashboard
    # ====================================================
    story.extend(header_block("Product · Manager", "A pattern is a statistical finding, not an impression.", "Finite-sample hypergeometric testing (Fisher's exact test) prevents alert fatigue"))

    img_pd_path = ASSETS_DIR / "07-pattern-dashboard.png"
    img_pd = Image(str(img_pd_path), width=620, height=348) if img_pd_path.exists() else Paragraph("", style_body)

    desc_stat = [
        Paragraph("<b>1 · Longitudinal Monthly View</b>", style_card_title),
        Paragraph("Tracks flag frequency over time across age, gender, disability, race, and family status categories, visualizing continuous improvement.", style_bullet),
        Spacer(1, 4),
        Paragraph("<b>2 · Fisher's Exact Test Gating</b>", style_card_title),
        Paragraph("Alerts like <i>'family commitment appears in 5 documents — all 5 about women'</i> only trigger when the 2 &times; 2 contingency matrix calculates <b><i>p</i> &lt; 0.05</b>. Five flags across 100 documents is ignored as noise.", style_bullet),
        Spacer(1, 4),
        Paragraph("<b>3 · Deep Evidence Drill-Down</b>", style_card_title),
        Paragraph("Managers can expand any recurring pattern to inspect historical source documents, verbatim quotes, and original context.", style_bullet),
        Spacer(1, 4),
        Paragraph("<b>4 · Manager Behavioral Adoption</b>", style_card_title),
        Paragraph("Measures the proportion of flags voluntarily revised vs. dismissed over 12 months, charting genuine mindset evolution.", style_bullet),
    ]

    t_s7 = Table([[img_pd, make_card(desc_stat, padding=14)]], colWidths=[630, 442])
    story.append(t_s7)
    story.extend(footer_block(7))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 08: HR View — Aggregates & Anonymity
    # ====================================================
    story.extend(header_block("Product · HR", "HR sees firm-level trends and cannot see any manager's writing.", "Structural k-anonymity guarantee: private at the database schema layer"))

    img_hr1_path = ASSETS_DIR / "08-hr-trends-dashboard.png"
    img_hr2_path = ASSETS_DIR / "08-hr-dictionary-review.png"
    img_hr1 = Image(str(img_hr1_path), width=520, height=292) if img_hr1_path.exists() else Paragraph("", style_body)
    img_hr2 = Image(str(img_hr2_path), width=520, height=292) if img_hr2_path.exists() else Paragraph("", style_body)

    story.append(Table([[img_hr1, img_hr2]], colWidths=[536, 536]))
    story.append(Spacer(1, 8))

    hr_notes = [
        Paragraph("<b>Left: Firm-Wide Effectiveness Portal</b> — High-level adoption KPIs (82% revision rate, total document throughput). <b>Small-cell suppression:</b> Any cohort with fewer than 3 distinct managers is suppressed (<i>k</i> &ge; 3 anonymity enforced in SQL).", style_body),
        Paragraph("<b>Right: Autonomous Dictionary Review Queue</b> — Interactive word cloud and 4-agent debate drawer for emerging workplace slang. HR humans retain the final approval button before terms enter live dictionaries.", style_body_muted),
    ]
    story.append(make_card(hr_notes, padding=8))
    story.extend(footer_block(8))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 09: Engineering — 7-Stage Pipeline
    # ====================================================
    story.extend(header_block("Engineering · Engine", "The 7-stage bias-detection hybrid pipeline.", "Deterministic AST and lemmatization guardrails ensure zero hallucinated flags reach users"))

    pipe_rows = [
        ("Stage 1", "Deterministic Pass", "spaCy regex & lemmatizer (<10ms). Instant exact matches against region-scoped statutory lexicons."),
        ("Stage 2", "Contextual Pass", "Async Google Gemini 3.5 Flash Lite call. Evaluates coded language, agentic/communal adjectives, and GDOR exceptions."),
        ("Stage 3", "Verbatim Adjudicator", "Strict Python substring validator. Verifies that the flagged quote exists verbatim in the user text; non-exact spans dropped."),
        ("Stage 4", "Statutory Rulings", "Applies labor law definitions. Checks genuine occupational justifications (e.g. physical fitness in safety roles)."),
        ("Stage 5", "Suppression Module", "Computes sentence-level SHA-256 fingerprint hashes against historical manager dismissals, suppressing repeats."),
        ("Stage 6", "LLM Judge Gate", "Multi-sampling confidence consensus for borderline flags (threshold: agreement rate &ge; 0.70)."),
        ("Stage 7", "Recommendations", "Generates 2–3 evidence-grounded neutral alternative rewrite chips (`motivated`, `driven`)."),
    ]
    p_cards = []
    for num, name, desc in pipe_rows:
        c = [Paragraph(f"<b>{num}: {name}</b>", style_card_title), Spacer(1, 1), Paragraph(desc, style_body_muted)]
        p_cards.append([make_card(c, padding=5)])

    story.append(Table(p_cards, colWidths=[1072]))
    story.extend(footer_block(9))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 10: Engineering — LLM as a Judge
    # ====================================================
    story.extend(header_block("Engineering · Judge", "A second model must independently agree, or the flag is held back.", "The Judge acts as an adversarial confidence gate, eliminating generator self-preference bias"))

    j1 = [
        Paragraph("<b>1 · Different Model Architecture</b>", style_card_title),
        Paragraph("To mitigate LLM self-preference bias, the Judge stage evaluates candidate flags without seeing the generator's explanation or internal chain-of-thought.", style_body),
    ]
    j2 = [
        Paragraph("<b>2 · Rubric Checklist Decomposition</b>", style_card_title),
        Paragraph("Instead of asking for an unstable 0–1 score, the Judge answers narrow boolean questions: <code>references_characteristic</code>, <code>gdor_plausible</code>, and <code>stated_objectively</code>.", style_body),
    ]
    j3 = [
        Paragraph("<b>3 · Confidence as Empirical Frequency</b>", style_card_title),
        Paragraph("Confidence is derived from empirical agreement frequency across <i>N</i> independent stochastic samples. Flags with agreement &lt; 0.70 are discarded.", style_body),
    ]
    j4 = [
        Paragraph("<b>4 · Position-Invariant Shuffling</b>", style_card_title),
        Paragraph("Candidate flag order is randomized prior to prompt serialization to eliminate list-position and primacy bias.", style_body),
    ]

    t_judge = Table([[make_card(j1, padding=12), make_card(j2, padding=12)], [make_card(j3, padding=12), make_card(j4, padding=12)]], colWidths=[530, 542])
    story.append(t_judge)
    story.append(Spacer(1, 8))

    formula_card = [
        Paragraph("<b>The Deterministic Adjudication Formula:</b>", style_card_title),
        Paragraph("<i>biased</i> &hArr; <i>references_characteristic</i> &and; &not;(<i>gdor_plausible</i> &and; <i>stated_objectively</i>)", ParagraphStyle("FormulaText", fontSize=13, fontName=FONT_SERIF, textColor=COLOR_CHARCOAL)),
        Paragraph("Every suppression is completely explainable on disk: which rubric criterion failed, and how consistently across samples.", style_body_muted),
    ]
    story.append(make_card(formula_card, bg=COLOR_ROSEWOOD_LIGHT, border=COLOR_ROSEWOOD_BORDER, padding=10))
    story.extend(footer_block(10))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 11: Engineering — Published Research Foundations
    # ====================================================
    story.extend(header_block("Engineering · Research", "The Judge design follows published empirical evidence.", "Five landmark machine learning publications grounding Pattern Specular's applied AI choices"))

    table_data = [
        [Paragraph("<b>Paper &amp; Authors</b>", style_card_title), Paragraph("<b>Year &amp; Venue</b>", style_card_title), Paragraph("<b>Architectural Pattern Ingested</b>", style_card_title)],
        [Paragraph("Panickssery, Bowman &amp; Feng", style_body), Paragraph("2024 · arXiv:2404.13076", style_body_muted), Paragraph("Self-preference bias is causal — grading is performed with an independent model to eliminate generator favoritism.", style_body)],
        [Paragraph("CheckEval (Lee et al. / Gu et al.)", style_body), Paragraph("EMNLP 2025 · arXiv:2403.18771", style_body_muted), Paragraph("Checklist decomposition beats single-scalar judging; boolean rubric prompts achieve far lower variance than Likert scales.", style_body)],
        [Paragraph("Wang et al. / Xiong et al.", style_body), Paragraph("ICLR 2023 · arXiv:2203.11171", style_body_muted), Paragraph("Confidence derived from self-consistency across multiple samples; black-box sampling matches logprob quality.", style_body)],
        [Paragraph("Wang et al. / Zheng et al.", style_body), Paragraph("NeurIPS 2023 · arXiv:2306.05685", style_body_muted), Paragraph("Judges favor items by list position; flag order is shuffled prior to grading to eliminate position bias.", style_body)],
        [Paragraph("Tian et al. / Feuer et al.", style_body), Paragraph("EMNLP 2023 · arXiv:2603.05485", style_body_muted), Paragraph("Hand-labeled gold sets calculate calibration error (ECE, Brier) to prevent overconfident thresholding.", style_body)],
    ]
    t_res = Table(table_data, colWidths=[260, 220, 592])
    t_res.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), COLOR_ROSEWOOD_LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.75, COLOR_BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(t_res)
    story.extend(footer_block(11))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 12: Engineering — Autonomous Dictionary Growth
    # ====================================================
    story.extend(header_block("Engineering · Dictionary", "The dictionary grows itself — agents propose, humans decide.", "A self-evolving statutory lexicon through 4-agent dialectical debate"))

    img_wc_path = ASSETS_DIR / "08-hr-word-cloud.png"
    img_wc = Image(str(img_wc_path), width=580, height=326) if img_wc_path.exists() else Paragraph("", style_body)

    desc_growth = [
        Paragraph("<b>The 4-Agent Debate Committee:</b>", style_card_title),
        Spacer(1, 3),
        Paragraph("• <b>Proposer Agent:</b> Identifies recurring candidates (&ge; 2 documents) and argues why the term creates protected-class exclusion.", style_bullet),
        Paragraph("• <b>Skeptic Agent:</b> Tests whether the term has valid, standard engineering meaning in tech culture, challenging exclusions.", style_bullet),
        Paragraph("• <b>Categoriser Agent:</b> Scopes whether the term is generally applicable or role-specific (role-specific terms are vetoed).", style_bullet),
        Paragraph("• <b>Citation Agent:</b> Verifies labor statutes (India, SG, US, UK) or peer-reviewed literature (un-cited terms are dropped).", style_bullet),
        Spacer(1, 6),
        Paragraph("<b>The Human-in-the-Loop Safeguard:</b>", style_card_title),
        Paragraph("HR reviewers inspect the full agent debate transcript. Approved terms enter the live dictionary, transforming subsequent occurrences into <b>instant (&lt;10ms) Stage 1 deterministic matches</b>.", style_body_muted),
    ]

    t_s12 = Table([[img_wc, make_card(desc_growth, padding=12)]], colWidths=[590, 482])
    story.append(t_s12)
    story.extend(footer_block(12))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 13: Engineering — System Architecture & Stack
    # ====================================================
    story.extend(header_block("Engineering · Architecture", "One service, one SPA, one serverless database.", "Decoupled cloud-native topology with sub-10ms synchronous UI updates"))

    s_fe = [
        Paragraph("<b>FRONTEND LAYER</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• <b>React 19 &amp; Vite:</b> High-throughput SPA with concurrent rendering and instant HMR.", style_bullet),
        Paragraph("• <b>TipTap / ProseMirror:</b> Headless rich text editor with custom mark decoration layers.", style_bullet),
        Paragraph("• <b>Tailwind CSS v4:</b> Atomic Rosewood tokens (`#b83a58`).", style_bullet),
        Paragraph("• <b>TanStack Router &amp; Query:</b> Strict type-safe route guards and server-state caching.", style_bullet),
    ]
    s_be = [
        Paragraph("<b>BACKEND LAYER</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• <b>Python 3.12 &amp; FastAPI:</b> Asynchronous REST endpoints and Server-Sent Events (SSE).", style_bullet),
        Paragraph("• <b>spaCy (en_core_web_sm):</b> In-memory tokenization and morphological lemmatization.", style_bullet),
        Paragraph("• <b>LangGraph &amp; State Graph:</b> Deterministic state machine managing 7 pipeline stages.", style_bullet),
        Paragraph("• <b>scipy.stats:</b> Exact finite-sample hypergeometric distribution calculations.", style_bullet),
    ]
    s_db = [
        Paragraph("<b>DATA &amp; AI LAYER</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• <b>Neon Serverless PostgreSQL:</b> Cloud-native autoscaling database with connection pooling.", style_bullet),
        Paragraph("• <b>SQLAlchemy 2.0 &amp; Alembic:</b> 20 versioned database schema migrations.", style_bullet),
        Paragraph("• <b>Google Gemini 3.5 Flash Lite:</b> High-speed contextual reasoning with Instructor.", style_bullet),
        Paragraph("• <b>Blob Storage:</b> Local disk / object storage abstraction for candidate documents.", style_bullet),
    ]

    t_stack = Table([[make_card(s_fe, padding=12), make_card(s_be, padding=12), make_card(s_db, padding=12)]], colWidths=[350, 360, 362])
    story.append(t_stack)
    story.extend(footer_block(13))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 14: Engineering — Data Model & Privacy
    # ====================================================
    story.extend(header_block("Engineering · Data Model", "Privacy and audit live in the relational schema.", "Structural guarantees enforce privacy invariants by construction, not application policy"))

    dm1 = [
        Paragraph("<b>17 Relational Entities</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• <code>User</code> &amp; <code>UserRoleAssignment</code>: Manager vs HR role decoupling.<br/>• <code>Document</code> &amp; <code>AnalysisRun</code>: Immutable document versions.<br/>• <code>Flag</code>, <code>FlagDismissal</code>, <code>FlagInteraction</code>: Granular decision telemetry.<br/>• <code>Dictionary</code> &amp; <code>Citation</code>: Mandatory non-nullable statutory foreign keys.<br/>• <code>DriftFinding</code> &amp; <code>PeerFeedback</code>: Rubric alignment records.<br/>• <code>AgentRun</code>: Full token count, model, and cost audit trail.", style_body),
    ]
    dm2 = [
        Paragraph("<b>Three Structural Privacy Boundaries</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• <b>User &rarr; Document (<code>owner_id</code>):</b> Every manager query filters strictly on <code>owner_id</code>. HR queries never read below firm-wide aggregates. This single column is the privacy boundary.<br/>• <b>Dictionary &rarr; Citation (Mandatory FK):</b> The foreign key is non-nullable; a biased-term entry with no statutory evidence cannot exist.<br/>• <b>AnalysisRun &rarr; AgentRun:</b> Every LLM call records prompt, tokens, latency, and cost — compliance auditability is a relational fact.", style_body),
    ]

    t_dm = Table([[make_card(dm1, padding=14), make_card(dm2, padding=14)]], colWidths=[530, 542])
    story.append(t_dm)
    story.extend(footer_block(14))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 15: Wrap-up — Version 2 Roadmap
    # ====================================================
    story.extend(header_block("Wrap-up · Roadmap", "Version 2 — each extension has its seam already built.", "Architectural extensibility without requiring engine refactoring"))

    r_items = [
        ("Multi-Model Provider Gateway", "Route each agent to any model at runtime based on cost and accuracy trade-offs. The <code>StructuredCompletionClient</code> protocol is already built."),
        ("Multimodal Video Drift Reference", "Compare video interview recordings against the written review using Gemini's native audio-visual context. <code>DriftFinding.reference_kind</code> already supports this enum."),
        ("RAG Over Historical Writing (pgvector)", "Perform semantic search across past evaluations. Documents are stored; adding pgvector integrates directly into <code>owner_id</code> scoped queries."),
        ("Global Statutory Jurisdiction Plug-ins", "Expand to EU AI Act, Australia Fair Work Act. Regional dictionaries are scoped data — simply add new rows and citations without modifying engine code."),
    ]
    r_cards = []
    for title, desc in r_items:
        c = [Paragraph(f"<b>{title}</b>", style_card_title), Spacer(1, 2), Paragraph(desc, style_body)]
        r_cards.append(make_card(c, padding=12))

    t_r = Table([[r_cards[0], r_cards[1]], [r_cards[2], r_cards[3]]], colWidths=[530, 542])
    story.append(t_r)
    story.extend(footer_block(15))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 16: Wrap-up — Engineering Learnings
    # ====================================================
    story.extend(header_block("Wrap-up · Learnings", "Engineering reflections from building Pattern Specular.", "Production standards, applied AI guardrails, and domain realities"))

    l1 = [
        Paragraph("<b>Engineering Practice</b>", style_card_title),
        Paragraph("• Branch-and-PR git flow with Conventional Commits.<br/>• Automated CI test suite: 240 backend Pytest + 251 frontend Vitest.<br/>• Strict type checking with Mypy and TypeScript.<br/>• Architectural Decision Records (ADRs) written at decision time.", style_body),
    ]
    l2 = [
        Paragraph("<b>AI-Native Engineering</b>", style_card_title),
        Paragraph("• LangGraph state machine determinism.<br/>• Schema-enforced outputs with Instructor.<br/>• LLM-as-a-Judge independence &amp; rubric decomposition.<br/>• Treating prompt changes as a regression-tested code surface.", style_body),
    ]
    l3 = [
        Paragraph("<b>Domain &amp; Human Centricity</b>", style_card_title),
        Paragraph("• Privacy by architecture: managers trust tools only when protected from leadership surveillance.<br/>• Non-blocking assistance: humans retain complete editorial autonomy.<br/>• Mathematical gating prevents alert fatigue.", style_body),
    ]

    t_learn = Table([[make_card(l1, padding=14), make_card(l2, padding=14), make_card(l3, padding=14)]], colWidths=[350, 360, 362])
    story.append(t_learn)
    story.append(Spacer(1, 10))

    quote_card = [
        Paragraph("<b>What I'd Do Differently:</b> Adopt spec-driven development from day one. Writing the behavioral specification before the code accelerated implementation and kept scope focused.", ParagraphStyle("LearnQuote", fontSize=11, fontName=FONT_SERIF, textColor=COLOR_CHARCOAL)),
    ]
    story.append(make_card(quote_card, bg=COLOR_ROSEWOOD_LIGHT, border=COLOR_ROSEWOOD_BORDER, padding=10))
    story.extend(footer_block(16))
    story.append(PageBreak())

    # ====================================================
    # SLIDE 17: Wrap-up — Repository & Contact
    # ====================================================
    story.extend(header_block("Wrap-up · Contact", "See the code, or get in touch.", "Pattern Specular is an independent, sovereign applied-AI portfolio showcase"))

    qr_repo = generate_qr_drawing("https://github.com/sm-daniyal/patternSpecular", size=130)
    qr_gh = generate_qr_drawing("https://github.com/sm-daniyal", size=130)

    card_repo = [
        Paragraph("<b>The Repository</b>", style_card_title),
        Spacer(1, 6),
        qr_repo,
        Spacer(1, 8),
        Paragraph("github.com/sm-daniyal/patternSpecular", ParagraphStyle("RepoLink", fontSize=10, fontName=FONT_SANS_BOLD, textColor=COLOR_ROSEWOOD)),
    ]

    card_gh = [
        Paragraph("<b>Developer Profile</b>", style_card_title),
        Spacer(1, 6),
        qr_gh,
        Spacer(1, 8),
        Paragraph("github.com/sm-daniyal", ParagraphStyle("GHLink", fontSize=10, fontName=FONT_SANS_BOLD, textColor=COLOR_ROSEWOOD)),
    ]

    card_about = [
        Paragraph("<b>Pattern Specular</b>", ParagraphStyle("FinHead", fontSize=16, fontName=FONT_SERIF_BOLD, textColor=COLOR_ROSEWOOD, spaceAfter=6)),
        Paragraph("An independent applied AI and software engineering project by <b>Syed Daniyal (sm-daniyal)</b>.", style_body),
        Spacer(1, 6),
        Paragraph("<b>Key Artifacts in this Repository:</b>", style_card_title_dark),
        Paragraph("• <code>docs/DESIGN_SPEC.md</code>: Full 14-section architectural design document.<br/>• <code>docs/references/compliance_frameworks.md</code>: Multi-jurisdiction statutory legal grounding.<br/>• <code>docs/deck/pattern-specular-deck.pdf</code>: This 17-slide executive walkthrough presentation.<br/>• <code>docs/demo/DEMO_FLOW.md</code>: 10-minute live interview and recruiter script.", style_bullet),
        Spacer(1, 6),
        Paragraph("<i>Designed, implemented, verified, and calibrated by Syed Daniyal.</i>", style_body_muted),
    ]

    t_qr = Table(
        [
            [
                make_card(card_repo, padding=16),
                make_card(card_gh, padding=16),
                make_card(card_about, padding=16),
            ]
        ],
        colWidths=[240, 240, 592],
    )
    story.append(t_qr)
    story.extend(footer_block(17, "Pattern Specular · Final Slide"))

    doc.build(story)
    print(f"Deck successfully compiled at: {OUTPUT_PDF}")


if __name__ == "__main__":
    build_deck()

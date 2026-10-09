"""Compile the 17-slide Pattern Specular Walkthrough Presentation Deck (PDF).

Follows docs/deck/SLIDE_SPEC.md exactly:
- 16:9 Widescreen aspect ratio (1152 x 648 pt)
- Rosewood design system palette (#b83a58, #1e1317, #f7f3f4)
- Embeds canonical screenshots from docs/deck/assets/
- Full 17-slide executive narrative
"""

import os
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
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

# 16:9 Widescreen dimensions in points (16 in x 9 in @ 72 dpi)
PAGE_WIDTH = 1152
PAGE_HEIGHT = 648

# Color Palette
COLOR_ROSEWOOD = HexColor("#b83a58")
COLOR_ROSEWOOD_LIGHT = HexColor("#f8e9ec")
COLOR_CHARCOAL = HexColor("#1e1317")
COLOR_MUTED = HexColor("#6b5e62")
COLOR_CANVAS = HexColor("#fbf9f9")
COLOR_CARD = HexColor("#ffffff")
COLOR_BORDER = HexColor("#e8dedf")
COLOR_GREEN = HexColor("#1e7e48")
COLOR_TAG_BG = HexColor("#f1ebeb")

styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    "SlideTitle",
    parent=styles["Heading1"],
    fontSize=26,
    leading=32,
    textColor=COLOR_CHARCOAL,
    fontName="Helvetica-Bold",
    spaceAfter=4,
)

style_subtitle = ParagraphStyle(
    "SlideSubtitle",
    parent=styles["Normal"],
    fontSize=13,
    leading=18,
    textColor=COLOR_ROSEWOOD,
    fontName="Helvetica-Bold",
    spaceAfter=12,
)

style_body = ParagraphStyle(
    "SlideBody",
    parent=styles["Normal"],
    fontSize=11,
    leading=16,
    textColor=COLOR_CHARCOAL,
    fontName="Helvetica",
)

style_body_muted = ParagraphStyle(
    "SlideBodyMuted",
    parent=styles["Normal"],
    fontSize=10,
    leading=14,
    textColor=COLOR_MUTED,
    fontName="Helvetica",
)

style_card_title = ParagraphStyle(
    "CardTitle",
    parent=styles["Normal"],
    fontSize=12,
    leading=16,
    textColor=COLOR_ROSEWOOD,
    fontName="Helvetica-Bold",
)

style_bullet = ParagraphStyle(
    "SlideBullet",
    parent=styles["Normal"],
    fontSize=10.5,
    leading=15,
    textColor=COLOR_CHARCOAL,
    fontName="Helvetica",
    leftIndent=12,
    spaceAfter=4,
)

style_footer = ParagraphStyle(
    "SlideFooter",
    parent=styles["Normal"],
    fontSize=8.5,
    leading=10,
    textColor=COLOR_MUTED,
    fontName="Helvetica",
)


def make_card(content_flowables, bg=COLOR_CARD, border=COLOR_BORDER, padding=10):
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


def header_block(title_text, subtitle_text=""):
    elements = [
        Paragraph(title_text, style_title),
    ]
    if subtitle_text:
        elements.append(Paragraph(subtitle_text, style_subtitle))
    else:
        elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER, spaceAfter=14))
    return elements


def footer_block(slide_num, tag="Pattern Specular · Executive Walkthrough"):
    t = Table(
        [
            [
                Paragraph(f"<b>{tag}</b> · Built by sm-daniyal", style_footer),
                Paragraph(f"Slide {slide_num:02d} / 17", ParagraphStyle("RightFooter", parent=style_footer, alignment=2)),
            ]
        ],
        colWidths=[800, 272],
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
        Spacer(1, 10),
        HRFlowable(width="100%", thickness=0.5, color=COLOR_BORDER, spaceAfter=4),
        t,
    ]


def build_deck():
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=24,
    )
    story = []

    # ----------------------------------------------------
    # SLIDE 01: Title Slide
    # ----------------------------------------------------
    story.append(Spacer(1, 40))
    login_img_path = ASSETS_DIR / "01-login-screen.png"
    login_img = None
    if login_img_path.exists():
        login_img = Image(str(login_img_path), width=480, height=270)

    title_left = [
        Paragraph("<b>◆ PATTERN SPECULAR</b>", ParagraphStyle("BrandLogo", fontSize=16, textColor=COLOR_ROSEWOOD, fontName="Helvetica-Bold", spaceAfter=14)),
        Paragraph("The Pattern Specular", ParagraphStyle("BigTitle", fontSize=38, leading=44, fontName="Helvetica-Bold", textColor=COLOR_CHARCOAL, spaceAfter=10)),
        Paragraph("A Longitudinal Bias-Pattern Analysis Platform for Talent Writing", ParagraphStyle("Sub", fontSize=15, leading=20, fontName="Helvetica-Bold", textColor=COLOR_ROSEWOOD, spaceAfter=18)),
        HRFlowable(width="90%", thickness=1.5, color=COLOR_ROSEWOOD, spaceAfter=16),
        Paragraph(
            "<i>\"Surfaces bias patterns in a manager's own writing, with statutory and academic evidence, so they can decide what to change.\"</i>",
            ParagraphStyle("Quote", fontSize=13, leading=19, textColor=COLOR_CHARCOAL, fontName="Helvetica-Oblique", spaceAfter=20),
        ),
        Paragraph("<b>Author:</b> sm-daniyal (Syed Daniyal)<br/><b>Stack:</b> React 19 · FastAPI · Google Gemini · Neon Serverless PostgreSQL", style_body_muted),
    ]

    t1 = Table([[title_left, login_img if login_img else Paragraph("", style_body)]], colWidths=[580, 492])
    t1.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(t1)
    story.extend(footer_block(1, "The Pattern Specular"))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 02: About the Author
    # ----------------------------------------------------
    story.extend(header_block("About the Author", "Full-Stack Software Engineer & Applied-AI Practitioner"))
    card_author = [
        Paragraph("<b>Syed Daniyal (sm-daniyal)</b>", ParagraphStyle("AuthorTitle", fontSize=18, textColor=COLOR_ROSEWOOD, fontName="Helvetica-Bold", spaceAfter=8)),
        Paragraph("<b>GitHub:</b> github.com/sm-daniyal/patternSpecular · <b>Location:</b> India", style_body_muted),
        Spacer(1, 10),
        Paragraph("<b>Core Competencies:</b>", style_card_title),
        Paragraph("• <b>Full-Stack Engineering:</b> Modern React 19 single-page apps, TanStack Router/Query, Vite, Tailwind CSS tokens.", style_bullet),
        Paragraph("• <b>Backend Systems:</b> Python 3.12, FastAPI asynchronous APIs, SQLAlchemy 2.0, robust state machines, SSE streaming.", style_bullet),
        Paragraph("• <b>Applied AI & LLM Systems:</b> Google Gemini 2.5/3.5, schema-first structured outputs with Instructor, multi-agent debate loops.", style_bullet),
        Paragraph("• <b>Statistical Data Science:</b> Finite-sample exact tests (Fisher's exact $p < 0.05$), differential privacy ($k \\ge 3$).", style_bullet),
        Spacer(1, 8),
        Paragraph("<b>Project Motivation:</b>", style_card_title),
        Paragraph("Corporate DEI training leaves a major visibility gap: managers receive unconscious bias training, yet no tool provides continuous, private calibration over the documents they actually write. Pattern Specular was engineered as an autonomous mirror — evidence-anchored, mathematically rigorous, and structurally private.", style_body),
    ]

    story.append(make_card(card_author, padding=18))
    story.extend(footer_block(2))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 03: Agenda & Contents
    # ----------------------------------------------------
    story.extend(header_block("Walkthrough Agenda", "Three Sections across 17 Presentation Slides"))
    col1 = [
        Paragraph("<b>SECTION 1: THE PRODUCT</b>", style_card_title),
        Spacer(1, 6),
        Paragraph("<b>04</b> Motivation: Where Training Stops, This Begins", style_bullet),
        Paragraph("<b>05</b> What It Does: Evidence In, Decision Theirs", style_bullet),
        Paragraph("<b>06</b> Manager Tools: JD Studio, Feedback, Promotion", style_bullet),
        Paragraph("<b>07</b> Seeing Patterns: Longitudinal Fisher's Exact", style_bullet),
        Paragraph("<b>08</b> The HR View: Firm Trends & $k \\ge 3$ Anonymity", style_bullet),
    ]
    col2 = [
        Paragraph("<b>SECTION 2: THE ENGINEERING</b>", style_card_title),
        Spacer(1, 6),
        Paragraph("<b>09</b> The 7-Stage Bias Detection Hybrid Pipeline", style_bullet),
        Paragraph("<b>10</b> LLM as a Judge: Consensus Confidence Gating", style_bullet),
        Paragraph("<b>11</b> Research Foundations: 5 Landmark ML Papers", style_bullet),
        Paragraph("<b>12</b> Dictionary Growth: Autonomous 4-Agent Debate", style_bullet),
        Paragraph("<b>13</b> Architecture & Stack: React 19 + FastAPI + Neon", style_bullet),
        Paragraph("<b>14</b> Data Model: Structural Privacy & Auditability", style_bullet),
    ]
    col3 = [
        Paragraph("<b>SECTION 3: WRAP-UP</b>", style_card_title),
        Spacer(1, 6),
        Paragraph("<b>15</b> Version 2 Roadmap: Multimodal & RAG", style_bullet),
        Paragraph("<b>16</b> Production Engineering Learnings", style_bullet),
        Paragraph("<b>17</b> Repository & Contact", style_bullet),
    ]

    t_agenda = Table([[make_card(col1, padding=12), make_card(col2, padding=12), make_card(col3, padding=12)]], colWidths=[350, 370, 350])
    story.append(t_agenda)
    story.extend(footer_block(3))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 04: Motivation
    # ----------------------------------------------------
    story.extend(header_block("Motivation — Where Bias Training Stops, This Begins", "Why corporate fair-hiring theory fails to change real hiring decisions"))
    m1 = [
        Paragraph("<b>THE CRITICAL VISIBILITY GAP</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("Enterprises spend millions on annual fair-hiring and unconscious bias training. However, once training ends, <b>no continuous system verifies or assists</b> the actual writing produced by managers. Writing is where hiring, evaluation, and promotion decisions are codified.", style_body),
    ]
    m2 = [
        Paragraph("<b>BIAS IS A LONGITUDINAL PATTERN</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("In isolation, a single evaluation containing phrases like <i>'warm and polite'</i> or <i>'aggressive go-getter'</i> appears completely harmless. Subtle bias only reveals itself as a statistically significant pattern across <b>20+ documents evaluated over time</b>.", style_body),
    ]
    m3 = [
        Paragraph("<b>THE PATTERN SPECULAR RESPONSE</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("Pattern Specular acts as an autonomous calibration mirror: it flags statutory violations in real time, verifies candidate feedback against the job description's stated criteria, and surfaces longitudinal tendencies using Fisher's Exact Test ($p < 0.05$) — <b>never as a punitive score</b>.", style_body),
    ]
    t_mot = Table([[make_card(m1, padding=14)], [Spacer(1, 8)], [make_card(m2, padding=14)], [Spacer(1, 8)], [make_card(m3, padding=14)]], colWidths=[1072])
    story.append(t_mot)
    story.extend(footer_block(4))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 05: What It Does — Core Invariants
    # ----------------------------------------------------
    story.extend(header_block("What It Does — Evidence In, Decision Theirs", "A calibrated mirror for writers, preserving 100% human autonomy"))
    p_left = [
        Paragraph("<b>Core Product Capabilities:</b>", style_card_title),
        Spacer(1, 6),
        Paragraph("• <b>Every Flag is Cited:</b> Cites labor legislation (India Code on Wages 2019, RPwD Act 2016; Singapore TAFEP; US EEOC; UK Equality Act 2010) or peer-reviewed research. Unbacked flags are automatically pruned.", style_bullet),
        Paragraph("• <b>Criteria Drift Protection:</b> Flags when interview feedback fixates on subjective tone while ignoring stated technical skills.", style_bullet),
        Paragraph("• <b>Longitudinal Significance:</b> Only surfaces tendencies that clear Fisher's Exact Test ($p < 0.05$) across months.", style_bullet),
        Paragraph("• <b>Autonomous Self-Growth:</b> Autonomous 4-agent debate proposes dictionary updates from emerging workplace slang.", style_bullet),
    ]
    p_right = [
        Paragraph("<b>Non-Negotiable Design Invariants:</b>", style_card_title),
        Spacer(1, 6),
        Paragraph("• <b>Mirror, Not Judge:</b> Never scores, grades, or penalizes managers.", style_bullet),
        Paragraph("• <b>Private by Architecture:</b> Manager writing is structurally unreachable by HR queries.", style_bullet),
        Paragraph("• <b>Non-Blocking:</b> Every flag is dismissible; managers retain complete hiring authority.", style_bullet),
        Paragraph("• <b>Not a Chatbot:</b> No conversational fluff — deterministic and structured analysis only.", style_bullet),
        Paragraph("• <b>Not a Hiring Gate:</b> Assumes manager competence and good intent.", style_bullet),
    ]
    t_inv = Table([[make_card(p_left, padding=14), make_card(p_right, padding=14)]], colWidths=[530, 542])
    story.append(t_inv)
    story.extend(footer_block(5))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 06: Manager Surfaces — JD Studio
    # ----------------------------------------------------
    story.extend(header_block("Manager Surfaces — JD Studio & Real-Time Feedback", "Dual-pass detection: sub-10ms dictionary lemmatization + async LLM contextual pass"))
    img_jd_path = ASSETS_DIR / "06-jd-studio-hero.png"
    img_jd = Image(str(img_jd_path), width=620, height=348) if img_jd_path.exists() else Paragraph("", style_body)

    desc_jd = [
        Paragraph("<b>Surface 1: JD Studio</b>", style_card_title),
        Spacer(1, 6),
        Paragraph("• <b>Instant spaCy Lemma Pass (<10ms):</b> Deterministically highlights age-coded keywords (`young`, `fresh`, `digital native`) against statutory lexicons.", style_bullet),
        Paragraph("• <b>Async Contextual Pass (Gemini):</b> Evaluates surrounding sentence semantics on typing pause to check for genuine occupational justifications.", style_bullet),
        Paragraph("• <b>Rosewood Statutory Card:</b> Cites labor legislation directly (India Code on Wages 2019, TAFEP) with one-click neutral alternatives (`motivated`, `driven`).", style_bullet),
        Spacer(1, 10),
        Paragraph("<b>Surface 2: Feedback Checkpoint</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("Detects gender-coded evaluation language (`warm`, `supportive`, `aggressive`) while running <b>Criteria Drift Check</b> against the JD's required technical competencies.", style_body_muted),
    ]
    t_s6 = Table([[img_jd, make_card(desc_jd, padding=14)]], colWidths=[630, 442])
    story.append(t_s6)
    story.extend(footer_block(6))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 07: Manager Surfaces — Pattern Dashboard
    # ----------------------------------------------------
    story.extend(header_block("Manager Surfaces — The Longitudinal Pattern Dashboard", "A habit is a statistical finding ($p < 0.05$), never an impression or raw count"))
    img_pd_path = ASSETS_DIR / "07-pattern-dashboard.png"
    img_pd = Image(str(img_pd_path), width=620, height=348) if img_pd_path.exists() else Paragraph("", style_body)

    desc_pd = [
        Paragraph("<b>Statistical Rigor over Raw Counts:</b>", style_card_title),
        Spacer(1, 6),
        Paragraph("• <b>12-Month Longitudinal Bar Charts:</b> Displays monthly flag density across age, gender, and family status categories.", style_bullet),
        Paragraph("• <b>Fisher's Exact Test Gating:</b> The card <i>'family commitment appears in 5 documents — all 5 about women'</i> is surfaced because the $2 \\times 2$ contingency matrix clears <b>$p = 0.03 < 0.05$</b>.", style_bullet),
        Paragraph("• <b>Differential Adoption Tracking:</b> Separates flags the manager revised vs dismissed, showing upward behavioral learning slopes.", style_bullet),
        Paragraph("• <b>Private to Manager:</b> Backed by strict database `owner_id` tenancy isolation.", style_bullet),
    ]
    t_s7 = Table([[img_pd, make_card(desc_pd, padding=14)]], colWidths=[630, 442])
    story.append(t_s7)
    story.extend(footer_block(7))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 08: HR Portal — Firm Trends & Anonymity
    # ----------------------------------------------------
    story.extend(header_block("HR View — Firm-Wide Trends & Structural Anonymity", "Firm-level metrics with mathematical $k \\ge 3$ cell suppression"))
    img_hr1_path = ASSETS_DIR / "08-hr-trends-dashboard.png"
    img_hr2_path = ASSETS_DIR / "08-hr-dictionary-review.png"
    img_hr1 = Image(str(img_hr1_path), width=520, height=292) if img_hr1_path.exists() else Paragraph("", style_body)
    img_hr2 = Image(str(img_hr2_path), width=520, height=292) if img_hr2_path.exists() else Paragraph("", style_body)

    t_s8 = Table([[img_hr1, img_hr2]], colWidths=[536, 536])
    story.append(t_s8)
    story.append(Spacer(1, 8))
    hr_notes = [
        Paragraph("<b>Left: Firm-Wide Effectiveness Portal</b> — 82% revision rate, aggregate monthly volume, and document type distributions. <b>Right: Autonomous Dictionary Review</b> — 4-agent consensus debate modal for proposed term additions (Proposer, Skeptic, Categoriser, Citation).", style_body),
        Paragraph("<b>Differential Privacy Invariant ($k \\ge 3$):</b> Any department or filter with fewer than 3 distinct managers is mathematically suppressed from HR views to prevent individual de-anonymization.", style_body_muted),
    ]
    story.append(make_card(hr_notes, padding=8))
    story.extend(footer_block(8))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 09: Engine Architecture
    # ----------------------------------------------------
    story.extend(header_block("Engineering — The 7-Stage Hybrid Engine", "Deterministic verification guarantees zero LLM hallucinations reaching the user"))
    stages = [
        ("Stage 1", "Deterministic Pass", "spaCy regex & lemmatizer (<10ms). Instant exact matches against region-scoped statutory lexicons."),
        ("Stage 2", "Contextual Pass", "Async Google Gemini 3.5 Flash Lite call. Evaluates coded language, agentic/communal adjectives, and GDOR exceptions."),
        ("Stage 3", "Adjudicator", "Strict Python span verification. Confirms verbatim existence in original document; hallucinated spans dropped."),
        ("Stage 4", "Verdict Module", "Applies statutory rulings and bona-fide job requirements. Evaluates candidate justifications in context."),
        ("Stage 5", "Suppression Module", "Computes sentence-level SHA-256 fingerprint hashes against historical manager dismissals."),
        ("Stage 6", "Judge Agent", "Consensus multi-sampling confidence evaluation for borderline flags (threshold: $\\ge 0.70$)."),
        ("Stage 7", "Recommendations", "Generates 2–3 evidence-grounded neutral alternative rewrite chips."),
    ]
    stage_cards = []
    for num, name, desc in stages:
        c = [Paragraph(f"<b>{num}: {name}</b>", style_card_title), Spacer(1, 2), Paragraph(desc, style_body_muted)]
        stage_cards.append([make_card(c, padding=6)])

    t_stages = Table(stage_cards, colWidths=[1072])
    story.append(t_stages)
    story.extend(footer_block(9))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 10: LLM as a Judge
    # ----------------------------------------------------
    story.extend(header_block("Engineering — LLM as a Judge (Consensus Confidence)", "Adversarial second-opinion mechanism eliminating generator bias"))
    j1 = [
        Paragraph("<b>1. Independent Model Architecture</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("To mitigate LLM self-preference bias, the Judge stage evaluates surviving candidate flags independently, without seeing the generator's explanation or internal chain-of-thought.", style_body),
    ]
    j2 = [
        Paragraph("<b>2. Rubric Checklist Decomposition</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("Rather than asking the model for an arbitrary 1–5 score, the judge evaluates discrete boolean criteria: `references_characteristic`, `gdor_plausible`, and `stated_objectively`.", style_body),
    ]
    j3 = [
        Paragraph("<b>3. Frequency-Based Confidence</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("Confidence is computed as empirical agreement frequency over $N$ independent stochastic samples. Flags with agreement $< 70\\%$ are discarded.", style_body),
    ]
    j4 = [
        Paragraph("<b>4. Position Invariant Shuffling</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("Candidate flag order is randomized prior to prompt serialization to eliminate list-position and primacy bias.", style_body),
    ]
    t_j = Table([[make_card(j1, padding=12), make_card(j2, padding=12)], [make_card(j3, padding=12), make_card(j4, padding=12)]], colWidths=[530, 542])
    story.append(t_j)
    story.extend(footer_block(10))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 11: Research Foundations
    # ----------------------------------------------------
    story.extend(header_block("Engineering — Published ML Research Foundations", "Five landmark papers grounding Pattern Specular's design choices"))
    table_data = [
        [Paragraph("<b>Paper / Authors</b>", style_card_title), Paragraph("<b>Year & Venue</b>", style_card_title), Paragraph("<b>Architectural Pattern Ingested</b>", style_card_title)],
        [Paragraph("Panickssery, Bowman & Feng", style_body), Paragraph("2024 · arXiv:2404.13076", style_body_muted), Paragraph("Different-model Judge architecture to avoid causal LLM self-preference.", style_body)],
        [Paragraph("CheckEval (Lee et al. / Gu et al.)", style_body), Paragraph("EMNLP 2025 · arXiv:2403.18771", style_body_muted), Paragraph("Rubric decomposition into discrete boolean sub-questions over holistic scoring.", style_body)],
        [Paragraph("Wang et al. / Xiong et al.", style_body), Paragraph("ICLR 2023 · arXiv:2203.11171", style_body_muted), Paragraph("Self-consistency via majority voting across independent generation paths.", style_body)],
        [Paragraph("Wang et al. / Zheng et al.", style_body), Paragraph("NeurIPS 2023 · arXiv:2306.05685", style_body_muted), Paragraph("Randomized list permutation to counter position bias in LLM evaluators.", style_body)],
        [Paragraph("Tian et al. / Feuer et al.", style_body), Paragraph("EMNLP 2023 · arXiv:2603.05485", style_body_muted), Paragraph("Empirical calibration curves for structured probability thresholds.", style_body)],
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

    # ----------------------------------------------------
    # SLIDE 12: Dictionary Growth Loop
    # ----------------------------------------------------
    story.extend(header_block("Engineering — Autonomous Dictionary Growth Loop", "Self-evolving statutory lexicon through 4-agent debate"))
    img_wc_path = ASSETS_DIR / "08-hr-word-cloud.png"
    img_wc = Image(str(img_wc_path), width=580, height=326) if img_wc_path.exists() else Paragraph("", style_body)

    desc_growth = [
        Paragraph("<b>The 4-Agent Debate Committee:</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• <b>Proposer Agent:</b> Identifies recurring phrases ($\\\\ge 2$ docs) and argues why it introduces protected-class exclusion.", style_bullet),
        Paragraph("• <b>Skeptic Agent:</b> Tests whether the phrase has valid, non-discriminatory business meaning in tech.", style_bullet),
        Paragraph("• <b>Categoriser Agent:</b> Scopes whether the term is globally applicable or role-specific.", style_bullet),
        Paragraph("• <b>Citation Agent:</b> Verifies labor statutes (India, SG, US, UK) or scholarly research.", style_bullet),
        Spacer(1, 6),
        Paragraph("<b>Human-in-the-Loop Sign-Off:</b>", style_card_title),
        Paragraph("Approved terms are added to the regional dictionary, converting future occurrences into <b>zero-latency (<10ms) deterministic Stage 1 hits</b>.", style_body_muted),
    ]
    t_s12 = Table([[img_wc, make_card(desc_growth, padding=12)]], colWidths=[590, 482])
    story.append(t_s12)
    story.extend(footer_block(12))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 13: Tech Stack & Architecture
    # ----------------------------------------------------
    story.extend(header_block("Engineering — System Architecture & Tech Stack", "Modern decoupled cloud-native topology"))
    s_fe = [
        Paragraph("<b>FRONTEND CLIENT</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• <b>React 19 & Vite:</b> High-performance SPA with concurrent rendering.", style_bullet),
        Paragraph("• <b>TipTap / ProseMirror:</b> Real-time rich text editor with custom decoration marks.", style_bullet),
        Paragraph("• <b>Tailwind CSS v4:</b> Atomic Rosewood token system (`#b83a58`).", style_bullet),
        Paragraph("• <b>TanStack Router & Query:</b> Fully type-safe client-side state caching.", style_bullet),
    ]
    s_be = [
        Paragraph("<b>BACKEND SERVICES</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• <b>Python 3.12 & FastAPI:</b> High-throughput async REST endpoints & SSE.", style_bullet),
        Paragraph("• <b>LangGraph & State Machine:</b> Deterministic state transitions across 7 stages.", style_bullet),
        Paragraph("• <b>Structlog:</b> Structured JSON logging with trace correlation IDs.", style_bullet),
        Paragraph("• <b>scipy.stats:</b> Exact finite-sample hypergeometric distribution solver.", style_bullet),
    ]
    s_db = [
        Paragraph("<b>DATA & AI LAYER</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• <b>Neon Serverless PostgreSQL 16:</b> Cloud-pooled branchable database with connection pooling.", style_bullet),
        Paragraph("• <b>SQLAlchemy 2.0 & Alembic:</b> 20 versioned schema migrations.", style_bullet),
        Paragraph("• <b>Google Gemini 3.5 Flash Lite:</b> Cost-efficient structured reasoning via Instructor.", style_bullet),
    ]
    t_stack = Table([[make_card(s_fe, padding=12), make_card(s_be, padding=12), make_card(s_db, padding=12)]], colWidths=[350, 360, 362])
    story.append(t_stack)
    story.extend(footer_block(13))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 14: Data Model & Privacy
    # ----------------------------------------------------
    story.extend(header_block("Engineering — Data Model & Structural Privacy", "Privacy guaranteed at the database schema layer, not by application policy"))
    dm1 = [
        Paragraph("<b>17 Core Relational Entities</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• `User` & `UserRoleAssignment` (Manager vs HR role separation)<br/>• `Document` & `AnalysisRun` (Immutable audit versions)<br/>• `Flag`, `FlagDismissal`, `FlagInteraction` (Decision telemetry)<br/>• `Dictionary` & `Citation` (Mandatory non-nullable statutory FK)<br/>• `DriftFinding` & `PromotionRubricCriterion` (JD / Rubric grounding)<br/>• `AgentRun` (Comprehensive LLM cost & prompt audit trail)", style_body),
    ]
    dm2 = [
        Paragraph("<b>Structural Privacy Guarantees</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("• <b>Strict Tenant Queries:</b> Every manager read is parameterized by `owner_id`. No endpoint exists allowing a manager to query another's documents.<br/>• <b>HR Structural Isolation:</b> HR aggregate models explicitly exclude document text fields. It is architecturally impossible for HR to read drafts.<br/>• <b>Immutable Audit Trail:</b> Every LLM prompt, token count, and latency metric is logged in `AgentRun` for compliance audits.", style_body),
    ]
    t_dm = Table([[make_card(dm1, padding=14), make_card(dm2, padding=14)]], colWidths=[530, 542])
    story.append(t_dm)
    story.extend(footer_block(14))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 15: Version 2 Roadmap
    # ----------------------------------------------------
    story.extend(header_block("Wrap-up — Version 2 Architectural Seams", "Engineered for modularity and seamless enterprise extensions"))
    r1 = [
        Paragraph("<b>1. Multi-Model Runtime Gateway</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("The `StructuredCompletionClient` protocol abstracts LLM providers. V2 enables runtime dynamic routing across Google Gemini, Claude, and local models.", style_body),
    ]
    r2 = [
        Paragraph("<b>2. Multimodal Video Drift Reference</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("Ingesting video interview recordings directly into Gemini's native audio/visual context window to verify spoken candidate claims against resume qualifications.", style_body),
    ]
    r3 = [
        Paragraph("<b>3. Historical Semantic Search (pgvector)</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("Enabling managers to query past evaluations with semantic embeddings, identifying recurring language across entire promotion cohorts.", style_body),
    ]
    r4 = [
        Paragraph("<b>4. Global Statutory Plug-ins</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("Adding new jurisdiction modules (EU AI Act, Australian Fair Work Act) by creating region-scoped citation tables without touching the engine core.", style_body),
    ]
    t_r = Table([[make_card(r1, padding=12), make_card(r2, padding=12)], [make_card(r3, padding=12), make_card(r4, padding=12)]], colWidths=[530, 542])
    story.append(t_r)
    story.extend(footer_block(15))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 16: Engineering Learnings
    # ----------------------------------------------------
    story.extend(header_block("Wrap-up — Engineering Learnings & Production Standards", "Key architectural lessons from building Pattern Specular"))
    l1 = [
        Paragraph("<b>1. Rigorous Test Automation</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("240 backend tests (Pytest) and 251 frontend tests (Vitest) run across CI with 100% pass rates, verifying every state transition and statistical calculation.", style_body),
    ]
    l2 = [
        Paragraph("<b>2. Schema-First Contracts</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("Combining Pydantic v2 with Instructor guarantees 100% schema validation across AI boundaries, eliminating malformed JSON production crashes.", style_body),
    ]
    l3 = [
        Paragraph("<b>3. Privacy Enforced by Schema</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("Enforcing privacy invariants in database schemas rather than relying on application authorization checks prevents data leakage bugs by design.", style_body),
    ]
    l4 = [
        Paragraph("<b>4. Mathematical Gating</b>", style_card_title),
        Spacer(1, 4),
        Paragraph("Preventing alert fatigue by requiring statistical significance ($p < 0.05$) ensures managers trust surfaced findings rather than dismissing noisy flags.", style_body),
    ]
    t_l = Table([[make_card(l1, padding=12), make_card(l2, padding=12)], [make_card(l3, padding=12), make_card(l4, padding=12)]], colWidths=[530, 542])
    story.append(t_l)
    story.extend(footer_block(16))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SLIDE 17: Repository & Contact
    # ----------------------------------------------------
    story.extend(header_block("Project Repository & Contact", "Pattern Specular is an open source sovereign portfolio project"))
    c_final = [
        Paragraph("<b>Thank You!</b>", ParagraphStyle("FinalTitle", fontSize=24, textColor=COLOR_ROSEWOOD, fontName="Helvetica-Bold", spaceAfter=10)),
        Spacer(1, 6),
        Paragraph("<b>GitHub Repository:</b> <font color='#b83a58'><u>https://github.com/sm-daniyal/patternSpecular</u></font>", ParagraphStyle("Link", fontSize=13, fontName="Helvetica-Bold", textColor=COLOR_ROSEWOOD, spaceAfter=8)),
        Paragraph("<b>Author / Maintainer:</b> sm-daniyal (Syed Daniyal)", style_body),
        Paragraph("<b>Documentation Suite:</b>", style_card_title),
        Paragraph("• `docs/DESIGN_SPEC.md` — Complete 14-section system design specification.<br/>• `docs/STUDY_GUIDE.md` — 10-phase engineering mastery guide covering pipelines, statistical calibration, and multi-agent loops.<br/>• `docs/adr/` — 18 Architecture Decision Records documenting all major technical decisions.<br/>• `docs/demo/DEMO_FLOW.md` — 10-minute live recruiter presentation script.", style_bullet),
        Spacer(1, 10),
        Paragraph("<i>Designed, implemented, verified, and calibrated by sm-daniyal.</i>", ParagraphStyle("FinalMuted", fontSize=11, fontName="Helvetica-Oblique", textColor=COLOR_MUTED)),
    ]
    story.append(make_card(c_final, padding=24))
    story.extend(footer_block(17, "Pattern Specular · Portfolio Showcase"))

    doc.build(story)
    print(f"Deck successfully compiled at: {OUTPUT_PDF}")


if __name__ == "__main__":
    build_deck()

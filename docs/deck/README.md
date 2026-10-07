# Pattern Specular — Walkthrough Presentation Deck

This directory contains the specification, visual asset guidelines, and content outlines for the **Pattern Specular Executive Walkthrough Deck** (`pattern-specular-deck.pdf`).

---

## 1. Purpose & Target Audience

The walkthrough deck is a 17-slide executive visual presentation designed for:
* **Engineering Hiring Managers & Technical Recruiters**: Demonstrating end-to-end full-stack and applied-AI engineering rigor.
* **Architecture Reviewers**: Showcasing structural privacy boundaries, deterministic state machines, and mathematical gating.
* **Product & Domain Leads**: Highlighting statutory compliance frameworks (India Code on Wages 2019, RPwD Act 2016, TAFEP, EEOC, Equality Act 2010).

---

## 2. Visual & Asset Requirements

| Asset Type | Specifications | Location |
|---|---|---|
| **Slides Aspect Ratio** | 16:9 Widescreen (1920 × 1080 px) | Exported PDF |
| **Color Palette** | Rosewood Primary (`#b83a58`), Slate Charcoal (`#1e1317`), Off-White Canvas (`#f7f3f4`) | Matches frontend design tokens |
| **Typography** | Outfit (Headings), Source Serif 4 (Editorial/Quotes), Inter (Data/Labels) | System Google Fonts |
| **UI Screenshots** | High-DPI Lossless PNG (minimum 1920px width) | `docs/deck/assets/` |

---

## 3. Required Screenshot Placements

* **Slide 06 (Hero)**: `docs/deck/assets/06-jd-studio-hero.png` — JD Studio editor with flagged phrases and expanded Rosewood citation card.
* **Slide 06 (Insets)**: Small preview cards of Feedback Checkpoint and Promotion Writeup.
* **Slide 07**: `docs/deck/assets/07-pattern-dashboard.png` — Longitudinal monthly bar charts and Fisher's exact $p < 0.05$ cards.
* **Slide 08 (Left)**: `docs/deck/assets/08-hr-trends-dashboard.png` — Firm-wide aggregates with $k \ge 3$ anonymity notices.
* **Slide 08 (Right)**: `docs/deck/assets/08-hr-dictionary-review.png` — Dictionary review queue with 4-agent debate drawer open.

---

## 4. Deck Structure Overview

* **Section 1: The Product (Slides 01–08)**: Problem statement, motivation, design invariants, 4 Manager views, and HR Portal.
* **Section 2: The Engineering (Slides 09–14)**: 7-stage hybrid pipeline, LLM Judge consensus, published research grounding, autonomous dictionary self-growth, architecture stack, and data model.
* **Section 3: Wrap-up & Roadmap (Slides 15–17)**: Version 2 roadmap seams, production engineering learnings, and repository contact.

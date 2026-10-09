# Pattern Specular — Documentation Assets Directory

This directory contains high-fidelity visual assets, UI screenshots, and diagrams for the Pattern Specular repository, portfolio presentations, and architectural documentation.

> **Note on Asset Clean-Up:**  
> Legacy low-resolution `.jpg` screen captures from earlier project lineage have been deprecated and removed. All official Pattern Specular documentation references lossless high-DPI `.png` captures reflecting the **Rosewood design system** (`#b83a58`), **Outfit font typography**, and the **diamond prism identity** (`psLogo`).

---

##  Official UI Screenshot Asset Inventory

The captured screenshots represent live captures from Pattern Specular running on Neon Serverless PostgreSQL and Google Gemini:

| Filename | Surface / View | Description / Primary Visual Focus |
|---|---|---|
| `01-jd-studio.png` | **JD Studio** | TipTap real-time editor showing statutory flag popover for "young" citing India's **Code on Wages, 2019** and Singapore **TAFEP**, with rewrite chips and Rosewood action buttons. |
| `02-feedback-checkpoint.png` | **Feedback Checkpoint** | Interview feedback for candidate Pooja Roy with expanded statutory citation on `family commitments` and observations panel. |
| `03-promotion-writeup.png` | **Promotion Writeup** | Published promotion evaluation for Nadia Farouk showing `Director — Markets` rubric chips, rubric coverage with `peers agree` indicators, and the static **"WHAT PEERS SAY"** corroboration panel exposing the under-selling gap. |
| `04-pattern-dashboard.png` | **Pattern Dashboard (Trends)** | Longitudinal manager dashboard displaying monthly flags bar chart, left navigation rail, and the statistically significant **Fisher's Exact Test** card (`family commitment appears in 5 documents — all 5 about women, p = 0.03 < 0.05`). |
| `04-pattern-dashboard-adoption.png` | **Pattern Dashboard (Decisions)** | Manager behavioural adoption layer displaying monthly revision rate chart (up to 73%) and gender flag resolution rate (`p = 0.03`). |
| `05-hr-portal.png` | **HR Trends Portal** | Firm-wide talent analytics dashboard displaying 82% language revision rate, monthly flags bar chart, and pending review queue preview with active $k \ge 3$ anonymity notices. |
| `06-hr-dictionary-review.png` | **Dictionary Review (Debate)** | HR terminology governance queue showcasing the **4-Agent Consensus Debate Modal** for `cultural fit` (proposer, skeptic, categoriser, and cited academic study from 2012). |
| `07-hr-word-cloud.png` | **Dictionary Review (Word Cloud)** | Interactive categorized word cloud displaying pending bias-coded candidate phrases (`cultural fit`, `work hard play hard`, `high-energy self-starter`, `no family commitments`, `able-bodied`). |
| `08-login-screen.png` | **Manager Login Portal** | High-design entry card showcasing the Rosewood diamond prism logo (`psLogo`), clean authentication inputs, and cross-portal navigation. |

---

##  Asset Capture Guidelines

1. **Resolution & Scaling:**
   - Format: 24-bit Lossless PNG.
   - Display scaling: 100% or 200% (Retina).
   - Browser viewport target: 1920×1080 (minimum 1600px width).

2. **Data State & Seeding:**
   - Seeded via `pattern_specular.jobs.seed_demo`, `seed_demo_analysis`, and `seed_demo_behaviour`.
   - Managers: `demo-manager-1` (`SM Daniyal`), `demo-manager-2` (`Areesha Naaz`), `demo-manager-3` (`Patrick Jane`).
   - HR Reviewer: `demo-hr-1` (`Teresa Lisbon`).

3. **Color & Branding Consistency:**
   - Rosewood primary accent (`#b83a58`).
   - Diamond prism logo (`psLogo`).
   - Manager privacy reminder: *"This is your own data — visible only to you."*
   - HR privacy protection: *$k \ge 3$ anonymity enforced by the data model.*

---

##  Presentation Deck Ingestion

Assets stored here are mirrored in [`docs/deck/assets/`](../deck/assets/) and ingested directly by the presentation deck generator .

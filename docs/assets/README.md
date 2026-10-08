# Pattern Specular — Documentation Assets Directory

This directory contains high-fidelity visual assets, UI screenshots, and diagrams for the Pattern Specular repository, portfolio presentations, and architectural documentation.

> **Note on Asset Clean-Up:**  
> Legacy low-resolution `.jpg` screen captures from earlier project lineage have been deprecated and removed. All official Pattern Specular documentation references lossless high-DPI `.png` captures reflecting the **Rosewood design system** (`#b83a58`), **Outfit font typography**, and the **diamond prism identity** (`psLogo`).

---

## 📸 Standard Screenshot Asset Inventory

The following 6 screenshot artifacts correspond to the canonical product surfaces and presentation slides outlined in [`docs/deck/SLIDE_SPEC.md`](../deck/SLIDE_SPEC.md):

| Filename | Surface / View | Dimensions | Description / Primary Visual Focus |
|---|---|---|---|
| `06-jd-studio-hero.png` | **JD Studio** | 1920×1080 (PNG) | TipTap real-time editor showing flagged phrases (`young`, `aggressive`, `weekend availability`) with expanded Rosewood citation card citing statutory labor standards. |
| `06-feedback-checkpoint-inset.png` | **Feedback Checkpoint** | 1200×800 (PNG) | Candidate interview evaluation showing dual-pass phrase detection alongside the **Criteria Drift Check** panel. |
| `06-promotion-writeup-inset.png` | **Promotion Writeup** | 1200×800 (PNG) | Promotion evaluation showing rubric alignment gaps and the deterministic peer corroboration comparison panel. |
| `07-pattern-dashboard.png` | **Pattern Dashboard** | 1920×1080 (PNG) | Longitudinal manager dashboard displaying 12-month category trends and Fisher's Exact Test ($p < 0.05$) significance callouts. |
| `08-hr-trends-dashboard.png` | **HR Trends Portal** | 1920×1080 (PNG) | Firm-wide talent analytics dashboard displaying cross-department metrics with active $k \ge 3$ anonymity suppression. |
| `08-hr-dictionary-review.png` | **Dictionary Review** | 1920×1080 (PNG) | HR terminology governance queue showcasing pending additions and the autonomous 4-agent LLM debate drawer. |

---

## 🎨 Asset Capture Guidelines

When capturing screenshots from the local live environment (`http://localhost:5173/`):

1. **Resolution & Scaling:**
   - Display scaling should be set to 100% or 200% (Retina).
   - Browser viewport target: 1920×1080 (minimum 1600px width).
   - Format: 24-bit Lossless PNG. Avoid lossy JPEG compression to preserve text crispness on highlighted editor spans.

2. **Data State & Seeding:**
   - Ensure the database is primed with demo data:
     ```bash
     python -m pattern_specular.jobs.seed_demo
     python -m pattern_specular.jobs.seed_demo_analysis
     python -m pattern_specular.jobs.seed_demo_behaviour
     ```
   - For Manager views, log in as `demo-manager-1` (`SM Daniyal`).
   - For HR views, log in as `demo-hr-1` (`Teresa Lisbon`).

3. **Color & Branding Consistency:**
   - Verify that the Rosewood primary accent (`#b83a58`) and diamond prism logo (`psLogo`) are rendered in the top-bar.
   - Manager views must show the privacy banner: *"This is your own data — visible only to you."*
   - HR views must show the $k \ge 3$ anonymity compliance badge.

---

## 🔗 Presentation Deck Symlink / Mirror

Assets stored here or in `docs/deck/assets/` are automatically ingested by the automated PDF presentation deck compiler (`docs/deck/compile_deck.py` or ReportLab renderer) specified in [`docs/deck/README.md`](../deck/README.md).

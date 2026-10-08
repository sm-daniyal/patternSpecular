# Pattern Specular — Live Demonstration Suite

This directory contains the demonstration playbooks, live text writeups, and evaluation scenarios for **Pattern Specular**.

---

## 📁 Demonstration Directory Structure

```
docs/demo/
├── README.md           # Demonstration suite overview & quickstart index (this file)
├── DEMO_FLOW.md        # 10-Minute live recruiter and interviewer demonstration script
└── demo-writeups.md    # Multi-manager, multi-jurisdiction copy-paste test scenarios
```

---

## 🧭 Live Demo Quickstart

### 1. Seed Background Data
Ensure Neon Serverless PostgreSQL has the submitted evaluation history and behavioural patterns seeded:

```bash
# In backend/ directory with activated virtual environment and GOOGLE_API_KEY
python -m pattern_specular.jobs.seed_demo
python -m pattern_specular.jobs.seed_demo_analysis
python -m pattern_specular.jobs.seed_demo_behaviour
```

### 2. Launch Local Services
- **Backend API**: `http://localhost:8000` (FastAPI / Uvicorn)
- **Frontend Client**: `http://localhost:5173` (Vite / React 19)

### 3. Manager Accounts Roster
All accounts use mock password authentication (`password123` or dev bypass):

| Manager Account | Name | Department | Primary Evaluation Focus |
|---|---|---|---|
| `demo-manager-1` | **SM Daniyal** | Engineering | Gender coding, family status & caregiver bias |
| `demo-manager-2` | **Areesha Naaz** | Engineering | Age discrimination & subtle interpersonal tone coding |
| `demo-manager-3` | **Patrick Jane** | Investigations | Statutory multi-jurisdiction compliance & disability accommodations |
| `demo-manager-4` | **Wayne Rigsby** | Operations | US EEOC Title VII & ADEA age/agentic coding |
| `demo-manager-5` | **Kimball Cho** | Compliance | UK Equality Act 2010 protected characteristics & pre-offer health inquiries |
| `demo-manager-6` | **Grace Van Pelt** | Data Analytics | India RPwD Act 2016 & Transgender Persons Protection Act 2019 |
| `demo-hr-1` | **Teresa Lisbon** | Human Resources | Firm-wide trends, $k \ge 3$ anonymity gating, 4-agent dictionary debate loop |

---

## 📖 Key Guides

- **[`DEMO_FLOW.md`](DEMO_FLOW.md):** The timed 10-minute presentation track for interviewers, outlining exact talking points for all 4 product surfaces and core architectural defense answers.
- **[`demo-writeups.md`](demo-writeups.md):** Ready-to-use text samples across JD Studio, Feedback Checkpoint, and Promotion Writeups with exact expected statutory citations and criteria drift outcomes.

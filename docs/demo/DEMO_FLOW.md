# Pattern Specular — Live Demonstration Playbook (10-Minute Script)

> **Audience:** Technical Recruiters, Engineering Managers, and Architecture Interviewers  
> **Host / Presenter:** `sm-daniyal` (Syed Daniyal)  
> **App URLs:** Manager Portal (`http://localhost:5173/login`) · HR Portal (`http://localhost:5173/hr/login`)

---

## ⏱️ Timeline Summary

| Time | Phase | Focus |
|---|---|---|
| **0:00 – 1:30** | **The Executive Framing** | The longitudinal bias visibility gap · Core architectural invariants |
| **1:30 – 3:30** | **Surface 1: JD Studio** | Real-time dual-pass detection · Indian Code on Wages + TAFEP statutory citations |
| **3:30 – 5:30** | **Surface 2: Feedback & Drift** | Interview feedback · Criteria drift detection against stated JD skills |
| **5:30 – 7:30** | **Surface 3: Pattern Dashboard** | Mathematical significance · Fisher's Exact Test ($p < 0.05$) vs raw count |
| **7:30 – 9:00** | **Surface 4: HR Portal & Growth** | $k \ge 3$ anonymity suppression · Autonomous 4-agent dictionary debate loop |
| **9:00 – 10:00** | **Technical Q&A Defense** | Verbatim span adjudication · Latency budgets · Neon DB schema isolation |

---

## 🎙️ Step-by-Step Walkthrough

### Part 1: Executive Framing (0:00 – 1:30)

> *"Unconscious bias training in corporate enterprises is broken. Companies spend significant budgets teaching managers fair hiring theory, yet subtle bias still creeps into job descriptions, candidate feedback, and promotion writeups.*
> 
> *In isolation, an individual document looks completely harmless or borderline. The bias only reveals itself across 20+ documents over time. Pattern Specular is a calibration mirror for managers: it flags statutory violations in real time, checks criteria drift, and surfaces longitudinal patterns using Fisher's exact test — never as a punitive score or hiring gate."*

---

### Part 2: JD Studio (1:30 – 3:30)

* **Action:** Sign into `http://localhost:5173/login` as `sm.daniyal@example.com`.
* **Action:** In JD Studio, select role `Lead Systems Architect`.
* **Paste Sample Text:**
  ```text
  We are hiring a young, dynamic go-getter to spearhead our high-throughput distributed systems squad — someone aggressive, hungry to scale, and able to dedicate 70 hours a week with round-the-clock weekend availability. 

  The ideal candidate is an able-bodied digital native who thrives in a fast-paced environment and has no family commitments getting in the way. Recent university graduates with boundless stamina are encouraged to apply.
  ```
* **Talking Points:**
  1. *"Notice that within 5 milliseconds, deterministic spaCy lemmatization caught `young`, `digital native`, and `able-bodied`."*
  2. *"When the user pauses, our background Google Gemini pass evaluates the sentence context and flags `no family commitments` and `aggressive`."*
  3. *"Clicking on any card reveals that every flag is backed by statutory labor law — citing India's **Code on Wages 2019** and Singapore's **TAFEP** guidelines with evidence-anchored rewrite chips."*

---

### Part 3: Feedback Checkpoint & Criteria Drift (3:30 – 5:30)

* **Action:** Click **Feedback Checkpoint** tab. Select role `Lead Systems Architect[demo]`.
* **Paste Sample Text:**
  ```text
  georgina is a polished, collaborative candidate who structured her architectural breakdown smoothly. Warm, polite, and a genuine team player. She did bring up evening family commitments, so I'm not convinced she'll manage on-call crunch rotations. While she has a pleasant personality, she lacks the aggressive edge we typically look for.
  ```
* **Hit "Re-check"**:
* **Talking Points:**
  1. *"Notice the dual analysis: the engine flags `family commitments` (statutory family status) and `warm` / `polished` (gendered interpersonal framing)."*
  2. *"Simultaneously, the **Criteria Drift Check** highlights that the interviewer evaluated none of the JD's required technical skills (*Distributed consensus*, *Database partitioning*, *Profiling*). This prevents interviewers from rejecting candidates based on subjective chemistry while ignoring core job qualifications."*

---

### Part 4: Pattern Dashboard (5:30 – 7:30)

* **Action:** Click **Pattern Dashboard** tab.
* **Talking Points:**
  1. *"This is the longitudinal view. Unlike naive grammar checkers that spam alerts, Pattern Specular looks at a manager's entire historical corpus across months."*
  2. *"Notice the **Still recurring** section. A tendency is only surfaced when **Fisher's Exact Test** proves $p < 0.05$ against peer baseline distributions. For example: `aggressive` appeared in 6 documents, all 6 about men ($p = 0.01$)."*
  3. *"Clicking 'View 6 notes' opens an evidence drawer showing exact document timestamps and source context, giving managers undeniable, objective proof to self-calibrate."*

---

### Part 5: HR Portal, $k \ge 3$ Privacy & Dictionary Growth (7:30 – 9:00)

* **Action:** Open Incognito window, go to `http://localhost:5173/hr/login`, sign in as `teresa.lisbon@example.com`.
* **Action:** Show the **Trends Dashboard** (`/hr`).
* **Talking Points:**
  1. *"Notice the footer: 'Aggregates only: enforced by the data model, not by policy.' HR endpoints physically cannot query individual manager documents or employee names."*
  2. *"Furthermore, all cohort reporting enforces **$k \ge 3$ anonymity suppression** — any category covering fewer than 3 managers is omitted to prevent statistical re-identification."*
* **Action:** Click **Dictionary Review** (`/hr/dictionary-review`). Click on `no family commitments` or `cultural fit`.
* **Talking Points:**
  1. *"This is our autonomous 4-agent growth loop. When the AI contextual pass repeatedly flags a new term across documents, 4 independent Gemini agents debate the phrase: Proposer, Skeptic, Categorizer, and Citation."*
  2. *"If it passes all consensus gates, it lands in this human-in-the-loop review queue. When HR clicks 'Approve', it becomes an instant, zero-latency Stage 1 dictionary rule firm-wide."*

---

### Part 6: Engineering Q&A & Tough Questions (9:00 – 10:00)

1. **"How do you stop the LLM from hallucinating flags?"**
   > *"Stage 3 is a deterministic Python Adjudicator. Every phrase the LLM claims to flag must match verbatim against the source character offsets. Any hallucinated quote is dropped immediately."*

2. **"Why use Fisher's Exact Test instead of Chi-Square?"**
   > *"Chi-Square approximations fail when cell counts are small ($N < 5$). In hiring and promotion reviews, individual managers often write 10 to 30 documents per cycle. Fisher's Exact Test calculates the exact hypergeometric probability, making it robust for small sample sizes."*

3. **"How is privacy guaranteed at the database level?"**
   > *"In our SQLAlchemy data model, manager documents are foreign-keyed to `owner_id`. HR query handlers execute group-by aggregates only and lack any query route accepting a `document_id` parameter. Privacy is an architectural invariant, not an application-layer if-statement."*

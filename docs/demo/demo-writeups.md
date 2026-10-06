# Demo content pack — live writeups to type in the UI

These are showcase documents to **enter by hand during live evaluation or demo**, on top of the seeded
history. The seeded history (run by the `seed_demo*` jobs) is what powers the Pattern Dashboard and
the HR view; these live entries show the *per-document* flow — flags streaming in as you type, drift
coverage, and the promotion corroboration panel — for a fresh document.

**Sign-in:** the manager roster features mock-login accounts:
- `demo-manager-1`: SM Daniyal (Engineering)
- `demo-manager-2`: Areesha Naaz (Engineering)
- `demo-manager-3`: Patrick Jane (Investigations)
- `demo-manager-4`: Wayne Rigsby (Operations)
- `demo-manager-5`: Kimball Cho (Compliance)
- `demo-manager-6`: Grace Van Pelt (Data Analytics)

HR reviewer is `demo-hr-1` (Teresa Lisbon, Human Resources).

Each writeup names the **role / subject / level** it belongs to so its links resolve against the
seeded data. Coded language that should flag is called out under each.

---

## SM Daniyal (Engineering) — gender + family_status

### JD Studio — publish a JD
**Role:** `Lead Systems Architect` (or a fresh `Senior Systems Engineer`).

> We're looking for a young, dynamic go-getter to spearhead our high-throughput distributed systems squad — someone
> aggressive, hungry to scale, and able to dedicate 70 hours a week with round-the-clock weekend availability. Recent
> university graduates with boundless stamina are encouraged to apply.

**Should flag:** `young`, `dynamic` (age), `aggressive` (gender), `recent university graduate` (age), and the
**70 hours / weekend availability** requirement (family status / caregiver exclusion across TAFEP, EEOC, and Equality Act). On
**Publish**, review the AI-extracted assessment criteria and confirm them.

### Feedback Checkpoint — interview feedback
**Role:** `Lead Systems Architect` · **Candidate:** any female candidate (e.g. "Pooja Roy").

> Pooja is a polished, collaborative candidate who structured her architectural breakdown smoothly. Warm, polite, and a
> genuine team player. She did bring up evening family commitments, so I'm not convinced she'll manage on-call crunch
> rotations.

**Should flag:** `polished`, `collaborative`, `warm` (gender-coded, contextual pass), `family commitments`
(family status statutory hit). **Drift:** the note addresses none of the JD's stated technical criteria (distributed consensus,
database partitioning, profiling) — the criteria coverage panel marks them unaddressed.

### Promotion Writeup — evaluate for promotion
**Level:** `Principal Engineer` · **Employee:** Nadia Farouk (seeded, has peer feedback + rubric).

> Nadia is a lovely, supportive presence on the squad — always willing to help, keeps everyone's
> morale up, and is nurturing with junior developers. She's dependable and well-liked. I'm putting her
> forward for Principal Engineer because she works tirelessly to keep the team harmonious.

**Should flag:** `supportive`, `nurturing`, `dependable` (gender-coded). **Rubric coverage:** the
writeup evidences none of *architecture ownership / system reliability / technical roadmap / cross-functional leadership*, yet the
**"what peers say"** panel shows peers corroborate all technical deliverables — illustrating the writeup-vs-corroboration gap.

### Seeded promotion showcases (open these — no typing needed)
SM Daniyal has seeded, submitted promotion writeups whose **peer-corroboration panels are static**
(rendering deterministically without an LLM call):

- **Nadia Farouk → Principal Engineer** — *gendered under-selling.* Writeup emphasizes warmth/support; peers
  corroborate all technical criteria the writeup omits.
- **Victor Salleh → Principal Engineer** — *personal advocacy bias.* Writeup over-advocates on personal chemistry
  ("we catch up regularly outside work, he's like family to me"), yet peers **do not** corroborate
  *system architecture* or *mentorship*.
- **Kavya Menon → Staff Engineer** — *fair, fact-based counter.* A newer hire: peers note she is
  "early in tenure" and corroborate little, but the writeup counters with verifiable technical milestones.

---

## Areesha Naaz (Engineering) — age + gender

### JD Studio — publish a JD
**Role:** `Software Engineer` (or `Fullstack Engineer`).

> Looking for a young, high-energy digital native to join our core product squad — someone who lives
> and breathes modern reactive stacks. Fresh grads welcome; we move fast and love an energetic rockstar.

**Should flag:** `young`, `digital native`, `fresh grad` (age / India Code on Wages + UK Equality Act). Confirm criteria on publish.

### Feedback Checkpoint — interview feedback
**Role:** `Software Engineer` · **Candidate:** a male candidate (e.g. "Arjun Mehta").

> Arjun is a sharp developer and a real digital native — grasped our microservices within an hour. Assertive in
> design discussions and a young, hungry problem solver. Strong hire.

**Should flag:** `sharp`, `assertive` (gender-coded), `digital native`, `young` (age). Drift: technical JD
criteria largely unaddressed.

### Promotion Writeup
**Level:** `Engineering Director` · **Employee:** Farah Idris (seeded).

> Farah is a pleasant, supportive teammate who maintains team spirit and coordinates team cohesion. She's
> nurturing with interns and everyone enjoys collaborating with her. Recommending her for Director
> because she's thoroughly dependable.

**Should flag:** `supportive`, `nurturing`, `dependable`. Coverage gap vs the leadership rubric, with
peers corroborating technical delivery.

---

## Patrick Jane (Investigations & Compliance) — statutory multi-jurisdiction

### JD Studio — publish a JD
**Role:** `Compliance Analyst` (or `Forensic Operations Specialist`).

> Fast-paced compliance investigation role in a young, dynamic unit. Must be physically fit and able-bodied.
> Local residents strictly preferred; work visa holders need not apply.

**Should flag:** `young`, `dynamic` (age), `physically fit`, `able-bodied` (disability-coded under India RPwD Act 2016 & ADA),
`work visa holders need not apply` (nationality exclusion under TAFEP & Title VII).

### Feedback Checkpoint — interview feedback
**Role:** `Compliance Analyst` · **Candidate:** candidate (e.g. "Devika Rao").

> Devika is calm and process-oriented. She indicated needing medical accommodations, which might present scheduling challenges
> during high-volume auditing cycles. Reliable and pleasant demeanor overall.

**Should flag:** medical accommodations framing (disability discrimination under RPwD Act 2016 / ADA / Equality Act),
`pleasant` (gender-coded).

---

## Notes

- The seeded promotion writeups are **submitted history** (enabling the Pattern Dashboard and longitudinal analysis);
  the entries above are **new drafts** to enter live, exercising the real-time engine as you type.
- Every coded term above is either a dictionary hit (deterministic, instant sub-100ms) or a contextual hit
  (streams in via SSE after typing pause).
- Multi-jurisdiction rules (India, Singapore, US, UK) run simultaneously on every analysis run.

### Priming the dashboard (requires Google Gemini API key)
`seed_demo` seeds the documents, subjects, peer feedback, rubrics, and corroboration. The **Pattern Dashboard** and the
**contextual flags** can be pre-analyzed by running from `backend/` with a valid `GOOGLE_API_KEY`:

```bash
python -m pattern_specular.jobs.seed_demo_analysis    # flags + drift over the submitted history
python -m pattern_specular.jobs.seed_demo_behaviour   # accept/dismiss interactions -> decision patterns
```

`seed_demo_analysis` is idempotent and safely retries any unanalyzed document.

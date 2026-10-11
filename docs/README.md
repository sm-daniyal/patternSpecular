# Documentation index

| Document | What it is | Audience |
|---|---|---|
| [DESIGN_SPEC.md](DESIGN_SPEC.md) | The captured product design specification — the product source of truth | Everyone; binding on engine semantics |
| [architecture/overview.md](architecture/overview.md) | The system as built: statutory boundaries, engine shape, data paths | Anyone reading or reviewing the code |
| [architecture/llm-judge.md](architecture/llm-judge.md) | The LLM Judge: rubric scoring, self-consistency confidence, calibration | Anyone interested in the LLM-as-judge design |
| [architecture/flags-and-suppression.md](architecture/flags-and-suppression.md) | Flag identity: lemma signatures, sentence fingerprints, dismissal suppression | Anyone touching flag persistence or dismissals |
| [architecture/dictionary-growth.md](architecture/dictionary-growth.md) | How the lexicon grows: trigger threshold, four-agent debate, HR approval | Anyone touching the growth loop or dictionary |
| [architecture/pattern-significance.md](architecture/pattern-significance.md) | Why a pattern surfaces: Fisher's Exact Test gating on the Pattern Dashboard | Anyone touching the Pattern Dashboard or aggregator |
| [architecture/data-model.md](architecture/data-model.md) | ER map of the 17 core entities and the columns that earn an explanation | Anyone touching models or migrations |
| [architecture/india-lexicon-mapping.md](architecture/india-lexicon-mapping.md) | Mapping of Indian labor legislation (Code on Wages, RPwD, Transgender Act) to lexicon categories | Anyone touching IN-jurisdiction dictionary entries |
| [architecture/api-contracts.md](architecture/api-contracts.md) | REST and SSE endpoint contracts, streaming protocol, and error shapes | Anyone writing or consuming the API |
| [future.md](future.md) | Post-MVP design proposals — explicitly not built | Anyone curious where the architecture could go |
| [project-management.md](project-management.md) | How the project is run: epics, issues, how changes ship | Non-technical readers; anyone curious about delivery |
| [CONVENTIONS.md](CONVENTIONS.md) | How we work: folder structure, testing, git, PRs, project management | Contributors |
| [CODE_STYLE.md](CODE_STYLE.md) | Language-level style rules for Python and TypeScript | Contributors |
| [adr/](adr/) | Architecture decision records — what was decided, when, and why | Anyone asking "why is it like this?" |
| [references/](references/) | Statutory legal frameworks (India, Singapore, US, UK) and TAFEP guidance | Dictionary curators & legal compliance |
| [references/compliance_frameworks.md](references/compliance_frameworks.md) | Multi-jurisdiction statutory legal grounding and GDOR/BFOQ exceptions | Compliance reviewers & legal teams |
| [demo/](demo/) | Live demonstration playbook and multi-jurisdiction test scenarios | Interviewers & evaluators |
| [deck/pattern-specular-deck.pdf](deck/pattern-specular-deck.pdf) | 17-slide executive walkthrough presentation deck (16:9 PDF) | Executive reviewers & technical hiring managers |

Architecture docs describe current state and change with the code; ADRs are immutable records of decisions at a point in time. When they disagree, the ADR is history and the architecture doc is the bug.

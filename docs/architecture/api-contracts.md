# API Contracts & SSE Protocol Specification

This specification documents all public and internal REST endpoints and Server-Sent Event (SSE) streaming channels provided by the Pattern Specular API (`backend/src/pattern_specular/api/`).

---

## 1. Authentication (`/auth`)

### `POST /auth/login`
Authenticates a seeded manager or HR administrator and returns a signed session token with cached user profile details.

* **Request Body (`LoginRequest`):**
  ```json
  {
    "email": "sm.daniyal@example.com",
    "password": "sample-password",
    "expected_role": "manager"
  }
  ```
  * `email` (string): Registered user email address.
  * `password` (string, min length 1): User password credential.
  * `expected_role` (enum: `"manager"` | `"hr"`): The portal role expected by the requesting client.

* **Response (200 OK — `LoginResponse`):**
  ```json
  {
    "token": "header.payload.signature",
    "user": {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "legal_name": "SM Daniyal",
      "initials": "SD",
      "email": "sm.daniyal@example.com",
      "role": "manager"
    }
  }
  ```

---

## 2. Real-Time Analysis (`/analyze`)

### `POST /analyze` (Synchronous Immediate Pass)
Executes deterministic dictionary analysis over an active document draft, persisting flags and citations.

* **Headers:** `Authorization: Bearer <token>`
* **Latency:** < 100ms
* **Request Body (`AnalyzeRequest`):**
  ```json
  {
    "document_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "content": "We are seeking a rockstar developer with aggressive drive."
  }
  ```
* **Response (200 OK — `AnalyzeResponse`):**
  ```json
  {
    "document_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "analysis_run_id": "8bb98c77-1064-4e4f-b673-c603952fb584",
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "flags": [
      {
        "id": "18f8e079-8806-4b2a-bf3d-24e526487e68",
        "source_stage": "dictionary",
        "category": "gender_coded_masculine",
        "raw_span": "rockstar",
        "start_offset": 19,
        "end_offset": 27,
        "explanation": "Identified as masculine-coded phrasing under employment non-discrimination lexicon.",
        "citation": {
          "source_type": "statutory",
          "title": "TAFEP Tripartite Guidelines on Fair Employment Practices",
          "reference": "TAFEP-G-2023-01",
          "publication_year": 2023,
          "finding": "Avoid masculine-coded exclusionary jargon that discourages diverse applicant pools."
        },
        "recommendations": null
      }
    ]
  }
  ```

---

## 3. Streaming Analysis (`/analyze/stream` & `/documents/{id}/recheck`)

### `POST /analyze/stream` (SSE Channel)
Opens a Server-Sent Events stream providing real-time stage progress and surfaced flags with embedded rewrite recommendations as the 7-stage engine completes each node.

* **Headers:**
  - `Authorization: Bearer <token>`
  - `Accept: text/event-stream`
* **Request Body (`AnalyzeStreamRequest`):**
  ```json
  {
    "document_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "content": "Looking for a digital native to lead our client communications."
  }
  ```

### SSE Stream Framing Protocol
The server emits standard `event:` and `data:` blocks formatted via `backend/src/pattern_specular/api/sse.py`.

#### 1. `event: stage`
Emitted as each engine stage completes (`dictionary`, `contextual_pass`, `span_adjudicator`, `drift_detection`, `llm_judge`, `recommendations`, `persistence`).
```
event: stage
data: {"stage":"contextual_pass"}

```

#### 2. `event: flag`
Emitted for each validated flag passing the Adjudicator and LLM Judge. If recommendations have been generated, they are embedded directly in the flag object.
```
event: flag
data: {"id":"18f8e079-8806-4b2a-bf3d-24e526487e68","source_stage":"contextual","category":"age_bias","raw_span":"digital native","start_offset":14,"end_offset":28,"explanation":"Phrasing suggests age preference excluding experienced candidates.","citation":{"source_type":"statutory","title":"TAFEP Fair Employment Guidelines","reference":"TAFEP-A-2023-04","publication_year":2023,"finding":"Age requirements must relate strictly to genuine occupational qualifications."},"recommendations":{"rationale":"Focus on demonstrated technological competence rather than generational identity.","alternatives":["proficient in modern digital communication platforms","experienced with digital workflow tools"]}}

```

#### 3. `event: done`
Emitted when the engine reaches a terminal state, summarizing the completed run.
```
event: done
data: {"analysis_run_id":"8bb98c77-1064-4e4f-b673-c603952fb584","status":"completed","flag_count":1}

```

---

## 4. Document Management (`/documents`)

* `GET /documents`: Lists all documents owned by the authenticated manager.
* `POST /documents`: Creates a new document container (`title`, `doc_type`, `region_code`).
* `GET /documents/{id}`: Returns document metadata, latest revision content, and active flag history.
* `POST /documents/{id}/dismiss`: Records a manager's dismissal of a flag (`flag_id`, `reason`), suppressing it from subsequent surface views.
* `POST /documents/{id}/recheck`: Re-runs the full 7-stage pipeline over an existing document revision, streaming progress over SSE.

---

## 5. Analytics & Statistical Portals (`/analytics`)

* `GET /analytics/patterns`:
  - **Audience:** Manager Portal (Individual).
  - **Purpose:** Surfaces recurring bias patterns across a manager's document portfolio.
  - **Statistical Invariant:** Only categories satisfying two-tailed Fisher's exact test significance ($p < 0.05$) against baseline corporate cohorts are displayed.
* `GET /analytics/firm-trends`:
  - **Audience:** HR Portal (Organization-wide).
  - **Purpose:** Displays firm-level aggregated bias distributions and category trends.
  - **Privacy Invariant:** Strictly enforces $k$-anonymity ($k \ge 3$). Any department, level, or cohort with fewer than 3 contributing managers is automatically suppressed.

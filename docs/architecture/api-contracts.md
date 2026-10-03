# API Contracts & SSE Protocol Specification

This specification documents all public and internal REST endpoints and Server-Sent Event (SSE) streaming channels.

## 1. Authentication (`/auth`)

### `POST /auth/login`
- **Request Body:** `{"email": "sm.daniyal@example.com", "role": "manager"}`
- **Response (200 OK):**
  ```json
  {
    "token": "payload.hmac_signature",
    "user": {
      "id": "uuid",
      "legal_name": "SM Daniyal",
      "email": "sm.daniyal@example.com",
      "roles": ["manager"]
    }
  }
  ```

---

## 2. Real-Time Analysis (`/analyze`)

### `POST /analyze` (Sync Dictionary Pass)
- **Latency:** < 100ms
- **Request:** `{"document_id": "uuid", "text": "...", "doc_type": "jd", "region_code": "SG"}`
- **Response:** List of immediate statutory flags with offsets and legal citations.

### `POST /analyze/stream` (SSE Channel)
- **Content-Type:** `text/event-stream`
- **Event Flow:**
  1. `event: run_started` — Analysis run ID assigned.
  2. `event: flag` — Contextual flag emitted after Adjudicator span check.
  3. `event: recommendations` — Neutral rewrite alternatives generated.
  4. `event: done` — LangGraph pipeline reaches terminal state.

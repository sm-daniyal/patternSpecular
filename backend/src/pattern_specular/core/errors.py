"""Project exception hierarchy.

Every error raised by pattern-mirror subclasses :class:`PatternSpecularError`, so
callers can catch the whole family at a boundary (an API handler, the engine
orchestrator) and map it to a response, while still raising the most specific
type at the point of failure.
"""


class PatternSpecularError(Exception):
    """Base class for all pattern-mirror domain errors."""


class SeedDataMissingError(PatternSpecularError):
    """Required seed data (e.g. the demo manager) is absent from the database."""


class InvalidCredentialsError(PatternSpecularError):
    """Login credentials do not match an active user holding the expected role."""

    def __init__(self) -> None:
        super().__init__("Invalid credentials.")


class NotAuthenticatedError(PatternSpecularError):
    """The request carries no valid session token."""

    def __init__(self) -> None:
        super().__init__("Not authenticated.")


class NotAuthorizedError(PatternSpecularError):
    """The caller is authenticated but lacks the role required for this resource."""

    def __init__(self) -> None:
        super().__init__("Not authorized.")


class BlobNotFoundError(PatternSpecularError):
    """No blob is stored under the given reference."""

    def __init__(self, ref: object) -> None:
        super().__init__(f"Blob not found: {ref}")
        self.ref = ref


class ResumeNotFoundError(PatternSpecularError):
    """The subject has no stored resume, or the caller may not read it."""

    def __init__(self, subject_id: object) -> None:
        super().__init__(f"Resume not found: {subject_id}")
        self.subject_id = subject_id


class DocumentNotFoundError(PatternSpecularError):
    """A requested document does not exist or is not owned by the current user."""

    def __init__(self, document_id: object) -> None:
        super().__init__(f"Document not found: {document_id}")
        self.document_id = document_id


class DocumentTypeMismatchError(PatternSpecularError):
    """An operation ran against a document of the wrong type (e.g. JD criteria on feedback)."""

    def __init__(self, document_id: object, expected: object, actual: object) -> None:
        super().__init__(f"Document {document_id} is {actual}, expected {expected}")
        self.document_id = document_id
        self.expected = expected
        self.actual = actual


class LlmClientUnavailableError(PatternSpecularError):
    """An LLM-backed action was requested but no Anthropic client is configured."""

    def __init__(self) -> None:
        super().__init__("LLM client is not configured.")


class FlagNotFoundError(PatternSpecularError):
    """A requested flag does not exist or belongs to another user's document."""

    def __init__(self, flag_id: object) -> None:
        super().__init__(f"Flag not found: {flag_id}")
        self.flag_id = flag_id


class DriftFindingNotFoundError(PatternSpecularError):
    """A requested drift finding does not exist or belongs to another user's document."""

    def __init__(self, finding_id: object) -> None:
        super().__init__(f"Drift finding not found: {finding_id}")
        self.finding_id = finding_id


class PendingAdditionNotFoundError(PatternSpecularError):
    """A requested pending dictionary addition does not exist."""

    def __init__(self, addition_id: object) -> None:
        super().__init__(f"Pending addition not found: {addition_id}")
        self.addition_id = addition_id


class ProposalNotFoundError(PatternSpecularError):
    """A requested dictionary-growth proposal does not exist."""

    def __init__(self, proposal_id: object) -> None:
        super().__init__(f"Proposal not found: {proposal_id}")
        self.proposal_id = proposal_id


class AdditionAlreadyDecidedError(PatternSpecularError):
    """A pending addition has already been approved or rejected and cannot be decided again."""

    def __init__(self, addition_id: object, status: object) -> None:
        super().__init__(f"Pending addition {addition_id} already decided: {status}")
        self.addition_id = addition_id
        self.status = status


class DictionaryEntryExistsError(PatternSpecularError):
    """An active dictionary entry already exists for this region, phrase, and category."""

    def __init__(self, lemma_key: object, category: object) -> None:
        super().__init__(f"Dictionary entry already exists: {lemma_key} ({category})")
        self.lemma_key = lemma_key
        self.category = category


class RecommendationCountError(PatternSpecularError):
    """The Recommendations Agent returned a different number of sets than the flags given."""

    def __init__(self, expected: int, received: int) -> None:
        super().__init__(f"Recommendations returned {received} sets for {expected} flags")
        self.expected = expected
        self.received = received

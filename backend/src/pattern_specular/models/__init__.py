"""SQLAlchemy ORM models.

Importing this package imports every model module, which is what registers all
mappers on the shared ``Base`` and lets string-based ``relationship()`` targets
resolve. Alembic's ``env.py`` and the test harness import it for exactly that
reason: a model missing from here is invisible to autogenerate.
"""

from pattern_specular.models.audit import AgentRun
from pattern_specular.models.calibration import CalibrationRun
from pattern_specular.models.dictionary import Dictionary
from pattern_specular.models.documents import AnalysisRun, Document
from pattern_specular.models.drift import (
    DriftFinding,
    DriftFindingDismissal,
    DriftFindingInteraction,
)
from pattern_specular.models.engine import Flag, FlagDismissal
from pattern_specular.models.growth import DictionaryProposal, PendingDictionaryAddition
from pattern_specular.models.identity import Subject, User, UserRoleAssignment
from pattern_specular.models.jd_criteria import JdCriterion
from pattern_specular.models.peer_corroboration import PeerCorroboration
from pattern_specular.models.peer_feedback import PeerFeedback
from pattern_specular.models.promotion_rubric import PromotionRubricCriterion
from pattern_specular.models.reference import Citation, Region

__all__ = [
    "AgentRun",
    "AnalysisRun",
    "CalibrationRun",
    "Citation",
    "Dictionary",
    "DictionaryProposal",
    "Document",
    "DriftFinding",
    "DriftFindingDismissal",
    "DriftFindingInteraction",
    "Flag",
    "FlagDismissal",
    "JdCriterion",
    "PeerCorroboration",
    "PeerFeedback",
    "PendingDictionaryAddition",
    "PromotionRubricCriterion",
    "Region",
    "Subject",
    "User",
    "UserRoleAssignment",
]

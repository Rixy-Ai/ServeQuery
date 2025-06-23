from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from servequery.legacy.test_preset.test_preset import AnyTest
from servequery.legacy.test_preset.test_preset import TestPreset
from servequery.legacy.tests import TestHitRateK
from servequery.legacy.tests import TestMAPK
from servequery.legacy.tests import TestNDCGK
from servequery.legacy.tests import TestPrecisionTopK
from servequery.legacy.tests import TestRecallTopK
from servequery.legacy.utils.data_preprocessing import DataDefinition


class RecsysTestPreset(TestPreset):
    class Config:
        type_alias = "servequery:test_preset:RecsysTestPreset"

    """
    Recsys performance tests.

    Contains tests:
    - `TestPrecisionTopK`
    - `TestRecallTopK`
    - `TestMAPK`
    - `TestNDCGK`
    - `TestHitRateK`
    """

    k: int
    min_rel_score: Optional[int]
    no_feedback_users: bool

    def __init__(self, k: int, min_rel_score: Optional[int] = None, no_feedback_users: bool = False):
        self.k = k
        self.min_rel_score = min_rel_score
        self.no_feedback_users = no_feedback_users
        super().__init__()

    def generate_tests(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyTest]:
        return [
            TestPrecisionTopK(k=self.k, min_rel_score=self.min_rel_score, no_feedback_users=self.no_feedback_users),
            TestRecallTopK(k=self.k, min_rel_score=self.min_rel_score, no_feedback_users=self.no_feedback_users),
            TestMAPK(k=self.k, min_rel_score=self.min_rel_score, no_feedback_users=self.no_feedback_users),
            TestNDCGK(k=self.k, min_rel_score=self.min_rel_score, no_feedback_users=self.no_feedback_users),
            TestHitRateK(k=self.k, min_rel_score=self.min_rel_score, no_feedback_users=self.no_feedback_users),
        ]

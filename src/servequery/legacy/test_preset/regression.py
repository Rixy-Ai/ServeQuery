from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from servequery.legacy.test_preset.test_preset import AnyTest
from servequery.legacy.test_preset.test_preset import TestPreset
from servequery.legacy.tests import TestValueMAE
from servequery.legacy.tests import TestValueMAPE
from servequery.legacy.tests import TestValueMeanError
from servequery.legacy.tests import TestValueRMSE
from servequery.legacy.utils.data_preprocessing import DataDefinition


class RegressionTestPreset(TestPreset):
    class Config:
        type_alias = "servequery:test_preset:RegressionTestPreset"

    """
    Regression performance tests.

    Contains tests:
    - `TestValueMeanError`
    - `TestValueMAE`
    - `TestValueRMSE`
    - `TestValueMAPE`
    """

    def generate_tests(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyTest]:
        return [
            TestValueMeanError(),
            TestValueMAE(),
            TestValueRMSE(),
            TestValueMAPE(),
        ]

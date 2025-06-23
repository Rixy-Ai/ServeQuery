from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from servequery.legacy.test_preset.test_preset import AnyTest
from servequery.legacy.test_preset.test_preset import TestPreset
from servequery.legacy.tests import TestAllColumnsShareOfMissingValues
from servequery.legacy.tests import TestCatColumnsOutOfListValues
from servequery.legacy.tests import TestColumnsType
from servequery.legacy.tests import TestNumberOfColumns
from servequery.legacy.tests import TestNumberOfRows
from servequery.legacy.tests import TestNumColumnsMeanInNSigmas
from servequery.legacy.tests import TestNumColumnsOutOfRangeValues
from servequery.legacy.utils.data_preprocessing import DataDefinition


class DataStabilityTestPreset(TestPreset):
    class Config:
        type_alias = "servequery:test_preset:DataStabilityTestPreset"

    """
    Data Stability tests.

    Contains tests:
    - `TestNumberOfRows`
    - `TestNumberOfColumns`
    - `TestColumnsType`
    - `TestAllColumnsShareOfMissingValues`
    - `TestNumColumnsOutOfRangeValues`
    - `TestCatColumnsOutOfListValues`
    - `TestNumColumnsMeanInNSigmas`
    """

    columns: Optional[List[str]]

    def __init__(
        self,
        columns: Optional[List[str]] = None,
    ):
        self.columns = columns
        super().__init__()

    def generate_tests(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyTest]:
        return [
            TestNumberOfRows(),
            TestNumberOfColumns(),
            TestColumnsType(),
            TestAllColumnsShareOfMissingValues(columns=self.columns),
            TestNumColumnsOutOfRangeValues(columns=self.columns),
            TestCatColumnsOutOfListValues(columns=self.columns),
            TestNumColumnsMeanInNSigmas(columns=self.columns),
        ]

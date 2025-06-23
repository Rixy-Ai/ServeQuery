from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from servequery.legacy.test_preset.test_preset import AnyTest
from servequery.legacy.test_preset.test_preset import TestPreset
from servequery.legacy.tests import TestAllColumnsMostCommonValueShare
from servequery.legacy.tests import TestAllColumnsShareOfMissingValues
from servequery.legacy.tests import TestNumberOfConstantColumns
from servequery.legacy.tests import TestNumberOfDuplicatedColumns
from servequery.legacy.tests import TestNumberOfDuplicatedRows
from servequery.legacy.utils.data_preprocessing import DataDefinition


class DataQualityTestPreset(TestPreset):
    class Config:
        type_alias = "servequery:test_preset:DataQualityTestPreset"

    """
    Data Quality tests.

    Contains tests:
    - `TestAllColumnsShareOfMissingValues`
    - `TestAllColumnsMostCommonValueShare`
    - `TestNumberOfConstantColumns`
    - `TestNumberOfDuplicatedColumns`
    - `TestNumberOfDuplicatedRows`
    - `TestHighlyCorrelatedColumns`
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
            TestAllColumnsShareOfMissingValues(columns=self.columns),
            TestAllColumnsMostCommonValueShare(columns=self.columns),
            TestNumberOfConstantColumns(),
            TestNumberOfDuplicatedColumns(),
            TestNumberOfDuplicatedRows(),
        ]

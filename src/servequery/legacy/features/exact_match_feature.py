from typing import ClassVar
from typing import List

import pandas as pd

from servequery.legacy.base_metric import ColumnName
from servequery.legacy.core import ColumnType
from servequery.legacy.features.generated_features import GeneratedFeature
from servequery.legacy.utils.data_preprocessing import DataDefinition


class ExactMatchFeature(GeneratedFeature):
    class Config:
        type_alias = "servequery:feature:ExactMatchFeature"

    __feature_type__: ClassVar = ColumnType.Categorical
    columns: List[str]

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        return pd.DataFrame({self._feature_name(): data[self.columns[0]] == data[self.columns[1]]})

    def _feature_name(self):
        return "|".join(self.columns)

    def _as_column(self) -> "ColumnName":
        return self._create_column(
            self._feature_name(),
            default_display_name=f"Exact Match for {' '.join(self.columns)}.",
        )

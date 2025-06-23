from typing import Callable
from typing import Union

import pandas as pd

from servequery.legacy.core import ColumnType
from servequery.legacy.core import new_id
from servequery.legacy.features.custom_feature import CustomPairColumnFeature
from servequery.legacy.features.custom_feature import CustomSingleColumnFeature
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneralDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature


class CustomColumnEval(FeatureDescriptor):
    class Config:
        type_alias = "servequery:descriptor:CustomColumnEval"

    func: Callable[[pd.Series], pd.Series]
    display_name: str
    feature_type: Union[str, ColumnType]
    name: str = ""

    def feature(self, column_name: str) -> GeneratedFeature:
        return CustomSingleColumnFeature(
            func=self.func,
            column_name=column_name,
            display_name=self.display_name,
            feature_type=ColumnType(self.feature_type),
            name=self.name or getattr(self.func, "__name__", str(new_id())),
        )


class CustomPairColumnEval(GeneralDescriptor):
    class Config:
        type_alias = "servequery:descriptor:CustomPairColumnEval"

    func: Callable[[pd.Series, pd.Series], pd.Series]
    display_name: str
    first_column: str
    second_column: str
    feature_type: Union[str, ColumnType]

    def feature(self) -> GeneratedFeature:
        return CustomPairColumnFeature(
            func=self.func,
            first_column=self.first_column,
            second_column=self.second_column,
            display_name=self.display_name,
            feature_type=ColumnType(self.feature_type),
        )

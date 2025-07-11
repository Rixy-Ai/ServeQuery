from typing import List
from typing import Optional

import pandas as pd

from servequery.legacy.base_metric import InputData
from servequery.legacy.base_metric import Metric
from servequery.legacy.base_metric import MetricResult
from servequery.legacy.core import IncludeTags
from servequery.legacy.model.widget import BaseWidgetInfo
from servequery.legacy.options.base import AnyOptions
from servequery.legacy.renderers.base_renderer import MetricRenderer
from servequery.legacy.renderers.base_renderer import default_renderer


class TrainStatsResult(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:TrainStatsResult"
        field_tags = {
            "current": {IncludeTags.Current},
            "current_n_users": {IncludeTags.Current},
            "reference": {IncludeTags.Reference},
            "reference_n_users": {IncludeTags.Reference},
        }

    current: pd.Series
    current_n_users: int
    reference: Optional[pd.Series] = None
    reference_n_users: Optional[int]


class TrainStats(Metric[TrainStatsResult]):
    class Config:
        type_alias = "servequery:metric:TrainStats"

    """Calculates the number of times each item has been rated in the training set"""

    def __init__(self, options: AnyOptions = None) -> None:
        super().__init__(options=options)

    def calculate(self, data: InputData) -> TrainStatsResult:
        current_train_data = data.additional_data.get("current_train_data")
        reference_train_data = data.additional_data.get("reference_train_data")
        user_id = data.column_mapping.user_id
        item_id = data.column_mapping.item_id
        if current_train_data is None:
            raise ValueError(
                """current_train_data should be presented in additional_data with key "current_train_data":
                report.run(reference_data=reference_df, current_data=current_df, column_mapping=column_mapping,
                additional_data={"current_train_data": current_train_df})"""
            )

        curr_user_interacted = current_train_data.groupby(item_id)[user_id].nunique()
        current_n_users = current_train_data[user_id].nunique()
        ref_user_interacted: Optional[pd.Series] = None
        reference_n_users: Optional[int] = None
        if reference_train_data is not None:
            ref_user_interacted = reference_train_data.groupby(item_id)[user_id].nunique()
            reference_n_users = reference_train_data[user_id].nunique()
        return TrainStatsResult(
            current=curr_user_interacted,
            current_n_users=current_n_users,
            reference=ref_user_interacted,
            reference_n_users=reference_n_users,
        )


@default_renderer(wrap_type=TrainStats)
class TrainStatsRenderer(MetricRenderer):
    def render_html(self, obj: TrainStats) -> List[BaseWidgetInfo]:
        return []

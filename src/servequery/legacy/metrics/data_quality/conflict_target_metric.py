from typing import List
from typing import Optional

from servequery.legacy.base_metric import InputData
from servequery.legacy.base_metric import Metric
from servequery.legacy.base_metric import MetricResult
from servequery.legacy.core import IncludeTags
from servequery.legacy.model.widget import BaseWidgetInfo
from servequery.legacy.renderers.base_renderer import MetricRenderer
from servequery.legacy.renderers.base_renderer import default_renderer
from servequery.legacy.renderers.html_widgets import CounterData
from servequery.legacy.renderers.html_widgets import counter
from servequery.legacy.renderers.html_widgets import header_text
from servequery.legacy.utils.data_operations import process_columns


class ConflictTargetMetricResults(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:ConflictTargetMetricResults"
        field_tags = {
            "number_not_stable_target": {IncludeTags.Current},
            "share_not_stable_target": {IncludeTags.Current},
            "number_not_stable_target_ref": {IncludeTags.Reference},
            "share_not_stable_target_ref": {IncludeTags.Reference},
        }

    number_not_stable_target: int
    share_not_stable_target: float
    number_not_stable_target_ref: Optional[int] = None
    share_not_stable_target_ref: Optional[float] = None


class ConflictTargetMetric(Metric[ConflictTargetMetricResults]):
    class Config:
        type_alias = "servequery:metric:ConflictTargetMetric"

    def calculate(self, data: InputData) -> ConflictTargetMetricResults:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        if target_name is None:
            raise ValueError("The column 'target' should be presented")
        columns = dataset_columns.get_all_features_list()
        if len(columns) == 0:
            raise ValueError("Target conflict is not defined. No features provided")
        duplicates = data.current_data[data.current_data.duplicated(subset=columns, keep=False)]
        number_not_stable_target = duplicates.drop(
            data.current_data[data.current_data.duplicated(subset=columns + [target_name], keep=False)].index
        ).shape[0]
        share_not_stable_target = round(number_not_stable_target / data.current_data.shape[0], 3)
        # reference
        number_not_stable_target_ref = None
        share_not_stable_target_ref = None
        if data.reference_data is not None:
            duplicates_ref = data.reference_data[data.reference_data.duplicated(subset=columns, keep=False)]
            number_not_stable_target_ref = duplicates_ref.drop(
                data.reference_data[data.reference_data.duplicated(subset=columns + [target_name], keep=False)].index
            ).shape[0]
            share_not_stable_target_ref = round(number_not_stable_target_ref / data.reference_data.shape[0], 3)
        return ConflictTargetMetricResults(
            number_not_stable_target=number_not_stable_target,
            share_not_stable_target=share_not_stable_target,
            number_not_stable_target_ref=number_not_stable_target_ref,
            share_not_stable_target_ref=share_not_stable_target_ref,
        )


@default_renderer(wrap_type=ConflictTargetMetric)
class ConflictTargetMetricRenderer(MetricRenderer):
    def render_html(self, obj: ConflictTargetMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        counters = [
            CounterData(
                "number of conflicts (current)",
                self._get_string(
                    metric_result.number_not_stable_target,
                    metric_result.share_not_stable_target,
                ),
            )
        ]
        if (
            metric_result.number_not_stable_target_ref is not None
            and metric_result.share_not_stable_target_ref is not None
        ):
            counters.append(
                CounterData(
                    "number of conflicts (reference)",
                    self._get_string(
                        metric_result.number_not_stable_target_ref,
                        metric_result.share_not_stable_target_ref,
                    ),
                )
            )
        result = [
            header_text(label="Conflicts in Target"),
            counter(counters=counters),
        ]
        return result

    @staticmethod
    def _get_string(number: int, ratio: float) -> str:
        return f"{number} ({ratio * 100}%)"

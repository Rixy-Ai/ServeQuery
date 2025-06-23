from typing import List
from typing import Optional
from typing import Union

import numpy as np

from servequery.legacy.base_metric import ColumnName
from servequery.legacy.base_metric import InputData
from servequery.legacy.base_metric import Metric
from servequery.legacy.base_metric import MetricResult
from servequery.legacy.core import ColumnType
from servequery.legacy.core import IncludeTags
from servequery.legacy.metric_results import Distribution
from servequery.legacy.metric_results import HistogramData
from servequery.legacy.model.widget import BaseWidgetInfo
from servequery.legacy.options.base import AnyOptions
from servequery.legacy.renderers.base_renderer import MetricRenderer
from servequery.legacy.renderers.base_renderer import default_renderer
from servequery.legacy.renderers.html_widgets import WidgetSize
from servequery.legacy.renderers.html_widgets import header_text
from servequery.legacy.renderers.html_widgets import plotly_figure
from servequery.legacy.utils.visualizations import get_distribution_for_column
from servequery.legacy.utils.visualizations import plot_distr_with_perc_button


class ColumnDistributionMetricResult(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:ColumnDistributionMetricResult"
        field_tags = {
            "current": {IncludeTags.Current},
            "reference": {IncludeTags.Reference},
            "column_name": {IncludeTags.Parameter},
        }

    column_name: str
    current: Distribution
    reference: Optional[Distribution] = None


class ColumnDistributionMetric(Metric[ColumnDistributionMetricResult]):
    class Config:
        type_alias = "servequery:metric:ColumnDistributionMetric"

    """Calculates distribution for the column"""

    column_name: ColumnName

    def __init__(self, column_name: Union[str, ColumnName], options: AnyOptions = None) -> None:
        self.column_name = ColumnName.from_any(column_name)
        super().__init__(options=options)

    def calculate(self, data: InputData) -> ColumnDistributionMetricResult:
        if not data.has_column(self.column_name):
            raise ValueError(f"Column '{self.column_name.display_name}' was not found in data.")

        if not self.column_name.is_main_dataset():
            column_type = ColumnType.Numerical
        else:
            column_type = data.data_definition.get_column(self.column_name.name).column_type
        current_column = data.get_current_column(self.column_name).replace([np.inf, -np.inf], np.nan)
        reference_column = data.get_reference_column(self.column_name)
        if reference_column is not None:
            reference_column = reference_column.replace([np.inf, -np.inf], np.nan)
        current, reference = get_distribution_for_column(
            column_type=column_type.value,
            current=current_column,
            reference=reference_column,
        )

        return ColumnDistributionMetricResult(
            column_name=self.column_name.display_name,
            current=current,
            reference=reference,
        )


@default_renderer(wrap_type=ColumnDistributionMetric)
class ColumnDistributionMetricRenderer(MetricRenderer):
    def render_html(self, obj: ColumnDistributionMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        distr_fig = plot_distr_with_perc_button(
            hist_curr=HistogramData.from_distribution(metric_result.current),
            hist_ref=HistogramData.from_distribution(metric_result.reference),
            xaxis_name="",
            yaxis_name="Count",
            yaxis_name_perc="Percent",
            same_color=False,
            color_options=self.color_options,
            subplots=False,
            to_json=False,
        )

        result = [
            header_text(label=f"Distribution for column '{metric_result.column_name}'."),
            plotly_figure(title="", figure=distr_fig, size=WidgetSize.FULL),
        ]
        return result

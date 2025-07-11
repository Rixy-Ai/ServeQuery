from itertools import combinations
from typing import Dict
from typing import List
from typing import Optional

import numpy as np
import pandas as pd

from servequery.legacy.base_metric import InputData
from servequery.legacy.base_metric import Metric
from servequery.legacy.base_metric import MetricResult
from servequery.legacy.calculations.recommender_systems import get_prediciton_name
from servequery.legacy.core import IncludeTags
from servequery.legacy.metric_results import Distribution
from servequery.legacy.metric_results import HistogramData
from servequery.legacy.metrics.recsys.pairwise_distance import PairwiseDistance
from servequery.legacy.model.widget import BaseWidgetInfo
from servequery.legacy.options.base import AnyOptions
from servequery.legacy.pipeline.column_mapping import RecomType
from servequery.legacy.renderers.base_renderer import MetricRenderer
from servequery.legacy.renderers.base_renderer import default_renderer
from servequery.legacy.renderers.html_widgets import CounterData
from servequery.legacy.renderers.html_widgets import counter
from servequery.legacy.renderers.html_widgets import header_text
from servequery.legacy.renderers.html_widgets import plotly_figure
from servequery.legacy.utils.visualizations import get_distribution_for_column
from servequery.legacy.utils.visualizations import plot_distr_with_perc_button


class DiversityMetricResult(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:DiversityMetricResult"
        field_tags = {
            "k": {IncludeTags.Parameter},
            "current_value": {IncludeTags.Current},
            "current_distr": {IncludeTags.Current},
            "reference_value": {IncludeTags.Reference},
            "reference_distr": {IncludeTags.Reference},
        }

    k: int
    current_value: float
    current_distr: Distribution
    reference_value: Optional[float] = None
    reference_distr: Optional[Distribution] = None


class DiversityMetric(Metric[DiversityMetricResult]):
    class Config:
        type_alias = "servequery:metric:DiversityMetric"

    """Intra list diversity"""

    _pairwise_distance: PairwiseDistance
    k: int
    item_features: List[str]

    def __init__(self, k: int, item_features: List[str], options: AnyOptions = None) -> None:
        self.k = k
        self.item_features = item_features
        self._pairwise_distance = PairwiseDistance(k=k, item_features=item_features)
        super().__init__(options=options)

    def get_ild(
        self,
        df: pd.DataFrame,
        k: int,
        recommendations_type: RecomType,
        user_id: str,
        item_id: str,
        predictions: str,
        dist_matrix: np.ndarray,
        name_dict: Dict,
    ):
        df = df.copy()
        if recommendations_type == RecomType.SCORE:
            df[predictions] = df.groupby(user_id)[predictions].transform("rank", ascending=False)
        ilds = []
        all_users = df[user_id].unique()
        for user in all_users:
            rec_list = df[(df[user_id] == user) & (df[predictions] <= k)][item_id]
            user_res = 0
            for i, j in combinations(rec_list, 2):
                user_res += dist_matrix[name_dict[i], name_dict[j]]
            ilds.append(user_res / len(rec_list))
        distr = pd.Series(ilds)
        value = np.mean(ilds)
        return distr, value

    def calculate(self, data: InputData) -> DiversityMetricResult:
        result = self._pairwise_distance.get_result()
        dist_matrix = result.dist_matrix
        name_dict = result.name_dict
        user_id = data.data_definition.get_user_id_column()
        item_id = data.data_definition.get_item_id_column()
        recommendations_type = data.column_mapping.recom_type
        if user_id is None or item_id is None or recommendations_type is None:
            raise ValueError("user_id and item_id and recommendations_type should be specified")
        prediction_name = get_prediciton_name(data)
        curr_distr_data, curr_value = self.get_ild(
            df=data.current_data,
            k=self.k,
            recommendations_type=recommendations_type,
            user_id=user_id.column_name,
            item_id=item_id.column_name,
            predictions=prediction_name,
            dist_matrix=dist_matrix,
            name_dict=name_dict,
        )

        ref_distr_data: Optional[pd.Series] = None
        ref_value: Optional[float] = None
        if data.reference_data is not None:
            ref_distr_data, ref_value = self.get_ild(
                df=data.reference_data,
                k=self.k,
                recommendations_type=recommendations_type,
                user_id=user_id.column_name,
                item_id=item_id.column_name,
                predictions=prediction_name,
                dist_matrix=dist_matrix,
                name_dict=name_dict,
            )
        curr_distr, ref_distr = get_distribution_for_column(
            column_type="num", current=curr_distr_data, reference=ref_distr_data
        )
        return DiversityMetricResult(
            k=self.k,
            current_value=curr_value,
            current_distr=curr_distr,
            reference_value=ref_value,
            reference_distr=ref_distr,
        )


@default_renderer(wrap_type=DiversityMetric)
class DiversityMetricRenderer(MetricRenderer):
    def render_html(self, obj: DiversityMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        counters = [CounterData.float(label="current", value=metric_result.current_value, precision=4)]
        if metric_result.reference_value is not None:
            counters.append(CounterData.float(label="reference", value=metric_result.reference_value, precision=4))

        distr_fig = plot_distr_with_perc_button(
            hist_curr=HistogramData.from_distribution(metric_result.current_distr),
            hist_ref=HistogramData.from_distribution(metric_result.reference_distr),
            xaxis_name="intra list diversity by user",
            yaxis_name="Count",
            yaxis_name_perc="Percent",
            same_color=False,
            color_options=self.color_options,
            subplots=False,
            to_json=False,
        )

        return [
            header_text(label=f"Diversity (top-{metric_result.k})"),
            counter(counters=counters),
            plotly_figure(title="", figure=distr_fig),
        ]

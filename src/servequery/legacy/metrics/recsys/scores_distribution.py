from typing import List
from typing import Optional
from typing import Tuple

import pandas as pd
from scipy.special import softmax
from scipy.stats import entropy

from servequery.legacy.base_metric import InputData
from servequery.legacy.base_metric import Metric
from servequery.legacy.base_metric import MetricResult
from servequery.legacy.calculations.recommender_systems import get_prediciton_name
from servequery.legacy.core import IncludeTags
from servequery.legacy.metric_results import Distribution
from servequery.legacy.metric_results import HistogramData
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
from servequery.legacy.utils.visualizations import plot_4_distr


class ScoreDistributionResult(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:ScoreDistributionResult"
        field_tags = {
            "k": {IncludeTags.Parameter},
            "current_top_k_distr": {IncludeTags.Current},
            "current_other_distr": {IncludeTags.Current},
            "current_entropy": {IncludeTags.Current},
            "reference_top_k_distr": {IncludeTags.Reference},
            "reference_other_distr": {IncludeTags.Reference},
            "reference_entropy": {IncludeTags.Reference},
        }

    k: int
    current_top_k_distr: Distribution
    current_other_distr: Optional[Distribution] = None
    reference_top_k_distr: Optional[Distribution] = None
    reference_other_distr: Optional[Distribution] = None
    current_entropy: float
    reference_entropy: Optional[float] = None


class ScoreDistribution(Metric[ScoreDistributionResult]):
    class Config:
        type_alias = "servequery:metric:ScoreDistribution"

    k: int

    def __init__(self, k: int, options: AnyOptions = None) -> None:
        self.k = k
        super().__init__(options=options)

    def get_distr(
        self,
        df: pd.DataFrame,
        user_id: Optional[str],
        prediction_name: str,
    ) -> Tuple[Distribution, Optional[Distribution], float]:
        df["rank"] = df.groupby(user_id)[prediction_name].transform("rank", ascending=False)
        top_k = df.loc[df["rank"] <= self.k, prediction_name]
        if self.k == df["rank"].max:
            other: Optional[pd.Series] = None
        else:
            other = df.loc[df["rank"] > self.k, prediction_name]
        top_k_distr, other_distr = get_distribution_for_column(column_type="num", current=top_k, reference=other)
        entropy_ = entropy(softmax(top_k))
        return top_k_distr, other_distr, entropy_

    def calculate(self, data: InputData) -> ScoreDistributionResult:
        if data.column_mapping.recom_type == RecomType.RANK:
            raise ValueError("ScoreDistribution metric is only defined when recommendations_type equals 'scores'.")
        prediction_name = get_prediciton_name(data)
        user_id = data.column_mapping.user_id
        curr = data.current_data.copy()
        current_top_k_distr, current_other_distr, curr_entropy = self.get_distr(curr, user_id, prediction_name)
        reference_top_k_distr: Optional[Distribution] = None
        reference_other_distr: Optional[Distribution] = None
        ref_entropy: Optional[float] = None
        if data.reference_data is not None:
            ref = data.reference_data.copy()
            reference_top_k_distr, reference_other_distr, ref_entropy = self.get_distr(ref, user_id, prediction_name)
        return ScoreDistributionResult(
            k=self.k,
            current_top_k_distr=current_top_k_distr,
            current_other_distr=current_other_distr,
            reference_top_k_distr=reference_top_k_distr,
            reference_other_distr=reference_other_distr,
            current_entropy=curr_entropy,
            reference_entropy=ref_entropy,
        )


@default_renderer(wrap_type=ScoreDistribution)
class ScoreDistributionRenderer(MetricRenderer):
    def render_html(self, obj: ScoreDistribution) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        distr_fig = plot_4_distr(
            curr_1=HistogramData.from_distribution(metric_result.current_top_k_distr),
            curr_2=HistogramData.from_distribution(metric_result.current_other_distr),
            ref_1=HistogramData.from_distribution(metric_result.reference_top_k_distr),
            ref_2=HistogramData.from_distribution(metric_result.reference_other_distr),
            name_1="top_k",
            name_2="other",
            xaxis_name="scores",
            color_2="secondary",
        )
        counters = [
            CounterData.float(label="current score entropy (top k)", value=metric_result.current_entropy, precision=4)
        ]
        if metric_result.reference_entropy is not None:
            counters.append(
                CounterData.float(
                    label="reference score entropy (top k)", value=metric_result.reference_entropy, precision=4
                )
            )

        return [
            header_text(label="Score Distribution"),
            counter(counters=counters),
            plotly_figure(title="", figure=distr_fig),
        ]

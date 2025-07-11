from typing import Dict
from typing import List
from typing import Optional

from servequery._pydantic_compat import BaseModel
from servequery.legacy.base_metric import InputData
from servequery.legacy.base_metric import MetricResult
from servequery.legacy.calculations.classification_performance import calculate_matrix
from servequery.legacy.core import IncludeTags
from servequery.legacy.metric_results import ConfusionMatrix
from servequery.legacy.metric_results import Label
from servequery.legacy.metrics.classification_performance.base_classification_metric import ThresholdClassificationMetric
from servequery.legacy.model.widget import BaseWidgetInfo
from servequery.legacy.options.base import AnyOptions
from servequery.legacy.pipeline.column_mapping import TargetNames
from servequery.legacy.renderers.base_renderer import MetricRenderer
from servequery.legacy.renderers.base_renderer import default_renderer
from servequery.legacy.renderers.html_widgets import header_text
from servequery.legacy.renderers.html_widgets import plotly_figure
from servequery.legacy.utils.visualizations import plot_conf_mtrx

DEFAULT_THRESHOLD = 0.5


class ClassificationConfusionMatrixResult(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:ClassificationConfusionMatrixResult"
        field_tags = {
            "current_matrix": {IncludeTags.Current},
            "reference_matrix": {IncludeTags.Reference},
            "target_names": {IncludeTags.Parameter},
        }
        smart_union = True

    current_matrix: ConfusionMatrix
    reference_matrix: Optional[ConfusionMatrix]
    target_names: Optional[TargetNames] = None


class ClassificationConfusionMatrixParameters(BaseModel):
    probas_threshold: Optional[float]
    k: Optional[int]

    def confusion_matric_metric(self):
        return ClassificationConfusionMatrix(probas_threshold=self.probas_threshold, k=self.k)


class ClassificationConfusionMatrix(
    ThresholdClassificationMetric[ClassificationConfusionMatrixResult], ClassificationConfusionMatrixParameters
):
    class Config:
        type_alias = "servequery:metric:ClassificationConfusionMatrix"

    def __init__(
        self,
        probas_threshold: Optional[float] = None,
        k: Optional[int] = None,
        options: AnyOptions = None,
    ):
        super().__init__(probas_threshold=probas_threshold, k=k, options=options)

    def calculate(self, data: InputData) -> ClassificationConfusionMatrixResult:
        current_target_data, current_pred = self.get_target_prediction_data(data.current_data, data.column_mapping)
        target_names = data.column_mapping.target_names
        current_results = calculate_matrix(
            current_target_data,
            current_pred.predictions,
            current_pred.labels,
        )

        reference_results = None
        if data.reference_data is not None:
            ref_target_data, ref_pred = self.get_target_prediction_data(data.reference_data, data.column_mapping)

            reference_results = calculate_matrix(
                ref_target_data,
                ref_pred.predictions,
                ref_pred.labels,
            )

        return ClassificationConfusionMatrixResult(
            current_matrix=current_results,
            reference_matrix=reference_results,
            target_names=target_names,
        )


@default_renderer(wrap_type=ClassificationConfusionMatrix)
class ClassificationConfusionMatrixRenderer(MetricRenderer):
    def render_html(self, obj: ClassificationConfusionMatrix) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        target_names: Optional[Dict[Label, str]]
        if isinstance(metric_result.target_names, list):
            target_names = {idx: str(item) for idx, item in enumerate(metric_result.target_names)}
        else:
            target_names = metric_result.target_names
        curr_matrix = metric_result.current_matrix
        ref_matrix = metric_result.reference_matrix
        if target_names is not None:
            curr_matrix.labels = [target_names[x] for x in curr_matrix.labels]
            if ref_matrix is not None:
                ref_matrix.labels = [target_names[x] for x in ref_matrix.labels]

        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        fig.for_each_xaxis(lambda axis: axis.update(title_text="Predicted Value"))
        fig.update_layout(yaxis_title="Actual Value")
        return [
            header_text(label="Confusion Matrix"),
            plotly_figure(figure=fig, title=""),
        ]

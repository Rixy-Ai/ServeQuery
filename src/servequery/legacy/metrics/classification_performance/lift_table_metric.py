from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union

import pandas as pd

from servequery._pydantic_compat import BaseModel
from servequery.legacy.base_metric import InputData
from servequery.legacy.base_metric import Metric
from servequery.legacy.base_metric import MetricResult
from servequery.legacy.calculations.classification_performance import calculate_lift_table
from servequery.legacy.calculations.classification_performance import get_prediction_data
from servequery.legacy.core import IncludeTags
from servequery.legacy.metric_results import Label
from servequery.legacy.metric_results import PredictionData
from servequery.legacy.model.widget import BaseWidgetInfo
from servequery.legacy.options.base import AnyOptions
from servequery.legacy.renderers.base_renderer import MetricRenderer
from servequery.legacy.renderers.base_renderer import default_renderer
from servequery.legacy.renderers.html_widgets import TabData
from servequery.legacy.renderers.html_widgets import WidgetSize
from servequery.legacy.renderers.html_widgets import table_data
from servequery.legacy.renderers.html_widgets import widget_tabs
from servequery.legacy.utils.data_operations import process_columns

if TYPE_CHECKING:
    from servequery._pydantic_compat import Model


class LabelModel(BaseModel):
    __root__: Union[int, str]

    def validate(cls: Type["Model"], value: Any):  # type: ignore[override, misc]
        try:
            return int(value)
        except TypeError:
            return value


LiftTable = Dict[Union[LabelModel, Label], List[List[Union[float, int]]]]


class ClassificationLiftTableResults(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:ClassificationLiftTableResults"
        pd_include = False
        field_tags = {
            "current_lift_table": {IncludeTags.Current},
            "reference_lift_table": {IncludeTags.Reference},
            "top": {IncludeTags.Parameter},
        }

    current_lift_table: Optional[LiftTable] = None
    reference_lift_table: Optional[LiftTable] = None
    top: Optional[int] = 10


class ClassificationLiftTable(Metric[ClassificationLiftTableResults]):
    class Config:
        type_alias = "servequery:metric:ClassificationLiftTable"

    """
    ServeQuery metric with inherited behaviour, provides data for lift analysis

    Parameters
    ----------
    top: Optional[dict] = 10
        Limit top percentiles for displaying in report

    """

    top: int

    def __init__(self, top: int = 10, options: AnyOptions = None) -> None:
        self.top = top
        super().__init__(options=options)

    def calculate(self, data: InputData) -> ClassificationLiftTableResults:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction
        if target_name is None or prediction_name is None:
            raise ValueError(("The columns 'target' and 'prediction' " "columns should be present"))
        curr_prediction = get_prediction_data(data.current_data, dataset_columns, data.column_mapping.pos_label)
        curr_lift_table = self.calculate_metrics(data.current_data[target_name], curr_prediction)
        ref_lift_table = None
        if data.reference_data is not None:
            ref_prediction = get_prediction_data(
                data.reference_data,
                dataset_columns,
                data.column_mapping.pos_label,
            )
            ref_lift_table = self.calculate_metrics(data.reference_data[target_name], ref_prediction)
        return ClassificationLiftTableResults(
            current_lift_table=curr_lift_table,
            reference_lift_table=ref_lift_table,
            top=self.top,
        )

    def calculate_metrics(self, target_data: pd.Series, prediction: PredictionData):
        labels = prediction.labels
        if prediction.prediction_probas is None:
            raise ValueError("Lift Table can be calculated only on " "binary probabilistic predictions")
        binaraized_target = (target_data.to_numpy().reshape(-1, 1) == labels).astype(int)
        lift_table = {}
        if len(labels) <= 2:
            binaraized_target = pd.DataFrame(binaraized_target[:, 0])
            binaraized_target.columns = ["target"]

            binded = list(
                zip(
                    binaraized_target["target"].tolist(),
                    prediction.prediction_probas.iloc[:, 0].tolist(),
                )
            )
            lift_table[int(prediction.prediction_probas.columns[0])] = calculate_lift_table(binded)
        else:
            binaraized_target = pd.DataFrame(binaraized_target)
            binaraized_target.columns = labels

            for label in labels:
                binded = list(
                    zip(
                        binaraized_target[label].tolist(),
                        prediction.prediction_probas[label],
                    )
                )
                lift_table[int(label)] = calculate_lift_table(binded)  # type: ignore[arg-type]
        return lift_table


@default_renderer(wrap_type=ClassificationLiftTable)
class ClassificationLiftTableRenderer(MetricRenderer):
    def render_html(self, obj: ClassificationLiftTable) -> List[BaseWidgetInfo]:
        reference_lift_table = obj.get_result().reference_lift_table
        current_lift_table = obj.get_result().current_lift_table
        top = obj.get_result().top
        columns = [
            "Top(%)",
            "Count",
            "Prob",
            "TP",
            "FP",
            "Precision",
            "Recall",
            "F1 score",
            "Lift",
            "Max lift",
            "Relative lift",
            "Percent",
        ]
        result = []
        size = WidgetSize.FULL
        if current_lift_table is not None:
            if len(current_lift_table.keys()) == 1:
                result.append(
                    table_data(
                        column_names=columns,
                        data=current_lift_table[list(current_lift_table.keys())[0]][:top],
                        title="Current: Lift Table",
                        size=size,
                    )
                )
            else:
                tab_data = []
                for label in current_lift_table.keys():
                    table = table_data(
                        column_names=columns,
                        data=current_lift_table[label],
                        title="",
                        size=size,
                    )
                    tab_data.append(TabData(str(label), table))
                result.append(widget_tabs(title="Current: Lift Table", tabs=tab_data))
        if reference_lift_table is not None:
            if len(reference_lift_table.keys()) == 1:
                result.append(
                    table_data(
                        column_names=columns,
                        data=reference_lift_table[list(reference_lift_table.keys())[0]][:top],
                        title="Reference: Lift Table",
                        size=size,
                    )
                )
            else:
                tab_data = []
                for label in reference_lift_table.keys():
                    table = table_data(
                        column_names=columns,
                        data=reference_lift_table[label],
                        title="",
                        size=size,
                    )
                    tab_data.append(TabData(str(label), table))
                result.append(widget_tabs(title="Reference: Lift Table", tabs=tab_data))
        return result

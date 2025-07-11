from typing import Dict
from typing import List
from typing import Optional

import pandas as pd

from servequery.legacy.base_metric import InputData
from servequery.legacy.base_metric import Metric
from servequery.legacy.base_metric import MetricResult
from servequery.legacy.base_metric import UsesRawDataMixin
from servequery.legacy.calculations.data_drift import ColumnDataDriftMetrics
from servequery.legacy.calculations.data_drift import get_dataset_drift
from servequery.legacy.calculations.data_drift import get_one_column_drift
from servequery.legacy.calculations.stattests import PossibleStatTestType
from servequery.legacy.core import ColumnType as ColumnType_data
from servequery.legacy.descriptors import OOV
from servequery.legacy.descriptors import NonLetterCharacterPercentage
from servequery.legacy.descriptors import TextLength
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeature
from servequery.legacy.metric_results import DatasetColumns
from servequery.legacy.metric_results import HistogramData
from servequery.legacy.metric_results import ScatterField
from servequery.legacy.model.widget import BaseWidgetInfo
from servequery.legacy.options.base import AnyOptions
from servequery.legacy.options.data_drift import DataDriftOptions
from servequery.legacy.pipeline.column_mapping import ColumnMapping
from servequery.legacy.renderers.base_renderer import MetricRenderer
from servequery.legacy.renderers.base_renderer import default_renderer
from servequery.legacy.renderers.html_widgets import ColumnDefinition
from servequery.legacy.renderers.html_widgets import ColumnType
from servequery.legacy.renderers.html_widgets import RichTableDataRow
from servequery.legacy.renderers.html_widgets import RowDetails
from servequery.legacy.renderers.html_widgets import header_text
from servequery.legacy.renderers.html_widgets import plotly_figure
from servequery.legacy.renderers.html_widgets import rich_table_data
from servequery.legacy.utils.data_operations import process_columns
from servequery.legacy.utils.data_operations import recognize_column_type_
from servequery.legacy.utils.data_preprocessing import DataDefinition
from servequery.legacy.utils.visualizations import plot_agg_line_data
from servequery.legacy.utils.visualizations import plot_distr_with_perc_button
from servequery.legacy.utils.visualizations import plot_scatter_for_data_drift


class TextDescriptorsDriftMetricResults(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:TextDescriptorsDriftMetricResults"

    number_of_columns: int
    number_of_drifted_columns: int
    share_of_drifted_columns: float
    dataset_drift: bool
    drift_by_columns: Dict[str, ColumnDataDriftMetrics]
    dataset_columns: DatasetColumns


class TextDescriptorsDriftMetric(UsesRawDataMixin, Metric[TextDescriptorsDriftMetricResults]):
    class Config:
        type_alias = "servequery:metric:TextDescriptorsDriftMetric"

    column_name: str
    stattest: Optional[PossibleStatTestType] = None
    stattest_threshold: Optional[float] = None
    descriptors: Dict[str, FeatureDescriptor]
    _drift_options: DataDriftOptions
    _generated_text_features: Dict[str, GeneratedFeature]

    def __init__(
        self,
        column_name: str,
        descriptors: Optional[Dict[str, FeatureDescriptor]] = None,
        stattest: Optional[PossibleStatTestType] = None,
        stattest_threshold: Optional[float] = None,
        options: AnyOptions = None,
    ):
        self.column_name = column_name

        if descriptors:
            self.descriptors = descriptors
        else:
            self.descriptors = {
                "Text Length": TextLength(),
                "Non Letter Character %": NonLetterCharacterPercentage(),
                "OOV %": OOV(),
            }
        super().__init__(stattest=stattest, stattest_threshold=stattest_threshold, options=options)
        self._generated_text_features = {}
        self._drift_options = DataDriftOptions(
            all_features_stattest=stattest, all_features_threshold=stattest_threshold
        )

    @property
    def generated_text_features(self):
        return self._generated_text_features

    def required_features(self, data_definition: DataDefinition):
        column_type = data_definition.get_column(self.column_name).column_type
        if column_type == ColumnType_data.Text:
            self._generated_text_features = {
                name: desc.feature(self.column_name) for name, desc in self.descriptors.items()
            }
            return list(self.generated_text_features.values())
        return []

    def get_parameters(self) -> tuple:
        return self.column_name, self._drift_options

    def calculate(self, data: InputData) -> TextDescriptorsDriftMetricResults:
        if data.reference_data is None:
            raise ValueError("Reference dataset should be present")
        if self.get_options().render_options.raw_data:
            agg_data = False
        else:
            agg_data = True
        curr_text_df = pd.concat(
            [data.get_current_column(x.as_column()) for x in list(self.generated_text_features.values())],
            axis=1,
        )
        curr_text_df.columns = pd.Index(list(self.generated_text_features.keys()))

        ref_text_df = pd.concat(
            [data.get_reference_column(x.as_column()) for x in list(self.generated_text_features.values())],
            axis=1,
        )
        ref_text_df.columns = pd.Index(list(self.generated_text_features.keys()))
        # text_dataset_columns = DatasetColumns(num_feature_names=curr_text_df.columns)
        text_dataset_columns = process_columns(
            ref_text_df,
            ColumnMapping(numerical_features=ref_text_df.columns.tolist()),
        )

        drift_by_columns: Dict[str, ColumnDataDriftMetrics] = {}
        for col in curr_text_df.columns:
            drift_by_columns[col] = get_one_column_drift(
                current_data=curr_text_df,
                reference_data=ref_text_df,
                column_name=col,
                column_type=recognize_column_type_(
                    dataset=pd.concat([ref_text_df, curr_text_df]),
                    column_name=col,
                    columns=text_dataset_columns,
                ),
                options=self._drift_options,
                dataset_columns=text_dataset_columns,
                agg_data=agg_data,
            )
        dataset_drift = get_dataset_drift(drift_by_columns, 0)

        return TextDescriptorsDriftMetricResults(
            number_of_columns=curr_text_df.shape[1],
            number_of_drifted_columns=dataset_drift.number_of_drifted_columns,
            share_of_drifted_columns=dataset_drift.dataset_drift_score,
            dataset_drift=dataset_drift.dataset_drift,
            drift_by_columns=drift_by_columns,
            dataset_columns=text_dataset_columns,
        )


@default_renderer(wrap_type=TextDescriptorsDriftMetric)
class TextDescriptorsDriftRenderer(MetricRenderer):
    def render_pandas(self, obj: TextDescriptorsDriftMetric) -> pd.DataFrame:
        result: TextDescriptorsDriftMetricResults = obj.get_result()
        return pd.concat([v.get_pandas() for v in result.drift_by_columns.values()])

    def _generate_column_params(
        self, column_name: str, data: ColumnDataDriftMetrics, agg_data: bool
    ) -> Optional[RichTableDataRow]:
        details = RowDetails()
        if (
            data.current.small_distribution is None
            or data.reference.small_distribution is None
            or data.current.distribution is None
        ):
            return None
        current_small_hist = data.current.small_distribution
        ref_small_hist = data.reference.small_distribution
        data_drift = "Detected" if data.drift_detected else "Not Detected"
        if data.column_type == "num" and data.scatter is not None:
            if not agg_data:
                if not isinstance(data.scatter, ScatterField):
                    raise ValueError(f"TypeMismatch, data.scatter({type(data.scatter)}) expected to be ScatterField ")
                scatter_fig = plot_scatter_for_data_drift(
                    curr_y=data.scatter.scatter[data.column_name].tolist(),
                    curr_x=data.scatter.scatter[data.scatter.x_name].tolist(),
                    y0=data.scatter.plot_shape["y0"],
                    y1=data.scatter.plot_shape["y1"],
                    y_name=data.column_name,
                    x_name=data.scatter.x_name,
                    color_options=self.color_options,
                )
            else:
                scatter_fig = plot_agg_line_data(
                    curr_data=data.scatter.scatter,
                    ref_data=None,
                    line=(data.scatter.plot_shape["y0"] + data.scatter.plot_shape["y1"]) / 2,
                    std=(data.scatter.plot_shape["y0"] - data.scatter.plot_shape["y1"]) / 2,
                    xaxis_name=data.scatter.x_name,
                    xaxis_name_ref=None,
                    yaxis_name=f"{data.column_name} (mean +/- std)",
                    color_options=self.color_options,
                    return_json=False,
                    line_name="reference (mean)",
                )
            scatter = plotly_figure(title="", figure=scatter_fig)
            details.with_part("DATA DRIFT", info=scatter)
            fig = plot_distr_with_perc_button(
                hist_curr=HistogramData.from_distribution(data.current.distribution),
                hist_ref=HistogramData.from_distribution(data.reference.distribution),
                xaxis_name="",
                yaxis_name="Count",
                yaxis_name_perc="Percent",
                same_color=False,
                color_options=self.color_options,
                subplots=False,
                to_json=False,
            )
            distribution = plotly_figure(title="", figure=fig)
            details.with_part("DATA DISTRIBUTION", info=distribution)
            return RichTableDataRow(
                details=details,
                fields={
                    "column_name": column_name,
                    "column_type": data.column_type,
                    "stattest_name": data.stattest_name,
                    "reference_distribution": {
                        "x": ref_small_hist.x,
                        "y": ref_small_hist.y,
                    },
                    "current_distribution": {
                        "x": current_small_hist.x,
                        "y": current_small_hist.y,
                    },
                    "data_drift": data_drift,
                    "drift_score": round(data.drift_score, 6),
                },
            )
        else:
            return None

    def render_html(self, obj: TextDescriptorsDriftMetric) -> List[BaseWidgetInfo]:
        results = obj.get_result()
        color_options = self.color_options

        # set params data
        params_data = []

        agg_data = not obj.get_options().render_options.raw_data

        # sort columns by drift score
        columns = sorted(
            results.drift_by_columns.keys(),
            key=lambda x: results.drift_by_columns[x].drift_score,
            reverse=True,
        )

        for column_name in columns:
            column_params = self._generate_column_params(column_name, results.drift_by_columns[column_name], agg_data)

            if column_params is not None:
                params_data.append(column_params)

        drift_percents = round(results.share_of_drifted_columns * 100, 3)

        return [
            header_text(label=f"Text Descriptors Drift for column '{obj.column_name}'"),
            rich_table_data(
                title=f"Drift is detected for {drift_percents}% of columns "
                f"({results.number_of_drifted_columns} out of {results.number_of_columns}).",
                columns=[
                    ColumnDefinition("Column", "column_name"),
                    ColumnDefinition("Type", "column_type"),
                    ColumnDefinition(
                        "Reference Distribution",
                        "reference_distribution",
                        ColumnType.HISTOGRAM,
                        options={
                            "xField": "x",
                            "yField": "y",
                            "color": color_options.primary_color,
                        },
                    ),
                    ColumnDefinition(
                        "Current Distribution",
                        "current_distribution",
                        ColumnType.HISTOGRAM,
                        options={
                            "xField": "x",
                            "yField": "y",
                            "color": color_options.primary_color,
                        },
                    ),
                    ColumnDefinition("Data Drift", "data_drift"),
                    ColumnDefinition("Stat Test", "stattest_name"),
                    ColumnDefinition("Drift Score", "drift_score"),
                ],
                data=params_data,
            ),
        ]

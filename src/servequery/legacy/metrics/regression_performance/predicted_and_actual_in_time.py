from typing import List
from typing import Optional
from typing import Union

import numpy as np

from servequery.legacy.base_metric import InputData
from servequery.legacy.base_metric import Metric
from servequery.legacy.base_metric import UsesRawDataMixin
from servequery.legacy.metric_results import ColumnAggScatterResult
from servequery.legacy.metric_results import ColumnScatter
from servequery.legacy.metric_results import ColumnScatterResult
from servequery.legacy.model.widget import BaseWidgetInfo
from servequery.legacy.options.base import AnyOptions
from servequery.legacy.renderers.base_renderer import MetricRenderer
from servequery.legacy.renderers.base_renderer import default_renderer
from servequery.legacy.renderers.html_widgets import header_text
from servequery.legacy.utils.data_operations import process_columns
from servequery.legacy.utils.visualizations import plot_agg_line_data
from servequery.legacy.utils.visualizations import plot_pred_actual_time
from servequery.legacy.utils.visualizations import prepare_df_for_time_index_plot


class RegressionPredictedVsActualPlot(UsesRawDataMixin, Metric[ColumnScatterResult]):
    class Config:
        type_alias = "servequery:metric:RegressionPredictedVsActualPlot"

    def __init__(self, options: AnyOptions = None):
        super().__init__(options=options)

    def calculate(self, data: InputData) -> ColumnScatterResult:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction
        datetime_column_name = dataset_columns.utility_columns.date
        curr_df = data.current_data.copy()
        ref_df = data.reference_data
        if target_name is None or prediction_name is None:
            raise ValueError("The columns 'target' and 'prediction' columns should be present")
        if not isinstance(prediction_name, str):
            raise ValueError("Expect one column for prediction. List of columns was provided.")
        curr_df = self._make_df_for_plot(curr_df, target_name, prediction_name, datetime_column_name)
        if ref_df is not None:
            ref_df = self._make_df_for_plot(ref_df.copy(), target_name, prediction_name, datetime_column_name)
        reference_scatter: Optional[Union[dict, ColumnScatter]] = None
        raw_data = self.get_options().render_options.raw_data
        if raw_data:
            current_scatter = {}
            current_scatter["Predicted"] = curr_df[prediction_name]
            current_scatter["Actual"] = curr_df[target_name]
            if datetime_column_name is not None:
                current_scatter["x"] = curr_df[datetime_column_name]
                x_name = "Timestamp"
            else:
                current_scatter["x"] = curr_df.index.to_series()
                x_name = "Index"
            if ref_df is not None:
                reference_scatter = {}
                reference_scatter["Predicted"] = ref_df[prediction_name]
                reference_scatter["Actual"] = ref_df[target_name]
                reference_scatter["x"] = (
                    ref_df[datetime_column_name] if datetime_column_name else ref_df.index.to_series()
                )
            return ColumnScatterResult(
                current=current_scatter,
                reference=reference_scatter,
                x_name=x_name,
            )
        agg_current_scatter = {}
        agg_reference_scatter = None
        plot_df, prefix = prepare_df_for_time_index_plot(curr_df, prediction_name, datetime_column_name)
        agg_current_scatter["Predicted"] = plot_df
        agg_current_scatter["Actual"], _ = prepare_df_for_time_index_plot(curr_df, target_name, datetime_column_name)
        x_name_ref: Optional[str] = None
        if ref_df is not None:
            agg_reference_scatter = {}
            plot_df, prefix_ref = prepare_df_for_time_index_plot(ref_df, prediction_name, datetime_column_name)
            agg_reference_scatter["Predicted"] = plot_df
            agg_reference_scatter["Actual"], _ = prepare_df_for_time_index_plot(
                ref_df,
                target_name,
                datetime_column_name,
            )
            if datetime_column_name is None:
                x_name_ref = "Index binned"
            else:
                x_name_ref = datetime_column_name + f" ({prefix_ref})"
        if datetime_column_name is None:
            x_name = "Index binned"
        else:
            x_name = datetime_column_name + f" ({prefix})"
        return ColumnAggScatterResult(
            current=agg_current_scatter,
            reference=reference_scatter,
            x_name=x_name,
            x_name_ref=x_name_ref,
        )

    def _make_df_for_plot(self, df, target_name: str, prediction_name: str, datetime_column_name: Optional[str]):
        result = df.replace([np.inf, -np.inf], np.nan)
        if datetime_column_name is not None:
            result.dropna(
                axis=0,
                how="any",
                inplace=True,
                subset=[target_name, prediction_name, datetime_column_name],
            )
            return result.sort_values(datetime_column_name)
        result.dropna(axis=0, how="any", inplace=True, subset=[target_name, prediction_name])
        return result.sort_index()


@default_renderer(wrap_type=RegressionPredictedVsActualPlot)
class RegressionPredictedVsActualPlotRenderer(MetricRenderer):
    def render_raw(self, current: ColumnScatter, reference: Optional[ColumnScatter], x_name: str):
        fig = plot_pred_actual_time(
            curr=current,
            ref=reference,
            x_name="x",
            xaxis_name=x_name,
            yaxis_name="Value",
            color_options=self.color_options,
        )
        return [
            header_text(label="Predicted vs Actual in Time"),
            BaseWidgetInfo(
                title="",
                size=2,
                type="big_graph",
                params={"data": fig["data"], "layout": fig["layout"]},
            ),
        ]

    def render_agg(
        self, current: ColumnScatter, reference: Optional[ColumnScatter], x_name: str, x_name_ref: Optional[str]
    ):
        fig = plot_agg_line_data(
            curr_data=current,
            ref_data=reference,
            line=0,
            std=None,
            xaxis_name=x_name,
            xaxis_name_ref=x_name_ref,
            yaxis_name="Value",
            color_options=self.color_options,
        )
        return [
            header_text(label="Predicted vs Actual in Time"),
            BaseWidgetInfo(
                title="",
                size=2,
                type="big_graph",
                params={"data": fig["data"], "layout": fig["layout"]},
            ),
        ]

    def render_html(self, obj: RegressionPredictedVsActualPlot) -> List[BaseWidgetInfo]:
        result = obj.get_result()
        current = result.current
        reference = result.reference
        if obj.get_options().render_options.raw_data:
            fig = plot_pred_actual_time(
                curr=current,
                ref=reference,
                x_name="x",
                xaxis_name=result.x_name,
                yaxis_name="Value",
                color_options=self.color_options,
            )
            return [
                header_text(label="Predicted vs Actual in Time"),
                BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig["data"], "layout": fig["layout"]},
                ),
            ]
        fig = plot_agg_line_data(
            curr_data=current,
            ref_data=reference,
            line=0,
            std=None,
            xaxis_name=result.x_name,
            xaxis_name_ref=result.x_name_ref,
            yaxis_name="Value",
            color_options=self.color_options,
        )
        return [
            header_text(label="Predicted vs Actual in Time"),
            BaseWidgetInfo(
                title="",
                size=2,
                type="big_graph",
                params={"data": fig["data"], "layout": fig["layout"]},
            ),
        ]

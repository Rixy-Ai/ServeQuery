from typing import Optional

import pandas as pd

from servequery.legacy.calculation_engine.engine import metric_implementation
from servequery.legacy.metrics.data_drift.feature_importance import SAMPLE_SIZE
from servequery.legacy.metrics.data_drift.feature_importance import FeatureImportanceMetric
from servequery.legacy.metrics.data_drift.feature_importance import FeatureImportanceMetricResult
from servequery.legacy.metrics.data_drift.feature_importance import get_feature_importance_from_samples
from servequery.legacy.spark.engine import SparkInputData
from servequery.legacy.spark.engine import SparkMetricImplementation


@metric_implementation(FeatureImportanceMetric)
class SparkFeatureImportanceMetric(SparkMetricImplementation[FeatureImportanceMetric]):
    def calculate(self, context, data: SparkInputData) -> FeatureImportanceMetricResult:
        if data.additional_data.get("current_feature_importance") is not None:
            return FeatureImportanceMetricResult(
                current=data.additional_data.get("current_feature_importance"),
                reference=data.additional_data.get("reference_feature_importance"),
            )

        cur_count = data.current_data.count()
        curr_sampled_data: pd.DataFrame = (
            data.current_data.toPandas()
            if cur_count < SAMPLE_SIZE
            else data.current_data.sample(cur_count / SAMPLE_SIZE, seed=0).toPandas()
        )
        ref_sampled_data: Optional[pd.DataFrame] = None
        if data.reference_data is not None:
            ref_count = data.reference_data.count()
            ref_sampled_data = (
                data.reference_data.toPandas()
                if ref_count < SAMPLE_SIZE
                else data.reference_data.sample(ref_count / SAMPLE_SIZE, seed=0).toPandas()
            )

        return get_feature_importance_from_samples(data.data_definition, curr_sampled_data, ref_sampled_data)

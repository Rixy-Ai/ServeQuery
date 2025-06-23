# ruff: noqa: E501
# fmt: off
from servequery.legacy.metric_preset.metric_preset import MetricPreset
from servequery.pydantic_utils import register_type_alias

register_type_alias(MetricPreset, "servequery.legacy.metric_preset.classification_performance.ClassificationPreset", "servequery:metric_preset:ClassificationPreset")
register_type_alias(MetricPreset, "servequery.legacy.metric_preset.data_drift.DataDriftPreset", "servequery:metric_preset:DataDriftPreset")
register_type_alias(MetricPreset, "servequery.legacy.metric_preset.data_quality.DataQualityPreset", "servequery:metric_preset:DataQualityPreset")
register_type_alias(MetricPreset, "servequery.legacy.metric_preset.recsys.RecsysPreset", "servequery:metric_preset:RecsysPreset")
register_type_alias(MetricPreset, "servequery.legacy.metric_preset.regression_performance.RegressionPreset", "servequery:metric_preset:RegressionPreset")
register_type_alias(MetricPreset, "servequery.legacy.metric_preset.target_drift.TargetDriftPreset", "servequery:metric_preset:TargetDriftPreset")
register_type_alias(MetricPreset, "servequery.legacy.metric_preset.text_evals.TextEvals", "servequery:metric_preset:TextEvals")

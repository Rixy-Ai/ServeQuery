# ruff: noqa: E501
# fmt: off
from servequery.core.container import MetricContainer
from servequery.pydantic_utils import register_type_alias

register_type_alias(MetricContainer, "servequery.core.container.ColumnMetricContainer", "servequery:metric_container:ColumnMetricContainer")
register_type_alias(MetricContainer, "servequery.generators.column.ColumnMetricGenerator", "servequery:metric_container:ColumnMetricGenerator")
register_type_alias(MetricContainer, "servequery.metrics.group_by.GroupBy", "servequery:metric_container:GroupBy")
register_type_alias(MetricContainer, "servequery.presets.classification.ClassificationDummyQuality", "servequery:metric_container:ClassificationDummyQuality")
register_type_alias(MetricContainer, "servequery.presets.classification.ClassificationPreset", "servequery:metric_container:ClassificationPreset")
register_type_alias(MetricContainer, "servequery.presets.classification.ClassificationQuality", "servequery:metric_container:ClassificationQuality")
register_type_alias(MetricContainer, "servequery.presets.classification.ClassificationQualityByLabel", "servequery:metric_container:ClassificationQualityByLabel")
register_type_alias(MetricContainer, "servequery.presets.dataset_stats.DataSummaryPreset", "servequery:metric_container:DataSummaryPreset")
register_type_alias(MetricContainer, "servequery.presets.dataset_stats.DatasetStats", "servequery:metric_container:DatasetStats")
register_type_alias(MetricContainer, "servequery.presets.dataset_stats.TextEvals", "servequery:metric_container:TextEvals")
register_type_alias(MetricContainer, "servequery.presets.dataset_stats.ValueStats", "servequery:metric_container:ValueStats")
register_type_alias(MetricContainer, "servequery.presets.drift.DataDriftPreset", "servequery:metric_container:DataDriftPreset")
register_type_alias(MetricContainer, "servequery.presets.regression.RegressionDummyQuality", "servequery:metric_container:RegressionDummyQuality")
register_type_alias(MetricContainer, "servequery.presets.regression.RegressionPreset", "servequery:metric_container:RegressionPreset")
register_type_alias(MetricContainer, "servequery.presets.regression.RegressionQuality", "servequery:metric_container:RegressionQuality")
register_type_alias(MetricContainer, "servequery.metrics.row_test_summary.RowTestSummary", "servequery:metric_container:RowTestSummary")

# ruff: noqa: E501
# fmt: off
from servequery.core.metric_types import MetricResult
from servequery.pydantic_utils import register_type_alias

register_type_alias(MetricResult, "servequery.core.metric_types.ByLabelCountValue", "servequery:metric_result_v2:ByLabelCountValue")
register_type_alias(MetricResult, "servequery.core.metric_types.ByLabelValue", "servequery:metric_result_v2:ByLabelValue")
register_type_alias(MetricResult, "servequery.core.metric_types.CountValue", "servequery:metric_result_v2:CountValue")
register_type_alias(MetricResult, "servequery.core.metric_types.MeanStdValue", "servequery:metric_result_v2:MeanStdValue")
register_type_alias(MetricResult, "servequery.core.metric_types.SingleValue", "servequery:metric_result_v2:SingleValue")

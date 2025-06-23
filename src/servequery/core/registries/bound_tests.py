# ruff: noqa: E501
# fmt: off
from servequery.core.metric_types import BoundTest
from servequery.pydantic_utils import register_type_alias

register_type_alias(BoundTest, "servequery.core.metric_types.ByLabelBoundTest", "servequery:bound_test:ByLabelBoundTest")
register_type_alias(BoundTest, "servequery.core.metric_types.ByLabelCountBoundTest", "servequery:bound_test:ByLabelCountBoundTest")
register_type_alias(BoundTest, "servequery.core.metric_types.CountBoundTest", "servequery:bound_test:CountBoundTest")
register_type_alias(BoundTest, "servequery.core.metric_types.MeanStdBoundTest", "servequery:bound_test:MeanStdBoundTest")
register_type_alias(BoundTest, "servequery.core.metric_types.SingleValueBoundTest", "servequery:bound_test:SingleValueBoundTest")
register_type_alias(BoundTest, "servequery.metrics.column_statistics.ValueDriftBoundTest", "servequery:bound_test:ValueDriftBoundTest")

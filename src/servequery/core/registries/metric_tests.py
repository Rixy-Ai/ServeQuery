# ruff: noqa: E501
# fmt: off
from servequery.core.metric_types import MetricTest
from servequery.pydantic_utils import register_type_alias

register_type_alias(MetricTest, "servequery.metrics.column_statistics.ValueDriftTest", "servequery:test_v2:ValueDriftTest")
register_type_alias(MetricTest, "servequery.tests.categorical_tests.IsInMetricTest", "servequery:test_v2:IsInMetricTest")
register_type_alias(MetricTest, "servequery.tests.categorical_tests.NotInMetricTest", "servequery:test_v2:NotInMetricTest")
register_type_alias(MetricTest, "servequery.tests.numerical_tests.ComparisonTest", "servequery:test_v2:ComparisonTest")
register_type_alias(MetricTest, "servequery.tests.numerical_tests.EqualMetricTest", "servequery:test_v2:EqualMetricTest")
register_type_alias(MetricTest, "servequery.tests.numerical_tests.EqualMetricTestBase", "servequery:test_v2:EqualMetricTestBase")
register_type_alias(MetricTest, "servequery.tests.numerical_tests.GreaterOrEqualMetricTest", "servequery:test_v2:GreaterOrEqualMetricTest")
register_type_alias(MetricTest, "servequery.tests.numerical_tests.GreaterThanMetricTest", "servequery:test_v2:GreaterThanMetricTest")
register_type_alias(MetricTest, "servequery.tests.numerical_tests.LessOrEqualMetricTest", "servequery:test_v2:LessOrEqualMetricTest")
register_type_alias(MetricTest, "servequery.tests.numerical_tests.LessThanMetricTest", "servequery:test_v2:LessThanMetricTest")
register_type_alias(MetricTest, "servequery.tests.numerical_tests.NotEqualMetricTest", "servequery:test_v2:NotEqualMetricTest")

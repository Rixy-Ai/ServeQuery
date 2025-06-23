from typing import List
from typing import Union

from servequery.core.metric_types import MetricCalculationBase
from servequery.core.metric_types import MetricTest
from servequery.core.metric_types import MetricTestResult
from servequery.core.metric_types import SingleValue
from servequery.core.metric_types import SingleValueTest
from servequery.core.report import Context
from servequery.legacy.tests.base_test import TestStatus
from servequery.legacy.utils.types import ApproxValue

InValueType = Union[int, str, float, ApproxValue]


class IsInMetricTest(MetricTest):
    class Config:
        smart_union = True

    values: List[InValueType]

    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue) -> MetricTestResult:
            check_value = value.value in self.values
            return MetricTestResult(
                id="is_in",
                name=f"{metric.display_name()}: Value in list [{', '.join(str(x) for x in self.values)}]",
                description=f"Actual value: {value.value}",
                status=TestStatus.SUCCESS if check_value else TestStatus.FAIL,
                metric_config=metric.to_metric_config(),
                test_config=self.dict(),
            )

        return func


class NotInMetricTest(MetricTest):
    class Config:
        smart_union = True

    values: List[InValueType]

    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue) -> MetricTestResult:
            check_value = value.value not in self.values
            return MetricTestResult(
                id="not_in",
                name=f"{metric.display_name()}: Value not in list [{', '.join(str(x) for x in self.values)}]",
                description=f"Actual value: {value.value}",
                status=TestStatus.SUCCESS if check_value else TestStatus.FAIL,
                metric_config=metric.to_metric_config(),
                test_config=self.dict(),
            )

        return func

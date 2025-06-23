from typing import Any
from typing import List
from typing import Optional
from typing import Union
from typing import overload

from servequery.core.datasets import DescriptorTest
from servequery.core.metric_types import MetricTest
from servequery.core.tests import FactoryGenericTest
from servequery.core.tests import GenericTest
from servequery.tests.categorical_tests import InValueType
from servequery.tests.categorical_tests import IsInMetricTest
from servequery.tests.categorical_tests import NotInMetricTest
from servequery.tests.descriptors import EqualsColumnCondition
from servequery.tests.descriptors import GreaterColumnCondition
from servequery.tests.descriptors import GreaterEqualColumnCondition
from servequery.tests.descriptors import IsInColumnCondition
from servequery.tests.descriptors import IsNotInColumnCondition
from servequery.tests.descriptors import LessColumnCondition
from servequery.tests.descriptors import LessEqualColumnCondition
from servequery.tests.descriptors import NotEqualsColumnCondition
from servequery.tests.numerical_tests import EqualMetricTest
from servequery.tests.numerical_tests import GreaterOrEqualMetricTest
from servequery.tests.numerical_tests import GreaterThanMetricTest
from servequery.tests.numerical_tests import LessOrEqualMetricTest
from servequery.tests.numerical_tests import LessThanMetricTest
from servequery.tests.numerical_tests import NotEqualMetricTest
from servequery.tests.numerical_tests import ThresholdType

AnyTest = Union[GenericTest, MetricTest, DescriptorTest]


@overload
def eq(expected: Any) -> GenericTest: ...


@overload
def eq(expected: ThresholdType, *, is_critical: bool = True) -> MetricTest: ...


@overload
def eq(expected: Any, *, column: Optional[str] = None, alias: Optional[str] = None) -> DescriptorTest: ...


def eq(
    expected: ThresholdType, *, is_critical: bool = True, column: Optional[str] = None, alias: Optional[str] = None
) -> AnyTest:
    return FactoryGenericTest(
        lambda: EqualMetricTest(expected=expected, is_critical=is_critical),
        lambda: DescriptorTest(condition=EqualsColumnCondition(expected=expected), column=column, alias=alias),
    )


@overload
def not_eq(expected: Any) -> GenericTest: ...


@overload
def not_eq(expected: ThresholdType, *, is_critical: bool = True) -> MetricTest: ...


@overload
def not_eq(expected: Any, *, column: Optional[str] = None, alias: Optional[str] = None) -> DescriptorTest: ...


def not_eq(
    expected: ThresholdType, *, is_critical: bool = True, column: Optional[str] = None, alias: Optional[str] = None
) -> AnyTest:
    return FactoryGenericTest(
        lambda: NotEqualMetricTest(expected=expected, is_critical=is_critical),
        lambda: DescriptorTest(condition=NotEqualsColumnCondition(expected=expected), column=column, alias=alias),
    )


@overload
def lt(threshold: ThresholdType) -> GenericTest: ...


@overload
def lt(threshold: ThresholdType, *, is_critical: bool = True) -> MetricTest: ...


@overload
def lt(threshold: ThresholdType, *, column: Optional[str] = None, alias: Optional[str] = None) -> DescriptorTest: ...


def lt(
    threshold: ThresholdType, *, is_critical: bool = True, column: Optional[str] = None, alias: Optional[str] = None
) -> AnyTest:
    return FactoryGenericTest(
        lambda: LessThanMetricTest(threshold=threshold, is_critical=is_critical),
        lambda: DescriptorTest(condition=LessColumnCondition(threshold=threshold), column=column, alias=alias),
    )


@overload
def gt(threshold: ThresholdType) -> GenericTest: ...


@overload
def gt(threshold: ThresholdType, *, is_critical: bool = True) -> MetricTest: ...


@overload
def gt(threshold: ThresholdType, *, column: Optional[str] = None, alias: Optional[str] = None) -> DescriptorTest: ...


def gt(
    threshold: ThresholdType, *, is_critical: bool = True, column: Optional[str] = None, alias: Optional[str] = None
) -> AnyTest:
    return FactoryGenericTest(
        lambda: GreaterThanMetricTest(threshold=threshold, is_critical=is_critical),
        lambda: DescriptorTest(condition=GreaterColumnCondition(threshold=threshold), column=column, alias=alias),
    )


@overload
def gte(threshold: ThresholdType) -> GenericTest: ...


@overload
def gte(threshold: ThresholdType, *, is_critical: bool = True) -> MetricTest: ...


@overload
def gte(threshold: ThresholdType, *, column: Optional[str] = None, alias: Optional[str] = None) -> DescriptorTest: ...


def gte(
    threshold: ThresholdType, *, is_critical: bool = True, column: Optional[str] = None, alias: Optional[str] = None
) -> AnyTest:
    return FactoryGenericTest(
        lambda: GreaterOrEqualMetricTest(threshold=threshold, is_critical=is_critical, alias=alias),
        lambda: DescriptorTest(condition=GreaterEqualColumnCondition(threshold=threshold), column=column, alias=alias),
    )


@overload
def lte(threshold: ThresholdType) -> GenericTest: ...


@overload
def lte(threshold: ThresholdType, *, is_critical: bool = True) -> MetricTest: ...


@overload
def lte(threshold: ThresholdType, *, column: Optional[str] = None, alias: Optional[str] = None) -> DescriptorTest: ...


def lte(
    threshold: ThresholdType, *, is_critical: bool = True, column: Optional[str] = None, alias: Optional[str] = None
) -> AnyTest:
    return FactoryGenericTest(
        lambda: LessOrEqualMetricTest(threshold=threshold, is_critical=is_critical),
        lambda: DescriptorTest(condition=LessEqualColumnCondition(threshold=threshold), column=column, alias=alias),
    )


@overload
def is_in(values: List[InValueType]) -> GenericTest: ...


@overload
def is_in(values: List[InValueType], *, is_critical: bool = True) -> MetricTest: ...


@overload
def is_in(
    values: List[InValueType], *, column: Optional[str] = None, alias: Optional[str] = None
) -> DescriptorTest: ...


def is_in(
    values: List[InValueType],
    *,
    is_critical: bool = True,
    column: Optional[str] = None,
    alias: Optional[str] = None,
) -> AnyTest:
    return FactoryGenericTest(
        lambda: IsInMetricTest(values=values, is_critical=is_critical),
        lambda: DescriptorTest(condition=IsInColumnCondition(values=set(values)), column=column, alias=alias),
    )


@overload
def not_in(values: List[InValueType]) -> GenericTest: ...


@overload
def not_in(values: List[InValueType], *, is_critical: bool = True) -> MetricTest: ...


@overload
def not_in(
    values: List[InValueType], *, column: Optional[str] = None, alias: Optional[str] = None
) -> DescriptorTest: ...


def not_in(
    values: List[InValueType],
    *,
    is_critical: bool = True,
    column: Optional[str] = None,
    alias: Optional[str] = None,
) -> AnyTest:
    return FactoryGenericTest(
        lambda: NotInMetricTest(values=values, is_critical=is_critical),
        lambda: DescriptorTest(condition=IsNotInColumnCondition(values=set(values)), column=column, alias=alias),
    )

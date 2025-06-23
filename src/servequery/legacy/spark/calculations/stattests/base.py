import dataclasses
from typing import Optional
from typing import Union

from servequery.legacy.calculations import stattests
from servequery.legacy.calculations.stattests.registry import PossibleStatTestType
from servequery.legacy.calculations.stattests.registry import StatTest
from servequery.legacy.calculations.stattests.registry import StatTestData
from servequery.legacy.calculations.stattests.registry import StatTestFuncReturns
from servequery.legacy.calculations.stattests.registry import StatTestImpl
from servequery.legacy.calculations.stattests.registry import add_stattest_impl
from servequery.legacy.calculations.stattests.registry import get_registered_stattest
from servequery.legacy.core import ColumnType
from servequery.legacy.spark import SparkEngine
from servequery.legacy.spark.base import SparkSeries


@dataclasses.dataclass
class SpartStatTestData(StatTestData):
    reference_data: SparkSeries
    current_data: SparkSeries
    column_name: str


class SparkStatTestImpl(StatTestImpl[SpartStatTestData, SparkEngine]):
    data_type = SpartStatTestData
    base_stat_test: StatTest

    def __call__(self, data: SpartStatTestData, feature_type: ColumnType, threshold: float) -> StatTestFuncReturns:
        raise NotImplementedError

    def __init_subclass__(cls):
        if hasattr(cls, "base_stat_test"):
            add_stattest_impl(cls.base_stat_test, SparkEngine, cls())


def get_stattest(
    reference_data: SparkSeries,
    current_data: SparkSeries,
    feature_type: Union[ColumnType, str],
    stattest_func: Optional[PossibleStatTestType],
) -> StatTest:
    if isinstance(feature_type, str):
        feature_type = ColumnType(feature_type)
    if stattest_func is None:
        return _get_default_stattest(reference_data, current_data, feature_type)
    return get_registered_stattest(stattest_func, feature_type, engine=SparkEngine)


def _get_default_stattest(
    reference_data: SparkSeries,
    current_data: SparkSeries,
    feature_type: ColumnType,
) -> StatTest:
    # n_values = pd.concat([reference_data, current_data]).nunique()
    ref_size = reference_data.count()
    if feature_type == ColumnType.Text:
        raise NotImplementedError("Text stattest are not implemented for Spark yet")
        # if ref_size > 1000:
        #     return stattests.abs_text_content_drift_stat_test
        # return stattests.perc_text_content_drift_stat_test
    if ref_size <= 1000:
        if feature_type == ColumnType.Numerical:
            return stattests.chi_stat_test
            # if n_values <= 5:
            #     return stattests.chi_stat_test if n_values > 2 else stattests.z_stat_test
            # elif n_values > 5:
            #     return stattests.ks_stat_test
        elif feature_type == ColumnType.Categorical:
            return stattests.chi_stat_test
            # return stattests.chi_stat_test if n_values > 2 else stattests.z_stat_test
    elif ref_size > 1000:
        if feature_type == ColumnType.Numerical:
            return stattests.wasserstein_stat_test
            # if n_values <= 5:
            #     return stattests.jensenshannon_stat_test
            # elif n_values > 5:
            #     return stattests.wasserstein_stat_test
        elif feature_type == ColumnType.Categorical:
            return stattests.jensenshannon_stat_test
    raise ValueError(f"Unexpected feature_type {feature_type}")

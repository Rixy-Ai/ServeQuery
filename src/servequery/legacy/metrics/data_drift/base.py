import abc
from typing import Dict
from typing import Generic
from typing import Optional
from typing import TypeVar

from servequery.legacy.base_metric import Metric
from servequery.legacy.base_metric import MetricResult
from servequery.legacy.calculations.stattests import PossibleStatTestType
from servequery.legacy.options.data_drift import DataDriftOptions
from servequery.pydantic_utils import FrozenBaseModel

T = TypeVar("T", bound=MetricResult)


class WithDriftOptionsFields(FrozenBaseModel):
    # todo: fields here are not consistent with DriftOptions, so no common base model
    stattest: Optional[PossibleStatTestType] = None
    cat_stattest: Optional[PossibleStatTestType] = None
    num_stattest: Optional[PossibleStatTestType] = None
    text_stattest: Optional[PossibleStatTestType] = None
    per_column_stattest: Optional[Dict[str, PossibleStatTestType]] = None

    stattest_threshold: Optional[float] = None
    cat_stattest_threshold: Optional[float] = None
    num_stattest_threshold: Optional[float] = None
    text_stattest_threshold: Optional[float] = None
    per_column_stattest_threshold: Optional[Dict[str, float]] = None


class WithDriftOptions(WithDriftOptionsFields, Metric[T], Generic[T], abc.ABC):
    _drift_options: DataDriftOptions

    @property
    def drift_options(self):
        return self._drift_options

from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union
from typing import overload

import numpy as np
import pandas as pd
from typing_extensions import Literal

from servequery._pydantic_compat import parse_obj_as
from servequery._pydantic_compat import validator
from servequery.legacy.base_metric import MetricResult
from servequery.legacy.core import IncludeTags
from servequery.legacy.core import Label
from servequery.legacy.core import pydantic_type_validator
from servequery.legacy.pipeline.column_mapping import TargetNames

try:
    List.__getitem__.__closure__[0].cell_contents.cache_clear()  # type: ignore
except AttributeError:  # since python 3.12
    from typing import _caches  # type: ignore[attr-defined]

    _caches[List.__getitem__.__wrapped__].cache_clear()  # type: ignore[attr-defined]

LabelList = List[Label]


class _LabelKeyType(int):
    pass


LabelKey = Union[_LabelKeyType, Label]  # type: ignore[valid-type]


@pydantic_type_validator(_LabelKeyType)
def label_key_valudator(value):
    try:
        return int(value)
    except ValueError:
        return value


ScatterData = Union[pd.Series]
ContourData = Tuple[np.ndarray, List[float], List[float]]
ColumnScatter = Dict[LabelKey, ScatterData]

ScatterAggData = Union[pd.DataFrame]
ColumnAggScatter = Dict[LabelKey, ScatterAggData]


class _ColumnScatterOrAggType:
    pass


ColumnScatterOrAgg = Union[_ColumnScatterOrAggType, ColumnScatter, ColumnAggScatter]  # type: ignore[valid-type]


@pydantic_type_validator(_ColumnScatterOrAggType)
def column_scatter_valudator(value):
    if any(isinstance(o, dict) for o in value.values()):
        # dict -> dataframe -> agg
        return parse_obj_as(ColumnAggScatter, value)
    if any(isinstance(o, (pd.DataFrame, pd.Series)) for o in value.values()):
        return value
    return parse_obj_as(ColumnScatter, value)


class Distribution(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:Distribution"
        pd_include = False
        tags = {IncludeTags.Render}
        smart_union = True
        extract_as_obj = True

    x: Union[np.ndarray, list, pd.Categorical, pd.Series]
    y: Union[np.ndarray, list, pd.Categorical, pd.Series]


class ConfusionMatrix(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:ConfusionMatrix"
        smart_union = True

        field_tags = {"labels": {IncludeTags.Parameter}}

    labels: Sequence[Label]
    values: list  # todo better typing


class PredictionData(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:PredictionData"
        dict_include = False
        smart_union = True

    predictions: pd.Series
    labels: LabelList
    prediction_probas: Optional[pd.DataFrame]

    @validator("prediction_probas")
    def validate_prediction_probas(cls, value: pd.DataFrame, values):
        """Align label types"""
        if value is None:
            return None
        labels = values["labels"]
        for col in list(value.columns):
            if col not in labels:
                if str(col) in labels:
                    value.rename(columns={col: str(col)}, inplace=True)
                    continue
                try:
                    int_col = int(col)
                    if int_col in labels:
                        value.rename(columns={col: int_col}, inplace=True)
                except ValueError:
                    pass
        return value


class StatsByFeature(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:StatsByFeature"
        dict_include = False
        pd_include = False
        tags = {IncludeTags.Render}

    plot_data: pd.DataFrame  # todo what type of plot?
    predictions: Optional[PredictionData]


class DatasetUtilityColumns(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:DatasetUtilityColumns"

    date: Optional[str]
    id: Optional[str]
    target: Optional[str]
    prediction: Optional[Union[str, Sequence[str]]]


class DatasetColumns(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:DatasetColumns"
        dict_exclude_fields = {"task", "target_type"}
        pd_include = False
        tags = {IncludeTags.Parameter}
        smart_union = True

    utility_columns: DatasetUtilityColumns
    target_type: Optional[str]
    num_feature_names: List[str]
    cat_feature_names: List[str]
    text_feature_names: List[str]
    datetime_feature_names: List[str]
    target_names: Optional[TargetNames]
    task: Optional[str]

    @property
    def target_names_list(self) -> Optional[List]:
        if isinstance(self.target_names, dict):
            return list(self.target_names.keys())
        return self.target_names

    def get_all_features_list(self, cat_before_num: bool = True, include_datetime_feature: bool = False) -> List[str]:
        """List all features names.

        By default, returns cat features than num features and du not return other.

        If you want to change the order - set  `cat_before_num` to False.

        If you want to add date time columns - set `include_datetime_feature` to True.
        """
        if cat_before_num:
            result = self.cat_feature_names + self.num_feature_names + self.text_feature_names

        else:
            result = self.num_feature_names + self.cat_feature_names + self.text_feature_names

        if include_datetime_feature and self.datetime_feature_names:
            result += self.datetime_feature_names

        return result

    def get_all_columns_list(self, skip_id_column: bool = False, skip_text_columns: bool = False) -> List[str]:
        """List all columns."""
        result: List[str] = self.cat_feature_names + self.num_feature_names

        if not skip_text_columns:
            result.extend(self.text_feature_names)

        result.extend(
            [
                name
                for name in (
                    self.utility_columns.id if not skip_id_column else None,
                    self.utility_columns.date,
                    self.utility_columns.target,
                    self.utility_columns.prediction,
                )
                if name is not None and isinstance(name, str)
            ]
        )
        return result

    def get_features_len(self, include_time_columns: bool = False) -> int:
        """How mane feature do we have. It is useful for pagination in widgets.

        By default, we sum category nad numeric features.

        If you want to include date time columns - set `include_datetime_feature` to True.
        """
        if include_time_columns and self.datetime_feature_names:
            len_time_columns = len(self.datetime_feature_names)

        else:
            len_time_columns = 0

        return (
            len(self.num_feature_names) + len(self.cat_feature_names) + len(self.text_feature_names) + len_time_columns
        )


def df_from_column_scatter(value: ColumnScatter) -> pd.DataFrame:
    df = pd.DataFrame.from_dict(value)
    if "index" in df.columns:
        df.set_index("index", inplace=True)
    return df


def column_scatter_from_df(df: Optional[pd.DataFrame], with_index: bool) -> Optional[ColumnScatter]:
    if df is None:
        return None
    data: ColumnScatter = {column: df[column] for column in df.columns}
    if with_index:
        data["index"] = df.index.to_series()
    return data


class ScatterAggField(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:ScatterAggField"
        smart_union = True
        dict_include = False
        pd_include = False

        tags = {IncludeTags.Render}

    scatter: ColumnAggScatter
    x_name: str
    plot_shape: Dict[str, float]


class ScatterField(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:ScatterField"
        smart_union = True
        dict_include = False
        pd_include = False

        tags = {IncludeTags.Render}

    scatter: ColumnScatter
    x_name: str
    plot_shape: Dict[str, float]


class ColumnScatterResult(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:ColumnScatterResult"
        smart_union = True
        dict_include = False
        pd_include = False

        tags = {IncludeTags.Render}
        field_tags = {"current": {IncludeTags.Current}, "reference": {IncludeTags.Reference}}

    current: ColumnScatter
    reference: Optional[ColumnScatter]
    x_name: str
    x_name_ref: Optional[str] = None


class ColumnAggScatterResult(ColumnScatterResult):
    class Config:
        type_alias = "servequery:metric_result:ColumnAggScatterResult"
        field_tags = {"current": {IncludeTags.Current}, "reference": {IncludeTags.Reference}}

    # TODO: fix type collision with super type
    current: ColumnAggScatter  # type: ignore[assignment]
    reference: Optional[ColumnAggScatter]  # type: ignore[assignment]


PlotData = List[float]


class Boxes(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:Boxes"
        dict_include = False
        tags = {IncludeTags.Render}

    mins: PlotData
    lowers: PlotData
    means: PlotData
    uppers: PlotData
    maxs: PlotData


class RatesPlotData(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:RatesPlotData"
        dict_include = False
        tags = {IncludeTags.Render}

    thrs: PlotData
    tpr: PlotData
    fpr: PlotData
    fnr: PlotData
    tnr: PlotData


class PRCurveData(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:PRCurveData"
        dict_include = False
        tags = {IncludeTags.Render}

    pr: PlotData
    rcl: PlotData
    thrs: PlotData


PRCurve = Dict[Label, PRCurveData]


class ROCCurveData(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:ROCCurveData"
        dict_include = False
        tags = {IncludeTags.Render}

    fpr: PlotData
    tpr: PlotData
    thrs: PlotData


ROCCurve = Dict[Label, ROCCurveData]


class LiftCurveData(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:LiftCurveData"
        dict_include = False
        tags = {IncludeTags.Render}

    lift: PlotData
    top: PlotData
    count: PlotData
    prob: PlotData
    tp: PlotData
    fp: PlotData
    precision: PlotData
    recall: PlotData
    f1_score: PlotData
    max_lift: PlotData
    relative_lift: PlotData
    percent: PlotData


LiftCurve = Dict[Label, LiftCurveData]


class HistogramData(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:HistogramData"
        dict_include = False
        tags = {IncludeTags.Render}
        extract_as_obj = True

    x: pd.Series
    count: pd.Series
    name: Optional[str] = None

    @classmethod
    def from_df(cls, value: pd.DataFrame, name: Optional[str] = None):
        return cls(x=value["x"], count=value["count"], name=name)

    @classmethod
    def from_distribution(cls, dist: Optional[Distribution], name: Optional[str] = None):
        if dist is None:
            return None
        return cls(x=pd.Series(dist.x), count=pd.Series(dist.y), name=name)

    @classmethod
    def from_dict(cls, data: Optional[Dict], name: Optional[str] = None):
        if data is None:
            return None
        return cls(x=pd.Series(data.keys()), count=pd.Series(data.values()), name=name)

    @classmethod
    def from_any(
        cls, value: Union[None, "HistogramData", pd.DataFrame, Distribution, Dict], name: Optional[str] = None
    ):
        if value is None:
            return None
        if isinstance(value, HistogramData):
            return value
        if isinstance(value, pd.DataFrame):
            return cls.from_df(value, name)
        if isinstance(value, Distribution):
            return cls.from_distribution(value, name)
        if isinstance(value, dict):
            return cls.from_dict(value, name)
        raise NotImplementedError(f"Cannot create {cls.__name__} from {value.__class__.__name__}")

    def to_df(self):
        return pd.DataFrame.from_dict(self.dict(include={"x", "count"}))


class Histogram(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:Histogram"
        dict_include = False
        tags = {IncludeTags.Render}
        field_tags = {
            "current": {IncludeTags.Current},
            "reference": {IncludeTags.Reference},
            "current_log": {IncludeTags.Current},
            "reference_log": {IncludeTags.Reference},
        }

    current: HistogramData
    reference: Optional[HistogramData]

    current_log: Optional[HistogramData] = None
    reference_log: Optional[HistogramData] = None


# todo need better config overriding logic in metricresult
class DistributionIncluded(Distribution):
    class Config:
        type_alias = "servequery:metric_result:DistributionIncluded"
        tags: Set[IncludeTags] = set()
        dict_include = True
        field_tags = {"x": {IncludeTags.Extra}}


class ColumnCorrelations(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:ColumnCorrelations"
        field_tags = {"column_name": {IncludeTags.Parameter}, "kind": {IncludeTags.Parameter}}

    column_name: str
    kind: str
    values: DistributionIncluded

    def get_pandas(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {"kind": self.kind, "column_name": key, "value": value}
                for key, value in zip(self.values.x, self.values.y)
            ]
        )


class DatasetClassificationQuality(MetricResult):
    class Config:
        type_alias = "servequery:metric_result:DatasetClassificationQuality"

    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: Optional[float] = None
    log_loss: Optional[float] = None
    tpr: Optional[float] = None
    tnr: Optional[float] = None
    fpr: Optional[float] = None
    fnr: Optional[float] = None
    rate_plots_data: Optional[RatesPlotData] = None
    plot_data: Optional[Boxes] = None


TR = TypeVar("TR")
TA = TypeVar("TA")


@overload
def raw_agg_properties(
    field_name, raw_type: Type[TR], agg_type: Type[TA], optional: Literal[False]
) -> Tuple[TR, TA]: ...


@overload
def raw_agg_properties(
    field_name, raw_type: Type[TR], agg_type: Type[TA], optional: Literal[True]
) -> Tuple[Optional[TR], Optional[TA]]: ...


def raw_agg_properties(field_name, raw_type: Type[TR], agg_type: Type[TA], optional: bool) -> Tuple[TR, TA]:
    def property_raw(self):
        val = getattr(self, field_name)
        if optional and val is None:
            return None
        if isinstance(raw_type, type) and not isinstance(val, raw_type):
            raise ValueError("Raw data not available")
        return val

    def property_agg(self):
        val = getattr(self, field_name)
        if optional and val is None:
            return None
        if isinstance(agg_type, type) and not isinstance(val, agg_type):
            raise ValueError("Agg data not available")
        return val

    return property(property_raw), property(property_agg)  # type: ignore[return-value]

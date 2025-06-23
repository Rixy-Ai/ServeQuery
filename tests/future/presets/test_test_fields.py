import dataclasses
from inspect import isabstract
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple
from typing import Type
from typing import Union
from typing import get_origin

import pandas as pd
import pytest

from servequery import BinaryClassification
from servequery import DataDefinition
from servequery import Dataset
from servequery._pydantic_compat import ModelField
from servequery.core.container import MetricContainer
from servequery.core.metric_types import MeanStdMetric
from servequery.core.metric_types import MeanStdMetricTests
from servequery.core.metric_types import Metric
from servequery.core.metric_types import MetricTest
from servequery.core.metric_types import convert_tests
from servequery.core.report import Report
from servequery.core.tests import GenericTest
from servequery.descriptors import TextLength
from servequery.generators import ColumnMetricGenerator
from servequery.metrics import FNR
from servequery.metrics import FPR
from servequery.metrics import MAE
from servequery.metrics import MAPE
from servequery.metrics import RMSE
from servequery.metrics import TNR
from servequery.metrics import TPR
from servequery.metrics import AbsMaxError
from servequery.metrics import Accuracy
from servequery.metrics import AlmostConstantColumnsCount
from servequery.metrics import AlmostDuplicatedColumnsCount
from servequery.metrics import ColumnCount
from servequery.metrics import ConstantColumnsCount
from servequery.metrics import DatasetMissingValueCount
from servequery.metrics import DummyMAE
from servequery.metrics import DummyMAPE
from servequery.metrics import DummyRMSE
from servequery.metrics import DuplicatedColumnsCount
from servequery.metrics import DuplicatedRowCount
from servequery.metrics import EmptyColumnsCount
from servequery.metrics import EmptyRowsCount
from servequery.metrics import F1ByLabel
from servequery.metrics import F1Score
from servequery.metrics import LogLoss
from servequery.metrics import MaxValue
from servequery.metrics import MeanError
from servequery.metrics import MeanValue
from servequery.metrics import MinValue
from servequery.metrics import MissingValueCount
from servequery.metrics import Precision
from servequery.metrics import PrecisionByLabel
from servequery.metrics import QuantileValue
from servequery.metrics import R2Score
from servequery.metrics import Recall
from servequery.metrics import RecallByLabel
from servequery.metrics import RocAuc
from servequery.metrics import RocAucByLabel
from servequery.metrics import RowCount
from servequery.metrics import StdValue
from servequery.metrics import UniqueValueCount
from servequery.metrics.group_by import GroupBy
from servequery.metrics.row_test_summary import RowTestSummary
from servequery.presets import ClassificationDummyQuality
from servequery.presets import ClassificationPreset
from servequery.presets import ClassificationQuality
from servequery.presets import ClassificationQualityByLabel
from servequery.presets import DataDriftPreset
from servequery.presets import DatasetStats
from servequery.presets import DataSummaryPreset
from servequery.presets import RegressionDummyQuality
from servequery.presets import RegressionPreset
from servequery.presets import RegressionQuality
from servequery.presets import TextEvals
from servequery.presets.dataset_stats import ValueStatsTests
from servequery.tests import eq
from tests.conftest import load_all_subtypes

load_all_subtypes(MetricContainer)


def mean_std_check(metric: MeanStdMetric, tests: MeanStdMetricTests):
    return metric.mean_tests == tests.mean and metric.std_tests == tests.std


value_stats_metric_mapping = {
    MissingValueCount: "missing_values_count_tests",
    MinValue: "min_tests",
    MaxValue: "max_tests",
    MeanValue: "mean_tests",
    RowCount: "row_count_tests",
    StdValue: "std_tests",
    UniqueValueCount: "unique_values_count_tests",
}


def value_stats_tests_check(metric: Metric, tests: Dict[str, ValueStatsTests]):
    ts = next(iter(tests.values())).convert()
    for metric_type, field_name in value_stats_metric_mapping.items():
        if not isinstance(metric, metric_type):
            continue
        return metric.tests == getattr(ts, field_name)
    if isinstance(metric, QuantileValue):
        return metric.tests == getattr(ts, f"q{int(metric.quantile * 100)}_tests")
    raise ValueError(f"Unknown metric type {metric.__class__.__name__}")


FieldOrFieldCheck = Union[str, Callable[[Metric, Any], bool]]
MetricTypeOrMetricCheck = Union[Type[Metric], Callable[[Metric], bool]]
preset_types: Dict[Type[MetricContainer], Dict[str, Tuple[MetricTypeOrMetricCheck, FieldOrFieldCheck]]] = {
    ClassificationQuality: {
        "accuracy_tests": (Accuracy, "tests"),
        "precision_tests": (Precision, "tests"),
        "recall_tests": (Recall, "tests"),
        "f1score_tests": (F1Score, "tests"),
        "rocauc_tests": (RocAuc, "tests"),
        "logloss_tests": (LogLoss, "tests"),
        "tpr_tests": (TPR, "tests"),
        "tnr_tests": (TNR, "tests"),
        "fpr_tests": (FPR, "tests"),
        "fnr_tests": (FNR, "tests"),
    },
    ClassificationDummyQuality: {},
    ClassificationQualityByLabel: {
        "f1score_tests": (F1ByLabel, "tests"),
        "precision_tests": (PrecisionByLabel, "tests"),
        "recall_tests": (RecallByLabel, "tests"),
        "rocauc_tests": (RocAucByLabel, "tests"),
    },
    ClassificationPreset: {
        "accuracy_tests": (Accuracy, "tests"),
        "precision_tests": (Precision, "tests"),
        "recall_tests": (Recall, "tests"),
        "f1score_tests": (F1Score, "tests"),
        "rocauc_tests": (RocAuc, "tests"),
        "logloss_tests": (LogLoss, "tests"),
        "tpr_tests": (TPR, "tests"),
        "tnr_tests": (TNR, "tests"),
        "fpr_tests": (FPR, "tests"),
        "fnr_tests": (FNR, "tests"),
        "f1score_by_label_tests": (F1ByLabel, "tests"),
        "precision_by_label_tests": (PrecisionByLabel, "tests"),
        "recall_by_label_tests": (RecallByLabel, "tests"),
        "rocauc_by_label_tests": (RocAucByLabel, "tests"),
    },
    DataSummaryPreset: {
        "row_count_tests": (lambda m: isinstance(m, RowCount) and m.tests, "tests"),
        "column_count_tests": (lambda m: isinstance(m, ColumnCount) and m.tests, "tests"),  # todo: duplicated metrics
        "duplicated_row_count_tests": (DuplicatedRowCount, "tests"),
        "duplicated_column_count_tests": (DuplicatedColumnsCount, "tests"),
        "almost_duplicated_column_count_tests": (AlmostDuplicatedColumnsCount, "tests"),
        "almost_constant_column_count_tests": (AlmostConstantColumnsCount, "tests"),
        "empty_row_count_tests": (EmptyRowsCount, "tests"),
        "empty_column_count_tests": (EmptyColumnsCount, "tests"),
        "constant_columns_count_tests": (ConstantColumnsCount, "tests"),
        "dataset_missing_value_count_tests": (DatasetMissingValueCount, "tests"),
        "column_tests": (lambda x: isinstance(x, Metric) and x.tests, value_stats_tests_check),
    },
    GroupBy: {},
    DataDriftPreset: {},
    RegressionPreset: {
        "mean_error_tests": (MeanError, mean_std_check),
        "mape_tests": (MAPE, mean_std_check),
        "rmse_tests": (RMSE, "tests"),
        "mae_tests": (MAE, mean_std_check),
        "r2score_tests": (R2Score, "tests"),
        "abs_max_error_tests": (AbsMaxError, "tests"),
    },
    TextEvals: {
        "row_count_tests": (lambda x: isinstance(x, RowCount) and x.tests, "tests"),
        # because of  duplicated RowCount metric in text evals
        "column_tests": (lambda x: not isinstance(x, RowCount) or x.tests, value_stats_tests_check),
    },
    RegressionDummyQuality: {
        "mae_tests": (DummyMAE, "tests"),
        "mape_tests": (DummyMAPE, "tests"),
        "rmse_tests": (DummyRMSE, "tests"),
    },
    ColumnMetricGenerator: {},
    DatasetStats: {
        "row_count_tests": (RowCount, "tests"),
        "column_count_tests": (lambda metric: isinstance(metric, ColumnCount) and metric.column_type is None, "tests"),
        "duplicated_row_count_tests": (DuplicatedRowCount, "tests"),
        "duplicated_column_count_tests": (DuplicatedColumnsCount, "tests"),
        "almost_duplicated_column_count_tests": (AlmostDuplicatedColumnsCount, "tests"),
        "almost_constant_column_count_tests": (AlmostConstantColumnsCount, "tests"),
        "empty_row_count_tests": (EmptyRowsCount, "tests"),
        "empty_column_count_tests": (EmptyColumnsCount, "tests"),
        "constant_columns_count_tests": (ConstantColumnsCount, "tests"),
        "dataset_missing_value_count_tests": (DatasetMissingValueCount, "tests"),
        "dataset_missing_value_share_tests": (DatasetMissingValueCount, "share_tests"),
    },
    RegressionQuality: {
        "mean_error_tests": (MeanError, mean_std_check),
        "mape_tests": (MAPE, mean_std_check),
        "rmse_tests": (RMSE, "tests"),
        "mae_tests": (MAE, mean_std_check),
        "r2score_tests": (R2Score, "tests"),
        "abs_max_error_tests": (AbsMaxError, "tests"),
    },
    RowTestSummary: {},
}


def test_all_presets_tested():
    tested_types_set = set(preset_types)
    all_preset_types = set(s for s in MetricContainer.__subclasses__() if not isabstract(s))

    missing_test_fields: Dict[Type[MetricContainer], List[str]] = {}
    for preset_type in all_preset_types:
        all_test_fields = [tf[0] for tf in iter_type_test_fields(preset_type)]
        if preset_type not in tested_types_set:
            missing_test_fields[preset_type] = all_test_fields
            continue
        tested_fields = set(preset_types[preset_type])
        if tested_fields != set(all_test_fields):
            missing_test_fields[preset_type] = list(tested_fields - set(all_test_fields))

    def guess_metric_name(s):
        s = s.split("_tests")[0]
        return s.split("_")[0].capitalize() + "".join(w.title() for w in s.split("_")[1:])

    def _fmt(fields):
        return ", ".join(f"'{f}': ({guess_metric_name(f)}, 'tests')" for f in fields)

    format_missing = ", ".join(f"{t.__name__}: {{{_fmt(fs)}" f"}}" for t, fs in missing_test_fields.items())
    assert len(missing_test_fields) == 0, "Missing tests for preset fields: {}".format(format_missing)


def _is_test_field(field: ModelField) -> bool:
    if field.outer_type_ is bool:
        return False
    return "tests" in field.name


def _get_test_field_instance(
    field: ModelField, check: Union[GenericTest, MetricTest], preset_type: Type[MetricContainer]
):
    if get_origin(field.outer_type_) == dict:
        if field.type_ is ValueStatsTests:
            col = "text_length"
            return {
                col: ValueStatsTests(
                    unique_values_count_tests={"b": [check]},
                    **{
                        f.name: [check]
                        for f in dataclasses.fields(ValueStatsTests)
                        if f.name != "unique_values_count_tests"
                    },
                )
            }
        return {"a": [check]}
    if get_origin(field.outer_type_) == list:
        return [check]
    if field.outer_type_ is MeanStdMetricTests:
        return MeanStdMetricTests(mean=[check], std=[check])
    return NotImplementedError(f"Not implemented for {field.outer_type_}")


def iter_type_test_fields(preset_type: Type[MetricContainer]) -> Iterable[Tuple[str, ModelField]]:
    for field_name, field in preset_type.__fields__.items():
        if not _is_test_field(field):
            continue
        yield field_name, field


@pytest.mark.parametrize("preset_type", preset_types)
@pytest.mark.parametrize("check", [eq(0)])
def test_preset_type_test_fields(preset_type: Type[MetricContainer], check: Union[GenericTest, MetricTest]):
    errors = {}

    for field_name, field in iter_type_test_fields(preset_type):
        field_instance = _get_test_field_instance(field, check, preset_type)
        try:
            instance = preset_type(**{field_name: field_instance})
        except Exception as e:
            errors[field_name] = e
            continue
        dataset = Dataset.from_pandas(
            pd.DataFrame({"a": [1], "b": ["b"]}),
            data_definition=DataDefinition(classification=[BinaryClassification()]),
            descriptors=[TextLength("b")],
        )
        run = Report([]).run(dataset)
        gen_metrics = instance.generate_metrics(run._context)
        assert (
            field_name in preset_types[preset_type]
        ), f"Missing target for {preset_type.__name__}.{field_name}: available {[m.__class__.__name__ for m in gen_metrics]}"
        target_metric, field_check = preset_types[preset_type][field_name]
        metrics = [
            m
            for m in gen_metrics
            if (isinstance(target_metric, type) and isinstance(m, target_metric))
            or (not isinstance(target_metric, type) and target_metric(m))
        ]
        assert (
            len(metrics) != 0
        ), f"Could not determine target metric for {preset_type.__name__}.{field_name}: {gen_metrics}"
        for metric in metrics:
            if callable(field_check):
                assert field_check(
                    metric, field_instance
                ), f"Failed for {preset_type.__name__}.{field_name} with {metric}"
            else:
                assert getattr(metric, field_check) == convert_tests(field_instance), (
                    f"Failed for {preset_type.__name__}.{field_name} {metric.__class__.__name__}:"
                    f" {getattr(metric, field_check)} != {field_instance}"
                )
    assert len(errors) == 0, f"Failed for {preset_type.__name__}: {errors}"

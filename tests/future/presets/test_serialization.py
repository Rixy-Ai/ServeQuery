import json
from inspect import isabstract
from typing import List

import pytest

from servequery._pydantic_compat import parse_obj_as
from servequery.core.container import MetricContainer
from servequery.generators import ColumnMetricGenerator
from servequery.metrics import MinValue
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
from tests.conftest import load_all_subtypes

load_all_subtypes(MetricContainer)

all_presets: List[MetricContainer] = [
    ClassificationPreset(),
    ClassificationQuality(),
    DatasetStats(),
    DataSummaryPreset(),
    RegressionDummyQuality(),
    ColumnMetricGenerator(metric_type=MinValue),
    ClassificationDummyQuality(),
    RegressionQuality(),
    DataDriftPreset(),
    TextEvals(),
    ClassificationQualityByLabel(),
    RegressionPreset(),
    GroupBy(metric=MinValue(column="a"), column_name="b"),
    RowTestSummary(),
]


def test_all_presets_tested():
    tested_types_set = {type(p) for p in all_presets}
    all_preset_types = set(s for s in MetricContainer.__subclasses__() if not isabstract(s))
    assert tested_types_set == all_preset_types, "Missing tests for presets " + ", ".join(
        f"{t.__name__}()" for t in all_preset_types - tested_types_set
    )


@pytest.mark.parametrize("preset", all_presets, ids=lambda p: p.__class__.__name__)
def test_all_presets_json_serialization(preset):
    payload = json.loads(preset.json())
    preset2 = parse_obj_as(MetricContainer, payload)
    assert preset2 == preset

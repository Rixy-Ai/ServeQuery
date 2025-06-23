# ruff: noqa: E501
# fmt: off
from servequery.legacy.test_preset.test_preset import TestPreset
from servequery.pydantic_utils import register_type_alias

register_type_alias(TestPreset, "servequery.legacy.test_preset.classification_binary.BinaryClassificationTestPreset", "servequery:test_preset:BinaryClassificationTestPreset")
register_type_alias(TestPreset, "servequery.legacy.test_preset.classification_binary_topk.BinaryClassificationTopKTestPreset", "servequery:test_preset:BinaryClassificationTopKTestPreset")
register_type_alias(TestPreset, "servequery.legacy.test_preset.classification_multiclass.MulticlassClassificationTestPreset", "servequery:test_preset:MulticlassClassificationTestPreset")
register_type_alias(TestPreset, "servequery.legacy.test_preset.data_drift.DataDriftTestPreset", "servequery:test_preset:DataDriftTestPreset")
register_type_alias(TestPreset, "servequery.legacy.test_preset.data_quality.DataQualityTestPreset", "servequery:test_preset:DataQualityTestPreset")
register_type_alias(TestPreset, "servequery.legacy.test_preset.data_stability.DataStabilityTestPreset", "servequery:test_preset:DataStabilityTestPreset")
register_type_alias(TestPreset, "servequery.legacy.test_preset.no_target_performance.NoTargetPerformanceTestPreset", "servequery:test_preset:NoTargetPerformanceTestPreset")
register_type_alias(TestPreset, "servequery.legacy.test_preset.recsys.RecsysTestPreset", "servequery:test_preset:RecsysTestPreset")
register_type_alias(TestPreset, "servequery.legacy.test_preset.regression.RegressionTestPreset", "servequery:test_preset:RegressionTestPreset")

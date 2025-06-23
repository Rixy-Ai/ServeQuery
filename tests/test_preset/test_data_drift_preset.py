from servequery.legacy.core import ColumnType
from servequery.legacy.test_preset import DataDriftTestPreset
from servequery.legacy.tests import TestAllFeaturesValueDrift
from servequery.legacy.tests import TestEmbeddingsDrift
from servequery.legacy.tests import TestShareOfDriftedColumns
from servequery.legacy.utils.data_preprocessing import ColumnDefinition
from servequery.legacy.utils.data_preprocessing import DataDefinition


def test_embeddings_data_drift_preset():
    data_definition = DataDefinition(
        columns={
            "target": ColumnDefinition("target", ColumnType.Numerical),
        },
        embeddings={
            "small_set": ["col_1", "col_2"],
            "big_set": ["col_3", "col_4"],
        },
        reference_present=True,
    )
    preset = DataDriftTestPreset(embeddings=["small_set", "big_set"])
    tests = preset.generate_tests(data_definition=data_definition, additional_data=None)
    assert len(tests) == 4
    expected_tests = [TestShareOfDriftedColumns, TestAllFeaturesValueDrift, TestEmbeddingsDrift, TestEmbeddingsDrift]
    assert expected_tests == [type(test) for test in tests]

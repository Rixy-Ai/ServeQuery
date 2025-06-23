import pandas as pd
import pytest

from servequery.core.datasets import Dataset
from servequery.core.report import Report
from servequery.core.report import Snapshot
from servequery.metrics import CategoryCount
from servequery.metrics import MeanValue
from servequery.metrics import MinValue
from servequery.metrics import RowCount
from servequery.tests import eq
from servequery.tests import lt


@pytest.mark.parametrize(
    "current,reference",
    [
        (Dataset.from_pandas(pd.DataFrame(data={"a": [1, 2, 3]})), None),
        (
            Dataset.from_pandas(pd.DataFrame(data={"a": [1, 2, 3]})),
            Dataset.from_pandas(pd.DataFrame(data={"a": [1, 2, 3]})),
        ),
        (pd.DataFrame(data={"a": [1, 2, 3]}), None),
        (pd.DataFrame(data={"a": [1, 2, 3]}), pd.DataFrame(data={"a": [1, 2, 3]})),
        (Dataset.from_pandas(pd.DataFrame(data={"a": [1, 2, 3]})), pd.DataFrame(data={"a": [1, 2, 3]})),
        (pd.DataFrame(data={"a": [1, 2, 3]}), Dataset.from_pandas(pd.DataFrame(data={"a": [1, 2, 3]}))),
    ],
)
def test_report_run(current, reference):
    report = Report(
        [
            RowCount(),
            MinValue(column="a", tests=[lt(1)]),
            CategoryCount(column="a", category=1, tests=[eq(0)]),
            MeanValue(column="a"),
        ]
    )

    snapshot = report.run(current_data=current, reference_data=reference)
    assert snapshot is not None

    data = snapshot.dumps()
    snapshot_2 = Snapshot.loads(data)
    assert snapshot_2 is not None
    assert snapshot.dumps() == snapshot_2.dumps()
    snapshot.json()

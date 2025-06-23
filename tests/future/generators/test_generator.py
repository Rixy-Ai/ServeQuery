import pandas as pd

from servequery.core.report import Report
from servequery.generators import ColumnMetricGenerator
from servequery.presets import ValueStats


def test_generator_renders():
    generator = ColumnMetricGenerator(ValueStats, columns=["a", "b"])
    report = Report([generator])
    snapshot = report.run(pd.DataFrame(data={"a": [1, 2, 3, 4], "b": [1, 2, 3, 4]}))
    assert len(snapshot._widgets) == 2

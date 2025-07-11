import os
import pathlib
from datetime import datetime
from datetime import timedelta

import pandas as pd
from sklearn import datasets

from servequery.legacy.pipeline.column_mapping import ColumnMapping
from servequery.legacy.renderers.html_widgets import WidgetSize
from servequery.legacy.test_preset import DataDriftTestPreset
from servequery.legacy.test_suite import TestSuite
from servequery.legacy.ui.dashboards import DashboardPanelTestSuite
from servequery.legacy.ui.dashboards import ReportFilter
from servequery.legacy.ui.dashboards import TestFilter
from servequery.legacy.ui.dashboards import TestSuitePanelType
from servequery.legacy.ui.demo_projects.base import DemoProject
from servequery.legacy.ui.workspace import WorkspaceBase


def create_data():
    if os.environ.get("SERVEQUERY_TEST_ENVIRONMENT", "0") != "1":
        adult_data = datasets.fetch_openml(name="adult", version=2, as_frame="auto")
        adult = adult_data.frame
    else:
        adult = pd.read_parquet(pathlib.Path(__file__).parent.joinpath("../../../../../test_data/adults.parquet"))

    reference = adult[~adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]
    current = adult[adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]
    column_mapping = ColumnMapping()
    return current, reference, column_mapping


def create_test_suite(i: int, data):
    current, reference, column_mapping = data
    ts = TestSuite(
        tests=[
            DataDriftTestPreset(),
        ],
        timestamp=datetime(2023, 1, 29) + timedelta(days=i + 1),
    )
    ts.metadata["batch_size"] = "daily"

    ts.run(
        reference_data=reference,
        current_data=current.iloc[1000 * i : 1000 * (i + 1), :],
        column_mapping=column_mapping,
    )

    return ts


def create_project(workspace: WorkspaceBase, name: str):
    project = workspace.create_project(name)
    project.description = "A toy demo project using Adult dataset. Showcases TestSuite panels"
    project.dashboard.add_panel(
        DashboardPanelTestSuite(
            title="Column Drift tests for key features: aggregated",
            test_filters=[
                TestFilter(test_id="TestColumnDrift", test_args={"column_name.name": "hours-per-week"}),
                TestFilter(test_id="TestColumnDrift", test_args={"column_name.name": "capital-gain"}),
            ],
            filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True),
            size=WidgetSize.HALF,
            time_agg="1D",
        )
    )
    project.dashboard.add_panel(
        DashboardPanelTestSuite(
            title="All tests: aggregated",
            filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True),
            size=WidgetSize.HALF,
            time_agg="1D",
        )
    )
    project.dashboard.add_panel(
        DashboardPanelTestSuite(
            title="Column Drift tests for key features: detailed",
            test_filters=[
                TestFilter(test_id="TestColumnDrift", test_args={"column_name.name": "hours-per-week"}),
                TestFilter(test_id="TestColumnDrift", test_args={"column_name.name": "capital-gain"}),
            ],
            filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True),
            size=WidgetSize.HALF,
            panel_type=TestSuitePanelType.DETAILED,
            time_agg="1D",
        )
    )
    project.dashboard.add_panel(
        DashboardPanelTestSuite(
            title="All tests: detailed",
            filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True),
            size=WidgetSize.HALF,
            panel_type=TestSuitePanelType.DETAILED,
            time_agg="1D",
        )
    )

    project.save()
    return project


adult_demo_project = DemoProject(
    name="Demo project - Adult",
    create_data=create_data,
    create_snapshot=None,
    create_report=None,
    create_project=create_project,
    create_test_suite=create_test_suite,
    count=19,
)

if __name__ == "__main__":
    # create_demo_project("http://localhost:8080")
    adult_demo_project.create("workspace")

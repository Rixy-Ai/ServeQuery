import warnings
from collections import Counter
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union

import pandas as pd

from servequery.legacy.base_metric import GenericInputData
from servequery.legacy.calculation_engine.engine import Engine
from servequery.legacy.calculation_engine.python_engine import PythonEngine
from servequery.legacy.core import IncludeOptions
from servequery.legacy.core import new_id
from servequery.legacy.model.dashboard import DashboardInfo
from servequery.legacy.model.widget import BaseWidgetInfo
from servequery.legacy.model.widget import set_source_fingerprint
from servequery.legacy.options.base import AnyOptions
from servequery.legacy.pipeline.column_mapping import ColumnMapping
from servequery.legacy.renderers.base_renderer import TestHtmlInfo
from servequery.legacy.renderers.base_renderer import TestRenderer
from servequery.legacy.renderers.base_renderer import WidgetIdGenerator
from servequery.legacy.renderers.base_renderer import replace_test_widget_ids
from servequery.legacy.suite.base_suite import MetadataValueType
from servequery.legacy.suite.base_suite import ReportBase
from servequery.legacy.suite.base_suite import Snapshot
from servequery.legacy.suite.base_suite import Suite
from servequery.legacy.suite.base_suite import find_test_renderer
from servequery.legacy.test_preset.test_preset import TestPreset
from servequery.legacy.tests.base_test import DEFAULT_GROUP
from servequery.legacy.tests.base_test import Test
from servequery.legacy.tests.base_test import TestStatus
from servequery.legacy.ui.type_aliases import SnapshotID
from servequery.legacy.utils.data_preprocessing import DataDefinition
from servequery.legacy.utils.generators import BaseGenerator

TEST_GENERATORS = "test_generators"
TEST_PRESETS = "test_presets"


class TestSuite(ReportBase):
    _data_definition: DataDefinition
    _test_presets: List[TestPreset]
    _test_generators: List[BaseGenerator]
    _tests: List[Test]
    _timestamp: Optional[datetime]

    def __init__(
        self,
        tests: Optional[List[Union[Test, TestPreset, BaseGenerator]]],
        options: AnyOptions = None,
        timestamp: Optional[datetime] = None,
        id: Optional[SnapshotID] = None,
        metadata: Dict[str, MetadataValueType] = None,
        tags: List[str] = None,
        name: str = None,
    ):
        super().__init__(options, name)
        if id is not None:
            warnings.warn("id argument is deprecated and has no effect", DeprecationWarning)
        self._timestamp = None
        if timestamp is not None:
            warnings.warn("timestamp argument is deprecated, use timestamp in run() method", DeprecationWarning)
            self._timestamp = timestamp
        self._inner_suite = Suite(self.options)
        self._test_presets = []
        self._test_generators = []
        self._tests = []
        self.metadata = metadata or {}
        self.tags = tags or []
        for original_test in tests or []:
            if isinstance(original_test, TestPreset):
                self._test_presets.append(original_test)
                if TEST_PRESETS not in self.metadata:
                    self.metadata[TEST_PRESETS] = []
                self.metadata[TEST_PRESETS].append(original_test.__class__.__name__)  # type: ignore[union-attr]
            elif isinstance(original_test, BaseGenerator):
                self._test_generators.append(original_test)

                if TEST_GENERATORS not in self.metadata:
                    self.metadata[TEST_GENERATORS] = []
                self.metadata[TEST_GENERATORS].append(original_test.__class__.__name__)  # type: ignore[union-attr]
            else:
                self._tests.append(original_test)

    def _add_tests(self):
        for original_test in self._tests or []:
            self._add_test(original_test)

    def _add_test(self, test: Test):
        new_test = test.copy()  # copy.copy(test)
        self._inner_suite.add_test(new_test)

    def __bool__(self):
        return all(test_result.is_passed() for _, test_result in self._inner_suite.context.test_results.items())

    def _add_tests_from_generator(self, test_generator: BaseGenerator):
        for test_item in test_generator.generate(self._data_definition):
            self._add_test(test_item)

    def run(
        self,
        *,
        reference_data: Optional[pd.DataFrame],
        current_data: pd.DataFrame,
        column_mapping: Optional[ColumnMapping] = None,
        engine: Optional[Type[Engine]] = None,
        additional_data: Dict[str, Any] = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        if column_mapping is None:
            column_mapping = ColumnMapping()
        self.id = new_id()
        if self._timestamp is not None:
            self.timestamp = self._timestamp
        else:
            self.timestamp = timestamp or datetime.now()
        self._inner_suite.reset()
        self._inner_suite.set_engine(PythonEngine() if engine is None else engine())
        self._add_tests()
        if self._inner_suite.context.engine is None:
            raise ValueError("Engine is not set")
        self._data_definition = self._inner_suite.context.get_data_definition(
            current_data,
            reference_data,
            column_mapping,
        )
        for preset in self._test_presets:
            tests = preset.generate_tests(self._data_definition, additional_data=additional_data)

            for test in tests:
                if isinstance(test, BaseGenerator):
                    self._add_tests_from_generator(test)
                else:
                    self._add_test(test)

        for test_generator in self._test_generators:
            self._add_tests_from_generator(test_generator)
        self._inner_suite.verify()
        data = GenericInputData(
            reference_data,
            current_data,
            column_mapping,
            self._data_definition,
            additional_data=additional_data or {},
        )

        self._inner_suite.run_calculate(data)
        self._inner_suite.run_checks()

    def json(  # type: ignore[override]
        self,
        include_metrics: bool = False,
        include_render: bool = False,
        include: Dict[str, IncludeOptions] = None,
        exclude: Dict[str, IncludeOptions] = None,
        **kwargs,
    ) -> str:
        return super().json(include_render, include, exclude, include_metrics=include_metrics)

    def as_dict(  # type: ignore[override]
        self,
        include_metrics: bool = False,
        include_render: bool = False,
        include: Dict[str, IncludeOptions] = None,
        exclude: Dict[str, IncludeOptions] = None,
        **kwargs,
    ) -> dict:
        test_results = []
        include = include or {}
        exclude = exclude or {}
        counter = Counter(test_result.status for test_result in self._inner_suite.context.test_results.values())

        for test in self._inner_suite.context.test_results:
            renderer = find_test_renderer(type(test), self._inner_suite.context.renderers)
            test_id = test.get_id()
            try:
                test_data = renderer.render_json(
                    test, include_render=include_render, include=include.get(test_id), exclude=exclude.get(test_id)
                )
                test_results.append(test_data)
            except BaseException as e:
                test_data = TestRenderer.render_json(renderer, test)
                test_data["status"] = TestStatus.ERROR
                test_data["description"] = f"Test failed with exception: {e}"
                test_results.append(test_data)

        total_tests = len(self._inner_suite.context.test_results)

        result = {
            "tests": test_results,
            "summary": {
                "all_passed": bool(self),
                "total_tests": total_tests,
                "success_tests": counter[TestStatus.SUCCESS] + counter[TestStatus.WARNING],
                "failed_tests": counter[TestStatus.FAIL],
                "by_status": {k.value: v for k, v in counter.items()},
            },
        }
        if include_metrics:
            from servequery.legacy.report import Report

            report = Report([])
            report._first_level_metrics = self._inner_suite.context.metrics
            report._inner_suite.context = self._inner_suite.context
            result["metric_results"] = report.as_dict(include_render=include_render, include=include, exclude=exclude)[
                "metrics"
            ]
        return result

    def _build_dashboard_info(self):
        test_results: List[TestHtmlInfo] = []
        total_tests = len(self._inner_suite.context.test_results)
        by_status = {}
        color_options = self.options.color_options

        generator = WidgetIdGenerator("")
        for test, test_result in self._inner_suite.context.test_results.items():
            generator.base_id = test.get_id()
            renderer = find_test_renderer(type(test), self._inner_suite.context.renderers)
            renderer.color_options = color_options
            by_status[test_result.status] = by_status.get(test_result.status, 0) + 1
            html = renderer.render_html(test)
            set_source_fingerprint((di.info for di in html.details), test)
            replace_test_widget_ids(html, generator)
            test_results.append(html)

        summary_widget = BaseWidgetInfo(
            title="",
            size=2,
            type="counter",
            params={
                "counters": [{"value": f"{total_tests}", "label": "Tests"}]
                + [
                    {"value": f"{by_status.get(status, 0)}", "label": f"{status.value.title()}"}
                    for status in [TestStatus.SUCCESS, TestStatus.WARNING, TestStatus.FAIL, TestStatus.ERROR]
                ]
            },
        )
        test_suite_widget = BaseWidgetInfo(
            title="",
            type="test_suite",
            size=2,
            params={
                "tests": [
                    dict(
                        title=test_info.name,
                        description=test_info.description,
                        test_fingerprint=test_info.test_fingerprint,
                        state=test_info.status.lower(),
                        details=dict(
                            parts=[dict(id=item.id, title=item.title, type="widget") for item in test_info.details]
                        ),
                        groups=test_info.groups,
                    )
                    for idx, test_info in enumerate(test_results)
                ],
                "testGroupTypes": DEFAULT_GROUP,
            },
            additionalGraphs=[],
        )
        return (
            "servequery_dashboard_" + str(new_id()).replace("-", ""),
            DashboardInfo(name="Test Suite", widgets=[summary_widget, test_suite_widget]),
            {item.id: item.info.dict() for idx, info in enumerate(test_results) for item in info.details},
        )

    def _get_snapshot(self) -> Snapshot:
        snapshot = super()._get_snapshot()
        snapshot.test_ids = list(range(len(snapshot.suite.tests)))
        return snapshot

    @classmethod
    def _parse_snapshot(cls, snapshot: Snapshot) -> "TestSuite":
        ctx = snapshot.suite.to_context()
        suite = TestSuite(
            tests=None,
            metadata=snapshot.metadata,
            tags=snapshot.tags,
            options=snapshot.options,
            name=snapshot.name,
        )
        suite.id = snapshot.id
        suite.timestamp = snapshot.timestamp
        suite._inner_suite.context = ctx
        return suite

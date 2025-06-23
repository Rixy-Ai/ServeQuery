import glob
import os
from collections import defaultdict
from importlib import import_module
from inspect import isabstract
from typing import Dict
from typing import Set
from typing import Type
from typing import TypeVar

import pytest

import servequery
from servequery._pydantic_compat import import_string
from servequery.core import registries
from servequery.core.container import MetricContainer
from servequery.core.datasets import ColumnCondition
from servequery.core.datasets import Descriptor
from servequery.core.metric_types import BoundTest
from servequery.core.metric_types import Metric as MetricV2
from servequery.core.metric_types import MetricResult as MetricResultV2
from servequery.core.metric_types import MetricTest
from servequery.legacy.base_metric import BasePreset
from servequery.legacy.base_metric import ColumnName
from servequery.legacy.base_metric import Metric
from servequery.legacy.base_metric import MetricResult
from servequery.legacy.collector.config import CollectorTrigger
from servequery.legacy.collector.storage import CollectorStorage
from servequery.legacy.features.generated_features import BaseDescriptor
from servequery.legacy.features.generated_features import FeatureDescriptor
from servequery.legacy.features.generated_features import GeneratedFeatures
from servequery.legacy.features.llm_judge import BaseLLMPromptTemplate
from servequery.legacy.metric_preset.metric_preset import MetricPreset
from servequery.legacy.metrics.data_drift.embedding_drift_methods import DriftMethod
from servequery.legacy.test_preset.test_preset import TestPreset
from servequery.legacy.tests.base_test import Test
from servequery.legacy.tests.base_test import TestParameters
from servequery.legacy.ui.components.base import Component as ComponentLegacy
from servequery.legacy.ui.dashboards.base import DashboardPanel
from servequery.legacy.utils.llm.prompts import PromptBlock
from servequery.legacy.utils.llm.prompts import PromptTemplate
from servequery.llm.prompts.content import PromptContent
from servequery.pydantic_utils import TYPE_ALIASES
from servequery.pydantic_utils import ServeQueryBaseModel
from servequery.pydantic_utils import PolymorphicModel
from servequery.pydantic_utils import WithTestAndMetricDependencies
from servequery.pydantic_utils import get_base_class
from servequery.pydantic_utils import is_not_abstract
from servequery.ui.service.components.base import Component

T = TypeVar("T")


# todo: deduplicate code
def find_all_subclasses(
    base: Type[T],
    base_module: str = "servequery",
    path: str = os.path.dirname(servequery.__file__),
    include_abstract: bool = False,
) -> Set[Type[T]]:
    classes = set()
    for mod in glob.glob(path + "/**/*.py", recursive=True):
        mod_path = os.path.relpath(mod, path)[:-3]
        mod_name = f"{base_module}." + mod_path.replace("/", ".").replace("\\", ".")
        if mod_name.endswith("__"):
            continue
        module = import_module(mod_name)
        for key, value in module.__dict__.items():
            if isinstance(value, type) and value is not base and issubclass(value, base):
                if not isabstract(value) or include_abstract:
                    classes.add(value)

    return classes


REGISTRY_MAPPING: Dict[Type[PolymorphicModel], str] = {
    # legacy
    Test: "servequery.legacy.tests._registry",
    TestParameters: "servequery.legacy.tests._registry",
    TestPreset: "servequery.legacy.test_preset._registry",
    MetricResult: "servequery.legacy.metrics._registry",
    Metric: "servequery.legacy.metrics._registry",
    MetricPreset: "servequery.legacy.metric_preset._registry",
    FeatureDescriptor: "servequery.legacy.descriptors._registry",
    GeneratedFeatures: "servequery.legacy.features._registry",
    PromptBlock: "servequery.legacy.utils.llm._registry",
    PromptTemplate: "servequery.legacy.utils.llm._registry",
    # new api
    MetricTest: registries.metric_tests.__name__,
    MetricV2: registries.metrics.__name__,
    MetricContainer: registries.presets.__name__,
    MetricResultV2: registries.metric_results.__name__,
    BoundTest: registries.bound_tests.__name__,
    Descriptor: registries.descriptors.__name__,
    ColumnCondition: registries.column_conditions.__name__,
    PromptContent: registries.prompts.__name__,
}


def test_all_aliases_registered():
    not_registered = []

    for cls in find_all_subclasses(PolymorphicModel, include_abstract=True):
        if cls.__is_base_type__():
            continue
        classpath = cls.__get_classpath__()
        typename = cls.__get_type__()
        if classpath == typename:
            # no typename
            continue
        key = (get_base_class(cls), typename)
        if key not in TYPE_ALIASES or TYPE_ALIASES[key] != classpath:
            not_registered.append(cls)

    register_msgs = []
    file_to_type = defaultdict(list)
    for cls in sorted(not_registered, key=lambda c: get_base_class(c).__name__ + " " + c.__get_classpath__()):
        base_class = get_base_class(cls)
        msg = f'register_type_alias({base_class.__name__}, "{cls.__get_classpath__()}", "{cls.__get_type__()}")'
        if base_class not in REGISTRY_MAPPING:
            register_msgs.append(msg)
            continue
        file_to_type[REGISTRY_MAPPING[base_class]].append(msg)

    for file, msgs in file_to_type.items():
        mod = import_string(file)
        with open(mod.__file__, "a") as f:
            f.write("\n")
            f.write("\n".join(msgs))
    print("\n".join(register_msgs))
    assert len(not_registered) == 0, "Not all aliases registered"


@pytest.mark.parametrize(
    "base_class,classpath", [(base_class, classpath) for (base_class, _), classpath in TYPE_ALIASES.items()]
)
def test_all_registered_classpath_exist(base_class: Type[PolymorphicModel], classpath):
    try:
        base_class.load_alias(classpath)
    except ImportError:
        assert False, f"wrong classpath registered '{classpath}'"


def test_all_aliases_correct():
    base_class_type_mapping = {
        Metric: "metric",
        Test: "test",
        GeneratedFeatures: "feature",
        BaseDescriptor: "descriptor",
        MetricPreset: "metric_preset",
        TestPreset: "test_preset",
        MetricResult: "metric_result",
        DriftMethod: "drift_method",
        TestParameters: "test_parameters",
        ColumnName: "base",
        CollectorTrigger: "collector_trigger",
        CollectorStorage: "collector_storage",
        BaseLLMPromptTemplate: "prompt_template",
        DashboardPanel: "dashboard_panel",
        PromptBlock: "prompt_block",
        PromptTemplate: "prompt_template",
        MetricV2: MetricV2.__alias_type__,
        MetricResultV2: MetricResultV2.__alias_type__,
        MetricTest: MetricTest.__alias_type__,
        BoundTest: BoundTest.__alias_type__,
        Descriptor: Descriptor.__alias_type__,
        MetricContainer: MetricContainer.__alias_type__,
        ColumnCondition: ColumnCondition.__alias_type__,
        PromptContent: PromptContent.__alias_type__,
    }
    skip = [Component, ComponentLegacy]
    skip_literal = [ServeQueryBaseModel, WithTestAndMetricDependencies, BasePreset]
    for cls in find_all_subclasses(PolymorphicModel, include_abstract=True):
        if cls in skip_literal or any(issubclass(cls, s) for s in skip) or not is_not_abstract(cls):
            continue
        for base_class, base_type in base_class_type_mapping.items():
            if issubclass(cls, base_class):
                # alias = getattr(cls.__config__, "type_alias")
                alias = cls.__get_type__()
                assert alias is not None, f"{cls.__name__} has no alias ({alias})"
                assert alias == f"servequery:{base_type}:{cls.__name__}", f"wrong alias for {cls.__name__}"
                break
        else:
            assert False, f"No base class type mapping for {cls}"

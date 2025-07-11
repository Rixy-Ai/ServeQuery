import dataclasses
import warnings
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

import pandas as pd
import uuid6

from servequery._pydantic_compat import BaseModel
from servequery._pydantic_compat import Field
from servequery.legacy.model.widget import AdditionalGraphInfo
from servequery.legacy.model.widget import BaseWidgetInfo
from servequery.legacy.model.widget import PlotlyGraphInfo
from servequery.legacy.options import ColorOptions

if TYPE_CHECKING:
    from servequery.legacy.base_metric import Metric
    from servequery.legacy.core import IncludeOptions
    from servequery.legacy.tests.base_test import Test


class BaseRenderer:
    """Base class for all renderers"""

    color_options: ColorOptions

    def __init__(self, color_options: Optional[ColorOptions] = None) -> None:
        if color_options is None:
            self.color_options = ColorOptions()

        else:
            self.color_options = color_options


TMetric = TypeVar("TMetric", bound="Metric")


class MetricRenderer(Generic[TMetric], BaseRenderer):
    def render_pandas(self, obj: TMetric) -> pd.DataFrame:
        result = obj.get_result()
        if not result.__config__.pd_include:
            warnings.warn(
                f"{obj.get_id()} metric does not support as_dataframe yet. Please submit an issue to https://github.com/Rixy-Ai/ServeQuery/issues"
            )
            return pd.DataFrame()
        return result.get_pandas()

    def render_json(
        self,
        obj: TMetric,
        include_render: bool = False,
        include: "IncludeOptions" = None,
        exclude: "IncludeOptions" = None,
    ) -> dict:
        result = obj.get_result()
        return result.get_dict(include_render=include_render, include=include, exclude=exclude)

    def render_html(self, obj: TMetric) -> List[BaseWidgetInfo]:
        raise NotImplementedError()


class DetailsInfo(BaseModel):
    title: str
    info: Union[BaseWidgetInfo, Any]
    id: str = Field(default_factory=lambda: str(uuid6.uuid7()))


class TestHtmlInfo(BaseModel):
    name: str
    description: str
    test_fingerprint: str
    status: str
    details: List[DetailsInfo]
    groups: Dict[str, str]

    def with_details(self, title: str, info: BaseWidgetInfo):
        self.details.append(DetailsInfo(title=title, info=info))
        return self


TTest = TypeVar("TTest", bound="Test")


class TestRenderer(Generic[TTest], BaseRenderer):
    def html_description(self, obj: TTest):
        return obj.get_result().description

    def json_description(self, obj: TTest):
        return obj.get_result().description

    def render_html(self, obj: TTest) -> TestHtmlInfo:
        result = obj.get_result()
        return TestHtmlInfo(
            name=result.name,
            description=self.html_description(obj),
            test_fingerprint=obj.get_fingerprint(),
            status=result.status.value,
            details=[],
            groups=obj.get_groups(),
        )

    def render_json(
        self,
        obj: TTest,
        include_render: bool = False,
        include: "IncludeOptions" = None,
        exclude: "IncludeOptions" = None,
    ) -> dict:
        return obj.get_result().get_dict(include_render=include_render, include=include, exclude=exclude)


@dataclasses.dataclass
class RenderersDefinitions:
    typed_renderers: dict = dataclasses.field(default_factory=dict)
    default_html_test_renderer: Optional[TestRenderer] = None
    default_html_metric_renderer: Optional[MetricRenderer] = None


def default_renderer(wrap_type):
    def wrapper(cls):
        DEFAULT_RENDERERS.typed_renderers[wrap_type] = cls()
        return cls

    return wrapper


DEFAULT_RENDERERS = RenderersDefinitions(default_html_test_renderer=TestRenderer())


class WidgetIdGenerator:
    def __init__(self, base_id: str):
        self.base_id = base_id
        self.counter = 0

    def get_id(self, postfix: str = None) -> str:
        val = f"{self.base_id}-{self.counter}"
        if postfix is not None:
            val = f"{val}-{postfix}"
        self.counter += 1
        return val


def replace_widgets_ids(widgets: List[BaseWidgetInfo], generator: WidgetIdGenerator):
    for widget in widgets:
        replace_widget_ids(widget, generator)


def replace_test_widget_ids(widget: TestHtmlInfo, generator: WidgetIdGenerator):
    for detail in widget.details:
        detail.id = generator.get_id()
        replace_widget_ids(detail.info, generator)


def replace_widget_ids(widget: BaseWidgetInfo, generator: WidgetIdGenerator):
    widget.id = generator.get_id()

    add_graph_id_mapping: Dict[str, Union[BaseWidgetInfo, AdditionalGraphInfo, PlotlyGraphInfo]] = {}
    for add_graph in widget.additionalGraphs:
        if isinstance(add_graph, BaseWidgetInfo):
            add_graph_id_mapping[add_graph.id] = add_graph
            replace_widget_ids(add_graph, generator)
        elif isinstance(add_graph, (AdditionalGraphInfo, PlotlyGraphInfo)):
            add_graph_id_mapping[add_graph.id] = add_graph
            add_graph.id = generator.get_id(add_graph.id.replace(" ", "-"))
        else:
            raise ValueError(f"Unknown add graph type {add_graph.__class__.__name__}")

    parts = []
    if isinstance(widget.params, dict):
        if "data" in widget.params:
            data = widget.params["data"]
            for item in data:
                if "details" in item and "parts" in item["details"]:
                    parts.extend(item["details"]["parts"])

        if "details" in widget.params:
            details = widget.params["details"]
            if "parts" in details:
                parts.extend(details["parts"])

    for part in parts:
        if "id" in part:
            widget_id = part["id"]
            if widget_id in add_graph_id_mapping:
                part["id"] = add_graph_id_mapping[widget_id].id

    for w in widget.widgets:
        replace_widget_ids(w, generator)

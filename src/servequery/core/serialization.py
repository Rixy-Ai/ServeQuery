from datetime import datetime
from typing import Dict
from typing import List
from typing import Union

from servequery._pydantic_compat import BaseModel
from servequery.core.metric_types import MetricId
from servequery.core.metric_types import MetricResult
from servequery.legacy.model.widget import BaseWidgetInfo
from servequery.legacy.suite.base_suite import MetadataValueType


class MetricReportItem(BaseModel):
    metric_id: MetricId
    params: dict


class PresetReportItem(BaseModel):
    pass  # TODO: support presets


class ReportModel(BaseModel):
    items: List[Union[MetricReportItem, PresetReportItem]]


class SnapshotModel(BaseModel):
    report: ReportModel
    timestamp: datetime
    metadata: Dict[str, MetadataValueType]
    tags: List[str]
    metric_results: Dict[MetricId, MetricResult]
    top_level_metrics: List[MetricId]
    widgets: List[BaseWidgetInfo]
    tests_widgets: List[BaseWidgetInfo]

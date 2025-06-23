from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import uuid6

from servequery._pydantic_compat import BaseModel
from servequery._pydantic_compat import Field
from servequery._pydantic_compat import validator
from servequery.legacy.core import new_id
from servequery.legacy.suite.base_suite import SnapshotLinks
from servequery.legacy.ui.type_aliases import OrgID
from servequery.legacy.ui.type_aliases import PanelID
from servequery.legacy.ui.type_aliases import ProjectID
from servequery.legacy.ui.type_aliases import SnapshotID
from servequery.legacy.ui.type_aliases import TabID


class DashboardTabModel(BaseModel):
    id: TabID = Field(default_factory=uuid6.uuid7)
    title: Optional[str]
    panels: List[PanelID]


class PanelMetric(BaseModel):
    legend: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, str] = Field(default_factory=dict)
    metric: str
    metric_labels: Dict[str, str] = Field(default_factory=dict)
    view_params: Dict[str, Any] = Field(default_factory=dict)

    @validator("metric")
    def metric_is_alias(cls, v):
        if not v.startswith("servequery:metric_v2:"):
            v = f"servequery:metric_v2:{v}"
        return v


class DashboardPanelPlot(BaseModel):
    id: PanelID = Field(default_factory=uuid6.uuid7)
    title: str
    subtitle: Optional[str]
    size: Optional[str]
    values: List[PanelMetric]
    plot_params: Dict[str, Any] = Field(default_factory=dict)


class DashboardModel(BaseModel):
    tabs: List[DashboardTabModel]
    panels: List[DashboardPanelPlot]


class ProjectModel(BaseModel):
    id: ProjectID = Field(default_factory=new_id)
    name: str
    description: Optional[str] = None
    org_id: Optional[OrgID] = None
    version: str = "2"


class SnapshotLink(BaseModel):
    snapshot_id: SnapshotID
    dataset_type: str
    dataset_subtype: str


class SnapshotMetadataModel(BaseModel):
    id: SnapshotID
    metadata: Dict[str, str]
    tags: List[str]
    timestamp: datetime
    links: SnapshotLinks

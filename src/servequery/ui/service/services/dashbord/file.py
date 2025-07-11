import typing
from typing import Optional

from servequery.sdk.models import DashboardModel
from servequery.ui.service.services.dashbord.base import DashboardManager
from servequery.ui.service.type_aliases import ProjectID

if typing.TYPE_CHECKING:
    from servequery.ui.service.storage.local import LocalState


class JsonFileDashboardManager(DashboardManager):
    def __init__(self, path: str, local_state: Optional["LocalState"] = None):
        from servequery.ui.service.storage.local import LocalState

        self._path = path
        self._state = local_state or LocalState(path, None)

    async def get_dashboard(self, project_id: ProjectID) -> DashboardModel:
        return self._state.read_dashboard(project_id)

    async def save_dashboard(self, project_id: ProjectID, dashboard: DashboardModel) -> None:
        return self._state.write_dashboard(project_id, dashboard)

from abc import ABC
from typing import Callable
from typing import ClassVar
from typing import Optional

from servequery.legacy.ui.base import BlobStorage
from servequery.legacy.ui.base import DataStorage
from servequery.legacy.ui.base import ProjectMetadataStorage
from servequery.legacy.ui.components.base import FactoryComponent
from servequery.legacy.ui.managers.projects import ProjectManager
from servequery.legacy.ui.storage.common import NoopAuthManager
from servequery.legacy.ui.storage.local import create_local_project_manager
from servequery.pydantic_utils import register_type_alias


class StorageComponent(FactoryComponent[ProjectManager], ABC):
    class Config:
        is_base_type = True

    dependency_name: ClassVar = "project_manager"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = False


class LocalStorageComponent(StorageComponent):
    path: str = "workspace"
    autorefresh: bool = True

    def dependency_factory(self) -> Callable[..., ProjectManager]:
        return lambda: create_local_project_manager(self.path, autorefresh=self.autorefresh, auth=NoopAuthManager())


class MetadataStorageComponent(FactoryComponent[ProjectMetadataStorage], ABC):
    class Config:
        is_base_type = True

    __section__: ClassVar = "metadata"
    dependency_name: ClassVar = "project_metadata"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[Optional[bool]] = None


class DataStorageComponent(FactoryComponent[DataStorage], ABC):
    class Config:
        is_base_type = True

    __section__: ClassVar = "data"

    dependency_name: ClassVar = "data_storage"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = False


class BlobStorageComponent(FactoryComponent[BlobStorage], ABC):
    class Config:
        is_base_type = True

    __section__: ClassVar = "blob"

    dependency_name: ClassVar = "blob_storage"
    use_cache: ClassVar[bool] = True
    sync_to_thread: ClassVar[bool] = False


register_type_alias(BlobStorageComponent, "servequery.legacy.ui.components.local_storage.FSSpecBlobComponent", "fsspec")
register_type_alias(
    MetadataStorageComponent, "servequery.legacy.ui.components.local_storage.JsonMetadataComponent", "json_file"
)
register_type_alias(
    DataStorageComponent, "servequery.legacy.ui.components.local_storage.InmemoryDataComponent", "inmemory"
)

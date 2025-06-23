"""For backward compatibility with servequery <= 4.9"""

import warnings

from servequery.legacy.ui.workspace import RemoteWorkspace

__all__ = ["RemoteWorkspace"]

warnings.warn(
    "Importing RemoteWorkspace from servequery.legacy.ui.remote is deprecated. Please import from servequery.legacy.ui.workspace",
    DeprecationWarning,
)

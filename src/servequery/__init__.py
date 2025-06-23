#!/usr/bin/env python
# coding: utf-8
from servequery.core.compare import compare
from servequery.core.datasets import BinaryClassification
from servequery.core.datasets import DataDefinition
from servequery.core.datasets import Dataset
from servequery.core.datasets import MulticlassClassification
from servequery.core.datasets import Recsys
from servequery.core.datasets import Regression
from servequery.core.report import Report
from servequery.core.report import Run
from servequery.legacy.core import ColumnType

from . import _registry
from ._version import __version__
from ._version import version_info
from .nbextension import _jupyter_nbextension_paths

__all__ = [
    "__version__",
    "version_info",
    "_jupyter_nbextension_paths",
    "_registry",
    "Report",
    "Run",
    "Dataset",
    "DataDefinition",
    "BinaryClassification",
    "MulticlassClassification",
    "Regression",
    "Recsys",
    "compare",
    "ColumnType",  # legacy support
]

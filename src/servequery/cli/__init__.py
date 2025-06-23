import sys
from pathlib import Path

from servequery.cli.demo_project import generate_demo_project
from servequery.cli.legacy_ui import legacy_ui
from servequery.cli.main import app
from servequery.cli.report import run_report
from servequery.cli.ui import ui

__all__ = ["app", "ui", "legacy_ui", "generate_demo_project", "run_report"]

sys.path.append(str(Path.cwd()))
if __name__ == "__main__":
    app()

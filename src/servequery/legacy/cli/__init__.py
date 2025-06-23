from servequery.legacy.cli.collector import collector
from servequery.legacy.cli.main import app
from servequery.legacy.cli.ui import ui

__all__ = ["app", "ui", "collector"]


def main():
    app()


if __name__ == "__main__":
    main()

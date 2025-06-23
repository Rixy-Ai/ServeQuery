import logging
import os
import time
from typing import Dict
from typing import Optional

import litestar
from litestar import Litestar
from litestar import Request
from litestar import Response
from litestar.di import Provide
from litestar.logging import LoggingConfig

from servequery.errors import ServeQueryError
from servequery.ui.service.api.projects import create_projects_api
from servequery.ui.service.api.projects import projects_api_dependencies
from servequery.ui.service.api.service import service_api
from servequery.ui.service.api.static import assets_router
from servequery.ui.service.components.base import AppBuilder
from servequery.ui.service.components.base import Component
from servequery.ui.service.components.base import ComponentContext
from servequery.ui.service.components.base import ServiceComponent
from servequery.ui.service.components.dashboard import DashboardComponent
from servequery.ui.service.components.security import NoSecurityComponent
from servequery.ui.service.components.security import SecurityComponent
from servequery.ui.service.components.storage import LocalStorageComponent
from servequery.ui.service.components.storage import StorageComponent
from servequery.ui.service.components.telemetry import TelemetryComponent
from servequery.ui.service.config import AppConfig
from servequery.ui.service.config import ConfigContext
from servequery.ui.service.errors import ServeQueryServiceError


def servequery_service_exception_handler(_: Request, exc: ServeQueryServiceError) -> Response:
    return exc.to_response()


def servequery_exception_handler(_: Request, exc: ServeQueryError) -> Response:
    return Response(content={"detail": exc.get_message()}, status_code=500)


class LocalServiceComponent(ServiceComponent):
    debug: bool = False

    @property
    def debug_enabled(self) -> bool:
        return self.debug or os.environ.get("SERVEQUERY_DEBUG") is not None

    def get_api_route_handlers(self, ctx: ComponentContext):
        guard = ctx.get_component(SecurityComponent).get_auth_guard()
        return [create_projects_api(guard), service_api()]

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        deps = super().get_dependencies(ctx)
        deps.update(projects_api_dependencies)
        return deps

    def get_route_handlers(self, ctx: ComponentContext):
        return [assets_router()]

    def apply(self, ctx: ComponentContext, builder: AppBuilder):
        super().apply(ctx, builder)
        assert isinstance(ctx, ConfigContext)
        builder.exception_handlers[ServeQueryServiceError] = servequery_service_exception_handler
        builder.exception_handlers[ServeQueryError] = servequery_exception_handler
        builder.kwargs["debug"] = self.debug_enabled
        if self.debug_enabled:
            log_config = create_logging()
            builder.kwargs["logging_config"] = LoggingConfig(**log_config)


def create_logging() -> dict:
    logging.Formatter.converter = time.gmtime
    return {
        "version": 1,
        "log_exceptions": "always",
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "logging.Formatter",
                "format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            },
            "access": {
                "()": "logging.Formatter",
                "format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            },
            "standard": {
                "()": "logging.Formatter",
                "format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "litestar": {"handlers": ["default"]},
            "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
        },
    }


class LitestarComponent(Component):
    __section__ = "litestar"
    request_max_body_size: Optional[int] = None

    def finalize(self, ctx: ComponentContext, app: Litestar):
        if self.request_max_body_size is not None:
            if hasattr(app, "request_max_body_size"):
                app.request_max_body_size = self.request_max_body_size
            else:
                logging.warning(
                    f"Litestar version {litestar.__version__.formatted()}"
                    f" does not support 'request_max_body_size' parameter"
                )


class LocalConfig(AppConfig):
    security: SecurityComponent = NoSecurityComponent()
    service: ServiceComponent = LocalServiceComponent()
    storage: StorageComponent = LocalStorageComponent()
    telemetry: TelemetryComponent = TelemetryComponent()
    dashboard: DashboardComponent = DashboardComponent()
    litestar: LitestarComponent = LitestarComponent()

import abc
from typing import Optional

from litestar import Request

from servequery.ui.service.base import User


class SecurityService:
    @abc.abstractmethod
    def authenticate(self, request: Request) -> Optional[User]:
        raise NotImplementedError()

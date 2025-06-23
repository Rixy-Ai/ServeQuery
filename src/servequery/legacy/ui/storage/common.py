from typing import ClassVar
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

from servequery.legacy.ui.base import EntityType
from servequery.legacy.ui.base import Org
from servequery.legacy.ui.base import Team
from servequery.legacy.ui.base import User
from servequery.legacy.ui.managers.auth import AuthManager
from servequery.legacy.ui.managers.auth import DefaultRole
from servequery.legacy.ui.managers.auth import Permission
from servequery.legacy.ui.managers.auth import Role
from servequery.legacy.ui.managers.auth import UserWithRoles
from servequery.legacy.ui.managers.auth import get_default_role_permissions
from servequery.legacy.ui.type_aliases import ZERO_UUID
from servequery.legacy.ui.type_aliases import EntityID
from servequery.legacy.ui.type_aliases import OrgID
from servequery.legacy.ui.type_aliases import ProjectID
from servequery.legacy.ui.type_aliases import TeamID
from servequery.legacy.ui.type_aliases import UserID

SERVEQUERY_SECRET_ENV = "SERVEQUERY_SECRET"
SECRET_HEADER_NAME = "servequery-secret"


class NoUser(User):
    id: UserID = ZERO_UUID
    name: str = ""


class NoTeam(Team):
    id: TeamID = ZERO_UUID
    name = ""
    org_id: OrgID = ZERO_UUID


class NoOrg(Org):
    id: OrgID = ZERO_UUID
    name = ""


NO_USER = NoUser()
NO_TEAM = NoTeam()
NO_ORG = NoOrg()


class NoopAuthManager(AuthManager):
    user: ClassVar[User] = NO_USER
    team: ClassVar[Team] = NO_TEAM
    org: ClassVar[Org] = NO_ORG

    async def create_org(self, owner: UserID, org: Org):
        return self.org

    async def get_org(self, org_id: OrgID) -> Optional[Org]:
        return self.org

    async def get_default_role(self, default_role: DefaultRole, entity_type: Optional[EntityType]) -> Role:
        return Role(
            id=0,
            name=default_role.value,
            entity_type=entity_type,
            permissions=get_default_role_permissions(default_role, entity_type)[1],
        )

    async def update_role(self, role: Role):
        return role

    async def _grant_entity_role(self, entity_type: EntityType, entity_id: EntityID, user_id: UserID, role: Role):
        pass

    async def _revoke_entity_role(self, entity_type: EntityType, entity_id: EntityID, user_id: UserID, role: Role):
        pass

    async def get_available_project_ids(
        self, user_id: UserID, team_id: Optional[TeamID], org_id: Optional[OrgID]
    ) -> Optional[Set[ProjectID]]:
        return None

    async def check_entity_permission(
        self, user_id: UserID, entity_type: EntityType, entity_id: EntityID, permission: Permission
    ) -> bool:
        return True

    async def create_user(self, user_id: UserID, name: Optional[str]) -> User:
        return self.user

    async def get_user(self, user_id: UserID) -> Optional[User]:
        return self.user

    async def get_default_user(self) -> User:
        return self.user

    async def _create_team(self, author: UserID, team: Team, org_id: OrgID) -> Team:
        return self.team

    async def get_team(self, team_id: TeamID) -> Optional[Team]:
        return self.team

    async def list_user_teams(self, user_id: UserID, org_id: Optional[OrgID]) -> List[Team]:
        return []

    async def _delete_team(self, team_id: TeamID):
        pass

    async def _list_entity_users(
        self, entity_type: EntityType, entity_id: EntityID, read_permission: Permission
    ) -> List[User]:
        return []

    async def _list_entity_users_with_roles(
        self, entity_type: EntityType, entity_id: EntityID, read_permission: Permission
    ) -> List[UserWithRoles]:
        return []

    async def _delete_org(self, org_id: OrgID):
        pass

    async def list_user_orgs(self, user_id: UserID):
        return []

    async def list_user_entity_permissions(
        self, user_id: UserID, entity_type: EntityType, entity_id: EntityID
    ) -> Set[Permission]:
        return set(Permission)

    async def list_user_entity_roles(
        self, user_id: UserID, entity_type: EntityType, entity_id: EntityID
    ) -> List[Tuple[EntityType, EntityID, Role]]:
        return [(entity_type, entity_id, await self.get_default_role(DefaultRole.OWNER, None))]

    async def list_roles(self, entity_type: Optional[EntityType]) -> List[Role]:
        return [await self.get_default_role(DefaultRole.OWNER, None)]

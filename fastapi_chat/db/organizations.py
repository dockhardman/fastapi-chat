from typing import TYPE_CHECKING, Literal, Optional, Sequence, Text

from fastapi_chat.schemas.organizations import (
    Organization,
    OrganizationCreate,
    OrganizationUpdate,
)
from fastapi_chat.schemas.pagination import Pagination
from fastapi_chat.utils.common import run_as_coro

if TYPE_CHECKING:
    from fastapi_chat.db._base import DatabaseBase


async def list_organizations(
    db: "DatabaseBase",
    *,
    organization_id: Optional[Text] = None,
    organization_ids: Optional[Sequence[Text]] = None,
    disabled: Optional[bool] = False,
    sort: Literal["asc", "desc"] = "asc",
    start: Optional[Text] = None,
    before: Optional[Text] = None,
    limit: Optional[int] = 10,
) -> Pagination[Organization]:
    return await run_as_coro(
        db.list_organizations,
        organization_id=organization_id,
        organization_ids=organization_ids,
        disabled=disabled,
        sort=sort,
        start=start,
        before=before,
        limit=limit,
    )


async def create_organization(
    db: "DatabaseBase",
    *,
    organization_create: OrganizationCreate,
    owner_id: Text,
) -> Optional[Organization]:
    return await run_as_coro(
        db.create_organization,
        organization_create=organization_create,
        owner_id=owner_id,
    )


async def update_organization(
    db: "DatabaseBase",
    *,
    organization_id: Text,
    organization_update: OrganizationUpdate,
) -> Optional[Organization]:
    return await run_as_coro(
        db.update_organization,
        organization_id=organization_id,
        organization_update=organization_update,
    )


async def retrieve_organization(
    db: "DatabaseBase",
    *,
    organization_id: Text,
) -> Optional[Organization]:
    return await run_as_coro(db.retrieve_organization, organization_id)


async def delete_organization(
    db: "DatabaseBase",
    *,
    organization_id: Text,
    soft_delete: bool = True,
) -> Optional[Organization]:
    return await run_as_coro(
        db.delete_organization, organization_id=organization_id, soft_delete=soft_delete
    )

from typing import Annotated, List, Literal, Optional, Text

from app.db.conversations import (
    create_conversation,
    delete_conversation,
    fake_conversations_db,
    list_conversations,
    retrieve_conversation,
    update_conversation,
)
from app.deps.oauth import RoleChecker
from app.schemas.conversations import (
    Conversation,
    ConversationCreate,
    ConversationUpdate,
)
from app.schemas.oauth import Role
from app.schemas.pagination import Pagination
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Path as QueryPath
from fastapi import Query, Response, status

router = APIRouter()


@router.post(
    "/conversations",
    dependencies=[Depends(RoleChecker([Role.ADMIN, Role.EDITOR]))],
    response_model=Conversation,
)
async def api_create_conversation(conversation_create: ConversationCreate):
    """Create a new conversation."""

    conversation = conversation_create.to_conversation()
    create_conversation(fake_conversations_db, conversation=conversation)
    return conversation


@router.get(
    "/conversations",
    dependencies=[Depends(RoleChecker([Role.ADMIN, Role.EDITOR]))],
    response_model=List[Conversation],
)
async def api_list_conversations(
    disabled: Optional[bool] = Query(default=None),
    sort: Literal["asc", "desc", 1, -1] = Query(default="asc"),
    start: Optional[Text] = Query(default=None),
    before: Optional[Text] = Query(default=None),
    limit: Optional[int] = Query(default=20),
) -> Pagination[Conversation]:
    """List conversations from the database."""

    return Pagination[Conversation].model_validate(
        list_conversations(
            fake_conversations_db,
            disabled=disabled,
            sort=sort,
            start=start,
            before=before,
            limit=limit,
        ).model_dump()
    )


@router.get(
    "/conversations/{conversation_id}",
    dependencies=[Depends(RoleChecker([Role.ADMIN, Role.EDITOR]))],
    response_model=Conversation,
)
async def api_get_conversation(
    conversation_id: Annotated[Text, QueryPath(...)],
):
    """Retrieve a conversation by ID."""

    conversation = retrieve_conversation(
        fake_conversations_db, conversation_id=conversation_id
    )
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return conversation


@router.put(
    "/conversations/{conversation_id}",
    dependencies=[Depends(RoleChecker([Role.ADMIN, Role.EDITOR]))],
    response_model=Conversation,
)
async def api_update_conversation(
    conversation_id: Annotated[Text, QueryPath(...)],
    conversation_update: ConversationUpdate,
):
    """Update an existing conversation."""

    conversation = update_conversation(
        fake_conversations_db,
        conversation_id=conversation_id,
        conversation_update=conversation_update,
    )
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.delete(
    "/conversations/{conversation_id}",
    dependencies=[Depends(RoleChecker([Role.ADMIN]))],
)
async def api_delete_conversation(
    conversation_id: Annotated[Text, QueryPath(...)],
    soft_delete: Annotated[bool, Query(default=True)],
):
    """Delete a conversation"""

    delete_conversation(
        fake_conversations_db, conversation_id=conversation_id, soft_delete=soft_delete
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

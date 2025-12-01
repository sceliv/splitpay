from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.group_service import (
    create_group,
    get_groups,
    add_member_to_group,
    remove_member_from_group,
)
from app.services.group_query_service import get_group_with_members
from app.schemas.group_schema import GroupCreate, AddMemberSchema, AddMemberByEmailSchema, GroupResponse
from app.core.exceptions import not_found
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("/", response_model=GroupResponse)
def create_new_group(
    data: GroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> GroupResponse:

    # 1. Crear grupo
    group = create_group(db, data, current_user.id)

    # 2. Agregar creador como miembro del grupo
    add_member_to_group(
        db,
        group.id,
        AddMemberSchema(
            user_id=current_user.id,
            role="admin"
        )
    )

    # 3. Obtener el grupo completo
    full = get_group_with_members(db, group.id)

    return GroupResponse(**full)

@router.get("/", response_model=list[GroupResponse])
def list_groups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # opcional para MVP
) -> list[GroupResponse]:

    groups = get_groups(db)
    result: list[GroupResponse] = []
    for g in groups:
        full = get_group_with_members(db, g.id)
        if full is not None:
            result.append(GroupResponse(**full))
    return result


@router.get("/{group_id}", response_model=GroupResponse)
def get_group_data(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> GroupResponse:

    group_with_members = get_group_with_members(db, group_id)
    if group_with_members is None:
        not_found("Group not found")
    return GroupResponse(**group_with_members)


@router.post("/{group_id}/add-member")
def add_member(group_id: int, data: AddMemberByEmailSchema, db: Session = Depends(get_db)):
    return add_member_to_group(db, group_id, data)

@router.delete("/{group_id}/remove-member/{user_id}")
def remove_member(
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_member_from_group(db, group_id, user_id)

from sqlalchemy.orm import Session
from app.models.group import Group
from app.models.group_member import GroupMember
from app.schemas.group_schema import GroupCreate, AddMemberSchema


def create_group(db: Session, data: GroupCreate, creator_id: int):
    group = Group(
        name=data.name,
        creator_id=creator_id,
        type=data.type,
        currency=data.currency
    )
    db.add(group)
    db.commit()
    db.refresh(group)
    return group



def get_group(db: Session, group_id: int) -> Group | None:
    return db.query(Group).filter(Group.id == group_id).first()


def get_groups(db: Session) -> list[Group]:
    return db.query(Group).all()


def add_member_to_group(db: Session, group_id: int, data):
    # Si viene email → buscar user_id
    user_id = None

    if hasattr(data, "email"):  # frontend enviará email
        user = db.query(User).filter(User.email == data.email).first()
        if not user:
            raise ValueError("El usuario no existe")
        user_id = user.id
        role = getattr(data, "role", "member")

    else:
        # Caso antiguo: venía user_id directo
        user_id = data.user_id
        role = data.role

    member = GroupMember(
        group_id=group_id,
        user_id=user_id,
        role=role,
    )

    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def get_group_members(db: Session, group_id: int) -> list[GroupMember]:
    return db.query(GroupMember).filter(GroupMember.group_id == group_id).all()


def remove_member_from_group(db: Session, group_id: int, user_id: int) -> GroupMember | None:
    member = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id,
        )
        .first()
    )

    if member:
        db.delete(member)
        db.commit()

    return member

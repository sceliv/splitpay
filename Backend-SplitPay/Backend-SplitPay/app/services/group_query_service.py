from sqlalchemy.orm import Session
from app.models.group import Group
from app.models.group_member import GroupMember


def get_group_with_members(db: Session, group_id: int) -> dict | None:
    """
    Devuelve la información del grupo junto con sus miembros,
    en una estructura compatible con GroupResponse.

    {
      "id": int,
      "name": str,
      "members": [{"user_id": int, "role": str}, ...]
    }
    """
    group = db.query(Group).filter(Group.id == group_id).first()
    if group is None:
        return None

    members = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == group_id)
        .all()
    )

    return {
        "id": group.id,
        "name": group.name,
        "members": [
            {"user_id": m.user_id, "role": m.role}
            for m in members
        ],
    }



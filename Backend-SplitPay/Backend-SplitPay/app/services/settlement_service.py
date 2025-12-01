from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.settlement import Settlement
from app.schemas.settlement_schema import SettlementCreate
from app.utils.file_upload import save_evidence


def create_settlement(db: Session, data: SettlementCreate, evidence_url: str | None = None) -> Settlement:
    s = Settlement(
        group_id=data.group_id,
        from_user=data.from_user,
        to_user=data.to_user,
        amount=data.amount,
        evidence_url=evidence_url,
        status="pending",
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


def validate_settlement(
    db: Session,
    settlement_id: int,
    file: UploadFile | None = None,
) -> Settlement | None:
    s = db.query(Settlement).filter(Settlement.id == settlement_id).first()
    if not s:
        return None

    # Si se recibe un archivo, lo guardamos y actualizamos la evidencia
    if file is not None:
        evidence_path = save_evidence(file, settlement_id)
        s.evidence_url = evidence_path

    s.status = "validated"
    db.commit()
    db.refresh(s)
    return s

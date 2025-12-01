from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.settlement_schema import SettlementCreate, SettlementResponse
from app.services.settlement_service import create_settlement, validate_settlement

router = APIRouter(prefix="/settlements", tags=["Settlements"])


@router.post("/", response_model=SettlementResponse)
def create_settlement_route(data: SettlementCreate, db: Session = Depends(get_db)):
    """
    Crea un registro de pago pendiente (sin evidencia aún).
    """
    return create_settlement(db, data)


@router.post("/{settlement_id}/validate", response_model=SettlementResponse)
def validate_payment_route(
    settlement_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Valida un pago y guarda la evidencia asociada.
    """
    return validate_settlement(db, settlement_id, file)

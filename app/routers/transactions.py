from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.transaction import TransaksiPenjualanCreate, TransaksiPenjualanResponse
from app.crud import crud_transaction
from app.dependencies import get_current_user # Dependency kita tadi
from app.models.user import User

router = APIRouter()

@router.post("/transactions", response_model=TransaksiPenjualanResponse)
def create_transaction(
    transaksi: TransaksiPenjualanCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Wajib Login!
):
    # Kita kirim current_user.id_user ke logic CRUD
    return crud_transaction.create_transaksi_penjualan(
        db=db, 
        transaksi=transaksi, 
        user_id=current_user.id_user
    )

@router.get("/transactions", response_model=List[TransaksiPenjualanResponse])
def read_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Wajib Login
):
    return crud_transaction.get_all_transaksi(db)
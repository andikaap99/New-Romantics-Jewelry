from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.transaction import TransaksiPenjualanCreate, TransaksiPenjualanResponse, TransaksiPembelianCreate, TransaksiPembelianResponse
from app.crud import crud_transaction
from app.dependencies import get_current_user # Dependency kita tadi
from app.models.user import User

router = APIRouter()

@router.post("/purchases", response_model=TransaksiPembelianResponse)
def create_purchase(
    transaksi: TransaksiPembelianCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Tetap butuh login biar aman
):
    return crud_transaction.create_pembelian(db, transaksi)

@router.get("/purchases", response_model=List[TransaksiPembelianResponse])
def read_purchases_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Tetap diproteksi login
):
    return crud_transaction.get_all_pembelian(db)


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
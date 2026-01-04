from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.crud.crud_user import get_user_by_username
from app.schemas.token import Token

router = APIRouter()

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), # Bawaan FastAPI buat form login
    db: Session = Depends(get_db)
):
    # 1. Cari user di DB
    user = get_user_by_username(db, username=form_data.username)
    
    # 2. Validasi: User ada? Password cocok?
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau Password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Kalau lolos, bikin Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, # Simpan username di dalam token
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
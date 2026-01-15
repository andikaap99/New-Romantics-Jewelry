# app/schemas/predict.py
from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    carat: float = Field(..., gt=0, description="Berat berlian")
    
    # Kita pakai angka 1-5 biar simpel (1: Fair, 5: Ideal)
    cut: int = Field(..., ge=1, le=5, description="Kualitas Potongan (1-5)")
    
    # Kita pakai angka 1-7 (1: J, 7: D - Paling putih)
    color: int = Field(..., ge=1, le=7, description="Warna (1-7)")
    
    # Kita pakai angka 1-8 (1: I1, 8: IF - Paling bening)
    clarity: int = Field(..., ge=1, le=8, description="Kejernihan (1-8)")

class PredictionResponse(BaseModel):
    estimated_price: float
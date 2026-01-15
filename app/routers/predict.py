from fastapi import APIRouter, HTTPException
from app.schemas.predict import PredictionInput, PredictionResponse
from app.ml_utils import predict_price

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict_diamond_price(input_data: PredictionInput):
    try:
        harga_prediksi = predict_price(
            input_data.carat,
            input_data.cut,
            input_data.color,
            input_data.clarity
        )
        
        return {"estimated_price": int(harga_prediksi*15000)} 
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memprediksi: {str(e)}")
import joblib
import os

# Path ke file model yang tadi kita generate
MODEL_PATH = os.path.join(os.path.dirname(__file__), "diamond_model.pkl")

_model = None

def get_model():
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
            print("Model ML berhasil di-load!")
        else:
            print("File model tidak ditemukan!")
            return None
    return _model

def predict_price(carat: float, cut: int, color: int, clarity: int):
    model = get_model()
    if not model:
        return 0
    
    # Prediksi (Input harus array 2D)
    prediction = model.predict([[carat, cut, color, clarity]])
    return max(0, float(prediction[0])) # Pastikan tidak minus
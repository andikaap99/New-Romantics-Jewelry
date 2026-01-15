from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.models import User, Kategori, Produk, TransaksiPembelian, TransaksiPenjualan, ProdukTerjual
from app.routers import users, products, auth, transactions, predict

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Dayamond")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, tags=["Users"])
app.include_router(products.router, tags=["Products"])
app.include_router(transactions.router, tags=["Transactions"])
app.include_router(predict.router, tags=["ML Prediction"])

@app.get("/")
def read_root():
    return {"message": "Server Berjalan!"}
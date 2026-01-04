from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.models import User, Kategori, Produk, TransaksiPembelian, TransaksiPenjualan, ProdukTerjual
from app.routers import users, products, auth, transactions

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Dayamond")

origins = [
    "http://localhost:3000",      # React default port
    "http://127.0.0.1:3000",      # Kadang browser pake IP ini
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Izinkan frontend React mengakses
    allow_credentials=True,
    allow_methods=["*"],          # Izinkan semua method (GET, POST, PUT, DELETE, dll)
    allow_headers=["*"],          # Izinkan semua header
)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, tags=["Users"])
app.include_router(products.router, tags=["Products"])
app.include_router(transactions.router, tags=["Transactions"])

@app.get("/")
def read_root():
    return {"message": "Server Berjalan!"}
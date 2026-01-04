# app/schemas/transaction.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# --- 1. Schema Kecil (Untuk Ambil Nama Produk dari Tabel Sebelah) ---
class ProdukMini(BaseModel):
    nama_produk: str
    harga: float  # Kita tampilin harganya sekalian biar lengkap
    
    class Config:
        from_attributes = True

# --- 2. Schema Detail Barang (Child) ---
class ProdukTerjualBase(BaseModel):
    id_produk: int
    jumlah: int

class ProdukTerjualCreate(ProdukTerjualBase):
    pass

class ProdukTerjualResponse(ProdukTerjualBase):
    # Field 'id' ini adalah ID detail transaksi (bukan ID produk)
    # id: int  <-- Opsional, kalau error 'field required' boleh dihapus/dikomentari
    
    # MAGIC DISINI: Field ini akan otomatis mengambil data dari relasi 'produk'
    produk: ProdukMini 

    class Config:
        from_attributes = True

# --- 3. Schema Header Transaksi (Parent) ---
class TransaksiPenjualanBase(BaseModel):
    nama_pembeli: Optional[str] = "Umum"
    no_hp_pembeli: Optional[str] = None

class TransaksiPenjualanCreate(TransaksiPenjualanBase):
    kode_penjualan: str
    detail_produk: List[ProdukTerjualCreate]

class TransaksiPenjualanResponse(TransaksiPenjualanBase):
    kode_penjualan: str
    tgl_transaksi: datetime
    # Ini akan berisi list produk + nama produknya
    detail_produk: List[ProdukTerjualResponse]

    class Config:
        from_attributes = True
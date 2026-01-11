# app/schemas/transaction.py
from pydantic import BaseModel, validator
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


class TransaksiPembelianCreate(BaseModel):
    # Opsi 1: Barang Lama (Cukup isi ID)
    id_produk: Optional[int] = None 
    
    # Opsi 2: Barang Baru (Wajib isi ini kalau ID kosong)
    nama_produk_baru: Optional[str] = None
    kode_kategori_baru: Optional[str] = None
    harga_jual_baru: Optional[float] = None # Harga jual ke pelanggan nanti
    
    # Field Wajib (Selalu ada)
    jumlah: int
    harga_beli: float # Harga modal dari supplier
    nama_penjual: Optional[str] = "Supplier Umum"
    no_hp_penjual: Optional[str] = None

    # Validasi: Kalau ID kosong, data baru wajib diisi
    @validator('nama_produk_baru')
    def check_new_product_data(cls, v, values):
        if not values.get('id_produk') and not v:
            raise ValueError('Jika ID Produk kosong (Barang Baru), Nama Produk wajib diisi!')
        return v

class TransaksiPembelianResponse(BaseModel):
    kode_pembelian: int
    tgl_transaksi: datetime
    nama_penjual: str
    jumlah: int
    produk: ProdukMini # Reuse schema produk mini biar keren ada namanya

    class Config:
        from_attributes = True
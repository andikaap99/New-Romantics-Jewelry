from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

class KategoriBase(BaseModel):
    nama_kategori: str

class KategoriCreate(KategoriBase):
    kode_kategori: str

class KategoriResponse(KategoriBase):
    kode_kategori: str
    
    class Config:
        from_attributes = True

class ProdukBase(BaseModel):
    nama_produk: str
    harga: Decimal = Field(..., ge=0, description="Harga dalam Rupiah")
    stok: int = Field(default=0, ge=0)
    kode_kategori: str

class ProdukCreate(ProdukBase):
    pass

class ProdukResponse(ProdukBase):
    id_produk: int

    class Config:
        from_attributes = True
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.product import KategoriCreate, KategoriResponse, ProdukCreate, ProdukResponse
from app.crud import crud_product

router = APIRouter()

# --- ENDPOINTS KATEGORI ---
@router.post("/categories", response_model=KategoriResponse)
def create_category(kategori: KategoriCreate, db: Session = Depends(get_db)):
    # Cek duplikat
    cek = crud_product.get_kategori_by_kode(db, kategori.kode_kategori)
    if cek:
        raise HTTPException(status_code=400, detail="Kode Kategori sudah ada")
    return crud_product.create_kategori(db=db, kategori=kategori)

@router.get("/categories", response_model=List[KategoriResponse])
def read_categories(db: Session = Depends(get_db)):
    return crud_product.get_all_kategori(db)

@router.put("/categories/{kode_kategori}", response_model=KategoriResponse)
def update_category_data(kode_kategori: str, kategori: KategoriCreate, db: Session = Depends(get_db)):
    updated_kategori = crud_product.update_kategori(db, kode_kategori, kategori)
    if not updated_kategori:
        raise HTTPException(status_code=404, detail="Kategori tidak ditemukan")
    
    return updated_kategori

@router.delete("/categories/{kode_kategori}")
def delete_category_data(kode_kategori: str, db: Session = Depends(get_db)):
    try:
        deleted_kategori = crud_product.delete_kategori(db, kode_kategori)
        if not deleted_kategori:
            raise HTTPException(status_code=404, detail="Kategori tidak ditemukan")
    except Exception as e:
        # Error terjadi jika kategori masih dipakai di tabel Produk
        raise HTTPException(status_code=400, detail="Gagal hapus: Kategori sedang dipakai oleh Produk!")
        
    return {"message": "Kategori berhasil dihapus"}


# --- ENDPOINTS PRODUK ---
@router.post("/products", response_model=ProdukResponse)
def create_product(produk: ProdukCreate, db: Session = Depends(get_db)):
    # Cek apakah kategorinya ada?
    cek_kategori = crud_product.get_kategori_by_kode(db, produk.kode_kategori)
    if not cek_kategori:
        raise HTTPException(status_code=404, detail="Kode Kategori tidak ditemukan")
    
    return crud_product.create_produk(db=db, produk=produk)

@router.get("/products", response_model=List[ProdukResponse])
def read_products(db: Session = Depends(get_db)):
    return crud_product.get_all_produk(db)

@router.put("/products/{product_id}", response_model=ProdukResponse)
def update_product_data(product_id: int, produk: ProdukCreate, db: Session = Depends(get_db)):
    # 1. Cek dulu apakah kategori baru valid?
    cek_kategori = crud_product.get_kategori_by_kode(db, produk.kode_kategori)
    if not cek_kategori:
        raise HTTPException(status_code=404, detail="Kode Kategori tidak ditemukan")

    # 2. Lakukan Update
    updated_produk = crud_product.update_produk(db, product_id, produk)
    if not updated_produk:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    
    return updated_produk

@router.delete("/products/{product_id}")
def delete_product_data(product_id: int, db: Session = Depends(get_db)):
    deleted_produk = crud_product.delete_produk(db, product_id)
    if not deleted_produk:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    
    return {"message": "Produk berhasil dihapus"}
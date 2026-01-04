from sqlalchemy.orm import Session
from app.models.product import Kategori, Produk
from app.schemas.product import KategoriCreate, ProdukCreate

# --- LOGIC KATEGORI ---
def get_kategori_by_kode(db: Session, kode_kategori: str):
    return db.query(Kategori).filter(Kategori.kode_kategori == kode_kategori).first()

def get_all_kategori(db: Session):
    return db.query(Kategori).all()

def create_kategori(db: Session, kategori: KategoriCreate):
    db_kategori = Kategori(
        kode_kategori=kategori.kode_kategori,
        nama_kategori=kategori.nama_kategori
    )
    db.add(db_kategori)
    db.commit()
    db.refresh(db_kategori)
    return db_kategori

# --- LOGIC PRODUK ---
def get_all_produk(db: Session):
    return db.query(Produk).all()

def create_produk(db: Session, produk: ProdukCreate):
    db_produk = Produk(
        kode_kategori=produk.kode_kategori,
        nama_produk=produk.nama_produk,
        harga=produk.harga,
        stok=produk.stok
    )
    db.add(db_produk)
    db.commit()
    db.refresh(db_produk)
    return db_produk

# 1. Update Kategori
def update_kategori(db: Session, kode_kategori: str, kategori_update: KategoriCreate):
    # Cari kategori berdasarkan kode lama
    db_kategori = get_kategori_by_kode(db, kode_kategori)
    if not db_kategori:
        return None
    
    # Update field (Kode boleh diganti, Nama boleh diganti)
    db_kategori.kode_kategori = kategori_update.kode_kategori
    db_kategori.nama_kategori = kategori_update.nama_kategori
    
    db.commit()
    db.refresh(db_kategori)
    return db_kategori

# 2. Delete Kategori
def delete_kategori(db: Session, kode_kategori: str):
    db_kategori = get_kategori_by_kode(db, kode_kategori)
    if not db_kategori:
        return None
    
    try:
        db.delete(db_kategori)
        db.commit()
        return db_kategori
    except Exception as e:
        db.rollback()
        # Biasanya error kalau kategori ini masih dipakai oleh Produk (Foreign Key)
        raise e

# 1. Cari Produk by ID (Helper)
def get_produk_by_id(db: Session, product_id: int):
    return db.query(Produk).filter(Produk.id_produk == product_id).first()

# 2. Update Produk
def update_produk(db: Session, product_id: int, produk_update: ProdukCreate):
    db_produk = get_produk_by_id(db, product_id)
    if not db_produk:
        return None
    
    # Update field satu per satu
    db_produk.nama_produk = produk_update.nama_produk
    db_produk.harga = produk_update.harga
    db_produk.stok = produk_update.stok
    db_produk.kode_kategori = produk_update.kode_kategori
    
    db.commit()
    db.refresh(db_produk)
    return db_produk

# 3. Delete Produk
def delete_produk(db: Session, product_id: int):
    db_produk = get_produk_by_id(db, product_id)
    if not db_produk:
        return None
    
    db.delete(db_produk)
    db.commit()
    return db_produk
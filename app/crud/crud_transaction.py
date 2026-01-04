from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.transaction import TransaksiPenjualan, ProdukTerjual
from app.models.product import Produk
from app.schemas.transaction import TransaksiPenjualanCreate

def create_transaksi_penjualan(db: Session, transaksi: TransaksiPenjualanCreate, user_id: int):
    # 1. Buat Header Transaksi
    db_transaksi = TransaksiPenjualan(
        kode_penjualan=transaksi.kode_penjualan,
        id_user=user_id, # Ambil otomatis dari Token
        nama_pembeli=transaksi.nama_pembeli,
        no_hp_pembeli=transaksi.no_hp_pembeli
    )
    db.add(db_transaksi)
    
    # 2. Loop Detail Barang (Cart)
    for item in transaksi.detail_produk:
        # A. Cek Produk ada atau tidak
        produk_db = db.query(Produk).filter(Produk.id_produk == item.id_produk).first()
        if not produk_db:
            db.rollback() # Batalkan semua jika error
            raise HTTPException(status_code=404, detail=f"Produk ID {item.id_produk} tidak ditemukan")
        
        # B. Cek Stok Cukup?
        if produk_db.stok < item.jumlah:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Stok {produk_db.nama_produk} tidak cukup! Sisa: {produk_db.stok}")
        
        # C. KURANGI STOK (Logic Penting!)
        produk_db.stok -= item.jumlah
        
        # D. Catat di tabel ProdukTerjual
        db_detail = ProdukTerjual(
            kode_penjualan=transaksi.kode_penjualan,
            id_produk=item.id_produk,
            jumlah=item.jumlah
        )
        db.add(db_detail)
    
    # 3. Simpan Perubahan (Commit)
    try:
        db.commit()
        db.refresh(db_transaksi)
        return db_transaksi
    except Exception as e:
        db.rollback()
        raise e
    
def get_all_transaksi(db: Session):
    # UPDATE DISINI: Ganti id_transaksi menjadi tgl_transaksi
    return db.query(TransaksiPenjualan).order_by(TransaksiPenjualan.tgl_transaksi.desc()).all()
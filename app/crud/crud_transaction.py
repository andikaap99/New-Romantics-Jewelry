from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.transaction import TransaksiPenjualan, ProdukTerjual, TransaksiPembelian
from app.models.product import Produk, Kategori
from app.schemas.transaction import TransaksiPenjualanCreate, TransaksiPembelianCreate

def create_pembelian(db: Session, pembelian: TransaksiPembelianCreate):
    final_id_produk = pembelian.id_produk

    # SKENARIO 1: BARANG BARU (Jika ID kosong/None)
    if not final_id_produk:
        # A. Validasi Data Baru
        if not all([pembelian.nama_produk_baru, pembelian.kode_kategori_baru, pembelian.harga_jual_baru]):
            raise HTTPException(status_code=400, detail="Untuk barang baru: Nama, Kategori, dan Harga Jual wajib diisi.")
        
        # B. Cek Kategori Valid Gak?
        cek_kategori = db.query(Kategori).filter(Kategori.kode_kategori == pembelian.kode_kategori_baru).first()
        if not cek_kategori:
            raise HTTPException(status_code=404, detail=f"Kategori {pembelian.kode_kategori_baru} tidak ditemukan. Buat kategori dulu!")

        # C. Buat Produk Baru di Database
        new_produk = Produk(
            nama_produk=pembelian.nama_produk_baru,
            kode_kategori=pembelian.kode_kategori_baru,
            harga=pembelian.harga_jual_baru, # Harga Jual Toko
            stok=0 # Stok awal 0, nanti ditambah di bawah
        )
        db.add(new_produk)
        db.flush() # Flush biar kita dapet ID-nya (new_produk.id_produk) tanpa commit dulu
        
        final_id_produk = new_produk.id_produk # Dapet ID baru!

    # SKENARIO 2: BARANG LAMA (Cek ID ada gak)
    produk_db = db.query(Produk).filter(Produk.id_produk == final_id_produk).first()
    if not produk_db:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

    # --- PROSES TRANSALSI (SAMA UNTUK BARU & LAMA) ---
    
    # 1. Catat History Pembelian
    db_pembelian = TransaksiPembelian(
        id_produk=final_id_produk,
        jumlah=pembelian.jumlah,
        harga_beli=pembelian.harga_beli, # Harga Beli Supplier
        nama_penjual=pembelian.nama_penjual,
        no_hp_penjual=pembelian.no_hp_penjual
    )
    db.add(db_pembelian)

    # 2. Update Stok (+ bertambah)
    produk_db.stok += pembelian.jumlah

    # 3. Commit Semua
    try:
        db.commit()
        db.refresh(db_pembelian)
        return db_pembelian
    except Exception as e:
        db.rollback()
        raise e

def get_all_pembelian(db: Session):
    # Mengambil semua data pembelian, urutkan dari yang terbaru
    return db.query(TransaksiPembelian).order_by(TransaksiPembelian.tgl_transaksi.desc()).all()


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
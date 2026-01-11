# app/models/transaction.py
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class TransaksiPembelian(Base):
    __tablename__ = "transaksi_pembelian"

    kode_pembelian = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_produk = Column(Integer, ForeignKey("produk.id_produk"), nullable=False)
    nama_penjual = Column(String(100)) # Nama Supplier
    no_hp_penjual = Column(String(20))
    harga_beli = Column(DECIMAL(18, 2), nullable=False) # Harga beli dari supplier
    
    # --- TAMBAHAN BARU ---
    jumlah = Column(Integer, nullable=False) # Berapa pcs yang dibeli?
    
    tgl_transaksi = Column(DateTime(timezone=True), server_default=func.now())

    produk = relationship("Produk", back_populates="pembelian")

class TransaksiPenjualan(Base):
    __tablename__ = "transaksi_penjualan"

    kode_penjualan = Column(String(50), primary_key=True, index=True)
    
    id_user = Column(Integer, ForeignKey("user.id_user"), nullable=False) 
    
    nama_pembeli = Column(String(100))
    no_hp_pembeli = Column(String(20))
    tgl_transaksi = Column(DateTime(timezone=True), server_default=func.now())

    # Hubungan ke User & Detail
    user = relationship("User", back_populates="transaksi_penjualan")
    detail_produk = relationship("ProdukTerjual", back_populates="transaksi_parent")

class ProdukTerjual(Base):
    __tablename__ = "produk_terjual"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_produk = Column(Integer, ForeignKey("produk.id_produk"), nullable=False)
    kode_penjualan = Column(String(50), ForeignKey("transaksi_penjualan.kode_penjualan"), nullable=False)
    jumlah = Column(Integer, nullable=False)

    # Hubungan balik
    produk = relationship("Produk", back_populates="detail_penjualan")
    transaksi_parent = relationship("TransaksiPenjualan", back_populates="detail_produk")
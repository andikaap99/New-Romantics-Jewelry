from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Kategori(Base):
    __tablename__ = "kategori"

    kode_kategori = Column(String(50), primary_key=True, index=True)
    nama_kategori = Column(String(100), nullable=False)

    produk = relationship("Produk", back_populates="kategori")


class Produk(Base):
    __tablename__ = "produk"

    id_produk = Column(Integer, primary_key=True, index=True, autoincrement=True)
    kode_kategori = Column(String(50), ForeignKey("kategori.kode_kategori"), nullable=False)
    nama_produk = Column(String(150), nullable=False)
    harga = Column(DECIMAL(18, 2), nullable=False) 
    stok = Column(Integer, default=0)

    kategori = relationship("Kategori", back_populates="produk")
    pembelian = relationship("TransaksiPembelian", back_populates="produk")
    detail_penjualan = relationship("ProdukTerjual", back_populates="produk")
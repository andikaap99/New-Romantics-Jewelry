from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(20), nullable=False, unique=True)
    nama_user = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)

    transaksi_penjualan = relationship("TransaksiPenjualan", back_populates="user")
from sqlalchemy import Column, Integer, BigInteger, String, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=False)
    balance = Column(Numeric, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())

    transactions = relationship("Transaction", back_populates='user')
    portfolio = relationship("Portfolio", back_populates='user')

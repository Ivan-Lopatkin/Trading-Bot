from src.database.database import Base
from sqlalchemy import Column, Integer, BigInteger, String, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    usernames = Column(String, nullable=False)
    balance = Column(Numeric, default=0)
    created_at = Column(TIMESTAMP, default='now()')


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(String, nullable=False)
    asset = Column(String, nullable=True)
    amount = Column(Numeric, nullable=False)
    price = Column(Numeric, nullable=True)
    total = Column(Numeric, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="transactions")

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, ForeignKey
from .base import Base


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

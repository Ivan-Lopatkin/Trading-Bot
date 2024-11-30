from .base import Base
from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship


class Portfolio(Base):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    asset = Column(String, nullable=False)
    quantity = Column(Numeric, nullable=False, default=0)
    value = Column(Numeric, nullable=True)

    user = relationship("User", back_populates="portfolio")

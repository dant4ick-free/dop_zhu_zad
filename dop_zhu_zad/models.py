from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    bonus = relationship("Bonus", back_populates="owner")
    transactions = relationship("Transaction", back_populates="owner")

class Bonus(Base):
    __tablename__ = "bonus"

    id = Column(Integer, primary_key=True, index=True)
    current_level = Column(String)
    current_cashback = Column(Float)
    next_level = Column(String)
    required_spending = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="bonus")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="transactions")

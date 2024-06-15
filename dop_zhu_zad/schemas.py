from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class BonusOut(BaseModel):
    current_level: str
    current_cashback: float
    next_level: str
    required_spending: float

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class TransactionCreate(BaseModel):
    amount: float

class TransactionOut(BaseModel):
    id: int
    amount: float

    class Config:
        orm_mode = True

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from .models import User, Bonus, Transaction
from .schemas import UserCreate, TransactionCreate
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "yoursecretkey"
ALGORITHM = "HS256"

LEVELS = [
    {"level": "bronze", "cashback": 1.0, "next_level": "silver", "required_spending": 1000.0},
    {"level": "silver", "cashback": 2.0, "next_level": "gold", "required_spending": 5000.0},
    {"level": "gold", "cashback": 3.0, "next_level": "platinum", "required_spending": 10000.0},
    {"level": "platinum", "cashback": 5.0, "next_level": None, "required_spending": None},
]

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Создаем запись о бонусах
    db_bonus = Bonus(
        current_level=LEVELS[0]["level"],
        current_cashback=LEVELS[0]["cashback"],
        next_level=LEVELS[0]["next_level"],
        required_spending=LEVELS[0]["required_spending"],
        owner_id=db_user.id
    )
    db.add(db_bonus)
    db.commit()
    db.refresh(db_bonus)

    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_bonus(db: Session, user_id: int):
    return db.query(Bonus).filter(Bonus.owner_id == user_id).first()

def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = Transaction(amount=transaction.amount, owner_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    update_bonus_level(db, user_id)
    return db_transaction

def update_bonus_level(db: Session, user_id: int):
    user_bonus = get_bonus(db, user_id)
    user_transactions = db.query(Transaction).filter(Transaction.owner_id == user_id).all()
    total_spent = sum(transaction.amount for transaction in user_transactions)

    for level in LEVELS:
        if user_bonus.current_level == level["level"] and total_spent >= user_bonus.required_spending:
            next_level = next((lvl for lvl in LEVELS if lvl["level"] == level["next_level"]), None)
            if next_level:
                user_bonus.current_level = next_level["level"]
                user_bonus.current_cashback = next_level["cashback"]
                user_bonus.next_level = next_level["next_level"]
                user_bonus.required_spending = next_level["required_spending"]
                db.commit()
                db.refresh(user_bonus)
            break

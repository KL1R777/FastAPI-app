import datetime

import jwt
from passlib.context import CryptContext
from typing_extensions import deprecated

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, "abc", "HS256")
    return encoded_jwt

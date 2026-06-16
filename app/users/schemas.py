from pydantic import BaseModel, EmailStr, ConfigDict


class SRegisterUser(BaseModel):
    model_config = ConfigDict(strict=True)
    name: str
    email: EmailStr
    password: str

class SLoginUser(BaseModel):
    model_config = ConfigDict(strict=True)
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    username: str
    password: bytes
    email: EmailStr








from pydantic import BaseModel, EmailStr


class CheckUser(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

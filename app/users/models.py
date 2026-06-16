from sqlalchemy.orm import Mapped, mapped_column

from app.databases.base import Base
from app.databases.dao import BaseDAO


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password : Mapped[str] = mapped_column(nullable=False, onupdate=True)


class UsersDAO(BaseDAO):
    model = Users
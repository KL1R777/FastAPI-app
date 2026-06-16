from sqlalchemy import ForeignKey

from app.databases.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from app.databases.dao import BaseDAO



class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)


class CategoryDAO(BaseDAO):
    model = Category


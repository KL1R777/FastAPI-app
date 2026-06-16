from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.databases.base import Base
from app.databases.dao import BaseDAO


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    completed: Mapped[bool] = mapped_column(default=False, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), default=None, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)


class TasksDAO(BaseDAO):
    model = Tasks

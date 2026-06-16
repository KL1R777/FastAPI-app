from app.databases.database import async_session_maker
from sqlalchemy import select




class BaseDAO:

    model = None

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            res = await session.execute(query)

            return res.scalars().all()


    @classmethod
    async def find_one_or_none(cls, **data):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**data)
            res = await session.execute(query)

            return res.scalars().one_or_none()

    @classmethod
    async def find_all_by_filter(cls, **data):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**data)
            res = await session.execute(query)

            return res.scalars().all()







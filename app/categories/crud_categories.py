from app.categories.models import Category
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update
from app.categories.models import CategoryDAO
from app.categories.schemas import SCategory
from app.databases.dependency_db import get_db
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/categories", tags=["Категории задач"])


@router.post("/create_category", status_code=status.HTTP_201_CREATED)
async def create_category(data: SCategory, db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
    existing_category = await CategoryDAO.find_one_or_none(title=data.title, user_id=current_user.id)

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail="Category is was created"
        )

    query = insert(Category).values(title=data.title, user_id=current_user.id)
    await db.execute(query)
    await db.commit()

@router.put("/update_category")
async def update_category(begin_category: str,data: SCategory, db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
    existing_category = await CategoryDAO.find_one_or_none(title=begin_category, user_id=current_user.id)

    if not existing_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category is not created"
        )

    updation = update(Category).values(title=data.title).where(Category.user_id == current_user.id)
    updation = await db.execute(updation)
    await db.commit()

    return {
        "message": "success",
        "updated_category": True
    }


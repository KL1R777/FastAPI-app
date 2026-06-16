import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from app.categories.models import CategoryDAO
from app.categories.schemas import SCategory
from app.databases.dependency_db import get_db
from app.tasks.models import Tasks, TasksDAO
from app.tasks.schemas import SCreateTask, UpdateTaskPartial, UpdateTaskFull
from app.users.dependencies import get_current_user
from app.users.models import Users
from fastapi_cache.decorator import cache
router = APIRouter(prefix="/tasks", tags=["Tasks"])



@router.get("/get_all_tasks")
@cache(expire=60)
async def get_tasks(db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
    query = select(Tasks).where(Tasks.user_id==current_user.id)
    res = await db.execute(query)
    return res.scalars().all()

@router.post("/create_task")
@cache(expire=60)
async def add_task(data: SCreateTask, db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
    insertion = insert(Tasks).values(title=data.title, completed=data.completed, user_id=current_user.id)
    insertion = await db.execute(insertion)
    await db.commit()
    return {
        "message": "sucess",
        "task data": data
    }
@router.put("/add_or_update_category_for_task")
async def add_category_for_task(task_title: str, data_category: SCategory,  db: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)):
    category = await CategoryDAO.find_one_or_none(title=data_category.title)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category was not found"
        )
    task = await TasksDAO.find_one_or_none(user_id=current_user.id, title=task_title)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No found task with this title"
        )

    updation = update(Tasks).where(Tasks.user_id==current_user.id, Tasks.title==task_title).values(category_id=category.id)
    await db.execute(updation)
    await db.commit()







@router.put("/update_task_full")
async def update_task_full(begin_title: str, data: UpdateTaskFull,current_user: Users = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await TasksDAO.find_one_or_none(user_id=current_user.id, title=begin_title)
    category = await CategoryDAO.find_one_or_none(title=data.category)

    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category was not found"
        )

    updation = update(Tasks).values(title=data.title, completed=data.completed,category_id=category.id, user_id=current_user.id).where(Tasks.user_id==current_user.id, Tasks.id==res.id)
    updation = await db.execute(updation)
    await db.commit()

    return {
        "message": "success",
        "updated task data": data
    }


@router.patch("/update_task_partial")
async def update_task_partial(begin_title: str, data: UpdateTaskPartial, current_user: Users = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    existing_task = await TasksDAO.find_one_or_none(title=begin_title, user_id=current_user.id)


    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    category_id = None
    if data.category is not None:
        category = await CategoryDAO.find_one_or_none(title=data.category)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category was not found"
            )
        category_id = category.id
    data.category = category_id

    if data.title is not None:
        updation = update(Tasks).values(title=data.model_dump()["title"]).where(Tasks.id == existing_task.id)
        updation = await db.execute(updation)

        await db.commit()
    if data.completed is not None:
        updation = update(Tasks).values(completed=data.model_dump()["completed"]).where(Tasks.id == existing_task.id)
        updation = await db.execute(updation)

        await db.commit()
    if data.category is not None:
        updation = update(Tasks).values(category_id=data.model_dump()["category"]).where(Tasks.id == existing_task.id)
        updation = await db.execute(updation)

        await db.commit()


    return {
        "message": "sucess",
        "updated partial task data": True
    }





@router.delete("/delete_task", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(begin_title: str, current_user: Users = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> None:
    query = delete(Tasks).where(Tasks.user_id==current_user.id, Tasks.title==begin_title)
    res = await db.execute(query)
    await db.commit()



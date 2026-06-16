
from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from fastapi_cache.decorator import cache
from app.auth.utils import get_password_hash, verify_password, create_access_token
from app.users.dependencies import get_current_user
from app.users.models import UsersDAO
from app.databases.dependency_db import get_db
from app.users.models import Users
from app.users.schemas import SRegisterUser, SLoginUser

router = APIRouter(prefix="/auth", tags=['Регистрация & Юзеры'])

@router.post("/registration")
async def register_user(user_data: SRegisterUser, db: AsyncSession = Depends(get_db)):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользовать уже авторизован"
        )
    hasshed_password = get_password_hash(user_data.password)

    query = insert(Users).values(name=user_data.name, email=user_data.email, password=hasshed_password)
    await db.execute(query)
    await db.commit()

@router.post("/login")
async def login_user(response: Response,user_data: SLoginUser, db: AsyncSession = Depends(get_db)):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user login or password"
        )

    is_verifided = verify_password(user_data.password, existing_user.password)
    if not is_verifided:
        raise HTTPException(
            status_code=status.HTTP_401_FORBIDDEN,
            detail="Incorrect user login or password"
        )
    access_token = create_access_token({"sub": str(existing_user.id)})
    response.set_cookie("user_access_token",access_token, httponly=True)
    return access_token



@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("user_access_token")


@cache(expire=30)
@router.get("/me")
async def read_user_me(current_user: Users = Depends(get_current_user)):
    return current_user



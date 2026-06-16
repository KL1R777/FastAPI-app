import datetime

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError

from app.users.models import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return token

async def get_current_user(token: str = Depends(get_token)):

    try:
        payload = jwt.decode(
            token, "abc", "HS256"
        )
        expire: str = payload.get("exp")
        if (not expire) or (int(expire) < datetime.datetime.utcnow().timestamp()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        user_id: str = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        user = await UsersDAO.find_one_or_none(id=int(user_id))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        return user

    except JWTError:
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                      detail="Я хз лол, может ошибка формата токена"
                      )



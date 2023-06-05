from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app import database, models
from app.crud.crud import user_crud

from .jwt_handler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/signin')


async def authenticate(
    session: Annotated[database.AsyncSession,
                       Depends(database.get_async_session)],
    token: Annotated[str, Depends(oauth2_scheme)]
) -> models.User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=('Для получения доступа авторизуйтейсь '
                    'и добавьте токен в запрос.'))
    decoded_token = verify_access_token(token)
    user = await user_crud.get(
        obj_id=decoded_token['user_id'],
        session=session)
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=('Пользователь неактивен.'))
    return user


async def check_superuser(
    user: Annotated[models.User, Depends(authenticate)]
) -> bool:
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Недостаточно прав для операции')
    return True

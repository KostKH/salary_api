from .jwt_handler import verify_access_token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app import database
from app.crud.crud import user_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/signin')


async def authenticate(token: str = Depends(oauth2_scheme)) -> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Sign in for access')
    decoded_token = verify_access_token(token)
    return decoded_token['user_id']


async def check_superuser(
    session: database.AsyncSession = Depends(database.get_async_session),
    token: str = Depends(oauth2_scheme)
) -> bool:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sign in for access")
    decoded_token = verify_access_token(token)
    user_to_check = await user_crud.get(
        obj_id=decoded_token['user_id'],
        session=session)
    if not user_to_check or not user_to_check.is_superuser:
        raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized",
                )
    return True
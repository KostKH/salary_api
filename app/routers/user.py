"""Роутеры для едпойнтов юзера."""
from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas, database
from app.crud.crud import user_crud
from app.auth.hash_password import HashPassword
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.jwt_handler import verify_access_token, create_access_token
router = APIRouter()
hash_password = HashPassword()

@router.get(
    path='/',
    summary='Посмотреть всех юзеров',
    response_model=list[schemas.User])
async def get_all_users(
    session: database.AsyncSession = Depends(database.get_async_session)
) -> list[schemas.User]:
    return await user_crud.get_all(session=session)


@router.post(
    path='/',
    summary='создание юзера',
    response_model=schemas.User,
    response_model_exclude_none=True)
async def create_user(
    new_user: schemas.UserCreate,
    session: database.AsyncSession = Depends(database.get_async_session),
) -> schemas.User:
    hashed_password = hash_password.create_hash(new_user.password)
    new_user.password = hashed_password
    created_user = await user_crud.create(
        new_obj=new_user,
        session=session)
    return created_user


@router.post(
    path='/signin',
    response_model=schemas.TokenResponse)
async def sign_user_in(
    user: OAuth2PasswordRequestForm = Depends(),
    session: database.AsyncSession = Depends(database.get_async_session),
    ) -> dict:
    user_exists = await user_crud.get_by_field(
        required_field='username',
        value=user.username,
        session=session)
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден.")
    if not hash_password.verify_hash(user.password, user_exists.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid details passed.")
    access_token = create_access_token(user_exists.id)
    return {
        'access_token': access_token,
        'token_type': 'Bearer'
    }

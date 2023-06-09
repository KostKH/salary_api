"""Сборник базовых операций CRUD."""
from typing import Any, Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from api import database, schemas

ModelType = TypeVar('ModelType', bound=database.Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=schemas.BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=schemas.BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс с операциями CRUD."""

    def __init__(
        self,
        model: Type[ModelType]
    ) -> None:
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: database.AsyncSession
    ) -> ModelType | None:
        """Метод получает объект из БД по `id`."""
        return await session.get(self.model, obj_id)

    async def get_all(
        self,
        session: database.AsyncSession
    ) -> list[ModelType]:
        """Метод получает все объекты из запрошенной таблицы."""
        objects = await session.scalars(select(self.model))
        return objects.all()

    async def get_by_field(
        self,
        required_field: str,
        value: Any,
        session: database.AsyncSession,
        one_obj: bool = True
    ) -> ModelType | list[ModelType]:
        """Метод находит объекты по значению указанного поля."""
        field = getattr(self.model, required_field, None)
        if field is None:
            raise AttributeError(
                f'Поле {required_field} отсуствует в таблице'
            )
        query = select(self.model).where(field == value)
        if one_obj:
            return await session.scalar(query.limit(1))
        some_objs = await session.scalars(query)
        return some_objs.all()

    async def create(
        self,
        new_obj: CreateSchemaType,
        session: database.AsyncSession,
    ) -> ModelType:
        """Метод создаёт запись в БД."""
        new_obj = new_obj.dict()
        new_obj = self.model(**new_obj)
        session.add(new_obj)
        await session.commit()
        await session.refresh(new_obj)
        return new_obj

    async def update(
        self,
        obj: ModelType,
        session: database.AsyncSession,
        update_data: UpdateSchemaType,
    ) -> ModelType:
        """Метод обновляет запись указанного объекта в БД."""
        obj_data = jsonable_encoder(obj)
        update_data = update_data.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(obj, field, update_data[field])
        await session.commit()
        await session.refresh(obj)
        return obj

    async def remove(
        self,
        obj: database.Base,
        session: database.AsyncSession
    ) -> ModelType:
        """Метод удаляет запись из БД."""
        await session.delete(obj)
        await session.commit()
        return obj

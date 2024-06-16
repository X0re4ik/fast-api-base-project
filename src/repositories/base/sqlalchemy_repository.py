from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import Base

from .base_repository import AbstractRepository

ModelType = TypeVar("ModelType", bound=Base)
Payload = TypeVar("Payload")


class SqlAlchemyRepository(AbstractRepository, Generic[ModelType]):

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.session = session
        self.model = model
        
    async def commit(self):
        return await self.session.commit()

    async def create(self, data: Payload) -> ModelType:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def update(self, data: Payload, **filters) -> ModelType:
        statement = update(self.model).values(**data).filter_by(**filters).returning(self.model)
        res = await self.session.execute(statement)
        await self.session.flush()
        return res.scalar_one()

    async def delete(self, **filters) -> None:
        await self.session.execute(delete(self.model).filter_by(**filters))
        await self.session.flush()

    async def get(self, id: int):
        statement = select(self.model).filter_by(id=id)
        row = await self.session.execute(statement)
        return row.unique().scalars().first()
    
    async def get_single(self, **filters) -> Optional[ModelType]:
        statement = select(self.model).filter_by(**filters)
        row = await self.session.execute(statement)
        return row.unique().scalars().first()
    
    async def get_or_create(self,  default={}, **filters) -> Tuple[ModelType, bool]:
        instance = await self.get_single(**filters)
        if instance is None:
            instance = await self.create({
                **filters,
                **default,
            })
            return (instance, True)
        return (instance, False)
    
    async def update_or_create(self, default={}, **filters) -> Tuple[ModelType, bool]:
        instance, created = await self.get_or_create(default, **filters)
        if created:
            return instance
        instance = await self.update(default, **filters)
        return (instance, created)
        
        
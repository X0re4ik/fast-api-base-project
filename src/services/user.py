
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from settings import db_helper
from src.repositories.user import UserUnitOfWork
from src.schemes.user import UserConfirmSchema, UserCreateSchema


class UserService:
    
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self.session_factory = session_factory
    
    async def create_or_update(self, model: UserCreateSchema):
        async with UserUnitOfWork(self.session_factory) as uof:
            user, _ = await uof.user.get_or_create(
                phone=model.phone,
                default=model.model_dump()
            )
            
            secret, _ = await uof.secret.get_or_create(
                user_id=user.id,
                default={ "secret": "3434" }
            )
            return user
    
    async def reissue_secret(self, user_id: int):
        async with UserUnitOfWork(self.session_factory) as uof:
            user = uof.user.get(user_id)
            secret, _ = await uof.secret.update_or_create(
                user_id=user.id,
                default={ "secret": "3434" }
            )
            return True
    
    async def activate(self, model: UserConfirmSchema) -> bool:
        async with UserUnitOfWork(self.session_factory) as uof:
            user = await uof.user.get_single(phone=model.phone)
            result = await uof.secret.is_valid(user.id, model.secret)
            if result is True:
                await uof.user.update(
                    {"is_active": True}, 
                    id=user.id
                )
            return result
    
    async def deactivate(self, user_id: int) -> bool:
        async with UserUnitOfWork(self.session_factory) as uof:
            await uof.user.update({ "is_activate": False }, user_id=user_id)
            await uof.secret.delete(user_id=user_id)
            return True
        
    async def is_active(self, **filters):
        async with UserUnitOfWork(self.session_factory) as uof:
            return uof.user.is_active(filters)

user_service = UserService(
    db_helper.get_db_session
)
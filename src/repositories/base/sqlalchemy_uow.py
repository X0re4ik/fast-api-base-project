import abc

from .base_uow import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        async with self.session_factory() as session:
            self.session = session
            self._repositories_init(session)
            return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        if exc_type is not None:
            await self.rollback()
        await self.commit()
        await self.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()
    
    @abc.abstractmethod
    def _repositories_init(self, session):
        pass
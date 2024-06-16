from sqlalchemy import text

from .base import sqlalchemy_models

tables_names = [
    sql_sqlalchemy_model.__tablename__
    for sql_sqlalchemy_model in sqlalchemy_models
]

async def async_clear_db(db_session_manager):
    async with db_session_manager() as session:
        for table_name in tables_names:
            await session.execute(text(f'TRUNCATE TABLE {table_name} CASCADE RESTART IDENTITY'))
        await session.commit()
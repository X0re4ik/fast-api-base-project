import asyncio

import pytest
import pytest_asyncio
from mixer.backend.sqlalchemy import mixer as _mixer

from migrations.clear_db import async_clear_db
from src.settings import db_helper


@pytest.fixture
def db_session_manager():
    return db_helper.get_db_session

@pytest.fixture
def mixer():
    return _mixer


@pytest_asyncio.fixture(autouse=True, scope="function")
async def clean_database(event_loop, db_session_manager):
    await async_clear_db(db_session_manager)
    yield
    await async_clear_db(db_session_manager)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
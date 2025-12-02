import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import get_db
from app.core.config import settings

# Use a separate test database in real scenarios, or mock
# For this setup, we will mock the DB session or use the dev DB carefully (not recommended for prod)
# Ideally: override settings.SQLALCHEMY_DATABASE_URI to a test DB.

@pytest.fixture
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

import asyncio
from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from config import TEST_DB_PATH
from main import app
from models.base import Base, DBConnect, e_store_db
from models.product import ProductModel


test_db = DBConnect(url=TEST_DB_PATH, echo=False)
app.dependency_overrides[e_store_db.session_dependency] = test_db.session_dependency


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_db():
    async with test_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000/"
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="session")
async def product_for_orders():
    async with test_db.async_session() as session:
        test_product: ProductModel = ProductModel(
            title="Clock",
            description="CASIO",
            price=1000,
            quantity=50000,
        )
        session.add(test_product)
        await session.commit()

    return test_product

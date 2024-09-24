"""Модуль для тестов endpoint`ов связанных с моделью `Product`"""

import pytest
from httpx import AsyncClient
from sqlalchemy import select, desc

from .conftest import test_db
from models.product import ProductModel


@pytest.mark.asyncio(loop_scope="session")
async def test_get_products(ac: AsyncClient):
    """Тест на получение списка продуктов"""

    product_quantity = 3

    async with test_db.async_session() as session:
        for num in range(product_quantity):
            test_product = ProductModel(
                title=f"Moto{num}",
                description="FooBar",
                price=777,
                quantity=3,
            )
            session.add(test_product)

        await session.commit()
    response = await ac.get("/api/products/")

    assert response.status_code == 200
    assert len(response.json()) == product_quantity + 1


@pytest.mark.asyncio(loop_scope="session")
async def test_post_product(ac: AsyncClient):
    """Тест на создание нового продукта"""

    response = await ac.post(
        "/api/products/",
        json={
            "title": "Auto",
            "description": "FooBar",
            "price": 777,
            "quantity": 3,
        },
    )

    async with test_db.async_session() as session:
        query = select(ProductModel).order_by(desc(ProductModel.id)).limit(1)
        result = await session.scalar(query)

    assert response.status_code == 201
    assert response.json()["id"] == result.id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_id(ac: AsyncClient):
    """Тест на получение продукта по id"""

    async with test_db.async_session() as session:
        test_product: ProductModel = ProductModel(
            title="Game",
            description="FooBar",
            price=777,
            quantity=333,
        )
        session.add(test_product)
        await session.commit()
    response = await ac.get(f"/api/products/{test_product.id}")

    assert response.status_code == 200
    assert (
        test_product.id == response.json()["id"]
    ), "Запрашиваемый id не совпадает с возвращаемым id"


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_by_id(ac: AsyncClient):
    """Тест на обновление продукта по id"""

    async with test_db.async_session() as session:
        test_product: ProductModel = ProductModel(
            title="Book",
            description="FooBar",
            price=10,
            quantity=333,
        )
        session.add(test_product)
        await session.commit()

    response = await ac.put(
        f"/api/products/{test_product.id}",
        json={
            "title": "Comix",
            "description": "Egg",
            "price": 777,
            "quantity": 20,
        },
    )

    assert response.status_code == 200
    assert (
        test_product.id == response.json()["id"]
    ), "Запрашиваемый id не совпадает с возвращаемым id"
    assert (
        test_product.title != response.json()["title"]
    ), "Запрашиваемый title совпадает со старым title"


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product_by_id(ac: AsyncClient):
    """Тест на удаление продукта по id"""

    async with test_db.async_session() as session:
        test_product: ProductModel = ProductModel(
            title="Phone",
            description="FooBar",
            price=1000,
            quantity=2,
        )
        session.add(test_product)
        await session.commit()

        query = select(ProductModel).order_by(desc(ProductModel.id)).limit(1)
        result = await session.scalar(query)
        assert result.id == test_product.id

        response = await ac.delete(f"/api/products/{result.id}")
        result = await session.scalar(query)
        assert result is None or result.id != test_product.id

    assert response.status_code == 204

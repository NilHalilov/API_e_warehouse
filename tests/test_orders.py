"""Модуль для тестов endpoint`ов связанных с моделью `Order`"""

import pytest
from httpx import AsyncClient
from sqlalchemy import select, desc

from .conftest import test_db
from models.order import OrderModel, OrderStatus


@pytest.mark.asyncio(scope="session")
async def test_get_orders(ac: AsyncClient):
    """Тест на получение списка заказов"""

    order_quantity = 3

    async with test_db.async_session() as session:

        for num in range(order_quantity):
            test_order: OrderModel = OrderModel(
                status=OrderStatus.sent,
            )
            session.add(test_order)

        await session.commit()
    response = await ac.get("/api/orders/")

    assert response.status_code == 200
    assert len(response.json()) == order_quantity


@pytest.mark.asyncio(scope="session")
async def test_post_order(ac: AsyncClient, product_for_orders):
    """Тест на создание нового заказа"""

    product_count = 20
    response = await ac.post(
        f"/api/orders/?product_id={product_for_orders.id}&product_count={product_count}&order_status={OrderStatus.sent.value}"
    )

    async with test_db.async_session() as session:
        query = select(OrderModel).order_by(desc(OrderModel.id)).limit(1)
        result = await session.scalar(query)

    assert response.status_code == 201
    assert response.json()["id"] == result.id
    assert response.json()["products_details"][0]["product_count"] == product_count
    assert len(response.json()["products_details"]) == 1


@pytest.mark.asyncio(scope="session")
async def test_add_product_in_order(ac: AsyncClient, product_for_orders):
    """Тест на добавление продукта в заказ"""

    async with test_db.async_session() as session:
        test_order = OrderModel(
            status=OrderStatus.sent,
        )
        session.add(test_order)
        await session.commit()

    response = await ac.post(
        f"/api/orders/{test_order.id}/product?product_id={product_for_orders.id}&product_count={20}"
    )

    assert response.status_code == 201
    assert len(response.json()["products_details"]) == 1
    assert response.json()["id"] == test_order.id
    assert (
        response.json()["products_details"][0]["product"]["title"]
        == product_for_orders.title
    )


@pytest.mark.asyncio(scope="session")
async def test_get_order_by_id(ac: AsyncClient):
    """Тест на получение заказа по id"""

    async with test_db.async_session() as session:
        test_order: OrderModel = OrderModel(
            status=OrderStatus.sent,
        )
        session.add(test_order)
        await session.commit()

    response = await ac.get(f"/api/orders/{test_order.id}")

    assert response.status_code == 200
    assert (
        test_order.id == response.json()["id"]
    ), "Запрашиваемый id не совпадает с возвращаемым id"


@pytest.mark.asyncio(scope="session")
async def test_update_order_status(ac: AsyncClient):
    """Тест на обновление статуса заказа по id"""

    async with test_db.async_session() as session:
        test_order: OrderModel = OrderModel(
            status=OrderStatus.in_process,
        )
        session.add(test_order)
        await session.commit()

    response = await ac.patch(
        f"/api/orders/{test_order.id}/status?order_status={OrderStatus.sent.value}"
    )

    assert response.status_code == 200
    assert (
        test_order.id == response.json()["id"]
    ), "Запрашиваемый id не совпадает с возвращаемым id"
    assert (
        test_order.status.value != response.json()["status"]
    ), "Запрашиваемый status совпадает со старым status"

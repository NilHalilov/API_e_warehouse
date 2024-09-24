"""Модуль для описания endpoint`ов к модели `Order` """

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import e_store_db
from . import crud
from .schemas import OrderBase, Order
from models.order import OrderStatus


router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def post_order(
    product_id: int,
    product_count: int,
    order_status: OrderStatus,
    session: AsyncSession = Depends(e_store_db.session_dependency),
):
    """
    Endpoint для создания нового заказа
    * :param product_id: id товара добавляемого в новый заказ
    * :param product_count: количество товара добавляемого в новый заказ
    * :param order_status: статус нового заказа
    * :param session: объект сессии
    """
    return await crud.create_order(
        session=session,
        product_id=product_id,
        product_count=product_count,
        order_status=order_status,
    )


@router.post(
    "/{order_id}/product", response_model=Order, status_code=status.HTTP_201_CREATED
)
async def post_product_in_order(
    order_id: Annotated[int, Path(..., ge=1)],
    product_id: int,
    product_count: int,
    session: AsyncSession = Depends(e_store_db.session_dependency),
):
    """
    Endpoint для добавления товара в существующий заказ
    * :param order_id: id заказa в который нужно добавить товар
    * :param product_id: id товара добавляемого в существующий заказ
    * :param product_count: количество товара добавляемого в существующий заказ
    * :param session: объект сессии
    """
    return await crud.add_product_in_order(
        session=session,
        product_id=product_id,
        order_id=order_id,
        product_count=product_count,
    )


@router.get("/", response_model=list[Order], status_code=status.HTTP_200_OK)
async def get_orders(session: AsyncSession = Depends(e_store_db.session_dependency)):
    """
    Endpoint для получения списка заказов
    * :param session: объект сессии
    """
    return await crud.read_orders(session=session)


@router.get("/{id}", response_model=Order, status_code=status.HTTP_200_OK)
async def get_order_by_id(
    id: Annotated[int, Path(..., ge=1)],
    session: AsyncSession = Depends(e_store_db.session_dependency),
):
    """
    Endpoint для получения информации о заказе по `id`
    * :param id: id искомого заказа
    * :param session: объект сессии
    """
    return await crud.read_order(session=session, order_id=id)


@router.patch("/{id}/status", response_model=OrderBase, status_code=status.HTTP_200_OK)
async def update_order_status(
    id: Annotated[int, Path(..., ge=1)],
    order_status: OrderStatus,
    session: AsyncSession = Depends(e_store_db.session_dependency),
):
    """
    Endpoint для обновления статуса заказа по `id`
    * :param id: id обновляемого заказа
    * :param order_status: новый статус заказа
    * :param session: объект сессии
    """
    return await crud.change_order_status(
        session=session,
        order_id=id,
        order_status=order_status,
    )

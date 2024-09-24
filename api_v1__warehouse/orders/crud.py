"""Модуль для описания CRUD-действий модели `Order`"""

from fastapi import HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import OrderModel, OrderItemModel, OrderStatus
from ..products.crud import read_product_by_id


async def create_order(
    session: AsyncSession,
    product_id: int,
    product_count: int,
    order_status: OrderStatus,
) -> OrderModel:
    """
    Создание в БД записи о новом заказе
    :param session: объект сессии
    :param product_id: id товара добавляемого в новый заказ
    :param product_count: количество товара добавляемого в новый заказ
    :param order_status: статус нового заказа
    """
    product = await read_product_by_id(session=session, product_id=product_id)

    if product.quantity >= product_count:

        product.quantity -= product_count
        order = OrderModel(status=order_status)
        session.add(order)
        order.products_details.append(
            OrderItemModel(
                product=product,
                product_count=product_count,
            )
        )
        await session.commit()

        return order

    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"There ara only {product.quantity} products with id={product_id} left in the warehouse!",
        )


async def add_product_in_order(
    session: AsyncSession,
    order_id: int,
    product_id: int,
    product_count: int,
) -> OrderModel:
    """
    Добавление в БД записи о присвоении заказу товара
    :param session: объект сессии
    :param order_id: id заказa в который нужно добавить товар
    :param product_id: id товара добавляемого в существующий заказ
    :param product_count: количество товара добавляемого в существующий заказ
    """
    product = await read_product_by_id(session=session, product_id=product_id)

    if product.quantity >= product_count:

        query_order = (
            select(OrderModel)
            .options(
                selectinload(OrderModel.products_details),
                selectinload(OrderModel.products),
            )
            .filter(OrderModel.id == order_id)
        )
        order_result: OrderModel | None = await session.scalar(query_order)

        if order_result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id={order_id} not found!",
            )
        product.quantity -= product_count

        for product_detail in order_result.products_details:
            if (
                product_detail.product_id == product_id
                and product_detail.order_id == order_id
            ):
                product_detail.product_count += product_count
                await session.commit()

                return order_result

        else:
            order_result.products_details.append(
                OrderItemModel(
                    product=product,
                    product_count=product_count,
                )
            )
            await session.commit()

            return order_result

    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"There ara only {product.quantity} products with id={product_id} left in the warehouse!",
        )


async def read_orders(session: AsyncSession) -> list[OrderModel] | None:
    """
    Получение из БД списка всех заказов
    :param session: объект сессии
    """
    query = (
        select(OrderModel)
        .options(
            selectinload(OrderModel.products_details),
            selectinload(OrderModel.products),
        )
        .order_by(desc(OrderModel.created_at))
    )
    results: Result = await session.execute(query)
    orders_list = results.scalars().all()

    if orders_list is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orders not found!",
        )
    return list(orders_list)


async def read_order(
    session: AsyncSession,
    order_id: int,
) -> OrderModel | None:
    """
    Получение из БД заказа по его `id`
    :param session: объект сессии
    :param order_id: id искомого заказа
    """
    query = (
        select(OrderModel)
        .options(
            selectinload(OrderModel.products_details),
            selectinload(OrderModel.products),
        )
        .filter(OrderModel.id == order_id)
    )
    order: OrderModel | None = await session.scalar(query)

    if order is not None:
        return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with id={order_id} not found!",
    )


async def change_order_status(
    session: AsyncSession,
    order_id: id,
    order_status: OrderStatus,
) -> OrderModel:
    """
    Обновляем в БД статус заказа по `id`
    :param order_id: id обновляемого заказа
    :param order_status: новый статус заказа
    :param session: объект сессии
    """
    query = select(OrderModel).filter(OrderModel.id == order_id)
    order: OrderModel | None = await session.scalar(query)

    if order is not None:
        order.status = order_status
        await session.commit()

        return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with id={order_id} not found!",
    )

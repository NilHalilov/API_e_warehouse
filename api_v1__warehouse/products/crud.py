"""Модуль для описания CRUD-действий модели `Product`"""

from fastapi import HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import ProductModel
from .schemas import ProductCreate, ProductUpdate


async def create_product(
    session: AsyncSession,
    new_product: ProductCreate,
) -> ProductModel:
    """
    Создание в БД записи о новом продукте
    :param session: объект сессии
    :param new_product: вся информация о новом продукте
    """
    product = ProductModel(**new_product.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def read_products(session: AsyncSession) -> list[ProductModel] | None:
    """
    Получение из БД списка всех продуктов
    :param session: объект сессии
    """
    query = select(ProductModel).order_by(desc(ProductModel.price))
    results: Result = await session.execute(query)
    products_list = results.scalars().all()

    if products_list is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Products not found!",
        )

    return list(products_list)


async def read_product_by_id(
    session: AsyncSession,
    product_id: int,
) -> ProductModel | None:
    """
    Получение из БД товара по его `id`
    :param session: объект сессии
    :param product_id: id искомого товара
    """
    product = await session.get(ProductModel, product_id)

    if product is not None:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with id={product_id} not found!",
    )


async def update_product_by_id(
    session: AsyncSession,
    product: ProductModel,
    new_product_info: ProductUpdate,
) -> ProductModel:
    """
    Обновляем в БД информацию о товаре по `id`
    :param new_product_info: новая информация о продукте
    :param product: обновляемый продукт
    :param session: объект сессии
    """
    for _name, _value in new_product_info.model_dump().items():
        setattr(product, _name, _value)

    await session.commit()
    return product


async def delete_product_by_id(
    session: AsyncSession,
    product: ProductModel,
) -> None:
    """
    Удаляем из БД товар по `id`
    :param product: удаляемый продукт
    :param session: объект сессии
    """
    await session.delete(product)
    await session.commit()

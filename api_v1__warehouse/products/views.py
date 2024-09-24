"""Модуль для описания endpoint`ов к модели `Product` """

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import ProductModel
from models.base import e_store_db
from . import crud
from .schemas import ProductCreate, Product, ProductUpdate


router = APIRouter(prefix="/api/products", tags=["Products"])


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def post_product(
    new_product: ProductCreate,
    session: AsyncSession = Depends(e_store_db.session_dependency),
):
    """
    Endpoint для создания нового товара
    * :param new_product: вся информация о новом продукте
    * :param session: объект сессии
    """
    return await crud.create_product(
        session=session,
        new_product=new_product,
    )


@router.get("/", response_model=list[Product], status_code=status.HTTP_200_OK)
async def get_products(session: AsyncSession = Depends(e_store_db.session_dependency)):
    """
    Endpoint для получения списка товаров
    * :param session: объект сессии
    """
    return await crud.read_products(session=session)


@router.get("/{id}", response_model=Product, status_code=status.HTTP_200_OK)
async def get_product_by_id(
    id: Annotated[int, Path(..., ge=1)],
    session: AsyncSession = Depends(e_store_db.session_dependency),
):
    """
    Endpoint для получения информации о товаре по `id`
    * :param id: id искомого товара
    * :param session: объект сессии
    """
    return await crud.read_product_by_id(session=session, product_id=id)


@router.put("/{id}", response_model=Product, status_code=status.HTTP_200_OK)
async def update_product(
    new_product_info: ProductUpdate,
    product: ProductModel = Depends(get_product_by_id),
    session: AsyncSession = Depends(e_store_db.session_dependency),
):
    """
    Endpoint для обновления товара по `id`
    * :param new_product_info: новая информация о продукте
    * :param product: обновляемый продукт
    * :param session: объект сессии
    """
    return await crud.update_product_by_id(
        session=session,
        product=product,
        new_product_info=new_product_info,
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: ProductModel = Depends(get_product_by_id),
    session: AsyncSession = Depends(e_store_db.session_dependency),
):
    """
    Endpoint для удаления товара по `id`
    * :param product: удаляемый продукт
    * :param session: объект сессии
    """
    return await crud.delete_product_by_id(
        session=session,
        product=product,
    )

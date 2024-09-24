"""Модуль для описания схем `Product`"""

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):

    title: str
    description: str
    price: int


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quantity: int


class ProductInOrder(ProductBase):
    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBase):
    quantity: int


class ProductUpdate(ProductBase):
    quantity: int

"""Модуль для описания схем `Order`"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..products.schemas import ProductInOrder
from models.order import OrderStatus


class OrderItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_count: int
    product: ProductInOrder


class OrderItem(OrderItemBase):
    id: int


class OrderBase(BaseModel):
    id: int
    status: OrderStatus
    created_at: datetime


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    products_details: list[OrderItemBase]

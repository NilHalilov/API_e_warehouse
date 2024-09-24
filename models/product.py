"""Модуль для создания модели `Product` в БД"""

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .order import OrderModel
    from .order_product_rel import OrderItemModel


class ProductModel(Base):
    __tablename__ = "products"

    title: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int]
    quantity: Mapped[int] = mapped_column(default=0, server_default="0")

    orders: Mapped[list["OrderModel"]] = relationship(
        secondary="order_product_relation",
        back_populates="products",
    )
    orders_details: Mapped[list["OrderItemModel"]] = relationship(
        back_populates="product"
    )

"""Модуль для создания модели связи `Product` и `Order` в БД"""

from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .order import OrderModel
    from .product import ProductModel


class OrderItemModel(Base):
    __tablename__ = "order_product_relation"
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "product_id",
            name="idx_unique_order_product",
        ),
    )

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product_count: Mapped[int] = mapped_column(default=1, server_default="1")

    product: Mapped["ProductModel"] = relationship(back_populates="orders_details")
    order: Mapped["OrderModel"] = relationship(back_populates="products_details")

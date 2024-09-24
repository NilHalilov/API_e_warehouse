"""Модуль для создания модели `Order` в БД"""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .product import ProductModel
    from .order_product_rel import OrderItemModel


class OrderStatus(Enum):
    in_process = "В процессе"
    sent = "Отправлен"
    delivered = "Доставлен"


class OrderModel(Base):
    __tablename__ = "orders"

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )
    status: Mapped[OrderStatus]

    products: Mapped[list["ProductModel"]] = relationship(
        secondary="order_product_relation",
        back_populates="orders",
    )
    products_details: Mapped[list["OrderItemModel"]] = relationship(
        back_populates="order"
    )

from app.backend.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .product import Product


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    slug: Mapped[str] = mapped_column(unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=True)

    products: Mapped[list['Product']] = relationship('Product', back_populates='category', lazy='selectin')




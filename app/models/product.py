from app.backend.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Product(Base):

    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    slug: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    image_url: Mapped[str] = mapped_column()
    stock: Mapped[int] = mapped_column()
    rating: Mapped[float] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    supplier_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)

    category: Mapped['Category'] = relationship('Category', back_populates='products', lazy='selectin')

    feedback: Mapped[list['Feedback']] = relationship('Feedback', back_populates='product', lazy='selectin')


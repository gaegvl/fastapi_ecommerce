from app.backend.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import datetime


class Feedback(Base):

    __tablename__ = 'feedback'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    rating_id: Mapped[int] = mapped_column(ForeignKey('rating.id'), nullable=False)
    comment: Mapped[str] = mapped_column()
    comment_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(datetime.timezone.utc))
    is_active: Mapped[bool] = mapped_column(default=True)

    product: Mapped['Product'] = relationship('Product', back_populates='feedback', lazy='selectin')
    user: Mapped['User'] = relationship('User', back_populates='feedback', lazy='selectin')
    rating: Mapped['Rating'] = relationship('Rating', back_populates='feedback', lazy='selectin')
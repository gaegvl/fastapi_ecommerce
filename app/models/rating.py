from app.backend.db import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey


class Rating(Base):

    __tablename__ = 'rating'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    grade: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    is_active: Mapped[bool] = mapped_column(default=True)

    feedback: Mapped['Rating'] = relationship('Feedback', back_populates='rating', lazy='selectin')

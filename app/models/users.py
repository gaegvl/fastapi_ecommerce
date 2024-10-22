from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship
from app.backend.db import Base

class User(Base):

    __tablename__='users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_supplier: Mapped[bool]= mapped_column(default=False)
    is_customer: Mapped[bool]=mapped_column(default=True)

    feedback: Mapped[list['Feedback']] = relationship('Feedback', back_populates='user', lazy='selectin')
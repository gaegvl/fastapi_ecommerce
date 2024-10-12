from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str
    parend_id: int | None
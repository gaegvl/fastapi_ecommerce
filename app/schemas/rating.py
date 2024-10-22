from pydantic import BaseModel


class CreateRating(BaseModel):
    grade: int
    product_id: int


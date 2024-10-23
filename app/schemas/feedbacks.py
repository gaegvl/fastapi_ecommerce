from pydantic import BaseModel
from .rating import CreateRating

class CreateFeedback(BaseModel):
    product_id: int
    comment: str
    rating: CreateRating

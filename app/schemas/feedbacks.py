from pydantic import BaseModel


class CreateFeedback(BaseModel):
    product_id: int
    comment: str

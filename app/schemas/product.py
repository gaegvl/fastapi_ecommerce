from pydantic import BaseModel, ConfigDict


class CreateProduct(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    stock: int
    category_id: int
    rating: float

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
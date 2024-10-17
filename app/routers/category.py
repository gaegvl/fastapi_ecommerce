from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy import insert
from slugify import slugify

from app.backend.db import Database
from app.schemas.category import CreateCategory
from app.models.category import Category
from app.models.product import Product


router = APIRouter(prefix='/category', tags=['category'])

@router.get("/all_categories")
async def get_all_categories():
    pass

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_category(db: Annotated[AsyncSession, Depends(Database().sesion_dependency)], create_category: CreateCategory):
    await db.execute(insert(Category).values(name=create_category.name,
                                       parent_id=create_category.parend_id,
                                       slug=slugify(create_category.name)))
    await db.commit()
    return {"status_code": status.HTTP_201_CREATED,
            "transaction": "Success"}

@router.put("/update_category")
async def update_category():
    pass

@router.delete("/delete")
async def delete_category():
    pass
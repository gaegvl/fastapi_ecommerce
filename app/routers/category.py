from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy import insert, select, update
from slugify import slugify

from app.backend.db import Database
from app.schemas.category import CreateCategory
from app.models.category import Category


router = APIRouter(prefix='/category', tags=['category'])
db = Database()


async def category_by_id(db: Annotated[AsyncSession, Depends(db.session_dependency)], category_id: int):
    category = await db.scalar(select(Category).where(Category.id == category_id))
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category_id


@router.get("/all_categories")
async def get_all_categories(db: Annotated[AsyncSession, Depends(db.session_dependency)]):
    categories = await db.scalars(select(Category).where(Category.is_active == True))
    return categories.all()


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_category(db: Annotated[AsyncSession, Depends(db.session_dependency)], create_category: CreateCategory):
    await db.execute(insert(Category).values(name=create_category.name,
                                       parent_id=create_category.parend_id,
                                       slug=slugify(create_category.name)))
    await db.commit()
    return {"status_code": status.HTTP_201_CREATED,
            "transaction": "Success"}


@router.put("/update_category")
async def update_category(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                          category_id: Annotated[int, Depends(category_by_id)],
                          update_category: CreateCategory):
    await db.execute(update(Category).where(Category.id == category_id).values(name=update_category.name,
                                                                               parent_id=update_category.parend_id,
                                                                               slug=slugify(update_category.name)))
    await db.commit()
    return {"status_code": status.HTTP_200_OK, 'transaction': 'Success'}


@router.delete("/delete")
async def delete_category(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                          category_id: Annotated[int, Depends(category_by_id)]):

    await db.execute(update(Category).where(Category.id == category_id).values(is_active=False))
    await db.commit()
    return {"status_code": status.HTTP_200_OK, 'transaction': 'Success'}

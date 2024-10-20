from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from slugify import slugify

from app.backend.db import Database
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import CreateProduct

db = Database()
router = APIRouter(prefix="/products", tags=["products"])


async def product_by_id(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                        product_id: int):
    product = await db.scalar(select(Product).where(Product.id==product_id))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


async def category_by_product(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                              product: CreateProduct):
    category = await db.scalar(select(Category).where(Category.id==product.category_id))
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return product


async def category_by_slug(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                              category_slug: str):
    category = await db.scalar(select(Category).where(Category.slug==category_slug))
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category_slug


async def product_by_slug(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                           product_slug: str):
    product = await db.scalar(select(Product).where(Product.slug==product_slug))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

async def get_all_category_ids(db: AsyncSession,
                               category: int,
                               category_ids: set[int]):
    category_ids.add(category)
    subcategories = await db.scalars(select(Category).where(Category.parent_id==category))
    for subcategory in subcategories.all():
        if subcategory.id not in category_ids:
            await get_all_category_ids(db, subcategory.id, category_ids)
    return category_ids


@router.get("/all_products")
async def all_products(db: Annotated[AsyncSession, Depends(db.session_dependency)]):
    products = await db.scalars(select(Product).where(Product.is_active==True))
    return products.all()


@router.post("/create")
async def create_products(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                          create_product: Annotated[CreateProduct, Depends(category_by_product)]):
    await db.execute(insert(Product).values(name=create_product.name,
                                            slug=slugify(create_product.name),
                                            description=create_product.description,
                                            price=create_product.price,
                                            image_url=create_product.image_url,
                                            stock=create_product.stock,
                                            rating=create_product.rating,
                                            category_id=create_product.category_id
                                            ))
    await db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Success'}


@router.get("/{category_slug}")
async def get_products_by_category(category_slug: Annotated[str, Depends(category_by_slug)],
                                   db: Annotated[AsyncSession, Depends(db.session_dependency)]):
    category = await db.scalar(select(Category).where(Category.slug==category_slug))
    category_ids: set[int] = set()
    category_ids = await get_all_category_ids(db, category.id, category_ids)
    products = await db.scalars(select(Product).where(Product.stock > 0,
                                                      Product.is_active==True,
                                                      Product.category_id.in_(category_ids)))
    return [CreateProduct.model_validate(product) for product in products.all()]


@router.get("/detail/{product_slug}")
async def product_detail(product_slug: Annotated[str, Depends(product_by_slug)]):
    return product_slug


@router.put("/detail/{product_slug}")
async def update_product(product_slug: Annotated[str, Depends(product_by_slug)],
                         db: Annotated[AsyncSession, Depends(db.session_dependency)],
                         update_product: Annotated[CreateProduct, Depends(category_by_product)]):
    product: Product = product_slug
    for field in update_product.model_fields:
        setattr(product, field, update_product.__dict__[field])
    product.slug = slugify(update_product.name)
    await db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Product updated successfully'}


@router.delete("/detail/{product_slug}")
async def delete_product(product_slug: Annotated[str, Depends(product_by_slug)],
                         db: Annotated[AsyncSession, Depends(db.session_dependency)]):
    product: Product = product_slug
    product.is_active = False
    await db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'Product deleted successfully'}

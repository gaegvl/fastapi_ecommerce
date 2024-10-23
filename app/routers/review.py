from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from typing import Annotated

from app.backend.db import Database
from app.models.rating import Rating
from app.models.feedback import Feedback
from app.models.users import User
from app.models.product import Product
from app.schemas.feedbacks import CreateFeedback
from .auth import get_current_user


db = Database()
router = APIRouter(prefix='/reviews', tags=['Reviews'])

@router.get('/')
async def all_reviews(db: Annotated[AsyncSession, Depends(db.session_dependency)]):
    feedbacks = await db.scalars(select(Feedback).where(Feedback.is_active == True))
    return feedbacks.all()


async def product_by_id(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                        product_id: int):
    product = await db.scalar(select(Product).where(Product.id==product_id))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.get('/products_reviews')
async def products_reviews(product: Annotated[Product, Depends(product_by_id)]):
    reviews = product.feedback
    return reviews

@router.post('/create_review')
async def create_review(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                        current_user: Annotated[dict, Depends(get_current_user)],
                        create_feedback: CreateFeedback):
    if current_user.get('is_customer'):
        product = await db.scalar(select(Product).where(Product.id==create_feedback.product_id))
        if not product or not product.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        rating_id= await db.execute(insert(Rating).values(grade=create_feedback.rating.grade,
                                               user_id=current_user.get('user_id'),
                                               product_id=product.id
                                               ).returning(Rating.id))

        await db.execute(insert(Feedback).values(user_id=current_user.get('user_id'),
                                                 product_id=product.id,
                                                 rating_id=rating_id.scalar(),
                                                 comment=create_feedback.comment
                                                 ))

        product.rating=create_feedback.rating.grade

        await db.commit()

        return {'status_code': status.HTTP_201_CREATED,
                'transaction': 'Success'}
    else:
        HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only customers can create reviews")

async def get_feedback_by_id(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                             feedback_id: int):
    feedback = await db.scalar(select(Feedback).where(Feedback.id==feedback_id))
    if not feedback or not feedback.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    return feedback

@router.delete('/delete_review')
async def delete_review(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                        feedback: Annotated[Feedback, Depends(get_feedback_by_id)],
                        current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.get('is_admin'):
        feedback.is_active = False
        feedback.rating.is_active = False
        await db.commit()

        return {'status_code': status.HTTP_200_OK,
                'transaction': 'Success'}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete reviews")

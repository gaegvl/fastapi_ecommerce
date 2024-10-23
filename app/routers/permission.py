from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, get_origin
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db import Database
from app.models.users import User
from .auth import get_current_user

db = Database()
router = APIRouter(prefix='/permission', tags=["permission"])

async def get_user_by_id(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                         user_id: int):
    user = await db.scalar(select(User).where(User.id == user_id))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
    return user

@router.patch('/')
async def supplier_permission(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                              current_user: Annotated[dict, Depends(get_current_user)],
                              user: Annotated[User, Depends(get_user_by_id)]):
    if current_user.get('is_admin'):

        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")

        if user.is_supplier:
            user.is_supplier = False
            user.is_customer = True
            await db.commit()
            return {'status_code': status.HTTP_200_OK, 'detail': 'User is no longer supplier'}
        elif user.is_customer:
            user.is_supplier = True
            user.is_customer = False
            await db.commit()
            return {'status_code': status.HTTP_200_OK, 'detail': 'User is supplier'}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")


@router.delete('/delete')
async def delete_user(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                      current_user: Annotated[dict, Depends(get_current_user)],
                      user: Annotated[User, Depends(get_user_by_id)]):
    if current_user.get('is_admin'):

        if user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Deletion is not allowed")

        if user.is_active:
            user.is_active = False
            await db.commit()
            return {'status_code': status.HTTP_200_OK, 'detail': 'User is deleted'}

        else:
            raise HTTPException(status_code=status.HTTP_200_OK, detail="User already deleted")

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
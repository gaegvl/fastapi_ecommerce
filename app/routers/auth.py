from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from typing import Annotated
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from os import getenv
from dotenv import load_dotenv

load_dotenv()

from app.models.users import User
from app.schemas.users import CreateUser
from app.backend.db import Database


db = Database()
router = APIRouter(prefix="/auth", tags=["auth"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/')
async def create_user(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                      create_user: CreateUser):
    await db.execute(insert(User).values(
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        username=create_user.username,
        email=create_user.email,
        hashed_password=bcrypt_context.hash(create_user.password)
    ))
    await db.commit()
    return {"status_code": status.HTTP_201_CREATED, 'transaction': 'Success'}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def authenticate_user(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                            username: str, password: str):
    user = await db.scalar(select(User).where(User.username == username))
    if not user or not bcrypt_context.verify(password, user.hashed_password) or user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def create_access_token(username:str, user_id: int, is_admin: bool, is_supplier: bool, is_customer: bool, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'is_admin': is_admin, 'is_supplier': is_supplier, 'is_customer': is_customer}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, getenv('SECRET_KEY'), algorithm=getenv('ALGORITHM'))

@router.post("/token")
async def login(db: Annotated[AsyncSession, Depends(db.session_dependency)],
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(db, form_data.username, form_data.password)

    token = await create_access_token(user.username, user.id, user.is_admin, user.is_supplier, user.is_customer, timedelta(minutes=30))

    return {'access_token': token, 'token_type': 'bearer'}

async def get_current_user(token: Annotated[str,  Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, getenv('SECRET_KEY'), algorithms=[getenv('ALGORITHM')])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        is_admin: str = payload.get('is_admin')
        is_supplier: str = payload.get('is_supplier')
        is_customer: str = payload.get('is_customer')

        return {'username': username,
                'user_id': user_id,
                'is_admin': is_admin,
                'is_supplier': is_supplier,
                'is_customer': is_customer}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.get('/read_current_user')
async def read_current_user(user: User = Depends(get_current_user)):
    return user
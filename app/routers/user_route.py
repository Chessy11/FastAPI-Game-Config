import logging
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.user_schema import UserInSchema, Token, UserOutSchema
from app.cruds import user_crud
from app.utils.auth import login_user, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_active_user

router = APIRouter()


@router.post("/create-user", tags=["user"], status_code=201)
async def create_user(user: UserInSchema, session: AsyncSession = Depends(get_session)):
    try:
        existing_user = await user_crud.get_user_by_email(user.email, session)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email Already Exists")
        new_user = await user_crud.create_user(session, user)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return {"detail": "user created", "username": new_user.username, "email": new_user.email}


@router.get("/user/{user_id}", tags=["user"], status_code=200)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await user_crud.get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/token", tags=["auth"], status_code=200, response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: AsyncSession = Depends(get_session)):
    user = await login_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/userss/me/", tags=["user"], status_code=200)
async def read_users_me(current_user: UserOutSchema = Depends(get_current_active_user)):
    return current_user



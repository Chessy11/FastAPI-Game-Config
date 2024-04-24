from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserOutSchema
from app.utils.auth import get_current_active_user
from app.db import get_session
from app.schemas import choos_bonus_schema
from app.cruds import choose_bonus_crud

router = APIRouter()



@router.post("/create-choose-bonus", tags=["choose bonus"], status_code=201)
async def create_choose_bonus_config(create_choose_bonus: choos_bonus_schema.ChooseBonusInSchema,
                                     current_user: UserOutSchema = Depends(get_current_active_user),
                                     session: AsyncSession = Depends(get_session)):
    try:
        new_choose_bonus = await choose_bonus_crud.create_choose_bonus(session, create_choose_bonus, current_user.user_id)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_choose_bonus


@router.get("/choose-bonus/{c_bonus_id}", tags=["choose bonus"], status_code=200)
async def get_choose_bonus_by_id(c_bonus_id: int, session: AsyncSession = Depends(get_session)):
    bonus = await choose_bonus_crud.get_choose_bonus_by_id(c_bonus_id, session)
    if bonus is None:
        raise HTTPException(status_code=404, detail="Choose bonus not found")
    return bonus
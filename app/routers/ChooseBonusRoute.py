from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import ChooseBonusSchema
from app.cruds import ChooseBonusCrud

router = APIRouter()


@router.post("/create-choose-bonus", tags=["choose bonus"], status_code=201)
async def create_choose_bonus_config(create_choose_bonus: ChooseBonusSchema.ChooseBonusInSchema,
                                     session: AsyncSession = Depends(get_session)):
    try:
        new_choose_bonus = await ChooseBonusCrud.create_choose_bonus(session, create_choose_bonus)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_choose_bonus


@router.get("/choose-bonus/{c_bonus_id}", tags=["choose bonus"], status_code=200)
async def get_choose_bonus_by_id(c_bonus_id: int, session: AsyncSession = Depends(get_session)):
    bonus = await ChooseBonusCrud.get_choose_bonus_by_id(c_bonus_id, session)
    if bonus is None:
        raise HTTPException(status_code=404, detail="Choose bonus not found")
    return bonus
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import BonusSchema
from app.cruds import BonusCrud

router = APIRouter()


@router.post("/create-bonus", tags=["bonus"], status_code=201)
async def create_bonus_config(create_bonus: BonusSchema.BonusInSchema, session: AsyncSession = Depends(get_session)):
    try:
        new_bonus = await BonusCrud.create_bonus(session, create_bonus)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_bonus


@router.get("/bonuses/{game_id}", tags=["bonus"], status_code=200)
async def get_bonuses_by_game_id(game_id: int, session: AsyncSession = Depends(get_session)):
    bonuses = await BonusCrud.get_bonuses_by_game_id(session, game_id)
    return bonuses

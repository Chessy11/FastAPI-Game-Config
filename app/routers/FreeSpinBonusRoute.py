from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import FreeSpinBonusSchema
from app.cruds import FreeSpinBonusCrud

router = APIRouter()


@router.post("/create-bonus", tags=["bonus"], status_code=201)
async def create_bonus_config(create_bonus: FreeSpinBonusSchema.FreeSpinBonusInSchema,
                              session: AsyncSession = Depends(get_session)):
    try:
        new_bonus = await FreeSpinBonusCrud.create_bonus(session, create_bonus)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_bonus


@router.get("/bonuses/{game_id}", tags=["bonus"], status_code=200)
async def get_bonuses_by_game_id(game_id: int, session: AsyncSession = Depends(get_session)):
    bonuses = await FreeSpinBonusCrud.get_bonuses_by_game_id(session, game_id)
    return bonuses


@router.get("/bonus/{bonus_id}", tags=["bonus"], status_code=200)
async def get_bonus_by_id(bonus_id: int, session: AsyncSession = Depends(get_session)):
    bonus = await FreeSpinBonusCrud.get_bonus_by_id(bonus_id, session)
    if bonus is None:
        raise HTTPException(status_code=404, detail="Bonus not found")
    return bonus


@router.post("/create-bonus-win", tags=["bonus"], status_code=201)
async def create_bonus_win_config(create_bonus_win: FreeSpinBonusSchema.BonusWinInSchema,
                                  session: AsyncSession = Depends(get_session)):
    try:
        new_bonus_win = await FreeSpinBonusCrud.create_bonus_win(session, create_bonus_win)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_bonus_win

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.ReelSchema import ReelInSchema, ReelSymbolInSchema
from app.cruds import ReelCrud

router = APIRouter()


@router.post("/create-reel", tags=["reel"], status_code=201)
async def create_reel_config(create_reel: ReelInSchema, session: AsyncSession = Depends(get_session)):
    try:
        new_reel = await ReelCrud.create_reel(session, create_reel)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_reel


@router.get("/reels/{game_id}", tags=["reel"], status_code=200)
async def get_reels_by_game_id(game_id: int, session: AsyncSession = Depends(get_session)):
    reels = await ReelCrud.get_reels_by_game_id(session, game_id)
    return reels


@router.get("/reel/{reel_id}", tags=["reel"], status_code=200)
async def get_reel_by_id(reel_id: int, session: AsyncSession = Depends(get_session)):
    reel = await ReelCrud.get_reel_by_id(reel_id, session)
    if reel is None:
        raise HTTPException(status_code=404, detail="Reel not found")
    return reel


@router.post("/add-symbol-to-reel", tags=["reel"], status_code=201)
async def add_symbol_to_reel(add_symbol: ReelSymbolInSchema, session: AsyncSession = Depends(get_session)):
    try:
        new_symbol = await ReelCrud.add_symbols_to_reel(session, add_symbol)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_symbol




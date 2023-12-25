from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.ReelSchema import ReelInSchema, ReelSymbolInSchema
from app.cruds import ReelCrud
from app.schemas.UserSchema import UserOutSchema
from app.utils.auth import get_current_active_user

router = APIRouter()

@router.post("/create-reel", tags=["reel"], status_code=201)
async def create_reel_config(
    create_reel: ReelInSchema, 
    current_user: UserOutSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    try:
        # Ensure that the new reel is associated with the current user
        new_reel = await ReelCrud.create_reel(session, create_reel, current_user.user_id)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_reel

@router.get("/reels/{game_id}", tags=["reel"], status_code=200)
async def get_reels_by_game_id(
    game_id: int, 
    current_user: UserOutSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    # Ensure that the current user has access to the requested game's reels
    reels = await ReelCrud.get_reels_by_game_id(session, game_id, current_user.user_id)
    return reels

@router.get("/reel/{reel_id}", tags=["reel"], status_code=200)
async def get_reel_by_id(
    reel_id: int, 
    current_user: UserOutSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    # Pass arguments in the correct order
    reel = await ReelCrud.get_reel_by_id(reel_id, current_user.user_id, session)
    if reel is None:
        raise HTTPException(status_code=404, detail="Reel not found")
    return reel

@router.post("/add-symbol-to-reel", tags=["reel"], status_code=201)
async def add_symbol_to_reel(add_symbol: ReelSymbolInSchema,
                             current_user: UserOutSchema = Depends(get_current_active_user),
                             session: AsyncSession = Depends(get_session)
                             ):
    try:
        new_symbol = await ReelCrud.add_symbols_to_reel(session, add_symbol, current_user.user_id)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_symbol

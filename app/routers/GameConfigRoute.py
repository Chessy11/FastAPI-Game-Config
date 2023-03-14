from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.GameConfigSchema import GameConfigSchema
from app.cruds import GameConfigCrud

router = APIRouter()


@router.post("/create", tags=["game config"], status_code=201)
async def create_game_config(create_game: GameConfigSchema, session: AsyncSession = Depends(get_session)):
    try:
        new_game = await GameConfigCrud.create_game_config(session, create_game)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_game


@router.get("/games", tags=["game config"], status_code=200)
async def get_games(skip: int = 0, limit: int = 20, session: AsyncSession = Depends(get_session)):
    games = await GameConfigCrud.get_games(session, skip, limit)
    return games


@router.get("/game/{game_id}", tags=["game config"], status_code=200)
async def get_game_by_id(game_id: int, session: AsyncSession = Depends(get_session)):
    game = await GameConfigCrud.get_game_by_id(game_id, session)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

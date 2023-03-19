from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.GameSchema import GameInSchema, GameOutSchema
from app.cruds import GameCrud

router = APIRouter()


@router.post("/create-game", tags=["game"], status_code=201)
async def create_game_config(create_game: GameInSchema, session: AsyncSession = Depends(get_session)):
    try:
        new_game = await GameCrud.create_game(session, create_game)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_game


@router.get("/games", tags=["game"], status_code=200)
async def get_games(skip: int = 0, limit: int = 20, session: AsyncSession = Depends(get_session)):
    games = await GameCrud.get_games(session, skip, limit)
    return games


@router.get("/game/{game_id}", tags=["game"], status_code=200, response_model=GameOutSchema)
async def get_game_by_id(game_id: int, session: AsyncSession = Depends(get_session)):
    game = await GameCrud.get_game_by_id(game_id, session)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

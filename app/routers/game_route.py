
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schemas.game_schema import GameInSchema, GameOutSchema
from app.schemas.user_schema import UserOutSchema
from app.cruds import game_crud
from app.utils import redis
from app.utils.auth import get_current_active_user
import json

router = APIRouter()


@router.post("/create-game", tags=["game"], status_code=201)
async def create_game_config(create_game: GameInSchema,
                             current_user: UserOutSchema = Depends(get_current_active_user),
                             session: AsyncSession = Depends(get_session)):
    try:
        new_game = await game_crud.create_game(session, create_game, current_user.user_id)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_game


@router.get("/games", tags=["game"], status_code=200)
async def get_games(skip: int = 0, limit: int = 20, 
                    current_user: UserOutSchema = Depends(get_current_active_user),
                    session: AsyncSession = Depends(get_session)):
    games = await game_crud.get_games(session, current_user.user_id, skip, limit)
    return games


@router.get("/game/{game_id}", tags=["game"], status_code=200, response_model=GameOutSchema)
async def get_game_by_id(game_id: int, current_user: UserOutSchema = Depends(get_current_active_user), session: AsyncSession = Depends(get_session)):
    print(f"Handler start: Fetching game by ID {game_id} for user {current_user.user_id}")  # Debug log
    game = await game_crud.get_game_by_id(game_id, current_user.user_id, session)
    if game is None:
        print(f"Handler error: Game ID {game_id} not found for user {current_user.user_id}")  # Debug log
        raise HTTPException(status_code=404, detail="Game not found")
    print(f"Handler end: Game found for ID {game_id}")  # Debug log
    return game


@router.get("/publish/{game_id}", tags=["game"], status_code=200)
async def publish_game_endpoint(game_id: int, 
                                current_user: UserOutSchema = Depends(get_current_active_user),
                                session: AsyncSession = Depends(get_session)):
    # Fetch the game first
    game = await game_crud.get_game_by_id(game_id, current_user.user_id, session)  # Pass user_id and session
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    # Update and save the game as published
    game = await game_crud.publish_game(game_id, session)  # This call is fine as is

    # Convert game object to JSON
    game_json = jsonable_encoder(game)

    # Save the updated game to Redis
    await redis.save_game("game:" + str(game_id), game_json)

    return {"message": "Game published"}

# @router.get("/redis-data/{game_id}")
# async def get_redis_game_data(game_id: int):
#     game_data = await redis.get_game(f"game:{game_id}")
#     if game_data is None:
#         raise HTTPException(status_code=404, detail="Game not fount")
#     return game_data


@router.get("/redis-data/{game_id}")
async def get_redis_game_data(game_id: int, current_user: UserOutSchema = Depends(get_current_active_user)):
    try:
        # Call the synchronous function without 'await'
        game_data = redis.get_game_sync(f"game:{game_id}")
        if game_data is None:
            raise HTTPException(status_code=404, detail="Game not found")
        return game_data
    except Exception as e:
        print(f"Failed to retrieve game data for game_id {game_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@router.delete("/delete/{game_id}", tags=["game"], status_code=200)
async def delete_game(game_id: int, 
                      current_user: UserOutSchema = Depends(get_current_active_user),
                      session: AsyncSession = Depends(get_session)):
    game_deleted = await game_crud.delete_game_by_id(game_id, current_user.user_id, session)
    if game_deleted:
        await redis.delete_game("game:" +str(game_id))
        return {"message": "Game successfully deleted"}
    else:
        raise HTTPException(status_code=404, detail="Game not found")

    


@router.post("/complete-setup/{game_id}", tags=["game"], status_code=200)
async def complete_game_setup(game_id: int, 
                              current_user: UserOutSchema = Depends(get_current_active_user),
                              session: AsyncSession = Depends(get_session)):
    completed_game = await game_crud.complete_setup(game_id, current_user.user_id, session)
    if completed_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"message": "Game setup completed"}


@router.get("/latest-game-setup-status")
async def latest_game_setup_status(current_user: UserOutSchema = Depends(get_current_active_user), 
                                   session: AsyncSession = Depends(get_session)):
    user_id = current_user.user_id # Assuming the current user object has an ID attribute
    setup_status = await game_crud.get_game_setup_status(session, user_id)
    if setup_status is None:
        raise HTTPException(status_code=404, detail="No games found for the current user")

    return {"isSetupComplete": setup_status}
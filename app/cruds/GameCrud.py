from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import exc as orm_exc
from app.models.Models import GameModel
from app.schemas.GameSchema import GameInSchema
from app.cruds.SymbolCrud import check_if_game_has_paytables, check_if_game_has_symbols
from app.cruds.LinesCrud import check_if_game_has_lines
from app.cruds.ReelCrud import check_if_game_has_reels, check_reels_have_minimum_symbols
from fastapi import HTTPException


async def create_game(session: AsyncSession, game: GameInSchema, user_id: int):
    game_data = game.dict()
    game_data['user_id'] = user_id  # Add the user_id to the game data
    new_game = GameModel(**game_data)
    session.add(new_game)
    await session.commit()
    await session.refresh(new_game)
    return new_game


async def get_games(session: AsyncSession, user_id: int, skip: int = 0, limit: int = 20):
    result = await session.execute(
        select(GameModel)
        .where(GameModel.user_id == user_id)  # Filter games by user_id
        .order_by(GameModel.game_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().unique().fetchall()



async def get_game_by_id(game_id: int, user_id: int, session: AsyncSession):
    game = await session.execute(
        select(GameModel)
        .options(selectinload(GameModel.symbols))  # Eagerly load 'symbols' relationship
        .where(GameModel.game_id == game_id, GameModel.user_id == user_id)
    )
    return game.scalars().first()



async def delete_game_by_id(game_id: int, session: AsyncSession):
    game_to_delete = await session.get(GameModel, game_id)
    
    if not game_to_delete:
        return False

    # Attempt to delete related entities, but continue even if they are not found
    try:
        await session.execute("DELETE FROM symbols WHERE game_id = :game_id", {'game_id': game_id})
        await session.execute("DELETE FROM lines WHERE game_id = :game_id", {'game_id': game_id})
        await session.execute("DELETE FROM free_spin_bonus WHERE game_id = :game_id", {'game_id': game_id})
        await session.execute("DELETE FROM choose_bonus WHERE game_id = :game_id", {'game_id': game_id})
    except orm_exc.StaleDataError:
        # Log this error or handle it as needed
        pass

    # Now delete the game
    await session.delete(game_to_delete)
    await session.commit()
    return True




async def publish_game(game_id: int, session: AsyncSession):
    game = await session.get(GameModel, game_id)
    game.isPublished = True
    await session.commit()
    return game


async def complete_setup(game_id: int, user_id: int, session: AsyncSession):
    game = await session.get(GameModel, game_id)
    if game is None:
        return None
    if game.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to complete setup for this game")
    
    has_symbols = await check_if_game_has_symbols(session, game_id, user_id)
    has_paytables = await check_if_game_has_paytables(session, game_id, user_id)
    has_reels = await check_if_game_has_reels(session, game_id, user_id)
    has_lines = await check_if_game_has_lines(session, game_id, user_id)
    has_symbols_on_reels = await check_reels_have_minimum_symbols(session, game_id, user_id)
    print("Has Symbols", has_symbols)
    print("Has Paytables", has_paytables)
    print("Has Reels", has_reels)
    print("Has Lines", has_lines)
    print("Has Symbols On Reels", has_symbols_on_reels)
    
    if has_symbols and has_paytables and has_reels and has_lines and has_symbols_on_reels:

        game.is_setup_complete = True
        await session.commit()
        return game
    else:
        raise HTTPException(status_code=500, detail="Game was not created")
    
    

async def get_game_setup_status(session: AsyncSession, user_id: int):
    latest_game_result = await session.execute(
        select(GameModel)
        .where(GameModel.user_id == user_id)  # Filter by user_id
        .order_by(GameModel.game_id.desc())
        .limit(1)
        .options(selectinload(GameModel.user))
    )
    
    latest_game = latest_game_result.scalars().first()
    
    if not latest_game:
        return None
    return {
        "is_setup_complete": latest_game.is_setup_complete,
        "game_name": latest_game.game_name,
        "game_id": latest_game.game_id
    }

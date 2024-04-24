from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import ReelsModel, ReelSymbolsModel, GameModel
from app.schemas.reel_schema import ReelInSchema, ReelSymbolInSchema
from fastapi import HTTPException

async def get_reels_by_game_id(session: AsyncSession, game_id: int, user_id: int):
    result = await session.execute(
        select(ReelsModel)
        .join(GameModel, GameModel.game_id == ReelsModel.game_id)
        .where(ReelsModel.game_id == game_id, GameModel.user_id == user_id)
    )
    return result.scalars().unique().all()  # Use unique() here


async def create_reel(session: AsyncSession, reel: ReelInSchema, user_id: int):
    # Verify if the game belongs to the user
    game = await session.get(GameModel, reel.game_id)
    if game is None or game.user_id != user_id:
        raise HTTPException(status_code=404, detail="Game not found or not owned by the user")

    new_reel = ReelsModel(**reel.dict())
    session.add(new_reel)
    await session.commit()
    await session.refresh(new_reel)
    return new_reel

async def get_reel_by_id(reel_id: int, user_id: int, session: AsyncSession):
    result = await session.execute(
        select(ReelsModel)
        .join(GameModel, GameModel.game_id == ReelsModel.game_id)
        .where(ReelsModel.reel_id == reel_id, GameModel.user_id == user_id)
    )
    return result.scalars().first()


async def add_symbols_to_reel(session: AsyncSession, reel_symbols: ReelSymbolInSchema, user_id: int):
    reel = await session.get(ReelsModel, reel_symbols.reel_id)
    
    if reel is None:
        raise HTTPException(status_code=404, detail="Reel not found")

    # Fetch GameModel separately to ensure it's loaded asynchronously
    game = await session.get(GameModel, reel.game_id)
    if game.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to add symbols to this reel")

    new_reel_symbol = ReelSymbolsModel(**reel_symbols.dict())
    session.add(new_reel_symbol)
    await session.commit()
    await session.refresh(new_reel_symbol)
    return new_reel_symbol

async def check_if_game_has_reels(session: AsyncSession, game_id: int, user_id: int):
    reels = await get_reels_by_game_id(session, game_id, user_id)
    if len(reels) < 3:
        raise HTTPException(status_code=422, detail="Game must contain at least three reels")
    return len(reels) >= 3


async def count_symbols_for_reel(session: AsyncSession, reel_id: int):
    result = await session.execute(
        select(ReelSymbolsModel)
        .where(ReelSymbolsModel.reel_id == reel_id)
    )
    reel_symbols = result.scalars().all()
    return len(reel_symbols)

async def check_reels_have_minimum_symbols(session: AsyncSession, game_id: int, user_id: int):
    reels = await get_reels_by_game_id(session, game_id, user_id)
    for reel in reels:
        symbol_count = await count_symbols_for_reel(session, reel.reel_id)
        if symbol_count < 4:
            raise HTTPException(status_code=422, detail="Reel must have at least four symbols")
    return True

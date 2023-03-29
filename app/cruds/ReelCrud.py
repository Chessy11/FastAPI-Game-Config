from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Models import ReelsModel, ReelSymbolsModel
from app.schemas.ReelSchema import ReelInSchema, ReelSymbolInSchema


async def get_reels_by_game_id(session: AsyncSession, game_id: int):
    result = await session.execute(
        select(ReelsModel)
        .where(ReelsModel.game_id == game_id)
    )
    return result.scalars().unique().fetchall()


async def create_reel(session: AsyncSession, reel: ReelInSchema):
    new_reel = ReelsModel(**reel.dict())
    session.add(new_reel)
    await session.commit()
    await session.refresh(new_reel)
    return new_reel


async def get_reel_by_id(reel_id: int, session: AsyncSession):
    return await session.get(ReelsModel, reel_id)


async def add_symbols_to_reel(session: AsyncSession, reel_symbols: ReelSymbolInSchema):
    new_reel_symbol = ReelSymbolsModel(**reel_symbols.dict())
    print(new_reel_symbol)
    session.add(new_reel_symbol)
    await session.commit()
    await session.refresh(new_reel_symbol)
    return new_reel_symbol

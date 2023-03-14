from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.Models import GameConfigModel
from app.schemas.GameConfigSchema import GameConfigSchema


async def get_games(session: AsyncSession, skip: int = 0, limit: int = 20):
    result = await session.execute(
        select(GameConfigModel)
        .order_by(GameConfigModel.game_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().fetchall()


async def create_game_config(session: AsyncSession, game: GameConfigSchema):
    new_game = GameConfigModel(**game.dict())
    session.add(new_game)
    await session.commit()
    await session.refresh(new_game)
    return new_game


async def get_game_by_id(game_id: int, session: AsyncSession):
    return await session.get(GameConfigModel, game_id)

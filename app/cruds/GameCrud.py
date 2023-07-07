from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.Models import GameModel
from app.schemas.GameSchema import GameInSchema


async def get_games(session: AsyncSession, skip: int = 0, limit: int = 20):
    result = await session.execute(
        select(GameModel)
        .order_by(GameModel.game_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().unique().fetchall()


async def create_game(session: AsyncSession, game: GameInSchema):
    new_game = GameModel(**game.dict())
    session.add(new_game)
    await session.commit()
    await session.refresh(new_game)
    return new_game


async def get_game_by_id(game_id: int, session: AsyncSession):
    return await session.get(
        GameModel,
        game_id,
        options=[
            selectinload(GameModel.symbols),
            selectinload(GameModel.lines),
            selectinload(GameModel.free_spin_bonuses),
            selectinload(GameModel.choose_bonuses),

        ],
    )


async def publish_game(game_id: int, session: AsyncSession):
    game = await session.get(GameModel, game_id)
    game.isPublished = True
    await session.commit()
    return game

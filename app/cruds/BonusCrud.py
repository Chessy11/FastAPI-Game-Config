from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Models import BonusModel
from app.schemas import BonusSchema


async def create_bonus(session: AsyncSession, bonus: BonusSchema.BonusInSchema):
    bonus_model = BonusModel(**bonus.dict())
    session.add(bonus_model)
    await session.commit()
    await session.refresh(bonus_model)
    return bonus_model


async def get_bonuses_by_game_id(session: AsyncSession, game_id: int):
    result = await session.execute(
        select(BonusModel)
        .where(BonusModel.game_id == game_id)
    )
    return result.scalars().fetchall()


async def get_bonus_by_id(bonus_id: int, session: AsyncSession):
    return await session.get(BonusModel, bonus_id)

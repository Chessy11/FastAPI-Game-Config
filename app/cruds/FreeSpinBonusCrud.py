from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Models import FreeSpinBonusModel, FreeSpinBonusWinModel
from app.schemas import FreeSpinBonusSchema


async def create_bonus(session: AsyncSession, bonus: FreeSpinBonusSchema.FreeSpinBonusInSchema):
    bonus_model = FreeSpinBonusModel(**bonus.dict())
    session.add(bonus_model)
    await session.commit()
    await session.refresh(bonus_model)
    return bonus_model


async def get_bonuses_by_game_id(session: AsyncSession, game_id: int):
    result = await session.execute(
        select(FreeSpinBonusModel)
        .where(FreeSpinBonusModel.game_id == game_id)
    )
    return result.scalars().unique().fetchall()




async def get_bonus_by_id(bonus_id: int, session: AsyncSession):
    return await session.get(FreeSpinBonusModel, bonus_id)


async def create_bonus_win(session: AsyncSession, bonus_win: FreeSpinBonusSchema.BonusWinInSchema):
    bonus_win_model = FreeSpinBonusWinModel(**bonus_win.dict())
    session.add(bonus_win_model)
    await session.commit()
    await session.refresh(bonus_win_model)
    return bonus_win_model

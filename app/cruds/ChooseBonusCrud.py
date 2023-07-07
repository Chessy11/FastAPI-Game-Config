from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Models import ChooseBonusModel
from app.schemas import ChooseBonusSchema


async def create_choose_bonus(session: AsyncSession, bonus: ChooseBonusSchema.ChooseBonusInSchema):
    bonus_model = ChooseBonusModel(**bonus.dict())
    session.add(bonus_model)
    await session.commit()
    await session.refresh(bonus_model)
    return bonus_model



async def get_choose_bonus_by_id(session: AsyncSession, c_bonus_id: int):
    return await session.get(ChooseBonusModel, c_bonus_id)
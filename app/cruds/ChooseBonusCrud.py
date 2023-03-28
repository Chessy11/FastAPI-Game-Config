from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Models import ChooseBonusModel
from app.schemas import ChooseBonusSchema


async def create_choose_bonus(session: AsyncSession, bonus: ChooseBonusSchema.ChooseBonusInSchema):
    bonus_model = ChooseBonusModel(**bonus.dict())
    session.add(bonus_model)
    await session.commit()
    await session.refresh(bonus_model)
    return bonus_model



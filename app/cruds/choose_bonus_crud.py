from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.models import ChooseBonusModel, GameModel
from app.schemas import choos_bonus_schema
from sqlalchemy import select


async def create_choose_bonus(session: AsyncSession, bonus: choos_bonus_schema.ChooseBonusInSchema, user_id: int):
    # Verify if the user owns the game associated with the bonus
    game = await session.get(GameModel, bonus.game_id)
    if game is None or game.user_id != user_id:
        raise HTTPException(status_code=404, detail="Game not found or not owned by the user")

    bonus_model = ChooseBonusModel(**bonus.dict())
    session.add(bonus_model)
    await session.commit()
    await session.refresh(bonus_model)
    return bonus_model


async def get_choose_bonus_by_id(session: AsyncSession, c_bonus_id: int, user_id: int):
    result = await session.execute(
        select(ChooseBonusModel)
        .join(GameModel, GameModel.game_id == ChooseBonusModel.game_id)
        .where(ChooseBonusModel.c_bonus_id == c_bonus_id, GameModel.user_id == user_id)
    )
    bonus = result.scalars().first()
    if bonus is None:
        raise HTTPException(status_code=404, detail="Choose bonus not found or not owned by the user")
    return bonus

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.models.models import FreeSpinBonusModel, FreeSpinBonusWinModel, GameModel, ChooseBonusModel
from app.schemas import free_spins_bonus_schema
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound,  MultipleResultsFound
from sqlalchemy.orm import selectinload
from app.schemas.free_spins_bonus_schema import BonusWinOutSchema 




async def create_bonus(session: AsyncSession, bonus: free_spins_bonus_schema.FreeSpinBonusInSchema, user_id: int):
    
    game = await session.get(GameModel, bonus.game_id)
    if game is None or game.user_id != user_id:
        raise HTTPException(status_code=404, detail="Game not found or user does not have access")
    
    bonus_model = FreeSpinBonusModel(**bonus.dict())
    session.add(bonus_model)
    await session.commit()
    await session.refresh(bonus_model)
    return bonus_model


async def get_bonuses_by_game_id(session: AsyncSession, game_id: int, user_id: int):
    # Query for FreeSpin bonuses
    free_spin_result = await session.execute(
        select(FreeSpinBonusModel)
        .join(GameModel, GameModel.game_id == FreeSpinBonusModel.game_id)
        .where(FreeSpinBonusModel.game_id == game_id, GameModel.user_id == user_id)
        .options(selectinload(FreeSpinBonusModel.bonus_wins))
    )
    free_spin_bonuses = free_spin_result.scalars().all()

    # Query for ChooseBox bonuses
    choose_box_result = await session.execute(
        select(ChooseBonusModel)
        .join(GameModel, GameModel.game_id == ChooseBonusModel.game_id)
        .where(ChooseBonusModel.game_id == game_id, GameModel.user_id == user_id)
    )
    choose_box_bonuses = choose_box_result.scalars().all()

    # Combine results
    bonuses = {
        "free_spin_bonuses": free_spin_bonuses,
        "choose_box_bonuses": choose_box_bonuses
    }

    return bonuses





async def get_bonus_by_id(bonus_id: int, user_id: int, session: AsyncSession):
    result = await session.execute(
        select(FreeSpinBonusModel)
        .join(GameModel, GameModel.game_id == FreeSpinBonusModel.game_id)
        .where(FreeSpinBonusModel.fs_bonus_id == bonus_id, GameModel.user_id == user_id)
    )
    return result.scalars().first()



async def create_bonus_win(session: AsyncSession, bonus_win: free_spins_bonus_schema.BonusWinInSchema, user_id: int):
    # Define the query with eager loading of the owner relationship
    stmt = select(FreeSpinBonusModel).options(selectinload(FreeSpinBonusModel.owner)).where(FreeSpinBonusModel.fs_bonus_id == bonus_win.fs_bonus_id)

    try:
        # Execute the query and fetch a unique result
        result = await session.execute(stmt)
        bonus = result.scalars().unique().one()

        # Check if the bonus belongs to the user
        if bonus.owner.user_id != user_id:
            raise HTTPException(status_code=403, detail="User does not have access to this bonus")

        # Create a new FreeSpinBonusWinModel instance
        bonus_win_model = FreeSpinBonusWinModel(**bonus_win.dict())

        # Establish the relationship with FreeSpinBonusModel
        bonus.bonus_wins.append(bonus_win_model)

        # Add the new instance to the session and commit
        session.add(bonus_win_model)
        await session.commit()

        # Convert SQLAlchemy model instance to Pydantic model instance
        pydantic_bonus_win = BonusWinOutSchema.from_orm(bonus_win_model)

        return pydantic_bonus_win

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Bonus not found")
    except MultipleResultsFound:
        raise HTTPException(status_code=400, detail="Multiple bonuses found")
    except Exception as e:
        # Rollback in case of an exception
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


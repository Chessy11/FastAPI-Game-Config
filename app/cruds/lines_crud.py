from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.models.models import LinesModel, GameModel
from app.schemas.line_schema import LineInSchema
from fastapi import HTTPException


async def create_line(session: AsyncSession, line: LineInSchema, user_id: int):
    game = await session.get(GameModel, line.game_id)
    if game is None or game.user_id != user_id:
        raise HTTPException(status_code=404, detail="Game not found or not owned by the user")
    
    new_line = LinesModel(**line.dict())
    session.add(new_line)
    await session.commit()
    await session.refresh(new_line)
    return new_line


async def get_line_by_id(line_id: int, user_id: int, session: AsyncSession):
    line = await session.execute(
        select(LinesModel)
        .join(GameModel, GameModel.game_id == LinesModel.game_id)
        .where(LinesModel.line_id == line_id, GameModel.user_id == user_id)
    )
    return line.scalars().first()


async def get_lines_by_game_id(session: AsyncSession, game_id: int, user_id: int):
    result = await session.execute(
        select(LinesModel)
        .join(GameModel, GameModel.game_id == LinesModel.game_id)
        .where(LinesModel.game_id == game_id, GameModel.user_id == user_id)
    )
    return result.scalars().unique().all()


async def delete_line_by_id(session: AsyncSession, line_id: int, user_id: int) -> int:
    line = await session.execute(
        select(LinesModel)
        .join(GameModel, GameModel.game_id == LinesModel.game_id)
        .where(LinesModel.line_id == line_id, GameModel.user_id == user_id)
    )
    line_to_delete = line.scalars().first()
    if line_to_delete is None:
        return 0

    await session.delete(line_to_delete)
    await session.commit()
    return 1


async def check_if_game_has_lines(session: AsyncSession, game_id: int, user_id: int):
    lines = await get_lines_by_game_id(session, game_id, user_id)
    if len(lines) < 3:
        raise HTTPException(status_code=422, detail="Game must contain at least three winning lines")
    return True

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Models import LinesModel
from app.schemas.LineSchema import LineInSchema


async def create_line(session: AsyncSession, line: LineInSchema):
    new_line = LinesModel(**line.dict())
    session.add(new_line)
    await session.commit()
    await session.refresh(new_line)
    return new_line


async def get_line_by_id(line_id: int, session: AsyncSession):
    return await session.get(LinesModel, line_id)


async def get_lines_by_game_id(session: AsyncSession, game_id: int):
    result = await session.execute(
        select(LinesModel)
        .where(LinesModel.game_id == game_id)
    )
    return result.scalars().unique().fetchall()



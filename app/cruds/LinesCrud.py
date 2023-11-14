from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
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


async def delete_line_by_id(session: AsyncSession, line_id: int) -> int:
    result = await session.execute(
        delete(LinesModel).where(LinesModel.line_id == line_id)
        
    )
    print(f"Attempting to delete line with ID: {line_id}")
    await session.commit()
    print(f"Deleted rows: {result.rowcount}")
    return result.rowcount

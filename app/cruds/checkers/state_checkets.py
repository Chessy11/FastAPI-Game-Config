from app.models.models import PaytableModel, ReelsModel, LinesModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

async def check_if_game_has_paytables(session: AsyncSession, game_id: int):
    result = await session.execute(
        select(PaytableModel)
        .where(PaytableModel.game_id == game_id)
    )
    paytables = result.scalars().unique().fetchall()
    return len(paytables) > 0


async def check_if_game_has_reels(session: AsyncSession, game_id: int):
    result = await session.execute(
        select(ReelsModel)
        .where(ReelsModel.game_id == game_id)
    )
    reels = result.scalars().unique().fetchall()
    if len(reels) < 3:
        raise HTTPException("Game must contain at least 3 reels")
    return len(reels) > 3

async def check_if_game_has_lines(session: AsyncSession, game_id: int):
    result = await session.execute(
        select(LinesModel)
        .where(LinesModel.game_id == game_id)
    )
    
    lines = result.scalars().unique().fetchall()
    if len(lines) < 3:
        raise HTTPException("Game must contain at least 3 winning lines")
    return len(lines) > 3

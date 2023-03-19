from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Models import SymbolModel
from app.schemas.SymbolSchema import SymbolInSchema


async def get_symbols_by_game_id(session: AsyncSession, game_id: int):
    result = await session.execute(
        select(SymbolModel)
        .where(SymbolModel.game_id == game_id)
    )
    return result.scalars().fetchall()


async def create_symbol(session: AsyncSession, symbol: SymbolInSchema):
    new_symbol = SymbolModel(**symbol.dict())
    session.add(new_symbol)
    await session.commit()
    await session.refresh(new_symbol)
    return new_symbol


async def get_symbol_by_id(symbol_id: int, session: AsyncSession):
    return await session.get(SymbolModel, symbol_id)

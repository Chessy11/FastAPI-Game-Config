from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.models.Models import SymbolModel, PaytableModel
from app.schemas.SymbolSchema import SymbolInSchema, PaytableInSchema


async def get_symbols_by_game_id(session: AsyncSession, game_id: int):
    result = await session.execute(
        select(SymbolModel)
        .where(SymbolModel.game_id == game_id)
    )
    return result.scalars().unique().fetchall()


async def create_symbol(session: AsyncSession, symbol: SymbolInSchema):
    new_symbol = SymbolModel(**symbol.dict())
    session.add(new_symbol)
    await session.commit()
    await session.refresh(new_symbol)
    return new_symbol


async def get_symbol_by_id(session: AsyncSession, symbol_id: int):
    return await session.get(SymbolModel, symbol_id)

# Delete Symbol
async def delete_symbol(session: AsyncSession, symbol_id: int) -> SymbolModel:
    async with session.begin():  # This starts a transaction
        # Direct delete statement
        result = await session.execute(
            delete(SymbolModel).where(SymbolModel.symbol_id == symbol_id)
        )
        if result.rowcount == 0:  # Check if any row was deleted
            return None
        
        deleted_symbol_result = await session.execute(
            select(SymbolModel)
            .where(SymbolModel.symbol_id == symbol_id)
        )
        deleted_symbol = deleted_symbol_result.scalars().unique().first()
    return deleted_symbol


async def create_paytable(session: AsyncSession, paytable: PaytableInSchema):
    new_paytable = PaytableModel(**paytable.dict())
    session.add(new_paytable)
    await session.commit()
    await session.refresh(new_paytable)
    return new_paytable


async def get_paytables_by_symbol_id(session: AsyncSession, symbol_id: int):
    result = await session.execute(
        select(PaytableModel)
        .where(PaytableModel.symbol_id == symbol_id)
    )
    return result.scalars().fetchall()

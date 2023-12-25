from sqlalchemy import select, delete 
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Models import SymbolModel, PaytableModel, GameModel
from app.schemas.SymbolSchema import SymbolInSchema, PaytableInSchema
from sqlalchemy.orm import selectinload
from fastapi import HTTPException


async def get_symbols_by_game_id(session: AsyncSession, game_id: int, user_id: int):
    result = await session.execute(
        select(SymbolModel)
        .join(GameModel, GameModel.game_id == SymbolModel.game_id)        
        .where(
            SymbolModel.game_id == game_id,
            GameModel.user_id == user_id
            )
    )
    return result.scalars().unique().fetchall()


async def create_symbol(session: AsyncSession, symbol: SymbolInSchema, user_id: int):
    
    game_id = symbol.game_id
    game = await session.get(GameModel, game_id)
    
    if not game or game.user_id != user_id:
        raise HTTPException(status_code=404, detail="Game does not exists or owned by the different user")
    
    new_symbol = SymbolModel(**symbol.dict())
    session.add(new_symbol)
    await session.commit()
    await session.refresh(new_symbol)
    return new_symbol

#  create get symbol by id with user id
async def get_symbol_by_id(session: AsyncSession, symbol_id: int, user_id: int):
    result = await session.execute(
        select(SymbolModel)
        .join(GameModel, GameModel.game_id == SymbolModel.game_id)
        .where(
            SymbolModel.symbol_id == symbol_id,
            GameModel.user_id == user_id
            )
    )
    return result.scalars().unique().first()


async def delete_symbol(session: AsyncSession, symbol_id: int, user_id: int):
    async with session.begin():
        symbol = await session.execute(
            select(SymbolModel)
            .join(GameModel, GameModel.game_id == SymbolModel.game_id)
            .where(SymbolModel.symbol_id == symbol_id, GameModel.user_id == user_id)
        )
        symbol_to_delete = symbol.scalars().first()
        if symbol_to_delete is None:
            return None
        
        await session.delete(symbol_to_delete)
    return symbol_to_delete


async def create_paytable(session: AsyncSession, paytable: PaytableInSchema, user_id: int):
    # Fetch the SymbolModel instance along with its related GameModel
    result = await session.execute(
        select(SymbolModel).options(selectinload(SymbolModel.owner))
        .where(SymbolModel.symbol_id == paytable.symbol_id)
    )
    symbol = result.scalars().first()

    if symbol is None or symbol.owner.user_id != user_id:
        raise HTTPException(status_code=404, detail="Symbol or game not found or not owned by the user")

    new_paytable = PaytableModel(**paytable.dict())
    session.add(new_paytable)
    await session.commit()
    await session.refresh(new_paytable)
    return new_paytable


async def get_paytables_by_symbol_id(session: AsyncSession, symbol_id: int, user_id: int):
    result = await session.execute(
        select(PaytableModel)
        .join(SymbolModel, SymbolModel.symbol_id == PaytableModel.symbol_id)
        .join(GameModel, GameModel.game_id == SymbolModel.game_id)
        .where(SymbolModel.symbol_id == symbol_id, GameModel.user_id == user_id)
    )
    return result.scalars().fetchall()



async def check_if_game_has_symbols(session: AsyncSession, game_id: int, user_id: int):
    symbols = await get_symbols_by_game_id(session, game_id, user_id)
    if len(symbols) < 8:
        raise HTTPException(status_code=422, detail="Game must have at least eight symbols")
    return len(symbols) >= 8


async def check_if_game_has_paytables(session: AsyncSession, game_id: int, user_id: int):
    symbols = await get_symbols_by_game_id(session, game_id, user_id)
    for symbol in symbols:
        # Skip the check if the symbol is a bonus symbol (type 5)
        if symbol.symbol_type == 5:
            continue

        paytables = await get_paytables_by_symbol_id(session, symbol.symbol_id, user_id)
        if len(paytables) == 0:
            raise HTTPException(status_code=422, detail="Each non-bonus symbol must have at least one paytable")
    return True
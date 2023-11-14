from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.SymbolSchema import SymbolInSchema, PaytableInSchema
from app.cruds import SymbolCrud

router = APIRouter()


@router.post("/create-symbol", tags=["symbol"], status_code=201)
async def create_symbol_config(create_symbol: SymbolInSchema, session: AsyncSession = Depends(get_session)):
    try:
        new_symbol = await SymbolCrud.create_symbol(session, create_symbol)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_symbol


@router.get("/symbols/{game_id}", tags=["symbol"], status_code=200)
async def get_symbols_by_game_id(game_id: int, session: AsyncSession = Depends(get_session)):
    symbols = await SymbolCrud.get_symbols_by_game_id(session, game_id)
    return symbols


@router.get("/symbol/{symbol_id}", tags=["symbol"], status_code=200)
async def get_symbol_by_id(symbol_id: int, session: AsyncSession = Depends(get_session)):
    symbol = await SymbolCrud.get_symbol_by_id(session, symbol_id)
    if symbol is None:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return symbol


@router.post("/create-paytable", tags=["symbol"], status_code=201)
async def create_paytable_config(create_paytable: PaytableInSchema, session: AsyncSession = Depends(get_session)):
    try:
        new_paytable = await SymbolCrud.create_paytable(session, create_paytable)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_paytable

@router.delete("/symbols/{symbol_id}", tags=["symbol"], status_code=200)
async def delete_symbol_by_id(symbol_id: int, session: AsyncSession = Depends(get_session)):
    # delete symbol from database
    await SymbolCrud.delete_symbol(session, symbol_id)
    return {"message": f"Symbol with id {symbol_id} deleted successfully"}

@router.get("/paytables/{symbol_id}", tags=["symbol"], status_code=200)
async def paytables_by_symbol_id(symbol_id: int, session: AsyncSession = Depends(get_session)):
    paytables = await SymbolCrud.get_paytables_by_symbol_id(session, symbol_id)
    return paytables




    
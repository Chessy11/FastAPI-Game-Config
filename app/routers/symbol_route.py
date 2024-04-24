from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.symbol_schema import SymbolInSchema, PaytableInSchema
from app.cruds import symbol_crud
from app.schemas.user_schema import UserOutSchema
from app.utils.auth import get_current_active_user

router = APIRouter()

@router.post("/create-symbol", tags=["symbol"], status_code=201)
async def create_symbol_config(
    create_symbol: SymbolInSchema, 
    current_user: UserOutSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    try:
        # Modify the function call to include the current_user's information if needed
        new_symbol = await symbol_crud.create_symbol(session, create_symbol, current_user.user_id)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_symbol

@router.get("/symbols/{game_id}", tags=["symbol"], status_code=200)
async def get_symbols_by_game_id(
    game_id: int, 
    current_user: UserOutSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    # Modify the logic here to ensure the current_user has access to the requested game_id
    symbols = await symbol_crud.get_symbols_by_game_id(session, game_id, current_user.user_id)
    return symbols

@router.get("/symbol/{symbol_id}", tags=["symbol"], status_code=200)
async def get_symbol_by_id(
    symbol_id: int, 
    current_user: UserOutSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    # Modify the logic here to ensure the current_user has access to the requested symbol_id
    symbol = await symbol_crud.get_symbol_by_id(session, symbol_id, current_user.user_id)
    if symbol is None:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return symbol

@router.post("/create-paytable", tags=["symbol"], status_code=201)
async def create_paytable_config(
    create_paytable: PaytableInSchema, 
    current_user: UserOutSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    try:
        # Modify the function call to include the current_user's information if needed
        new_paytable = await symbol_crud.create_paytable(session, create_paytable, current_user.user_id)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_paytable

@router.delete("/symbols/{symbol_id}", tags=["symbol"], status_code=200)
async def delete_symbol_by_id(
    symbol_id: int, 
    current_user: UserOutSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    # Modify the logic here to ensure the current_user has access to the requested symbol_id
    await symbol_crud.delete_symbol(session, symbol_id, current_user.user_id)
    return {"message": f"Symbol with id {symbol_id} deleted successfully"}

@router.get("/paytables/{symbol_id}", tags=["symbol"], status_code=200)
async def paytables_by_symbol_id(
    symbol_id: int, 
    current_user: UserOutSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    # Modify the logic here to ensure the current_user has access to the requested symbol_id
    paytables = await symbol_crud.get_paytables_by_symbol_id(session, symbol_id, current_user.user_id)
    return paytables

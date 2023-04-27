from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.LineSchema import LineInSchema
from app.cruds import LinesCrud

router = APIRouter(
    tags=["line"]
)


@router.post("/create-line", status_code=201)
async def create_line_config(create_line: LineInSchema, session: AsyncSession = Depends(get_session)):
    try:
        new_line = await LinesCrud.create_line(session, create_line)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_line


@router.get("/lines/{game_id}", status_code=200)
async def get_lines_by_game_id(game_id: int, session: AsyncSession = Depends(get_session)):
    lines = await LinesCrud.get_lines_by_game_id(session, game_id)
    return lines


@router.get("/line/{line_id}", status_code=200)
async def get_line_by_id(line_id: int, session: AsyncSession = Depends(get_session)):
    line = await LinesCrud.get_line_by_id(line_id, session)
    if line is None:
        raise HTTPException(status_code=404, detail="Line not found")
    return line
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.db import get_session
from app.schemas.LineSchema import LineInSchema
from app.schemas.UserSchema import UserOutSchema
from app.cruds import LinesCrud
from app.utils.auth import get_current_active_user


router = APIRouter(
    tags=["line"]
)


@router.post("/create-line", status_code=201)
async def create_line_config(create_line: LineInSchema, 
                             current_user: UserOutSchema = Depends(get_current_active_user),
                             session: AsyncSession = Depends(get_session)):
    try:
        new_line = await LinesCrud.create_line(session, create_line, current_user.user_id)
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=str(ie.orig))
    return new_line


@router.get("/lines/{game_id}", status_code=200)
async def get_lines_by_game_id(game_id: int, 
                               current_user: UserOutSchema = Depends(get_current_active_user),
                               session: AsyncSession = Depends(get_session)):
    lines = await LinesCrud.get_lines_by_game_id(session, game_id, current_user.user_id)
    return lines


@router.get("/line/{line_id}", status_code=200)
async def get_line_by_id(line_id: int,
                         current_user: UserOutSchema = Depends(get_current_active_user), 
                         session: AsyncSession = Depends(get_session)):
    line = await LinesCrud.get_line_by_id(line_id, session, current_user.user_id)
    if line is None:
        raise HTTPException(status_code=404, detail="Line not found")
    return line


logger = logging.getLogger(__name__)


@router.delete("/delete_line/{line_id}", status_code=200)
async def delete_line_by_id(line_id: int, 
                            current_user: UserOutSchema = Depends(get_current_active_user),
                            session: AsyncSession = Depends(get_session)):
    try:
        deleted_count = await LinesCrud.delete_line_by_id(session, line_id, current_user.user_id)
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Line not found")
        return {"deleted_count": deleted_count}
    except Exception as e:
        logger.error(f"Unexpected error deleting line: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error deleting line")

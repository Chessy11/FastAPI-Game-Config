from fastapi import FastAPI, HTTPException, Request, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.models.models import SymbolModel

router = APIRouter()

@router.post("/create-sprite")
async def create_sprite(request: Request, session: AsyncSession = Depends(get_session)):
    body = await request.json()
    tag = body.get("tag")
    symbol_id = body.get("symbolId")
    frame_count = body.get("frameCount")

    if not tag or not symbol_id:
        raise HTTPException(status_code=400, detail="Missing tag or symbol ID")

    try:
        cloud_name = 'dvkx54vv2'  # Replace with your Cloudinary cloud name
        sprite_url = f"https://res.cloudinary.com/{cloud_name}/image/sprite/{tag}.png"

        # Update symbol in database
        symbol = await session.get(SymbolModel, symbol_id)
        if not symbol:
            raise HTTPException(status_code=404, detail="Symbol not found")
        
        symbol.animation_url = sprite_url
        symbol.frame_count = frame_count
        await session.commit()
        await session.refresh(symbol)

        return {"sprite_url": sprite_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

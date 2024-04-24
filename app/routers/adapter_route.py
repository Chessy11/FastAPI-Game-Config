from fastapi import APIRouter, HTTPException
from app.schemas.adapter_schema import IdAdapterSchema

router = APIRouter()

game_id_store = {}

@router.post("/set-game-id/{session_id}")
async def set_game_id(session_id: str, game_id_request: IdAdapterSchema):
    game_id_store[session_id] = game_id_request.game_id
    return {"message": "Game ID received"}

@router.get("/get-game-id/{session_id}")
async def get_game_id(session_id: str):
    game_id = game_id_store.get(session_id)
    if game_id is None:
        raise HTTPException(status_code=404, detail="Game ID not found")
    return {"game_id": game_id}

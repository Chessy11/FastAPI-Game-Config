from pydantic import BaseModel, HttpUrl

from app.schemas.BonusSchema import BonusOutSchema
from app.schemas.SymbolSchema import SymbolOutSchema


class GameInSchema(BaseModel):
    game_name: str
    game_desc: str
    game_type: str
    banner_img: HttpUrl
    game_rtp: float


class GameOutSchema(BaseModel):
    game_id: int
    game_name: str
    game_desc: str
    game_type: str
    banner_img: HttpUrl
    game_rtp: float
    symbols: list[SymbolOutSchema]
    bonuses: list[BonusOutSchema]

    class Config:
        orm_mode = True

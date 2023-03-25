from pydantic import BaseModel, HttpUrl

from app.schemas.ChooseBonusSchema import ChooseBonusOutSchema
from app.schemas.FreeSpinBonusSchema import FreeSpinBonusOutSchema
from app.schemas.SymbolSchema import SymbolOutSchema
from app.schemas.ReelSchema import ReelOutSchema


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
    bonuses: list[FreeSpinBonusOutSchema, ChooseBonusOutSchema]
    reels: list[ReelOutSchema]

    class Config:
        orm_mode = True

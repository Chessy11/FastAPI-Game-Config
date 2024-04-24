from pydantic import BaseModel

from app.schemas.choos_bonus_schema import ChooseBonusOutSchema
from app.schemas.free_spins_bonus_schema import FreeSpinBonusOutSchema
from app.schemas.symbol_schema import SymbolOutSchema
from app.schemas.reel_schema import ReelOutSchema
from app.schemas.line_schema import LineOutSchema


class GameInSchema(BaseModel):
    game_name: str
    game_desc: str
    game_type: str
    banner_img: str
    game_rtp: float


class GameOutSchema(BaseModel):
    game_id: int
    game_name: str
    game_desc: str
    game_type: str
    banner_img: str
    game_rtp: float
    isPublished: bool
    symbols: list[SymbolOutSchema]
    free_spin_bonuses: list[FreeSpinBonusOutSchema]
    choose_bonuses: list[ChooseBonusOutSchema]
    reels: list[ReelOutSchema]
    lines: list[LineOutSchema]

    class Config:
        orm_mode = True

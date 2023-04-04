from pydantic import BaseModel

from app.schemas.ChooseBonusSchema import ChooseBonusOutSchema
from app.schemas.FreeSpinBonusSchema import FreeSpinBonusOutSchema
from app.schemas.SymbolSchema import SymbolOutSchema
from app.schemas.ReelSchema import ReelOutSchema


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
    banner_img: HttpUrl
    game_rtp: float
    isPublished: bool
    symbols: list[SymbolOutSchema]
    free_spin_bonuses: list[FreeSpinBonusOutSchema]
    choose_bonuses: list[ChooseBonusOutSchema]
    reels: list[ReelOutSchema]

    class Config:
        orm_mode = True

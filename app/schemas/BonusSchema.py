from pydantic import BaseModel


class BonusInSchema(BaseModel):
    game_id: int
    symbol_id: int
    bonus_name: str
    bonus_type: int


class BonusOutSchema(BaseModel):
    bonus_id: int
    game_id: int
    symbol_id: int
    bonus_name: str
    bonus_type: int

    class Config:
        orm_mode = True

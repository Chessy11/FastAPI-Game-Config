from pydantic import BaseModel


class BonusWinInSchema(BaseModel):
    fs_bonus_id: int
    symbol_count: int
    free_spin_count: int


class BonusWinOutSchema(BaseModel):
    fs_bonus_id: int
    symbol_count: int
    free_spin_count: int

    class Config:
        orm_mode = True


class FreeSpinBonusInSchema(BaseModel):
    game_id: int
    symbol_id: int
    bonus_type: int


class FreeSpinBonusOutSchema(BaseModel):
    bonus_id: int
    game_id: int
    symbol_id: int
    bonus_type: int
    bonus_wins: list['BonusWinOutSchema']

    class Config:
        orm_mode = True

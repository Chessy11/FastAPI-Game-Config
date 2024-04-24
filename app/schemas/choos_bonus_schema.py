from pydantic import BaseModel


class ChooseBonusInSchema(BaseModel):
    game_id: int
    symbol_id: int
    bonus_type: int
    choose_count: int
    win_list: list[int]


class ChooseBonusOutSchema(BaseModel):
    c_bonus_id: int
    game_id: int
    symbol_id: int
    bonus_type: int
    choose_count: int
    win_list: list[int]

    class Config:
        orm_mode = True

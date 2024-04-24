from pydantic import BaseModel, Field
from typing import List, Any


class LineInSchema(BaseModel):
    game_id: int
    line_number: int
    symbol_positions: List[int]


class LineOutSchema(BaseModel):
    line_id: int
    line_number: int
    symbol_positions: List[int]

    class Config:
        orm_mode = True

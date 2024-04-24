from pydantic import BaseModel
from typing import Optional



class PaytableInSchema(BaseModel):
    symbol_id: int
    s_count: int
    s_payout: int


class PaytableOutSchema(BaseModel):
    paytable_id: int
    symbol_id: int
    s_count: int
    s_payout: int

    class Config:
        orm_mode = True


class SymbolInSchema(BaseModel):
    game_id: int
    symbol_name: str
    symbol_type: int
    image_url: Optional[str] = None
    animation_url: Optional[str] = None
    frame_count: Optional[int] = None


class SymbolOutSchema(BaseModel):
    symbol_id: int
    symbol_name: str
    symbol_type: int
    paytables: list['PaytableOutSchema']
    image_url: Optional[str] = None
    animation_url: Optional[str] = None

    class Config:
        orm_mode = True

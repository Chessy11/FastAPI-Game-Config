from pydantic import BaseModel


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


class SymbolOutSchema(BaseModel):
    symbol_id: int
    game_id: int
    symbol_name: str
    symbol_type: int
    paytables: list['PaytableOutSchema']

    class Config:
        orm_mode = True

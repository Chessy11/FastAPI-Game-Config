from pydantic import BaseModel


class SymbolInSchema(BaseModel):
    game_id: int
    symbol_name: str
    symbol_type: int


class SymbolOutSchema(BaseModel):
    symbol_id: int
    game_id: int
    symbol_name: str
    symbol_type: int

    class Config:
        orm_mode = True

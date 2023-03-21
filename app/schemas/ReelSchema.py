from pydantic import BaseModel


class ReelInSchema(BaseModel):
    game_id: int
    position: int


class ReelSymbolInSchema(BaseModel):
    reel_id: int
    symbol_id: int
    location: int


class ReelSymbolOutSchema(BaseModel):
    reel_id: int
    symbol_id: int
    location: int

    class Config:
        orm_mode = True


class ReelOutSchema(BaseModel):
    reel_id: int
    game_id: int
    position: int
    symbols: list[ReelSymbolOutSchema]

    class Config:
        orm_mode = True

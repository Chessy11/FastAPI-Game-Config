from pydantic import BaseModel


class GameConfigSchema(BaseModel):
    name: str
    description: str
    reels: int
    lines: int
    symbols: int
    game_type: str
    symbol: str
    weight: int
    reel_num: list[int]
    position: list[int]
    payout: int
    count: int





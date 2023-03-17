from pydantic import BaseModel


class GameInSchema(BaseModel):
    name: str
    description: str
    type: str
    banner: str
    rtp: float






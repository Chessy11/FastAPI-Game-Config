from pydantic import BaseModel


class GameConfigSchema(BaseModel):
    name: str
    description: str

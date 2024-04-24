from pydantic import BaseModel

class IdAdapterSchema(BaseModel):
    game_id: int


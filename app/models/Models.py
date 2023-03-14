from sqlalchemy import Column, Integer, String

from app.db import Base


class GameConfigModel(Base):
    __tablename__ = "game_config"
    game_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String[255])

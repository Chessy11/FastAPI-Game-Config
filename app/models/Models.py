from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class GameConfigModel(Base):
    __tablename__ = "game_config"
    game_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String[255], nullable=False)
    symbols = Column(Integer, nullable=False)
    reels = Column(Integer, nullable=False)
    lines = Column(Integer, nullable=False)
    game_type = Column(String, nullable=False)


class GameSymbols(Base):
    __tablename__ = "game_symbols"
    symbol_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game_config.game_id", ondelete="CASCADE"), nullable=False)
    game = relationship("GameConfigModel", back_populates="symbols")
    symbol = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)


class ReelSymbols(Base):
    __tablename__ = "reel_symbols"
    rs_id = Column(Integer, primary_key=True, index=True)
    symbol_id = Column(Integer, ForeignKey("game_symbols.symbol_id", ondelete="CASCADE"), nullable=False, index=True)
    game_id = Column(Integer, ForeignKey("game_config.game_id", ondelete="CASCADE"), nullable=False)
    symbol = relationship("GameSymbols", back_populates="reels")
    reel_num = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)


class GamePaytable(Base):
    __tablename__ = "game_paytable"
    paytable_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game_config.game_id", ondelete="CASCADE"), nullable=False)
    game = relationship("GameConfigModel", back_populates="paytable")
    symbol_id = Column(Integer, ForeignKey("game_symbols.symbol_id", ondelete="CASCADE"), nullable=False, index=True)
    payout = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)


class BonusGame(Base):
    __tablename__ = "bonus_game"
    bonus_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game_config.game_id", ondelete="CASCADE"), nullable=False)
    game = relationship("GameConfigModel", back_populates="bonus")
    bonus_type = Column(Integer, nullable=False)

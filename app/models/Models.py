from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db import Base


class GameModel(Base):
    __tablename__ = "games"
    game_id = Column(Integer, primary_key=True, index=True)
    game_name = Column(String, nullable=False)
    game_desc = Column(String[255], nullable=False)
    game_type = Column(String, nullable=False)
    banner_img = Column(String, nullable=False)
    game_rtp = Column(Float, nullable=False)

    symbols = relationship("SymbolModel", back_populates="owner")
    bonuses = relationship("BonusModel", back_populates="owner", lazy="joined")
    reels = relationship("ReelsModel", back_populates="owner", lazy="joined")


class SymbolModel(Base):
    __tablename__ = "symbols"
    symbol_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.game_id", ondelete="CASCADE"), nullable=False)
    symbol_name = Column(String, nullable=False)
    symbol_type = Column(Integer, nullable=False)

    owner = relationship("GameModel", back_populates="symbols")
    paytables = relationship("PaytableModel", back_populates="owner", lazy="joined")


class BonusModel(Base):
    __tablename__ = "bonuses"
    bonus_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.game_id", ondelete="CASCADE"), nullable=False)
    symbol_id = Column(Integer, ForeignKey("symbols.symbol_id", ondelete="CASCADE"), nullable=False, index=True)
    bonus_type = Column(Integer, nullable=False)
    bonus_name = Column(String, nullable=False)

    owner = relationship("GameModel", back_populates="bonuses")


class ReelsModel(Base):
    __tablename__ = "reels"
    reel_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.game_id", ondelete="CASCADE"), nullable=False)
    position = Column(Integer, nullable=False)

    owner = relationship("GameModel", back_populates="reels")
    symbols = relationship("ReelSymbolsModel", back_populates="owner", lazy="joined")


class ReelSymbolsModel(Base):
    __tablename__ = "reel_symbols"
    rs_id = Column(Integer, primary_key=True, index=True)
    symbol_id = Column(Integer, ForeignKey("symbols.symbol_id", ondelete="CASCADE"), nullable=False)
    reel_id = Column(Integer, ForeignKey("reels.reel_id", ondelete="CASCADE"), nullable=False)
    location = Column(Integer, nullable=False)

    owner = relationship("ReelsModel", back_populates="symbols")


class BonusWinModel(Base):
    __tablename__ = "bonus_wins"
    bw_id = Column(Integer, primary_key=True, index=True)
    bonus_id = Column(Integer, ForeignKey("bonuses.bonus_id", ondelete="CASCADE"), nullable=False)
    b_count = Column(Integer, nullable=False)
    b_payout = Column(Integer, nullable=False)


class PaytableModel(Base):
    __tablename__ = "paytables"
    paytable_id = Column(Integer, primary_key=True, index=True)
    symbol_id = Column(Integer, ForeignKey("symbols.symbol_id", ondelete="CASCADE"), nullable=False)
    s_count = Column(Integer, nullable=False)
    s_payout = Column(Integer, nullable=False)

    owner = relationship("SymbolModel", back_populates="paytables")

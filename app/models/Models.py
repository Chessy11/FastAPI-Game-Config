from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
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
    isPublished = Column(Boolean, nullable=False, default=False)

    symbols = relationship("SymbolModel", back_populates="owner")
    free_spin_bonuses = relationship("FreeSpinBonusModel", back_populates="owner", lazy="joined")
    choose_bonuses = relationship("ChooseBonusModel", back_populates="owner", lazy="joined")
    reels = relationship("ReelsModel", back_populates="owner", lazy="joined")


class SymbolModel(Base):
    __tablename__ = "symbols"
    symbol_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.game_id", ondelete="CASCADE"), nullable=False)
    symbol_name = Column(String, nullable=False)
    symbol_type = Column(Integer, nullable=False)

    owner = relationship("GameModel", back_populates="symbols")
    paytables = relationship("PaytableModel", back_populates="owner", lazy="joined")


class FreeSpinBonusModel(Base):
    __tablename__ = "free_spin_bonus"
    fs_bonus_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.game_id", ondelete="CASCADE"), nullable=False)
    symbol_id = Column(Integer, ForeignKey("symbols.symbol_id", ondelete="CASCADE"), nullable=False, index=True)
    bonus_type = Column(Integer, nullable=False)

    owner = relationship("GameModel", back_populates="free_spin_bonuses")
    bonus_wins = relationship("FreeSpinBonusWinModel", back_populates="owner", lazy="joined")


class ChooseBonusModel(Base):
    __tablename__ = "choose_bonus"
    c_bonus_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.game_id", ondelete="CASCADE"), nullable=False)
    symbol_id = Column(Integer, ForeignKey("symbols.symbol_id", ondelete="CASCADE"), nullable=False, index=True)
    bonus_type = Column(Integer, nullable=False)
    choose_count = Column(Integer, nullable=False)
    win_list = Column(ARRAY(Integer), nullable=False)

    owner = relationship("GameModel", back_populates="choose_bonuses")


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


class FreeSpinBonusWinModel(Base):
    __tablename__ = "free_spin_bonus_wins"
    fsbw_id = Column(Integer, primary_key=True, index=True)
    fs_bonus_id = Column(Integer, ForeignKey("free_spin_bonus.fs_bonus_id", ondelete="CASCADE"), nullable=False)
    symbol_count = Column(Integer, nullable=False)
    free_spin_count = Column(Integer, nullable=False)

    owner = relationship("FreeSpinBonusModel", back_populates="bonus_wins")


class PaytableModel(Base):
    __tablename__ = "paytables"
    paytable_id = Column(Integer, primary_key=True, index=True)
    symbol_id = Column(Integer, ForeignKey("symbols.symbol_id", ondelete="CASCADE"), nullable=False)
    s_count = Column(Integer, nullable=False)
    s_payout = Column(Integer, nullable=False)

    owner = relationship("SymbolModel", back_populates="paytables")


class UserModel(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)


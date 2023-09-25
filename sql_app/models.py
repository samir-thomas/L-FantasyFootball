from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from sql_app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    squad_name = Column(String)

    squad = relationship("Squad", back_populates="user")


class Squad(Base):
    __tablename__ = "squad"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    player_id = Column(Integer, ForeignKey("player.id"))
    status = Column(Boolean, default=True)
    starter = Column(Boolean, default=False)
    captain = Column(Boolean, default=False)
    vice_captain = Column(Boolean, default=False)

    player = relationship("Player", back_populates="squad")
    user = relationship("User", back_populates="squad")


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    position = Column(String)
    club = Column(String)
    cost = Column(Float)
    total_points = Column(Integer)

    squad = relationship("Squad", back_populates="player")


class Position(Base):
    __tablename__ = "position"

    position_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Club(Base):
    __tablename__ = "club"

    team_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    league = Column(String, index=True)

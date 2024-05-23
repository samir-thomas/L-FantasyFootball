from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str
    position: str
    club: str
    cost: float
    total_points: int


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str
    email: str
    squad_name: str


class User(UserBase):
    id: int
    email: str
    is_active: bool
    squad_name: str

    class Config:
        from_attributes = True


class SquadBase(BaseModel):
    pass


class SquadCreate(SquadBase):
    user_id: int
    player_id: int
    starter: bool
    captain: bool
    vice_captain: bool


class SquadPlayerId(SquadBase):
    player_id: int


class Subs(BaseModel):
    player_in: int
    player_out: int


class SquadPlayerUser(BaseModel):
    user_id: int
    player_id: int
    starter: bool
    captain: bool
    vice_captain: bool
    position: str


class Squad(SquadBase):
    id: int
    status: bool

    class Config:
        orm_mode = True


class Club(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ClubBase(Club):
    pass


class ClubCreate(ClubBase):
    name: str


class League(BaseModel):
    name: str
    league_size: int

    class Config:
        orm_mode = True

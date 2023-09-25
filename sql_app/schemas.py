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


class Squad(SquadBase):
    id: int
    status: bool

    class Config:
        orm_mode = True





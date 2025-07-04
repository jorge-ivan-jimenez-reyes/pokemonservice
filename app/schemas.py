from pydantic import BaseModel
from typing import Optional

class PokemonBase(BaseModel):
    name: str
    type1: str
    type2: Optional[str] = None
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int
    height: float
    weight: float
    description: Optional[str] = None

class PokemonCreate(PokemonBase):
    pass

class PokemonUpdate(BaseModel):
    name: Optional[str] = None
    type1: Optional[str] = None
    type2: Optional[str] = None
    hp: Optional[int] = None
    attack: Optional[int] = None
    defense: Optional[int] = None
    sp_attack: Optional[int] = None
    sp_defense: Optional[int] = None
    speed: Optional[int] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    description: Optional[str] = None

class Pokemon(PokemonBase):
    id: int

    class Config:
        from_attributes = True 
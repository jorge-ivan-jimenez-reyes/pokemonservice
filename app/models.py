from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Pokemon(Base):
    __tablename__ = "pokemon"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    type1 = Column(String, nullable=False)
    type2 = Column(String, nullable=True)
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    sp_attack = Column(Integer, nullable=False)
    sp_defense = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    height = Column(Float, nullable=False)  # en metros
    weight = Column(Float, nullable=False)  # en kg
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)  # URL de la imagen del Pokémon 
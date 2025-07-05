from pydantic import BaseModel, Field
from typing import Optional

class PokemonBase(BaseModel):
    name: str = Field(..., description="Nombre del Pokémon", example="Pikachu")
    type1: str = Field(..., description="Tipo principal del Pokémon", example="Electric")
    type2: Optional[str] = Field(None, description="Tipo secundario del Pokémon (opcional)", example="Flying")
    hp: int = Field(..., ge=1, le=999, description="Puntos de vida", example=35)
    attack: int = Field(..., ge=1, le=999, description="Estadística de ataque", example=55)
    defense: int = Field(..., ge=1, le=999, description="Estadística de defensa", example=40)
    sp_attack: int = Field(..., ge=1, le=999, description="Estadística de ataque especial", example=50)
    sp_defense: int = Field(..., ge=1, le=999, description="Estadística de defensa especial", example=50)
    speed: int = Field(..., ge=1, le=999, description="Estadística de velocidad", example=90)
    height: float = Field(..., gt=0, description="Altura en metros", example=0.4)
    weight: float = Field(..., gt=0, description="Peso en kilogramos", example=6.0)
    description: Optional[str] = Field(None, description="Descripción del Pokémon", example="Un ratón eléctrico muy famoso")
    image_url: Optional[str] = Field(None, description="URL de la imagen del Pokémon", example="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png")

class PokemonCreate(PokemonBase):
    """Esquema para crear un nuevo Pokémon"""
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Pikachu",
                "type1": "Electric",
                "type2": None,
                "hp": 35,
                "attack": 55,
                "defense": 40,
                "sp_attack": 50,
                "sp_defense": 50,
                "speed": 90,
                "height": 0.4,
                "weight": 6.0,
                "description": "Un ratón eléctrico muy famoso y querido",
                "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
            }
        }

class PokemonUpdate(BaseModel):
    """Esquema para actualizar un Pokémon existente"""
    name: Optional[str] = Field(None, description="Nuevo nombre del Pokémon", example="Raichu")
    type1: Optional[str] = Field(None, description="Nuevo tipo principal", example="Electric")
    type2: Optional[str] = Field(None, description="Nuevo tipo secundario", example="Psychic")
    hp: Optional[int] = Field(None, ge=1, le=999, description="Nuevos puntos de vida", example=60)
    attack: Optional[int] = Field(None, ge=1, le=999, description="Nueva estadística de ataque", example=90)
    defense: Optional[int] = Field(None, ge=1, le=999, description="Nueva estadística de defensa", example=55)
    sp_attack: Optional[int] = Field(None, ge=1, le=999, description="Nueva estadística de ataque especial", example=90)
    sp_defense: Optional[int] = Field(None, ge=1, le=999, description="Nueva estadística de defensa especial", example=80)
    speed: Optional[int] = Field(None, ge=1, le=999, description="Nueva estadística de velocidad", example=110)
    height: Optional[float] = Field(None, gt=0, description="Nueva altura en metros", example=0.8)
    weight: Optional[float] = Field(None, gt=0, description="Nuevo peso en kilogramos", example=30.0)
    description: Optional[str] = Field(None, description="Nueva descripción del Pokémon", example="La evolución de Pikachu")
    image_url: Optional[str] = Field(None, description="Nueva URL de imagen del Pokémon", example="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/26.png")

    class Config:
        schema_extra = {
            "example": {
                "name": "Raichu",
                "hp": 60,
                "attack": 90,
                "speed": 110,
                "description": "La evolución de Pikachu con mayor poder eléctrico",
                "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/26.png"
            }
        }

class Pokemon(PokemonBase):
    """Esquema de respuesta con información completa del Pokémon"""
    id: int = Field(..., description="ID único del Pokémon", example=25)

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 25,
                "name": "Pikachu",
                "type1": "Electric",
                "type2": None,
                "hp": 35,
                "attack": 55,
                "defense": 40,
                "sp_attack": 50,
                "sp_defense": 50,
                "speed": 90,
                "height": 0.4,
                "weight": 6.0,
                "description": "Un ratón eléctrico muy famoso y querido",
                "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
            }
        }

class ErrorResponse(BaseModel):
    """Esquema de respuesta para errores"""
    detail: str = Field(..., description="Descripción del error", example="Pokemon no encontrado")

class SuccessResponse(BaseModel):
    """Esquema de respuesta para operaciones exitosas"""
    message: str = Field(..., description="Mensaje de éxito", example="Pokemon eliminado correctamente") 
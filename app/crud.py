from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

def get_pokemon(db: Session, pokemon_id: int):
    return db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()

def get_pokemon_by_name(db: Session, name: str):
    return db.query(models.Pokemon).filter(models.Pokemon.name == name).first()

def get_pokemons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pokemon).offset(skip).limit(limit).all()

def create_pokemon(db: Session, pokemon: schemas.PokemonCreate):
    db_pokemon = models.Pokemon(**pokemon.dict())
    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon

def update_pokemon(db: Session, pokemon_id: int, pokemon: schemas.PokemonUpdate):
    db_pokemon = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()
    if db_pokemon:
        update_data = pokemon.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_pokemon, field, value)
        db.commit()
        db.refresh(db_pokemon)
    return db_pokemon

def delete_pokemon(db: Session, pokemon_id: int):
    db_pokemon = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()
    if db_pokemon:
        db.delete(db_pokemon)
        db.commit()
    return db_pokemon

def search_pokemon_by_type(db: Session, pokemon_type: str):
    return db.query(models.Pokemon).filter(
        (models.Pokemon.type1 == pokemon_type) | 
        (models.Pokemon.type2 == pokemon_type)
    ).all() 
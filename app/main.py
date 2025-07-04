from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pokemon API", description="API CRUD para gestión de Pokémon", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de Pokémon!"}

@app.post("/pokemon/", response_model=schemas.Pokemon)
def create_pokemon(pokemon: schemas.PokemonCreate, db: Session = Depends(get_db)):
    db_pokemon = crud.get_pokemon_by_name(db, name=pokemon.name)
    if db_pokemon:
        raise HTTPException(status_code=400, detail="Pokemon ya existe")
    return crud.create_pokemon(db=db, pokemon=pokemon)

@app.get("/pokemon/", response_model=List[schemas.Pokemon])
def read_pokemons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pokemons = crud.get_pokemons(db, skip=skip, limit=limit)
    return pokemons

@app.get("/pokemon/{pokemon_id}", response_model=schemas.Pokemon)
def read_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    db_pokemon = crud.get_pokemon(db, pokemon_id=pokemon_id)
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")
    return db_pokemon

@app.get("/pokemon/name/{pokemon_name}", response_model=schemas.Pokemon)
def read_pokemon_by_name(pokemon_name: str, db: Session = Depends(get_db)):
    db_pokemon = crud.get_pokemon_by_name(db, name=pokemon_name)
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")
    return db_pokemon

@app.put("/pokemon/{pokemon_id}", response_model=schemas.Pokemon)
def update_pokemon(pokemon_id: int, pokemon: schemas.PokemonUpdate, db: Session = Depends(get_db)):
    db_pokemon = crud.update_pokemon(db, pokemon_id=pokemon_id, pokemon=pokemon)
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")
    return db_pokemon

@app.delete("/pokemon/{pokemon_id}")
def delete_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    db_pokemon = crud.delete_pokemon(db, pokemon_id=pokemon_id)
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")
    return {"message": "Pokemon eliminado correctamente"}

@app.get("/pokemon/type/{pokemon_type}", response_model=List[schemas.Pokemon])
def search_pokemon_by_type(pokemon_type: str, db: Session = Depends(get_db)):
    pokemons = crud.search_pokemon_by_type(db, pokemon_type=pokemon_type)
    return pokemons 
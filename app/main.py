from fastapi import FastAPI, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="🐉 Pokemon API",
    description="""
    ## API CRUD completa para gestión de Pokémon
    
    Esta API te permite:
    * **Crear** nuevos Pokémon con todas sus estadísticas
    * **Leer** información de Pokémon individuales o listas
    * **Actualizar** datos de Pokémon existentes
    * **Eliminar** Pokémon de la base de datos
    * **Buscar** Pokémon por tipo o nombre
    
    ### Base de datos incluye:
    - ✅ 200 Pokémon de la primera generación
    - ✅ Estadísticas completas de combate
    - ✅ Tipos primarios y secundarios
    - ✅ Medidas físicas (altura/peso)
    - ✅ Descripciones detalladas
    
    ### Tipos de Pokémon disponibles:
    `Normal`, `Fire`, `Water`, `Electric`, `Grass`, `Ice`, `Fighting`, `Poison`, 
    `Ground`, `Flying`, `Psychic`, `Bug`, `Rock`, `Ghost`, `Dragon`, `Dark`, 
    `Steel`, `Fairy`
    """,
    version="1.0.0",
    contact={
        "name": "Pokemon API Support",
        "email": "support@pokemonapi.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    tags_metadata=[
        {
            "name": "root",
            "description": "Endpoint principal de bienvenida",
        },
        {
            "name": "pokemon",
            "description": "Operaciones CRUD para Pokémon. Crear, leer, actualizar y eliminar Pokémon.",
        },
        {
            "name": "search",
            "description": "Funciones de búsqueda y filtrado de Pokémon.",
        },
    ]
)

@app.get(
    "/",
    tags=["root"],
    summary="Página de bienvenida",
    description="Endpoint principal que muestra información básica de la API"
)
def read_root():
    """
    ## ¡Bienvenido a la Pokemon API! 🐉
    
    Esta es la página principal de la API. Desde aquí puedes:
    - Explorar los endpoints en `/docs` (Swagger UI)
    - Ver la documentación alternativa en `/redoc`
    - Acceder a todos los endpoints CRUD de Pokémon
    """
    return {
        "message": "¡Bienvenido a la API de Pokémon!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "pokemon": "/pokemon/",
            "search_by_type": "/pokemon/type/{type}",
            "get_by_name": "/pokemon/name/{name}"
        }
    }

@app.post(
    "/pokemon/",
    response_model=schemas.Pokemon,
    status_code=201,
    tags=["pokemon"],
    summary="Crear nuevo Pokémon",
    description="Crea un nuevo Pokémon con todas sus estadísticas y datos",
    responses={
        201: {"description": "Pokémon creado exitosamente"},
        400: {"description": "Error de validación o Pokémon ya existe", "model": schemas.ErrorResponse},
        422: {"description": "Error de validación de datos"}
    }
)
def create_pokemon(
    pokemon: schemas.PokemonCreate,
    db: Session = Depends(get_db)
):
    """
    ## Crear un nuevo Pokémon
    
    Crea un nuevo Pokémon en la base de datos con todas sus estadísticas:
    
    - **name**: Nombre único del Pokémon
    - **type1**: Tipo principal (requerido)
    - **type2**: Tipo secundario (opcional)
    - **hp, attack, defense, sp_attack, sp_defense, speed**: Estadísticas de combate
    - **height**: Altura en metros
    - **weight**: Peso en kilogramos
    - **description**: Descripción del Pokémon (opcional)
    
    ### Tipos válidos:
    Normal, Fire, Water, Electric, Grass, Ice, Fighting, Poison, Ground, 
    Flying, Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, Fairy
    """
    try:
        db_pokemon = crud.get_pokemon_by_name(db, name=pokemon.name)
        if db_pokemon:
            raise HTTPException(
                status_code=400, 
                detail=f"El Pokémon '{pokemon.name}' ya existe en la base de datos"
            )
        return crud.create_pokemon(db=db, pokemon=pokemon)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail=f"Error al crear Pokémon: {str(e)}")

@app.get(
    "/pokemon/",
    response_model=List[schemas.Pokemon],
    tags=["pokemon"],
    summary="Obtener lista de Pokémon",
    description="Obtiene una lista paginada de todos los Pokémon",
    responses={
        200: {"description": "Lista de Pokémon obtenida exitosamente"},
        422: {"description": "Parámetros de paginación inválidos"}
    }
)
def read_pokemons(
    skip: int = Query(0, ge=0, description="Número de registros a omitir para paginación"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a devolver"),
    db: Session = Depends(get_db)
):
    """
    ## Obtener lista de Pokémon
    
    Devuelve una lista paginada de Pokémon con toda su información.
    
    ### Parámetros de paginación:
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a devolver (máximo 1000)
    
    ### Ejemplo de uso:
    - Primeros 10 Pokémon: `skip=0&limit=10`
    - Pokémon 11-20: `skip=10&limit=10`
    - Pokémon 51-100: `skip=50&limit=50`
    """
    try:
        pokemons = crud.get_pokemons(db, skip=skip, limit=limit)
        return pokemons
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener Pokémon: {str(e)}")

@app.get(
    "/pokemon/{pokemon_id}",
    response_model=schemas.Pokemon,
    tags=["pokemon"],
    summary="Obtener Pokémon por ID",
    description="Obtiene un Pokémon específico mediante su ID único",
    responses={
        200: {"description": "Pokémon encontrado exitosamente"},
        404: {"description": "Pokémon no encontrado", "model": schemas.ErrorResponse},
        422: {"description": "ID inválido"}
    }
)
def read_pokemon(
    pokemon_id: int = Path(..., ge=1, description="ID único del Pokémon a buscar"),
    db: Session = Depends(get_db)
):
    """
    ## Obtener Pokémon por ID
    
    Busca y devuelve un Pokémon específico usando su ID único.
    
    ### Parámetros:
    - **pokemon_id**: ID único del Pokémon (número entero positivo)
    
    ### Ejemplos:
    - Buscar Bulbasaur: `pokemon_id=1`
    - Buscar Pikachu: `pokemon_id=25`
    - Buscar Charizard: `pokemon_id=6`
    """
    try:
        db_pokemon = crud.get_pokemon(db, pokemon_id=pokemon_id)
        if db_pokemon is None:
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontró ningún Pokémon con ID {pokemon_id}"
            )
        return db_pokemon
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error al buscar Pokémon: {str(e)}")

@app.get(
    "/pokemon/name/{pokemon_name}",
    response_model=schemas.Pokemon,
    tags=["search"],
    summary="Obtener Pokémon por nombre",
    description="Obtiene un Pokémon específico mediante su nombre",
    responses={
        200: {"description": "Pokémon encontrado exitosamente"},
        404: {"description": "Pokémon no encontrado", "model": schemas.ErrorResponse}
    }
)
def read_pokemon_by_name(
    pokemon_name: str = Path(..., min_length=1, description="Nombre del Pokémon a buscar"),
    db: Session = Depends(get_db)
):
    """
    ## Buscar Pokémon por nombre
    
    Busca y devuelve un Pokémon específico usando su nombre exacto.
    
    ### Parámetros:
    - **pokemon_name**: Nombre exacto del Pokémon (sensible a mayúsculas/minúsculas)
    
    ### Ejemplos de nombres válidos:
    - `Pikachu`
    - `Charizard`
    - `Bulbasaur`
    - `Mr. Mime`
    - `Nidoran♀`
    
    **Nota**: El nombre debe coincidir exactamente con el almacenado en la base de datos.
    """
    try:
        db_pokemon = crud.get_pokemon_by_name(db, name=pokemon_name)
        if db_pokemon is None:
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontró ningún Pokémon con el nombre '{pokemon_name}'"
            )
        return db_pokemon
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error al buscar Pokémon: {str(e)}")

@app.put(
    "/pokemon/{pokemon_id}",
    response_model=schemas.Pokemon,
    tags=["pokemon"],
    summary="Actualizar Pokémon",
    description="Actualiza parcial o completamente los datos de un Pokémon existente",
    responses={
        200: {"description": "Pokémon actualizado exitosamente"},
        404: {"description": "Pokémon no encontrado", "model": schemas.ErrorResponse},
        400: {"description": "Error de validación", "model": schemas.ErrorResponse},
        422: {"description": "Datos inválidos"}
    }
)
def update_pokemon(
    pokemon_id: int = Path(..., ge=1, description="ID del Pokémon a actualizar"),
    pokemon: schemas.PokemonUpdate = None,
    db: Session = Depends(get_db)
):
    """
    ## Actualizar Pokémon existente
    
    Actualiza uno o más campos de un Pokémon existente. Solo se actualizarán los campos proporcionados.
    
    ### Parámetros:
    - **pokemon_id**: ID del Pokémon a actualizar
    - **pokemon**: Objeto con los campos a actualizar (todos opcionales)
    
    ### Campos actualizables:
    - **name**: Nuevo nombre
    - **type1, type2**: Tipos primario y secundario
    - **hp, attack, defense, sp_attack, sp_defense, speed**: Estadísticas
    - **height, weight**: Medidas físicas
    - **description**: Nueva descripción
    
    ### Ejemplo de actualización parcial:
    Solo actualizar HP y descripción:
    ```json
    {
        "hp": 120,
        "description": "Pokémon fortalecido"
    }
    ```
    """
    try:
        db_pokemon = crud.update_pokemon(db, pokemon_id=pokemon_id, pokemon=pokemon)
        if db_pokemon is None:
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontró ningún Pokémon con ID {pokemon_id}"
            )
        return db_pokemon
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail=f"Error al actualizar Pokémon: {str(e)}")

@app.delete(
    "/pokemon/{pokemon_id}",
    response_model=schemas.SuccessResponse,
    tags=["pokemon"],
    summary="Eliminar Pokémon",
    description="Elimina permanentemente un Pokémon de la base de datos",
    responses={
        200: {"description": "Pokémon eliminado exitosamente"},
        404: {"description": "Pokémon no encontrado", "model": schemas.ErrorResponse}
    }
)
def delete_pokemon(
    pokemon_id: int = Path(..., ge=1, description="ID del Pokémon a eliminar"),
    db: Session = Depends(get_db)
):
    """
    ## Eliminar Pokémon
    
    Elimina permanentemente un Pokémon de la base de datos.
    
    ### ⚠️ Advertencia:
    Esta operación es **irreversible**. El Pokémon será eliminado permanentemente.
    
    ### Parámetros:
    - **pokemon_id**: ID único del Pokémon a eliminar
    
    ### Respuesta exitosa:
    Devuelve un mensaje de confirmación cuando el Pokémon es eliminado correctamente.
    """
    try:
        db_pokemon = crud.delete_pokemon(db, pokemon_id=pokemon_id)
        if db_pokemon is None:
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontró ningún Pokémon con ID {pokemon_id}"
            )
        return {"message": f"Pokémon '{db_pokemon.name}' (ID: {pokemon_id}) eliminado correctamente"}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error al eliminar Pokémon: {str(e)}")

@app.get(
    "/pokemon/type/{pokemon_type}",
    response_model=List[schemas.Pokemon],
    tags=["search"],
    summary="Buscar Pokémon por tipo",
    description="Busca todos los Pokémon que tengan un tipo específico (principal o secundario)",
    responses={
        200: {"description": "Lista de Pokémon del tipo especificado"},
        404: {"description": "No se encontraron Pokémon del tipo especificado"}
    }
)
def search_pokemon_by_type(
    pokemon_type: str = Path(..., description="Tipo de Pokémon a buscar"),
    db: Session = Depends(get_db)
):
    """
    ## Buscar Pokémon por tipo
    
    Encuentra todos los Pokémon que tengan el tipo especificado como tipo principal o secundario.
    
    ### Tipos disponibles:
    `Normal`, `Fire`, `Water`, `Electric`, `Grass`, `Ice`, `Fighting`, `Poison`, 
    `Ground`, `Flying`, `Psychic`, `Bug`, `Rock`, `Ghost`, `Dragon`, `Dark`, 
    `Steel`, `Fairy`
    
    ### Ejemplos:
    - Buscar tipo `Fire`: Devuelve Charmander, Charmeleon, Charizard, Vulpix, etc.
    - Buscar tipo `Electric`: Devuelve Pikachu, Raichu, Magnemite, etc.
    - Buscar tipo `Flying`: Devuelve tanto Pokémon Flying primarios como secundarios
    
    ### Nota:
    La búsqueda incluye tanto el tipo principal como el secundario del Pokémon.
    """
    try:
        pokemons = crud.search_pokemon_by_type(db, pokemon_type=pokemon_type)
        if not pokemons:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron Pokémon del tipo '{pokemon_type}'. Verifica que el tipo sea válido."
            )
        return pokemons
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error al buscar Pokémon por tipo: {str(e)}") 
# Pokemon API 🐉

API CRUD completa para gestionar Pokémon usando FastAPI, PostgreSQL y Docker.

## Características

- ✅ CRUD completo (Create, Read, Update, Delete) para Pokémon
- ✅ Base de datos PostgreSQL con 200 Pokémon precargados
- ✅ API REST con FastAPI
- ✅ Dockerizado con docker-compose
- ✅ Documentación automática con Swagger
- ✅ Búsqueda por tipo de Pokémon
- ✅ Validación de datos con Pydantic

## Estructura del Proyecto

```
pokemonservice/
├── app/
│   ├── __init__.py
│   ├── main.py          # Aplicación FastAPI principal
│   ├── models.py        # Modelos SQLAlchemy
│   ├── schemas.py       # Esquemas Pydantic
│   ├── crud.py          # Operaciones CRUD
│   ├── database.py      # Configuración de base de datos
│   └── config.py        # Configuración de la aplicación
├── migrations/
│   └── init_pokemon_data.sql  # Script con 200 Pokémon
├── requirements.txt     # Dependencias Python
├── Dockerfile          # Imagen Docker de la aplicación
├── docker-compose.yml  # Configuración multi-contenedor
└── README.md
```

## Instalación y Uso

### Opción 1: Con Docker (Recomendado)

```bash
# Clonar el repositorio y navegar al directorio
cd pokemonservice

# Levantar los servicios
docker-compose up --build

# La API estará disponible en http://localhost:8000
```

### Opción 2: Instalación Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (crear archivo .env)
DATABASE_URL=postgresql://pokemon_user:pokemon_pass@localhost:5432/pokemon_db

# Ejecutar la aplicación
uvicorn app.main:app --reload
```

## Endpoints de la API

### Documentación Interactiva
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principales

#### 🏠 Root
- `GET /` - Mensaje de bienvenida

#### 🐉 Pokémon CRUD
- `POST /pokemon/` - Crear nuevo Pokémon
- `GET /pokemon/` - Obtener lista de Pokémon (con paginación)
- `GET /pokemon/{pokemon_id}` - Obtener Pokémon por ID
- `GET /pokemon/name/{pokemon_name}` - Obtener Pokémon por nombre
- `PUT /pokemon/{pokemon_id}` - Actualizar Pokémon
- `DELETE /pokemon/{pokemon_id}` - Eliminar Pokémon

#### 🔍 Búsqueda
- `GET /pokemon/type/{pokemon_type}` - Buscar Pokémon por tipo

## Ejemplos de Uso

### Crear un Pokémon
```bash
curl -X POST "http://localhost:8000/pokemon/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MiPokemon",
    "type1": "Electric",
    "type2": "Flying",
    "hp": 100,
    "attack": 85,
    "defense": 70,
    "sp_attack": 95,
    "sp_defense": 80,
    "speed": 120,
    "height": 1.5,
    "weight": 45.0,
    "description": "Un Pokémon eléctrico muy rápido"
  }'
```

### Obtener todos los Pokémon
```bash
curl "http://localhost:8000/pokemon/?skip=0&limit=10"
```

### Buscar por tipo
```bash
curl "http://localhost:8000/pokemon/type/Fire"
```

### Obtener Pokémon específico
```bash
curl "http://localhost:8000/pokemon/1"
curl "http://localhost:8000/pokemon/name/Pikachu"
```

## Modelo de Datos

Cada Pokémon tiene los siguientes campos:

```python
{
  "id": int,           # ID único
  "name": str,         # Nombre del Pokémon
  "type1": str,        # Tipo principal
  "type2": str|null,   # Tipo secundario (opcional)
  "hp": int,           # Puntos de vida
  "attack": int,       # Ataque
  "defense": int,      # Defensa
  "sp_attack": int,    # Ataque especial
  "sp_defense": int,   # Defensa especial
  "speed": int,        # Velocidad
  "height": float,     # Altura en metros
  "weight": float,     # Peso en kilogramos
  "description": str   # Descripción (opcional)
}
```

## Base de Datos

La base de datos PostgreSQL viene precargada con 200 Pokémon de la primera generación, incluyendo:
- Los 150 Pokémon originales (Bulbasaur a Mew)
- Estadísticas completas de combate
- Tipos primarios y secundarios
- Medidas físicas (altura/peso)
- Descripciones únicas

## Tecnologías Utilizadas

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Base de datos relacional
- **Pydantic** - Validación de datos
- **Docker** - Containerización
- **Uvicorn** - Servidor ASGI

## Variables de Entorno

```env
DATABASE_URL=postgresql://pokemon_user:pokemon_pass@db:5432/pokemon_db
POSTGRES_USER=pokemon_user
POSTGRES_PASSWORD=pokemon_pass
POSTGRES_DB=pokemon_db
```

## Comandos Útiles

```bash
# Ver logs de la aplicación
docker-compose logs app

# Ver logs de la base de datos
docker-compose logs db

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (resetear DB)
docker-compose down -v

# Reconstruir contenedores
docker-compose up --build --force-recreate
```

## Desarrollo

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

¡Disfruta construyendo con la Pokemon API! 🚀 
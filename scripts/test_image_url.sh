#!/bin/bash

# Script para probar la nueva funcionalidad de image_url
# Este script prueba crear, leer y actualizar Pokémon con imágenes

set -e

API_URL="http://localhost:8001"

echo "🧪 Probando nueva funcionalidad de image_url..."

# Probar obtener un Pokémon existente con imagen
echo "📋 1. Obteniendo Pikachu (debería tener image_url):"
curl -s "${API_URL}/pokemon/25" | jq '.'

echo -e "\n"

# Probar crear un nuevo Pokémon con imagen
echo "🆕 2. Creando un nuevo Pokémon con imagen:"
curl -s -X POST "${API_URL}/pokemon/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TestPokemon",
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
    "description": "Un Pokémon de prueba",
    "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
  }' | jq '.'

echo -e "\n"

# Obtener el ID del Pokémon recién creado
POKEMON_ID=$(curl -s "${API_URL}/pokemon/name/TestPokemon" | jq -r '.id')

if [ "$POKEMON_ID" != "null" ]; then
    echo "✅ Pokémon creado con ID: $POKEMON_ID"
    
    # Probar actualizar la imagen
    echo "🔄 3. Actualizando la imagen del Pokémon:"
    curl -s -X PUT "${API_URL}/pokemon/${POKEMON_ID}" \
      -H "Content-Type: application/json" \
      -d '{
        "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/26.png"
      }' | jq '.'
    
    echo -e "\n"
    
    # Verificar la actualización
    echo "🔍 4. Verificando la actualización:"
    curl -s "${API_URL}/pokemon/${POKEMON_ID}" | jq '.'
    
    echo -e "\n"
    
    # Limpiar - eliminar el Pokémon de prueba
    echo "🗑️ 5. Eliminando Pokémon de prueba:"
    curl -s -X DELETE "${API_URL}/pokemon/${POKEMON_ID}" | jq '.'
    
else
    echo "❌ Error: No se pudo crear el Pokémon de prueba"
fi

echo -e "\n"

# Probar búsqueda por tipo con imágenes
echo "🔍 6. Obteniendo Pokémon de tipo Electric (con imágenes):"
curl -s "${API_URL}/pokemon/type/Electric?limit=5" | jq '.'

echo -e "\n"

# Probar obtener lista con imágenes
echo "📋 7. Obteniendo lista de Pokémon con imágenes:"
curl -s "${API_URL}/pokemon/?limit=5" | jq '.'

echo -e "\n🎉 Pruebas completadas!"
echo "📝 Verifica que todos los Pokémon ahora incluyan el campo 'image_url'"
echo "🌐 Puedes ver la documentación actualizada en: ${API_URL}/docs" 
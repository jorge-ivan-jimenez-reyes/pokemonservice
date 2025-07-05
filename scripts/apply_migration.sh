#!/bin/bash

# Script para aplicar la migración de image_url
# Este script debe ejecutarse después de que la aplicación esté corriendo

set -e

echo "🔄 Aplicando migración para agregar campo image_url..."

# Verificar que Docker Compose esté corriendo
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Error: Los servicios no están corriendo. Ejecuta primero: docker-compose up -d"
    exit 1
fi

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que la base de datos esté lista..."
sleep 10

# Aplicar la migración
echo "🗄️ Ejecutando migración en la base de datos..."
docker-compose exec -T db psql -U pokemon_user -d pokemon_db -f /docker-entrypoint-initdb.d/add_image_url_column.sql

# Verificar que la migración se aplicó correctamente
echo "✅ Verificando que la migración se aplicó correctamente..."
docker-compose exec -T db psql -U pokemon_user -d pokemon_db -c "\d pokemon" | grep -q "image_url" && echo "✅ Campo image_url agregado exitosamente" || echo "❌ Error al agregar campo image_url"

# Mostrar algunos Pokémon con sus imágenes
echo "📋 Mostrando algunos Pokémon con sus imágenes:"
docker-compose exec -T db psql -U pokemon_user -d pokemon_db -c "SELECT id, name, image_url FROM pokemon WHERE id <= 10;"

echo "🎉 Migración completada exitosamente!"
echo ""
echo "📝 Ahora puedes:"
echo "1. Reiniciar la aplicación: docker-compose restart app"
echo "2. Probar la API con el nuevo campo image_url"
echo "3. Acceder a la documentación: http://localhost:8001/docs" 
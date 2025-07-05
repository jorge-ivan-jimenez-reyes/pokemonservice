#!/bin/bash

# Script de despliegue para Pokemon API
# Este script debe ejecutarse en el servidor de producción

set -e

echo "🚀 Iniciando despliegue de Pokemon API..."

# Verificar que Docker y Docker Compose están instalados
if ! [ -x "$(command -v docker)" ]; then
  echo '❌ Error: Docker no está instalado.' >&2
  exit 1
fi

if ! [ -x "$(command -v docker-compose)" ]; then
  echo '❌ Error: Docker Compose no está instalado.' >&2
  exit 1
fi

# Detener servicios existentes si están corriendo
echo "🛑 Deteniendo servicios existentes..."
docker-compose down

# Construir imágenes
echo "🔨 Construyendo imágenes..."
docker-compose build --no-cache

# Iniciar servicios de base de datos y aplicación
echo "🗄️ Iniciando base de datos y aplicación..."
docker-compose up -d db app

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que la base de datos esté lista..."
sleep 30

# Verificar que la aplicación esté funcionando
echo "🔍 Verificando que la aplicación esté funcionando..."
timeout 60 bash -c 'until curl -f http://localhost:8001/; do sleep 2; done' || {
  echo "❌ Error: La aplicación no responde"
  docker-compose logs app
  exit 1
}

echo "✅ Aplicación funcionando correctamente"

# Iniciar Nginx
echo "🌐 Iniciando Nginx..."
docker-compose up -d nginx

echo "✅ Despliegue completado!"
echo ""
echo "📝 Próximos pasos:"
echo "1. Configurar DNS para apuntar apps.api.ioslab.dev a este servidor"
echo "2. Ejecutar ./scripts/init-letsencrypt.sh para obtener certificados SSL"
echo "3. Tu API estará disponible en https://apps.api.ioslab.dev"
echo ""
echo "📊 Para verificar el estado de los servicios:"
echo "   docker-compose ps"
echo ""
echo "📋 Para ver los logs:"
echo "   docker-compose logs -f" 
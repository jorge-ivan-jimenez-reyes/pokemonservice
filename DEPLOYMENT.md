# Guía de Despliegue - Pokemon API 🚀

Esta guía te ayudará a desplegar tu Pokemon API en un servidor con el dominio `https://apps.api.ioslab.dev/`.

## Pre-requisitos

### En tu servidor de producción:
- Docker instalado
- Docker Compose instalado
- Puertos 80 y 443 abiertos
- Acceso root o sudo

### DNS Configuration:
- El dominio `apps.api.ioslab.dev` debe apuntar a la IP de tu servidor

## Pasos de Despliegue

### 1. Preparar el servidor

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker (si no está instalado)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
# Cerrar sesión y volver a iniciarla
```

### 2. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd pokemonservice
```

### 3. Configurar variables de entorno

Edita el archivo `scripts/init-letsencrypt.sh` y cambia:
```bash
email="tu-email@ejemplo.com"  # Cambia por tu email real
```

### 4. Ejecutar el despliegue

```bash
# Ejecutar el script de despliegue
./scripts/deploy.sh
```

### 5. Configurar SSL

Una vez que el DNS esté configurado correctamente:

```bash
# Obtener certificados SSL
./scripts/init-letsencrypt.sh
```

## Verificación

### Verificar que los servicios estén corriendo:
```bash
docker-compose ps
```

### Ver logs:
```bash
# Logs de todos los servicios
docker-compose logs -f

# Logs específicos
docker-compose logs -f app
docker-compose logs -f nginx
docker-compose logs -f db
```

### Probar la API:
```bash
# Probar localmente
curl http://localhost:8001/

# Probar con el dominio (después de configurar SSL)
curl https://apps.api.ioslab.dev/
```

## Estructura de Archivos Añadidos

```
pokemonservice/
├── nginx/
│   ├── nginx.conf                    # Configuración principal de Nginx
│   ├── sites-available/
│   │   └── pokemon-api              # Configuración del sitio
│   └── sites-enabled/
│       └── pokemon-api              # Enlace simbólico
├── scripts/
│   ├── deploy.sh                    # Script de despliegue
│   └── init-letsencrypt.sh          # Script para SSL
├── certbot/
│   ├── conf/                        # Certificados SSL
│   └── www/                         # Archivos de verificación
└── DEPLOYMENT.md                    # Esta guía
```

## Configuración de Nginx

La configuración de Nginx incluye:
- ✅ Reverse proxy hacia FastAPI
- ✅ SSL/TLS con Let's Encrypt
- ✅ Redirección HTTP → HTTPS
- ✅ Headers de seguridad
- ✅ Compresión gzip
- ✅ Configuración optimizada

## Mantenimiento

### Renovar certificados SSL:
Los certificados se renuevan automáticamente, pero puedes forzar la renovación:
```bash
docker-compose exec certbot certbot renew
docker-compose exec nginx nginx -s reload
```

### Actualizar la aplicación:
```bash
git pull origin main
docker-compose build --no-cache
docker-compose up -d
```

### Backup de la base de datos:
```bash
docker-compose exec db pg_dump -U pokemon_user pokemon_db > backup.sql
```

### Restaurar backup:
```bash
docker-compose exec -T db psql -U pokemon_user -d pokemon_db < backup.sql
```

## Troubleshooting

### Error: "nginx: [emerg] cannot load certificate"
- Asegúrate de que el DNS esté configurado correctamente
- Ejecuta primero `./scripts/init-letsencrypt.sh`

### Error: "Connection refused"
- Verifica que los puertos 80 y 443 estén abiertos
- Revisa los logs: `docker-compose logs nginx`

### Error: "Database connection failed"
- Verifica que la base de datos esté corriendo: `docker-compose ps`
- Revisa los logs: `docker-compose logs db`

## URLs Importantes

Una vez desplegado:
- **API Principal**: https://apps.api.ioslab.dev/
- **Documentación Swagger**: https://apps.api.ioslab.dev/docs
- **ReDoc**: https://apps.api.ioslab.dev/redoc

## Comandos Útiles

```bash
# Ver estado de servicios
docker-compose ps

# Reiniciar un servicio específico
docker-compose restart app

# Ver logs en tiempo real
docker-compose logs -f

# Ejecutar comando en contenedor
docker-compose exec app bash

# Limpiar sistema Docker
docker system prune -a
```

¡Tu Pokemon API estará disponible en https://apps.api.ioslab.dev/ ! 🎉 
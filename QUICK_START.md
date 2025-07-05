# Quick Start - Despliegue Pokemon API 🚀

## Resumen Rápido

Para exponer tu Pokemon API en `https://apps.api.ioslab.dev/`:

### 1. En tu servidor de producción:

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd pokemonservice

# Configurar email para SSL
nano scripts/init-letsencrypt.sh
# Cambiar: email="tu-email@ejemplo.com"

# Desplegar
./scripts/deploy.sh

# Configurar SSL (después de configurar DNS)
./scripts/init-letsencrypt.sh
```

### 2. Configurar DNS:
- Apuntar `apps.api.ioslab.dev` a la IP de tu servidor

### 3. Verificar:
```bash
curl https://apps.api.ioslab.dev/
```

## Archivos Creados

- `docker-compose.yml` - Actualizado con Nginx y Certbot
- `nginx/` - Configuración del reverse proxy
- `scripts/deploy.sh` - Script de despliegue
- `scripts/init-letsencrypt.sh` - Script para SSL
- `DEPLOYMENT.md` - Guía completa

## URLs Finales

- **API**: https://apps.api.ioslab.dev/
- **Docs**: https://apps.api.ioslab.dev/docs
- **ReDoc**: https://apps.api.ioslab.dev/redoc

¡Listo! 🎉 
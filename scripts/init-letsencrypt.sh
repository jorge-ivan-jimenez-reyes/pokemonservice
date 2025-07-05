#!/bin/bash

# Script para inicializar Let's Encrypt y obtener certificados SSL
# Este script debe ejecutarse en el servidor donde se desplegará la aplicación

if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Error: docker-compose no está instalado.' >&2
  exit 1
fi

domains=(apps.api.ioslab.dev)
rsa_key_size=4096
data_path="./certbot"
email="tu-email@ejemplo.com" # Cambia esto por tu email
staging=0 # Cambiar a 1 para usar el entorno de staging de Let's Encrypt

if [ -d "$data_path" ]; then
  read -p "Los datos de certificados existentes para $domains serán eliminados. ¿Continuar? (y/N) " decision
  if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
    exit
  fi
fi

if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
  echo "### Descargando configuración SSL recomendada ..."
  mkdir -p "$data_path/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"
  echo
fi

echo "### Creando certificado dummy para $domains ..."
path="/etc/letsencrypt/live/$domains"
mkdir -p "$data_path/conf/live/$domains"
docker-compose run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:$rsa_key_size -days 1\
    -keyout '$path/privkey.pem' \
    -out '$path/fullchain.pem' \
    -subj '/CN=localhost'" certbot
echo

echo "### Iniciando nginx ..."
docker-compose up --force-recreate -d nginx
echo

echo "### Eliminando certificado dummy para $domains ..."
docker-compose run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live/$domains && \
  rm -Rf /etc/letsencrypt/archive/$domains && \
  rm -Rf /etc/letsencrypt/renewal/$domains.conf" certbot
echo

echo "### Solicitando certificado SSL para $domains ..."

# Seleccionar argumentos apropiados
if [ $staging != "0" ]; then staging_arg="--staging"; fi

docker-compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    --email $email \
    --agree-tos \
    --no-eff-email \
    -d $domains" certbot
echo

echo "### Reiniciando nginx ..."
docker-compose exec nginx nginx -s reload 
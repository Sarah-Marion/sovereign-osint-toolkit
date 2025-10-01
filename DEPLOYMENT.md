# 🚀 Sovereign OSINT Toolkit - Deployment Guide

## Quick Start

### Option 1: Docker (Recommended)
```bash
# Copy environment template
cp .env.template .env

# Deploy with Docker
chmod +x deploy.sh
./deploy.sh

## SSL/TLS Configuration

### Using Let's Encrypt (Recommended for Production)

#### Option 1: Nginx Proxy with Let's Encrypt
```bash
# Start nginx-proxy
docker run -d \
  --name nginx-proxy \
  -p 80:80 -p 443:443 \
  -v /etc/nginx/certs \
  -v /etc/nginx/vhost.d \
  -v /usr/share/nginx/html \
  -v /var/run/docker.sock:/tmp/docker.sock:ro \
  jwilder/nginx-proxy

# Start Let's Encrypt companion
docker run -d \
  --name nginx-proxy-letsencrypt \
  --volumes-from nginx-proxy \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  jrcs/letsencrypt-nginx-proxy-companion

# Run your app with VIRTUAL_HOST and LETSENCRYPT_HOST env vars
docker run -d \
  --name sovereign-app \
  -e VIRTUAL_HOST=yourdomain.com \
  -e LETSENCRYPT_HOST=yourdomain.com \
  -e LETSENCRYPT_EMAIL=admin@yourdomain.com \
  your-image
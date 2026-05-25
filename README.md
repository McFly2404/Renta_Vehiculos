# DriveNow - Entregable 2

Ecosistema hibrido para renta de vehiculos con:
- Monolito Django (usuarios, reservas, UI, integraciones)
- Microservicio Flask para pagos (`/api/v2/pagos/`)
- API Gateway Nginx (Strangler Pattern)
- PostgreSQL compartida
- Redis + Celery para procesamiento asincrono

## 1. Arquitectura objetivo

Servicios en `docker-compose.yml`:
- `nginx`: punto de entrada y ruteo
- `django_web`: monolito legacy
- `flask_pagos`: microservicio extraido
- `db`: PostgreSQL
- `redis`: message broker
- `celery_worker`: tareas de fondo

Ruteo por Nginx:
- `/api/v2/pagos/` -> `flask_pagos`
- Todo lo demas -> `django_web`

## 2. Requisitos

- Docker y Docker Compose
- (Opcional local sin Docker) Python 3.11+

## 3. Variables de entorno importantes

- Copiar `.env.example` a `.env` y ajustar valores.
- `ALLY_SERVICE_URL`: endpoint JSON del equipo aliado
- `WEATHER_API_URL`: API de terceros (Adapter, Open-Meteo por defecto)
- `WEATHER_LAT`, `WEATHER_LON`, `WEATHER_CITY`: ubicacion para API externa
- `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`: Redis

## 4. Ejecucion con Docker

```bash
docker compose up --build
```

Accesos:
- App: `http://localhost/`
- Integraciones: `http://localhost/integraciones/`
- API docs UI: `http://localhost/docs/`
- Admin Django: `http://localhost/admin/`
- Health microservicio: `http://localhost/api/v2/health/`

Datos demo:
- Docker ejecuta `python manage.py seed_demo_data` al iniciar Django.
- Para correrlo manualmente: `docker compose exec django_web python manage.py seed_demo_data`
- Para liberar de nuevo los vehiculos demo: `docker compose exec django_web python manage.py seed_demo_data --reset-disponibilidad`

## 5. Endpoints relevantes (Entrega 2)

### Servicio a Proveer (JSON propio)
- `GET /api/integraciones/resumen/`

### Servicio a Consumir (aliado)
- `GET /api/integraciones/aliado/`

### API de terceros via Adapter (DIP)
- `GET /api/integraciones/tercero/`

### Snapshot combinado para UI
- `GET /api/integraciones/snapshot/`

### Strangler - pagos migrados
- `POST /api/v2/pagos/` (Flask)
- `GET /api/v2/pagos/<id>/` (Flask)

## 6. Asincronia con Celery

Tareas en segundo plano:
- `reservas.notificar_reserva_creada`
- `pagos.notificar_pago_confirmado`
- `reservas.generar_reporte_simple`

Se disparan al crear reserva/pago; si el broker no esta disponible, hay fallback sincronico.

## 7. i18n

- `LocaleMiddleware` habilitado
- Idiomas: `es`, `en`
- Selector de idioma en navbar
- Catalogos: `locale/es` y `locale/en`

Notas:
- `compilemessages` se ejecuta al iniciar `django_web` en Docker.
- Se usa `gettext` para textos base y mensajes clave de validacion.

## 8. Evidencia para sustentacion

- Mantener encendida la instancia EC2
- Compartir IP elastica y repo en rama `main`
- Verificar commits por integrante

# Matriz de Requisitos de Infraestructura y Componentes (AA1)

Este documento define la matriz numerada de requisitos de infraestructura tecnológica para el despliegue de la aplicación multiservicio en contenedores Docker, con sus respectivos criterios de aceptación técnicamente verificables (Competencia 220501086).

---

## 1. Matriz de Requisitos de Infraestructura

| # | Requisito de Infraestructura | Criterio de Aceptación Verificable |
|---|-----------------------------|-----------------------------------|
| **RI-01** | Los tres servicios se ejecutan en contenedores independientes. | `docker compose ps` muestra tres servicios (`proxy`, `api`, `db`) en estado `Up`. |
| **RI-02** | Solo el proxy inverso está expuesto al exterior (puerto público del host). | `docker compose port db 5432` no devuelve mapeo; `curl --max-time 3 http://localhost:5432` no responde desde el host. |
| **RI-03** | Los datos de la base de datos persisten a los reinicios del servicio. | Tras ejecutar `docker compose down` y posteriormente `docker compose up -d`, los datos previamente insertados continúan disponibles. |
| **RI-04** | La solución completa opera en equipos con límite de 4 GB de memoria RAM. | `docker stats` no supera los límites establecidos ni agota los recursos de memoria del host con los tres servicios en ejecución. |
| **RI-05** | La configuración sensible y credenciales no están escritas en el código fuente. | Las credenciales se inyectan mediante variables de entorno desde `.env`; el archivo `.env` está registrado en `.gitignore` y no figura en el repositorio. |
| **RI-06** | La API backend se ejecuta bajo un usuario sin privilegios de superusuario (no-root). | `docker exec <id_api> whoami` o `docker run --rm api-app:1.0.0 whoami` devuelve `appuser` (UID 1001) y no `root`. |
| **RI-07** | Aislamiento y resolución de nombres mediante red interna privada tipo bridge. | `docker compose exec api python -c "import socket; print(socket.gethostbyname('db'))"` resuelve exitosamente la IP privada del contenedor de base de datos. |
| **RI-08** | Verificación automática de salud (*healthcheck*) para control de dependencias en arranque. | `docker compose ps` muestra el servicio `db` en estado `healthy` antes de que el servicio `api` inicie su ejecución. |
| **RI-OS-01** | Compatibilidad y reproducibilidad en entorno Windows 10/11 con WSL2. | La solución se levanta sin errores de finales de línea o permisos en la terminal de Ubuntu sobre WSL2 con Docker Engine nativo. |
| **RI-OS-02** | Compatibilidad y reproducibilidad en entorno Linux nativo (Ubuntu 22.04/24.04/26.04). | Los servicios se ejecutan de manera idéntica usando Docker Engine como servicio systemd sin Docker Desktop. |
| **RI-OS-03** | Compatibilidad y reproducibilidad en entorno macOS con arquitectura ARM64/Intel. | La construcción y ejecución se realiza mediante Colima/Docker CLI sin diferencias funcionales de arquitectura. |

---

## 2. Componentes de Hardware y Software

| Componente | Imagen Base Oficial | Puerto Interno | Requisito Clave de Infraestructura |
|------------|---------------------|----------------|------------------------------------|
| **Proxy Inverso** | `nginx:1.30-alpine` | 80 | Enrutar peticiones entrantes hacia la API backend (`http://api:8000`) preservando headers HTTP. Único servicio con puerto expuesto al host (`8080:80`). |
| **API Backend** | `python:3.14-slim` | 8000 | Conexión a PostgreSQL vía red interna privada. Construcción multi-etapa para reducción de superficie de ataque y tamaño de imagen. |
| **Base de Datos** | `postgres:18-alpine` | 5432 | Almacenamiento persistente en volumen Docker con nombre (`pgdata`). Restricción de memoria para entornos de bajos recursos (`shared_buffers=32MB`, `max_connections=20`). |


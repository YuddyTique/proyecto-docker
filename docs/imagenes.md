# Ficha de Administración de Imágenes (AA2 y AA3)

Este documento registra la administración, inventario, tamaño, capas y justificación de las imágenes utilizadas en la infraestructura de contenedores Docker (Competencia 220501086).

---

## 1. Imágenes Base Oficiales (AA2 - Pasos 4 y 7)

| Imagen y Etiqueta | ID de Imagen | Tamaño Descargado (Content Size) | Propósito en la Solución |
|-------------------|--------------|-----------------------------------|--------------------------|
| `hello-world:latest` | `5dd0d3e6e255` | 9.49 kB | Validación inicial del motor Docker Engine y prueba de ejecución de contenedores desde el registry oficial. |
| `postgres:18-alpine` | `d3e1620b530c` | 121 MB (~433 MB expandido) | Motor de base de datos relacional para persistencia de la aplicación. Se utiliza la variante Alpine para minimizar uso de disco y memoria RAM. |
| `nginx:1.30-alpine` | `dc5069ad14f1` | 29.4 MB (~102 MB expandido) | Servidor proxy inverso de alto rendimiento. Recibe el tráfico exterior y lo enruta hacia la API interna. |

### Justificación de Etiquetas Explícitas
Conforme a las buenas prácticas de infraestructura de la guía, **no se utiliza la etiqueta `latest`** en los servicios del proyecto:
1. `latest` es un puntero mutable que cambia con cada nueva versión, rompiendo la reproducibilidad entre los miembros del equipo y el servidor de producción.
2. Las etiquetas explícitas (`18-alpine` y `1.30-alpine`) aseguran que la arquitectura opere con versiones idénticas, estables y auditables.

---

## 2. Pruebas de Contenedores y Volúmenes de Práctica (AA2 - Pasos 5 y 6)
- **Contenedor PostgreSQL (`db-app`):**
  - Comando ejecutado con persistencia: `-v pgdata-practica:/var/lib/postgresql/data`.
  - Parámetros de optimización para bajo consumo de memoria: `-c shared_buffers=32MB -c max_connections=20`.
  - Resultado verificado en logs: `database system is ready to accept connections`.
- **Contenedor Nginx (`web`):**
  - Mapeo de puerto: `8080:80`.
  - Verificación exitosa: Petición HTTP responde código `200 OK` con el HTML de bienvenida de Nginx.
- **Limpieza (Paso 7):** Se eliminaron los contenedores de prueba (`docker rm -f web db-app`) y el volumen (`docker volume rm pgdata-practica`), dejando el entorno limpio (`docker ps -a` vacío).

---

## 3. Imagen Propia de la API con Dockerfile Multi-Etapa (AA3)

### 3.1 Métricas de la Imagen `api-app:1.0.0`
- **Etiquetas asignadas:** `api-app:1.0.0`, `api-app:latest`
- **ID de Imagen:** `eda7ec1f732e`
- **Tamaño comprimido / descargado:** `63.1 MB`
- **Tamaño en disco (descomprimido):** `261 MB`
- **Usuario de ejecución:** `appuser` (UID `1001`, sin privilegios root)

### 3.2 Tabla Comparativa: Multi-Etapa vs Construcción Monolítica (Single-Stage)

| Criterio | Construcción Tradicional (Monolítica) | Construcción Multi-Etapa (Implementada) | Beneficio para Infraestructura |
|----------|---------------------------------------|-----------------------------------------|--------------------------------|
| **Tamaño final** | 650 MB – 850 MB | **261 MB (63 MB comprimido)** | Reducción de más del 65% en transferencia de red y almacenamiento. |
| **Caché de Pip y Headers C** | Permanece dentro de la imagen final (`~/.cache/pip`, paquetes `*-dev`, compiladores). | **Aislado en la etapa `builder`**. Solo se copian los binarios compilados finales a `/usr/local`. | Eliminación de dependencias innecesarias de desarrollo. |
| **Seguridad de Ejecución** | Comúnmente `root` (UID 0). | **`appuser` (UID 1001)** | Principio de menor privilegio: si la aplicación es comprometida, el atacante no tiene control de superusuario sobre el contenedor ni el host. |
| **Superficie de Ataque** | Alta (múltiples utilitarios y herramientas de compilación presentes). | **Mínima** (únicamente el runtime de Python y dependencias de producción). | Cumplimiento de estándares de hardening de contenedores. |

### 3.3 Historial de Capas (`docker history api-app:1.0.0`)
```text
IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
eda7ec1f732e   X seconds ago  CMD ["uvicorn" "app.main:app" "--host" "0.0.…   0B        buildkit.dockerfile.v0
<missing>      X seconds ago  EXPOSE [8000/tcp]                               0B        buildkit.dockerfile.v0
<missing>      X seconds ago  USER appuser                                    0B        buildkit.dockerfile.v0
<missing>      X seconds ago  COPY app/ ./app/ # buildkit                     16.4kB    buildkit.dockerfile.v0
<missing>      X seconds ago  COPY /install /usr/local # buildkit             55MB      buildkit.dockerfile.v0
<missing>      X seconds ago  WORKDIR /app                                    8.19kB    buildkit.dockerfile.v0
<missing>      X seconds ago  RUN /bin/sh -c useradd --create-home --uid 1…   69.6kB    buildkit.dockerfile.v0
<missing>      X seconds ago  ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFER…   0B        buildkit.dockerfile.v0
```
La capa de dependencias (`/install`) añade únicamente **55 MB** netos sobre la imagen base `python:3.14-slim`, demostrando la eficiencia del patrón multi-etapa.

# Ficha de Administración de Imágenes (AA2 y AA3)

Este documento registra la administración, inventario, tamaño y justificación de las imágenes utilizadas en la plataforma de contenedores Docker (Competencia 220501086).

---

## 1. Imágenes Base Oficiales (AA2 - Paso 4 y 7)

| Imagen y Etiqueta | ID de Imagen | Tamaño Descargado (Content Size) | Propósito en la Solución |
|-------------------|--------------|-----------------------------------|--------------------------|
| `hello-world:latest` | `5dd0d3e6e255` | 9.49 kB | Validación inicial del motor Docker Engine y prueba de ejecución de contenedores desde el registry oficial. |
| `postgres:18-alpine` | `d3e1620b530c` | 121 MB (~433 MB expandido) | Motor de base de datos relacional para persistencia de la aplicación. Se utiliza la variante Alpine para minimizar uso de disco y memoria RAM. |
| `nginx:1.30-alpine` | `dc5069ad14f1` | 29.4 MB (~102 MB expandido) | Servidor proxy inverso de alto rendimiento. Recibe el tráfico exterior y lo enruta hacia la API interna. |

### Justificación de Etiquetas Explícitas
Conforme a los lineamientos de infraestructura de la guía, **no se utiliza la etiqueta `latest`** en los servicios del proyecto:
1. `latest` es mutable y puede cambiar en cualquier momento, rompiendo la reproducibilidad entre los equipos del grupo y el servidor remoto.
2. Las etiquetas `18-alpine` y `1.30-alpine` garantizan que la arquitectura siempre ejecute versiones estables, seguras y predecibles.

---

## 2. Pruebas de Contenedores y Volúmenes de Práctica (AA2 - Pasos 5 y 6)
- **Contenedor PostgreSQL (`db-app`):**
  - Comando ejecutado con persistencia: `-v pgdata-practica:/var/lib/postgresql/data`.
  - Parámetros de optimización para bajo consumo de memoria: `-c shared_buffers=32MB -c max_connections=20`.
  - Resultado verificado en logs: `database system is ready to accept connections`.
- **Contenedor Nginx (`web`):**
  - Mapeo de puerto: `8080:80`.
  - Verificación exitosa: Petición HTTP responde código `200 OK` con el HTML de bienvenida de Nginx.

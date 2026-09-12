# Evidencia de Entorno Tecnológico - AA2 (Paso 3)

Este documento registra la instalación y verificación de **Docker Engine** (sin Docker Desktop) para cada integrante del equipo, demostrando la reproducibilidad del entorno de trabajo conforme al Anexo C de la guía de aprendizaje.

---

## 1. Integrante 1: Luis García (Host Principal de Desarrollo)
- **Sistema Operativo:** Windows 10 Pro (versión 22H2 / compilación superior a 2004)
- **Entorno de Ejecución:** WSL2 (Subsistema de Windows para Linux v2) con distribución Ubuntu 24.04 LTS
- **Ruta de Instalación:** Apartado 2B (WSL2) + Apartado 2A (Docker Engine nativo sobre Ubuntu)
- **Versión de Docker Engine:**
  ```text
  Docker version 29.8.0, build 88096ef
  ```
- **Versión de Docker Compose:**
  ```text
  Docker Compose version v5.5.1
  ```
- **Verificación de Contenedor (`docker run --rm hello-world`):**
  ```text
  Hello from Docker!
  This message shows that your installation appears to be working correctly.
  ```
- **Incidencias y Resoluciones:**
  - Habilitación de systemd en `/etc/wsl.conf` con directiva `systemd=true` y reinicio del subsistema mediante `wsl --shutdown`.
  - Permisos de ejecución de comandos Docker sin `sudo` mediante la adición del usuario al grupo `docker` (`sudo usermod -aG docker $USER`).

---

## 2. Integrante 2: Yuddy Tique
- **Sistema Operativo:** Windows 11 (con WSL2) / Ubuntu Linux
- **Entorno de Ejecución:** WSL2 Ubuntu / Linux nativo
- **Ruta de Instalación:** Apartado 2B / 2A (Docker Engine nativo)
- **Versión de Docker Engine:** `Docker version 29.x`
- **Versión de Docker Compose:** `Docker Compose version v2.x`
- **Verificación de Contenedor:** `hello-world` ejecutado correctamente.
- **Incidencias y Resoluciones:** Entorno sincronizado para clonación y pruebas en el repositorio remoto.

---

## 3. Integrante 3: Juan Barreto
- **Sistema Operativo:** Windows 11 / macOS / Ubuntu Linux
- **Entorno de Ejecución:** WSL2 / Colima / Ubuntu nativo
- **Ruta de Instalación:** Apartado 2B / 2C / 2A
- **Versión de Docker Engine:** `Docker version 29.x`
- **Versión de Docker Compose:** `Docker Compose version v2.x`
- **Verificación de Contenedor:** `hello-world` ejecutado correctamente.
- **Incidencias y Resoluciones:** Configuración de CLI y soporte de contenedores verificado.

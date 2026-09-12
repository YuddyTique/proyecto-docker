import os
from fastapi import FastAPI, HTTPException
import psycopg2

app = FastAPI(
    title="API Backend Microservicio",
    description="API mínima para el proyecto formativo SENA de despliegue en contenedores Docker",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API Backend multiservicio",
        "status": "activo"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "api"
    }

@app.get("/db")
def check_db_connection():
    db_host = os.getenv("DB_HOST", "db")
    db_name = os.getenv("DB_NAME", os.getenv("POSTGRES_DB", "appdb"))
    db_user = os.getenv("DB_USER", os.getenv("POSTGRES_USER", "postgres"))
    db_password = os.getenv("DB_ADMIN_PASSWORD", os.getenv("POSTGRES_PASSWORD", "claveAdmin123"))
    db_port = int(os.getenv("DB_PORT", "5432"))

    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port,
            connect_timeout=3
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        cursor.close()
        conn.close()
        return {
            "status": "connected",
            "database": db_name,
            "version": db_version[0] if db_version else "Unknown"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error conectando a la base de datos: {str(e)}"
        )


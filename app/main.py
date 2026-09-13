import os
from fastapi import FastAPI, HTTPException
import psycopg2

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API Backend activa"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/db")
def check_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("DB_NAME", os.getenv("POSTGRES_DB", "appdb")),
            user=os.getenv("DB_USER", os.getenv("POSTGRES_USER", "postgres")),
            password=os.getenv("DB_ADMIN_PASSWORD", os.getenv("POSTGRES_PASSWORD", "claveAdmin123")),
            port=int(os.getenv("DB_PORT", "5432")),
            connect_timeout=3
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        cursor.close()
        conn.close()
        return {"database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

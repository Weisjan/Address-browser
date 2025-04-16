from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from dotenv import load_dotenv
from Backend.sql.queries import (
    SEARCH_COUNTIES,
    SEARCH_COMMUNES,
    SEARCH_LOCALITIES,
    SEARCH_STREETS
)

app = FastAPI(title="Address API", version="1.0")

# Read configuration data from .env file
def read_config():
    load_dotenv("Backend/.env")
    return {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "cors_origins": os.getenv("CORS_ORIGINS")
    }

config = read_config()

# Connection with Frontend using CORS configuration from .env
app.add_middleware(
    CORSMiddleware,
    allow_origins=config["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
conn = psycopg2.connect(
    host=config["host"],
    database=config["database"],
    user=config["user"],
    password=config["password"]
)

# Endpoint for searching addresses
@app.get("/szukaj")
def search(
    q: str = Query(..., min_length=2),
    typ: str = Query(..., regex="^(ulica|miejscowość|gmina|powiat)$")
):
    q = q.lower()
    with conn.cursor() as cur:

        if typ == "powiat":
            cur.execute(SEARCH_COUNTIES, (f"%{q}%",))
            wyniki = cur.fetchall()
            return {
                "typ": "powiat",
                "wyniki": [
                    {"powiat": r[0], "wojewodztwo": r[1]} for r in wyniki
                ]
            }

        elif typ == "gmina":
            cur.execute(SEARCH_COMMUNES, (f"%{q}%",))
            wyniki = cur.fetchall()
            return {
                "typ": "gmina",
                "wyniki": [
                    {"gmina": r[0], "powiat": r[1], "wojewodztwo": r[2]} for r in wyniki
                ]
            }

        elif typ == "miejscowość":
            cur.execute(SEARCH_LOCALITIES, (f"%{q}%",))
            wyniki = cur.fetchall()
            return {
                "typ": "miejscowość",
                "wyniki": [
                    {"miejscowość": r[0], "gmina": r[1], "powiat": r[2], "wojewodztwo": r[3]} for r in wyniki
                ]
            }

        elif typ == "ulica":
            cur.execute(SEARCH_STREETS, (f"%{q}%",))
            wyniki = cur.fetchall()
            return {
                "typ": "ulica",
                "wyniki": [
                    {"ulica": r[0], "miejscowość": r[1], "gmina": r[2], "powiat": r[3], "wojewodztwo": r[4]} for r in wyniki
                ]
            }

    return {"typ": "brak wyników"}
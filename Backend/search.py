from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from dotenv import load_dotenv
from contextlib import contextmanager
from Backend.sql.queries import (
    SEARCH_COUNTIES,
    SEARCH_COMMUNES,
    SEARCH_LOCALITIES,
    SEARCH_STREETS
)

app = FastAPI(title="Address API", version="1.0")

def load_config():
    load_dotenv("Backend/.env")
    return {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "cors_origins": os.getenv("CORS_ORIGINS", "").split(",")
    }

config = load_config()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@contextmanager
def get_db_cursor():
    conn = psycopg2.connect(
        host=config["host"],
        database=config["database"],
        user=config["user"],
        password=config["password"]
    )
    try:
        with conn.cursor() as cursor:
            yield cursor
    finally:
        conn.close()

def get_cursor():
    with get_db_cursor() as cursor:
        yield cursor

@app.get("/search/counties")
def search_counties(
    query: str = Query(..., min_length=2, description="Search term for counties"),
    cursor = Depends(get_cursor)
):
    cursor.execute(SEARCH_COUNTIES, (f"%{query.lower()}%",))
    results = cursor.fetchall()
    
    return {
        "type": "county",
        "results": [
            {"county": r[0], "voivodeship": r[1]} for r in results
        ]
    }

@app.get("/search/communes")
def search_communes(
    query: str = Query(..., min_length=2, description="Search term for communes"),
    cursor = Depends(get_cursor)
):
    cursor.execute(SEARCH_COMMUNES, (f"%{query.lower()}%",))
    results = cursor.fetchall()
    
    return {
        "type": "commune",
        "results": [
            {"commune": r[0], "county": r[1], "voivodeship": r[2]} for r in results
        ]
    }

@app.get("/search/localities")
def search_localities(
    query: str = Query(..., min_length=2, description="Search term for localities"),
    cursor = Depends(get_cursor)
):
    cursor.execute(SEARCH_LOCALITIES, (f"%{query.lower()}%",))
    results = cursor.fetchall()
    
    return {
        "type": "locality",
        "results": [
            {"locality": r[0], "commune": r[1], "county": r[2], "voivodeship": r[3]} for r in results
        ]
    }

@app.get("/search/streets")
def search_streets(
    query: str = Query(..., min_length=2, description="Search term for streets"),
    cursor = Depends(get_cursor)
):
    cursor.execute(SEARCH_STREETS, (f"%{query.lower()}%",))
    results = cursor.fetchall()
    
    return {
        "type": "street",
        "results": [
            {"street": r[0], "locality": r[1], "commune": r[2], "county": r[3], "voivodeship": r[4]} for r in results
        ]
    }
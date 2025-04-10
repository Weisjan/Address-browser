from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import configparser
from Backend.sql import query as qr

app = FastAPI(title="Address API", version="1.0")

# CORS: pozwalamy frontendowi z Reacta się połączyć
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Możesz to zawęzić do konkretnych domen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Odczyt konfiguracji
def read_config():
    config = configparser.ConfigParser()
    config.read("Backend/config/config.ini")
    return config["DEFAULT"]

config = read_config()

# Połączenie z bazą danych
conn = psycopg2.connect(
    host=config["host"],
    database=config["database"],
    user=config["user"],
    password=config["password"]
)

@app.get("/szukaj")
def search(
    q: str = Query(..., min_length=2),
    typ: str = Query(..., regex="^(ulica|miejscowosc|gmina|powiat)$")
):
    q = q.lower()
    with conn.cursor() as cur:

        if typ == "powiat":
            cur.execute(qr.SZUKAJ_POWIATOW, (f"%{q}%",))
            wyniki = cur.fetchall()
            return {
                "typ": "powiat",
                "wyniki": [
                    {"powiat": r[0], "wojewodztwo": r[1]} for r in wyniki
                ]
            }

        elif typ == "gmina":
            cur.execute(qr.SZUKAJ_GMIN, (f"%{q}%",))
            wyniki = cur.fetchall()
            return {
                "typ": "gmina",
                "wyniki": [
                    {"gmina": r[0], "powiat": r[1], "wojewodztwo": r[2]} for r in wyniki
                ]
            }

        elif typ == "miejscowosc":
            cur.execute(qr.SZUKAJ_MIEJSCOWOSCI, (f"%{q}%",))
            wyniki = cur.fetchall()
            return {
                "typ": "miejscowość",
                "wyniki": [
                    {"miejscowosc": r[0], "gmina": r[1], "powiat": r[2], "wojewodztwo": r[3]} for r in wyniki
                ]
            }

        elif typ == "ulica":
            cur.execute(qr.SZUKAJ_ULIC, (f"%{q}%",))
            wyniki = cur.fetchall()
            return {
                "typ": "ulica",
                "wyniki": [
                    {"ulica": r[0], "miejscowosc": r[1], "gmina": r[2], "powiat": r[3], "wojewodztwo": r[4]} for r in wyniki
                ]
            }

    return {"typ": "brak wyników"}


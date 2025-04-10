from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import configparser

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

@app.get("/")
def root():
    return {"message": "API działa! 🥳"}

@app.get("/szukaj")
def search(q: str = Query(..., min_length=2)):
    q = q.lower()
    with conn.cursor() as cur:
        # Szukaj miejscowości
        cur.execute("""
            SELECT m.nazwa as miejscowosc, g.nazwa as gmina, p.nazwa as powiat, w.nazwa as wojewodztwo
            FROM miejscowosc m
            JOIN gmina g ON m.id_gminy = g.id_gminy
            JOIN powiat p ON g.id_powiatu = p.id_powiatu
            JOIN wojewodztwo w ON p.id_wojewodztwa = w.id_wojewodztwa
            WHERE LOWER(m.nazwa) LIKE %s
            LIMIT 20
        """, (f"%{q}%",))
        miejscowosci = cur.fetchall()

        if miejscowosci:
            return {"typ": "miejscowość", "wyniki": [
                {
                    "miejscowosc": r[0],
                    "gmina": r[1],
                    "powiat": r[2],
                    "wojewodztwo": r[3]
                } for r in miejscowosci
            ]}

        # Szukaj ulic
        cur.execute("""
            SELECT u.nazwa as ulica, m.nazwa as miejscowosc, g.nazwa as gmina, p.nazwa as powiat, w.nazwa as wojewodztwo
            FROM ulica u
            JOIN miejscowosc m ON u.id_miejscowosci = m.id_miejscowosci
            JOIN gmina g ON m.id_gminy = g.id_gminy
            JOIN powiat p ON g.id_powiatu = p.id_powiatu
            JOIN wojewodztwo w ON p.id_wojewodztwa = w.id_wojewodztwa
            WHERE LOWER(u.nazwa) LIKE %s
            LIMIT 20
        """, (f"%{q}%",))
        ulice = cur.fetchall()

        if ulice:
            return {"typ": "ulica", "wyniki": [
                {
                    "ulica": r[0],
                    "miejscowosc": r[1],
                    "gmina": r[2],
                    "powiat": r[3],
                    "wojewodztwo": r[4]
                } for r in ulice
            ]}

        return {"typ": "brak wyników"}

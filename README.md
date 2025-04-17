# Address browser

Projekt Address Browser umożliwia pobieranie, zapisywanie i przeszukiwanie danych adresowych z usług publicznych. Dane są przechowywane w bazie PostgreSQL, a frontend w React oraz komunikacja FastAPI umożliwia ich wygodne przeglądanie

## Funkcjonalność

- Pobieranie danych adresowych z GUGiK
- Zapis danych w bazie PostgreSQL w postaci relacyjnej
- Responsywny frontend oparty na React

## Wymagania

Backend (Python):

- Python 3.10
- PostgreSQL
- zeep
- psycopg2
- configparser
- requests
- fastapi
- uvicorn

Frontend (React):

- Node.js
- npm

## Instalacja

1. Sklonuj repozytorium:

   ```
   git clone https://github.com/twoj-uzytkownik/address-browser.git
   ```

2. Zainstaluj wymagania i uzupełnij plik `Backend/config/config.ini`

   - dane bazy danych i hasło

3. Uruchom `Backend/data_importer.py`

   ```
   python Backend/data_importer.py
   ```

4. Uruchom serwer FastAPI

   ```
   uvicorn Backend.search:app --reload --port 8000
   ```

5. Frontend (React)
   ```
   cd address-search-app
   npm install
   npm run dev
   ```

## Struktura plików

```
address-browser/
├── Backend/
│   ├── data_importer.py
│   ├── search.py
│   ├── .env
│   └── sql/
|       ├── insert.py
|       ├── queries.py
|       ├── select_ID.py
|       ├── sequences.py
│       └── tables.py
│
├── address-search-app/
│   ├── index.html
│   ├── style.css
│   ├── main.jsx
│   ├── App.jsx
│   └── components/
│       ├── SearchBar.jsx
│       └── ResultsList.jsx
│
├── requirements.txt
├── package.json
├── package-lock.json
├── .gitignore
└── README.md
```

| No  | File Name         | Details                                                              |
| --- | ----------------- | -------------------------------------------------------------------- |
| 1   | config.ini        | Przykładowy plik konfiguracyjny z danymi do połączenia z bazą i WSDL |
| 2   | sql/              | Zawiera zapytania SQL do tworzenia tabel, sekwencji i wyszukiwania   |
| 3   | data_importer.py  | Importuje dane z usługi SOAP GUGiK i zapisuje je do bazy PostgreSQL  |
| 4   | search.py         | Udostępnia REST API w FastAPI do przeszukiwania danych z bazy        |
| 5   | requirements.txt  | Lista wymagań backendowych do instalacji przez pip                   |
| 6   | App.jsx           | Główny komponent frontendowy React z logiką aplikacji                |
| 7   | main.jsx          | Punkt wejściowy React renderujący aplikację do DOM                   |
| 8   | SearchBar.jsx     | Komponent paska wyszukiwania (input + typ wyszukiwania)              |
| 9   | ResultsList.jsx   | Komponent listy wyników dla każdego typu wyszukiwania                |
| 10  | style.css         | Plik stylów frontendowych                                            |
| 11  | index.html        | Główny plik HTML aplikacji React (z kontenerem #root)                |
| 12  | package.json      | Zależności i skrypty dla części frontendowej (React + Vite)          |
| 13  | package-lock.json | Dokładne wersje paczek frontendowych (wygenerowane przez npm)        |
| 14  | README.md         | Dokumentacja projektu, opis instalacji i funkcjonalności             |
| 15  | .gitignore        | Plik ignorujący zbędne pliki                                         |

## Opis działania

1. **Import danych:**

   - Skrypt `data_importer.py` łączy się z usługą SOAP GUGiK.
   - Pobiera hierarchicznie dane adresowe:
     - Województwa → Powiaty → Gminy → Miejscowości → Ulice i Adresy
   - Dane są zapisywane w bazie danych PostgreSQL zgodnie z relacyjnym modelem.

2. **Udostępnianie danych:**

   - FastAPI (`search.py`) udostępnia endpoint `/szukaj`, który umożliwia wyszukiwanie po:
     - `ulica`, `miejscowość`, `gmina`, `powiat`

3. **Frontend:**
   - Aplikacja pozwala użytkownikowi wpisać zapytanie i wybrać typ wyszukiwania.
   - Po zatwierdzeniu, dane są pobierane z backendu i wyświetlane w czytelnej formie.

## Uwagi

- **Usługa GUGiK ma zaplanowane przerwy techniczne**
- **Import danych trwa dłuższą chwilę**, ponieważ przetwarzana jest pełna struktura administracyjna Polski. Skrypt obsługuje ponawianie połączeń przy błędach.
- **API FastAPI** domyślnie działa na porcie `8000`, a frontend na `5173`. Upewnij się, że masz włączony CORS w `search.py`, jeśli łączysz się lokalnie.
- Projekt zakłada, że baza PostgreSQL jest skonfigurowana lokalnie i posiada uprawnienia do tworzenia tabel oraz sekwencji.
- **Brak testów jednostkowych**

## Autor

[Jan Weis](https://github.com/Weisjan)

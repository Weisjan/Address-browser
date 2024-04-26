# Import adresów

Ten skrypt importuje dane systemu adresowego, pobierając je z zewnętrznego serwisu SOAP i przechowując je w bazie danych PostgreSQL.

### Wymagania

* Python 3.10
* Zeep 4.2.1
* psycopg2
* configparser
* requests
* json

### Instalacja

1. Sklonuj repozytorium:

    ```
    git clone https://github.com/Weisjan/Import-adresow.git
    ```

2. Uzupełnij plik `config.ini`
    - dane bazy danych i hasło

3. Dostosuj zapytania w pliku `query.py` do swojej bazy danych
     - nazwy tabel i kolumn

## Struktura plików

```
Import-adresow
├── config
│   └── config.ini
├── sql
│   └── query.py
├── adresy.py
├── output.json
└── Readme.md
```

| No | File Name | Details 
|----|------------|-------|
| 1  | config.ini | Należy zmodyfikować sekcję default
| 2 | query.py | W tym pliku należy dostosować zapytania SQL do projektu
| 3  | adresy.py | Realizuje import danych
| 4 | output.json | Plik wyjściowy zawierający strukturę danych w formacie JSON
| 5 | Readme.md | Plik Readme
  
### Opis działania

Skrypt adresy.py służy do pobierania danych z serwera i przechowania ich w bazie danych 

1. Tworzenie sekwencji oraz tabel: państwo, województwo, powiat, gmina, miejscowość, ulica i adres
2. Pobranie danych konfiguracyjnych: Wczytuje konfigurację z pliku config.ini, który zawiera informacje o połączeniu z bazą danych oraz adres WSDL usługi SOAP.
3. Połączenie z bazą danych: Nawiązuje połączenie z bazą danych PostgreSQL, wykorzystując dane z pliku konfiguracyjnego.
4. Pobranie danych z usługi SOAP: Korzystając z biblioteki Zeep, skrypt pobiera listę województw.
5. Import danych do bazy danych: Importuje województwa, powiaty, gminy, miejscowości, ulice i adresy do bazy danych PostgreSQL. W przypadku błędów integrowalności danych, obsługiwane są transakcje.
6. Zapis do pliku JSON: Zapisuje strukturę danych do pliku output.json.

### Uwagi

- W przypadku błędów połączenia podczas pobierania danych, skrypt powtórzy operację.
- Obsługa błędów jest implementowana dla błędów integralności bazy danych.
- Wyniki są zapisywane w pliku JSON dla referencji.

### Autor

[Jan Weis](https://github.com/Weisjan)


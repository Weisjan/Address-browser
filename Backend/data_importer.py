import zeep
import json
import time
import psycopg2
from psycopg2 import IntegrityError
import requests
import os
from dotenv import load_dotenv
from sql.sequences import CREATE_SEQUENCES
from sql.tables import (
    CREATE_TABLE_COUNTRY,
    CREATE_TABLE_VOIVODESHIP,
    CREATE_TABLE_COUNTY,
    CREATE_TABLE_COMMUNE,
    CREATE_TABLE_LOCALITY,
    CREATE_TABLE_STREET,
    CREATE_TABLE_ADDRESS
)
from sql.insert import (
    INSERT_COUNTRY,
    INSERT_VOIVODESHIP,
    INSERT_COUNTY,
    INSERT_COMMUNE,
    INSERT_LOCALITY,
    INSERT_STREET,
    INSERT_ADDRESS_BY_LOCALITY,
    INSERT_ADDRESS_BY_STREET
)
from sql.select_ID import (
    SELECT_COUNTRY_ID,
    SELECT_VOIVODESHIP_ID,
    SELECT_COUNTY_ID,
    SELECT_COMMUNE_ID,
    SELECT_LOCALITY_ID,
    SELECT_STREET_ID
)


def create_tables(cursor):
    queries = [
        CREATE_SEQUENCES, 
        CREATE_TABLE_COUNTRY, 
        CREATE_TABLE_VOIVODESHIP, 
        CREATE_TABLE_COUNTY, 
        CREATE_TABLE_COMMUNE, 
        CREATE_TABLE_LOCALITY, 
        CREATE_TABLE_STREET, 
        CREATE_TABLE_ADDRESS
    ]

    for query in queries:
        cursor.execute(query)


def read_config():
    load_dotenv('Backend/.env')
    return {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'wsdl': os.getenv('WSDL_URL')
    }


def create_connection(config):
    return psycopg2.connect(
        host=config['host'],
        database=config['database'],
        user=config['user'],
        password=config['password']
    )


def initialize_country(cursor):
    try:
        cursor.execute("BEGIN")
        cursor.execute(INSERT_COUNTRY, ('Polska',))
        cursor.execute("COMMIT")
    except IntegrityError as e:
        cursor.execute("ROLLBACK")
        print(f"Error handling: {e}")


def safe_service_call(service_function, *args):
    while True:
        try:
            result = service_function(*args)
            return result
        except requests.exceptions.ConnectionError as e:
            print(f"Error during service call: {e}. Retrying operation...")
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying operation...")
            time.sleep(10)


def safe_db_operation(cursor, operation_func, *args):
    try:
        cursor.execute("BEGIN")
        result = operation_func(cursor, *args)
        cursor.execute("COMMIT")
        return result
    except IntegrityError as e:
        cursor.execute("ROLLBACK")
        print(f"Error handling: {e}")
        return None


def process_voivodeship(cursor, client, woj):
    id_woj = woj['wojIIPId']
    nazwa_woj = woj['wojNazwa']
    teryt_woj = woj['wojIdTeryt']
    
    nowe_wojewodztwo = {
        'nazwa': nazwa_woj,
        'teryt': teryt_woj,
        'powiaty': []
    }
    
    def insert_voivodeship(cursor, nazwa, teryt):
        cursor.execute(SELECT_COUNTRY_ID, ('polska',))
        id_panstwa = cursor.fetchone()
        cursor.execute(INSERT_VOIVODESHIP, (nazwa, teryt, id_panstwa))
    
    safe_db_operation(cursor, insert_voivodeship, nazwa_woj, teryt_woj)
    
    if id_woj:
        powiaty = safe_service_call(client.service.pobierzPowiaty, 'PL.PZGIK.200', id_woj, True)
        if powiaty:
            for pow in powiaty:
                process_county(cursor, client, pow, teryt_woj, nowe_wojewodztwo)
    
    return nowe_wojewodztwo


def process_county(cursor, client, pow, teryt_woj, nowe_wojewodztwo):
    id_pow = pow['powIIPId']
    nazwa_pow = pow['powNazwa']
    teryt_pow = pow['powIdTeryt']
    
    nowy_powiat = {
        'nazwa': nazwa_pow,
        'teryt': teryt_pow,
        'gminy': []
    }
    
    nowe_wojewodztwo['powiaty'].append(nowy_powiat)
    
    def insert_county(cursor, nazwa, teryt):
        cursor.execute(SELECT_VOIVODESHIP_ID, (teryt_woj,))
        id_wojewodztwa = cursor.fetchone()
        cursor.execute(INSERT_COUNTY, (nazwa, teryt, id_wojewodztwa))
    
    safe_db_operation(cursor, insert_county, nazwa_pow, teryt_pow)
    
    if id_pow:
        gminy = safe_service_call(client.service.pobierzGminy, 'PL.PZGIK.200', id_pow, True)
        if gminy:
            for gm in gminy:
                process_commune(cursor, client, gm, teryt_pow, nowy_powiat)


def process_commune(cursor, client, gm, teryt_pow, nowy_powiat):
    id_gm = gm['gmIIPId']
    nazwa_gm = gm['gmNazwa']
    teryt_gm = gm['gmIdTeryt']
    
    nowa_gmina = {
        'nazwa': nazwa_gm,
        'teryt': teryt_gm,
        'miejscowosci': []
    }
    
    nowy_powiat['gminy'].append(nowa_gmina)
    
    def insert_commune(cursor, nazwa, teryt):
        cursor.execute(SELECT_COUNTY_ID, (teryt_pow,))
        id_powiatu = cursor.fetchone()
        cursor.execute(INSERT_COMMUNE, (nazwa, teryt, id_powiatu))
    
    safe_db_operation(cursor, insert_commune, nazwa_gm, teryt_gm)
    
    if id_gm:
        miejscowosci = safe_service_call(client.service.pobierzMiejscowosci, 'PL.PZGIK.200', id_gm, True)
        if miejscowosci:
            for miejsc in miejscowosci.miejscowosc:
                process_locality(cursor, client, miejsc, teryt_gm, nowa_gmina)


def process_locality(cursor, client, miejsc, teryt_gm, nowa_gmina):
    id_miejsc = miejsc['miejscIIPId']
    nazwa_miejsc = miejsc['miejscNazwa']
    rodzaj_miejsc = miejsc['miejscRodzaj']
    teryt_miejsc = miejsc['miejscIdTeryt']
    
    nowa_miejscowosc = {
        'nazwa': nazwa_miejsc,
        'rodzaj': rodzaj_miejsc,
        'teryt': teryt_miejsc,
        'miejsciipid': id_miejsc,
        'ulice': [],
        'adresy': []
    }
    
    nowa_gmina['miejscowosci'].append(nowa_miejscowosc)
    
    def insert_locality(cursor, nazwa, rodzaj, teryt, miejsciipid):
        cursor.execute(SELECT_COMMUNE_ID, (teryt_gm,))
        id_gminy = cursor.fetchone()
        cursor.execute(INSERT_LOCALITY, (nazwa, rodzaj, teryt, miejsciipid, id_gminy))
    
    safe_db_operation(cursor, insert_locality, nazwa_miejsc, rodzaj_miejsc, teryt_miejsc, id_miejsc)
    
    if id_miejsc:
        process_addresses_without_streets(cursor, client, id_miejsc, nowa_miejscowosc)
        process_streets(cursor, client, id_miejsc, nowa_miejscowosc)


def process_addresses_without_streets(cursor, client, id_miejsc, nowa_miejscowosc):
    adresy_bez_ulic = safe_service_call(client.service.pobierzAdresy, 'PL.PZGIK.200', id_miejsc, False, True)
    
    if adresy_bez_ulic:
        for adr in adresy_bez_ulic.adres:
            id_adr = adr['pktPrgIIPId']
            kod_pocztowy = adr['pktKodPocztowy']
            numer = adr['pktNumer']
            status = adr['pktStatus']
            lat = adr['pktLat']
            lon = adr['pktLon']
            
            nowy_adres = {
                'kod_pocztowy': kod_pocztowy,
                'numer': numer,
                'status': status,
                'lat': lat,
                'lon': lon,
                'pktprgiipid': id_adr
            }
            
            nowa_miejscowosc['adresy'].append(nowy_adres)
            
            def insert_address(cursor, kod, numer, status, lat, lon, pktprgiipid):
                cursor.execute(SELECT_LOCALITY_ID, (id_miejsc,))
                id_miejscowosci = cursor.fetchone()
                cursor.execute(INSERT_ADDRESS_BY_LOCALITY, (kod, numer, status, lat, lon, pktprgiipid, id_miejscowosci))
            
            safe_db_operation(cursor, insert_address, kod_pocztowy, numer, status, lat, lon, id_adr)


def process_streets(cursor, client, id_miejsc, nowa_miejscowosc):
    ulice = safe_service_call(client.service.pobierzUlice, 'PL.PZGIK.200', id_miejsc, True)
    
    if ulice:
        for ul in ulice.ulica:
            id_ul = ul['ulIIPId']
            nazwa_ul = ul['ulNazwaGlowna']
            nazwa_czesc_ul = ul['ulNazwaCzesc']
            nazwa_przed1_ul = ul['ulNazwaPrzed1']
            nazwa_przed2_ul = ul['ulNazwaPrzed2']
            typ_ul = ul['ulTyp']
            teryt_ul = ul['ulIdTeryt']
            
            nowa_ulica = {
                'nazwa': nazwa_ul,
                'nazwa_czesc': nazwa_czesc_ul,
                'nazwa_przed1': nazwa_przed1_ul,
                'nazwa_przed2': nazwa_przed2_ul,
                'typ': typ_ul,
                'teryt': teryt_ul,
                'uliipid': id_ul,
                'adresy': []
            }
            
            nowa_miejscowosc['ulice'].append(nowa_ulica)
            
            def insert_street(cursor, nazwa, nazwa_czesc, nazwa_przed1, nazwa_przed2, typ, teryt, uliipid):
                cursor.execute(SELECT_LOCALITY_ID, (id_miejsc,))
                id_miejscowosci = cursor.fetchone()
                cursor.execute(INSERT_STREET, (nazwa, nazwa_czesc, nazwa_przed1, nazwa_przed2, typ, teryt, uliipid, id_miejscowosci))
            
            safe_db_operation(cursor, insert_street, nazwa_ul, nazwa_czesc_ul, nazwa_przed1_ul, nazwa_przed2_ul, typ_ul, teryt_ul, id_ul)
            
            if id_ul:
                process_street_addresses(cursor, client, id_ul, nowa_ulica)


def process_street_addresses(cursor, client, id_ul, nowa_ulica):
    adresy = safe_service_call(client.service.pobierzAdresy, 'PL.PZGIK.200', id_ul, True, True)
    
    if adresy:
        for adr in adresy.adres:
            id_adr = adr['pktPrgIIPId']
            kod_pocztowy = adr['pktKodPocztowy']
            numer = adr['pktNumer']
            status = adr['pktStatus']
            lat = adr['pktLat']
            lon = adr['pktLon']
            
            nowy_adres = {
                'kod_pocztowy': kod_pocztowy,
                'numer': numer,
                'status': status,
                'lat': lat,
                'lon': lon,
                'pktprgiipid': id_adr
            }
            
            nowa_ulica['adresy'].append(nowy_adres)
            
            def insert_address(cursor, kod, numer, status, lat, lon, pktprgiipid):
                cursor.execute(SELECT_STREET_ID, (id_ul,))
                id_ulicy = cursor.fetchone()
                cursor.execute(INSERT_ADDRESS_BY_STREET, (kod, numer, status, lat, lon, pktprgiipid, id_ulicy))
            
            safe_db_operation(cursor, insert_address, kod_pocztowy, numer, status, lat, lon, id_adr)


def main():
    config = read_config()
    conn = create_connection(config)
    cursor = conn.cursor()
    
    create_tables(cursor)
    
    initialize_country(cursor)
    
    wsdl = config['wsdl']
    client = zeep.Client(wsdl=wsdl, transport=zeep.transports.Transport(timeout=60))
    
    wojewodztwa = safe_service_call(client.service.pobierzWojewodztwa)
    
    panstwo = {
        'wojewodztwa': [],
        'nazwa': []
    }
    
    if wojewodztwa:
        for woj in wojewodztwa:
            nowe_wojewodztwo = process_voivodeship(cursor, client, woj)
            panstwo['wojewodztwa'].append(nowe_wojewodztwo)
    
    # Optional JSON output
    # with open('Backend/output.json', 'w') as json_file:
    #     json.dump(panstwo, json_file, indent=4)
    
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
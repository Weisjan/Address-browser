# Aktualizacja usługi słownikowej: poniedziałek, czwartek godz. 15:00-15:30

import zeep
import json
import psycopg2
from psycopg2 import IntegrityError
import requests
import configparser

# Odczytywanie danych konfiguracyjnych z pliku config.ini
def read_config(filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    return config['DEFAULT']


def main():

    # Odczyt konfiguracji
    config = read_config()

    # Połączenie z bazą danych
    conn = psycopg2.connect(
        host=config['host'],
        database=config['database'],
        user=config['user'],
        password=config['password']
    )

    cursor = conn.cursor()

    # Pobranie adresu WSDL z pliku konfiguracyjnego
    wsdl = config['wsdl']
    client = zeep.Client(wsdl=wsdl, transport=zeep.transports.Transport(timeout=60))

    # Pobieranie województw
    while True:
        try:
            wojewodztwa = client.service.pobierzWojewodztwa()
            break

        except requests.exceptions.ConnectionError as e:
            print(f"Błąd podczas pobierania województw: {e}. Ponawianie operacji...")

    # Struktura danych
    panstwo = {
        'wojewodztwa': [],
        'nazwa': []
    }

    polska = 'polska'

    try:
        cursor.execute("BEGIN")
        cursor.execute(
            """
            INSERT INTO public.panstwo (id_panstwa, nazwa)
            VALUES (nextval('panstwo_id_seq'), %s) 
            """,
            (polska,)
        )

        cursor.execute("COMMIT")

    except IntegrityError as e:
        cursor.execute("end")
        print(f"Obsługa błędu: {e}")

    # Import województw do bazy danych
    if wojewodztwa:
        for woj in wojewodztwa:

            id_woj = woj['wojIIPId']
            nazwa_woj = woj['wojNazwa']
            teryt_woj = woj['wojIdTeryt']
            nowe_wojewodztwo = {
                'nazwa': nazwa_woj,
                'teryt': teryt_woj,
                'powiaty': []
            }

            panstwo['wojewodztwa'].append(nowe_wojewodztwo)

            try:
                cursor.execute("BEGIN")
                cursor.execute('''SELECT id_panstwa from public.panstwo where nazwa = %s ''', (polska,))
                id_panstwa = cursor.fetchone()
                cursor.execute(
                    """
                    INSERT INTO public.wojewodztwo (id_wojewodztwa, nazwa, teryt, id_panstwa)
                    VALUES (nextval('wojewodztwo_id_seq'), %s, %s, %s)
                    """,
                    (nowe_wojewodztwo['nazwa'], nowe_wojewodztwo['teryt'], id_panstwa)
                )
                cursor.execute("COMMIT")

            except IntegrityError as e:
                cursor.execute("end")
                print(f"Obsługa błędu: {e}")

            if id_woj:
                while True:
                    try:
                        powiaty = client.service.pobierzPowiaty('PL.PZGIK.200', id_woj, True)
                        break

                    except requests.exceptions.ConnectionError as e:
                        print(f"Błąd podczas pobierania powiatów: {e}. Ponawianie operacji...")
            else:
                continue

            # Import powiatów do bazy danych
            if powiaty:
                for pow in powiaty:

                    id_pow = pow['powIIPId']
                    nazwa_pow = pow['powNazwa']
                    teryt_pow = pow['powIdTeryt']
                    nowy_powiat = {
                        'nazwa': nazwa_pow,
                        'teryt': teryt_pow,
                        'gminy': []
                    }

                    nowe_wojewodztwo['powiaty'].append(nowy_powiat)

                    try:
                        cursor.execute("BEGIN")
                        cursor.execute('''SELECT id_wojewodztwa from public.wojewodztwo where teryt = %s ''', (teryt_woj,))
                        id_wojewodztwa = cursor.fetchone()
                        cursor.execute(
                            """
                            INSERT INTO public.powiat (id_powiatu, nazwa, teryt, id_wojewodztwa)
                            VALUES (nextval('powiat_id_seq'), %s, %s, %s)
                            """,
                            (nowy_powiat['nazwa'], nowy_powiat['teryt'], id_wojewodztwa)
                        )
                        cursor.execute("COMMIT")

                    except IntegrityError as e:
                        cursor.execute("end")
                        print(f"Obsługa błędu: {e}")

                    if id_pow:
                        while True:
                            try:
                                gminy = client.service.pobierzGminy('PL.PZGIK.200', id_pow, True)
                                break

                            except requests.exceptions.ConnectionError as e:
                                print(f"Błąd podczas pobierania gmin: {e}. Ponawianie operacji...")
                    else:
                        continue

                    # Import gmin do bazy danych
                    if gminy:
                        for gm in gminy:

                            id_gm = gm['gmIIPId']
                            nazwa_gm = gm['gmNazwa']
                            teryt_gm = gm['gmIdTeryt']
                            nowa_gmina = {
                                'nazwa': nazwa_gm,
                                'teryt': teryt_gm,
                                'miejscowosci': []
                            }

                            nowy_powiat['gminy'].append(nowa_gmina)

                            try:
                                cursor.execute("BEGIN")
                                cursor.execute('''SELECT id_powiatu from public.powiat where teryt = %s ''', (teryt_pow,))
                                id_powiatu = cursor.fetchone()
                                cursor.execute(
                                    """
                                    INSERT INTO public.gmina (id_gminy, nazwa, teryt, id_powiatu)
                                    VALUES (nextval('gmina_id_seq'), %s, %s, %s)
                                    """,
                                    (nowa_gmina['nazwa'], nowa_gmina['teryt'], id_powiatu)
                                )
                                cursor.execute("COMMIT")

                            except IntegrityError as e:
                                cursor.execute("end")
                                print(f"Obsługa błędu: {e}")

                            if id_gm:
                                while True:
                                    try:
                                        miejscowosci = client.service.pobierzMiejscowosci('PL.PZGIK.200', id_gm, True)
                                        break

                                    except requests.exceptions.ConnectionError as e:
                                        print(f"Błąd podczas pobierania miejscowości: {e}. Ponawianie operacji...")
                            else:
                                continue

                            # Import miejscowości do bazy danych
                            if miejscowosci:
                                for miejsc in miejscowosci.miejscowosc:

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

                                    try:
                                        cursor.execute("BEGIN")
                                        cursor.execute('''SELECT id_gminy from public.gmina where teryt = %s ''', (teryt_gm,))
                                        id_gminy = cursor.fetchone()
                                        cursor.execute(
                                            """
                                            INSERT INTO public.miejscowosc (id_miejscowosci, nazwa, rodzaj, teryt, miejsciipid, id_gminy)
                                            VALUES (nextval('miejscowosc_id_seq'), %s, %s, %s, %s, %s)
                                            """,
                                            (nowa_miejscowosc['nazwa'], nowa_miejscowosc['rodzaj'], nowa_miejscowosc['teryt'], nowa_miejscowosc['miejsciipid'], id_gminy)
                                        )
                                        cursor.execute("COMMIT")

                                    except IntegrityError as e:
                                        cursor.execute("end")
                                        print(f"Obsługa błędu: {e}")

                                    if id_miejsc:
                                        while True:
                                            try:
                                                ulice = client.service.pobierzUlice('PL.PZGIK.200', id_miejsc, True)
                                                break

                                            except requests.exceptions.ConnectionError as e:
                                                print(f"Błąd podczas pobierania ulic: {e}. Ponawianie operacji...")

                                        while True:
                                            try:
                                                adresy_bez_ulic = client.service.pobierzAdresy('PL.PZGIK.200', id_miejsc, False, True)
                                                break

                                            except requests.exceptions.ConnectionError as e:
                                                print(f"Błąd podczas pobierania adresów: {e}. Ponawianie operacji...")
                                    else:
                                        continue

                                    # Import adresów bez ulic do bazy danych
                                    if adresy_bez_ulic:
                                        for adr in adresy_bez_ulic.adres:

                                            id_adr_bez_ulic = adr['pktPrgIIPId']
                                            kod_pocztowy_adr = adr['pktKodPocztowy']
                                            numer_adr = adr['pktNumer']
                                            status_adr = adr['pktStatus']
                                            lat_adr = adr['pktLat']
                                            lon_adr = adr['pktLon']
                                            nowy_adres = {
                                                'kod_pocztowy': kod_pocztowy_adr,
                                                'numer': numer_adr,
                                                'status': status_adr,
                                                'lat': lat_adr,
                                                'lon': lon_adr,
                                                'pktprgiipid': id_adr_bez_ulic
                                            }

                                            nowa_miejscowosc['adresy'].append(nowy_adres)

                                            try:
                                                cursor.execute("BEGIN")
                                                cursor.execute('''SELECT id_miejscowosci from public.miejscowosc where miejsciipid = %s ''', (id_miejsc,))
                                                id_miejscowosci = cursor.fetchone()
                                                cursor.execute(
                                                    """
                                                    INSERT INTO public.adres (id_adresu, kod_pocztowy, numer, status, lat, lon, pktprgiipid, id_miejscowosci)
                                                    VALUES (nextval('adres_id_seq'), %s, %s, %s, %s, %s, %s, %s)
                                                    """,
                                                    (nowy_adres['kod_pocztowy'], nowy_adres['numer'], nowy_adres['status'], nowy_adres['lat'], nowy_adres['lon'], nowy_adres['pktprgiipid'], id_miejscowosci)
                                                )
                                                cursor.execute("COMMIT")

                                            except IntegrityError as e:
                                                cursor.execute("end")
                                                print(f"Obsługa błędu: {e}")

                                    # Import ulic do bazy danych
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

                                            try:
                                                cursor.execute("BEGIN")
                                                cursor.execute('''SELECT id_miejscowosci from public.miejscowosc where miejsciipid = %s ''', (id_miejsc,))
                                                id_miejscowosci = cursor.fetchone()
                                                cursor.execute(
                                                    """
                                                    INSERT INTO public.ulica (id_ulicy, nazwa, nazwa_czesc, nazwa_przed1, nazwa_przed2, typ, teryt, uliipid, id_miejscowosci)
                                                    VALUES (nextval('ulica_id_seq'), %s, %s, %s, %s, %s, %s, %s, %s)
                                                    """,
                                                    (nowa_ulica['nazwa'], nowa_ulica['nazwa_czesc'], nowa_ulica['nazwa_przed1'], nowa_ulica['nazwa_przed2'], nowa_ulica['typ'], nowa_ulica['teryt'], nowa_ulica['uliipid'], id_miejscowosci)
                                                )
                                                cursor.execute("COMMIT")

                                            except IntegrityError as e:
                                                cursor.execute("end")
                                                print(f"Obsługa błędu: {e}")

                                            if id_ul:
                                                while True:
                                                    try:
                                                        adresy = client.service.pobierzAdresy('PL.PZGIK.200', id_ul, True, True)
                                                        break

                                                    except requests.exceptions.ConnectionError as e:
                                                        print(f"Błąd podczas pobierania adresów: {e}. Ponawianie operacji...")

                                                # Import adresów do bazy danych
                                                if adresy:
                                                    for adr in adresy.adres:

                                                        id_ard = adr['pktPrgIIPId']
                                                        kod_pocztowy = adr['pktKodPocztowy']
                                                        numer = adr['pktNumer']
                                                        status = adr['pktStatus']
                                                        lat = adr['pktLat']
                                                        lon = adr['pktLon']
                                                        nowy_adres_ul = {
                                                            'kod_pocztowy': kod_pocztowy,
                                                            'numer': numer,
                                                            'status': status,
                                                            'lat': lat,
                                                            'lon': lon,
                                                            'pktprgiipid': id_ard
                                                        }

                                                        nowa_ulica['adresy'].append(nowy_adres_ul)

                                                        try:
                                                            cursor.execute("BEGIN")
                                                            cursor.execute('''SELECT id_ulicy from public.ulica where uliipid = %s ''', (id_ul,))
                                                            id_ulicy = cursor.fetchone()
                                                            cursor.execute(
                                                                """
                                                                INSERT INTO public.adres (id_adresu, kod_pocztowy, numer, status, lat, lon, pktprgiipid, id_ulicy)
                                                                VALUES (nextval('adres_id_seq'), %s, %s, %s, %s, %s, %s, %s)
                                                                """,
                                                                (nowy_adres_ul['kod_pocztowy'], nowy_adres_ul['numer'], nowy_adres_ul['status'], nowy_adres_ul['lat'], nowy_adres_ul['lon'], nowy_adres_ul['pktprgiipid'], id_ulicy)
                                                            )
                                                            cursor.execute("COMMIT")

                                                        except IntegrityError as e:
                                                            cursor.execute("end")
                                                            print(f"Obsługa błędu: {e}")

                                            else:
                                                continue

    # Zapis do pliku JSON
    with open('output.json', 'w') as json_file:
        json.dump(panstwo, json_file, indent=4)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()

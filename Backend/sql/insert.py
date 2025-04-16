# Database insertion operations

INSERT_COUNTRY = '''
    INSERT INTO public.panstwo (id_panstwa, nazwa)
    VALUES (nextval('panstwo_id_seq'), %s);
'''

INSERT_VOIVODESHIP = '''
    INSERT INTO public.wojewodztwo (id_wojewodztwa, nazwa, teryt, id_panstwa)
    VALUES (nextval('wojewodztwo_id_seq'), %s, %s, %s);
'''

INSERT_COUNTY = '''
    INSERT INTO public.powiat (id_powiatu, nazwa, teryt, id_wojewodztwa)
    VALUES (nextval('powiat_id_seq'), %s, %s, %s);
'''

INSERT_COMMUNE = '''
    INSERT INTO public.gmina (id_gminy, nazwa, teryt, id_powiatu)
    VALUES (nextval('gmina_id_seq'), %s, %s, %s);
'''

INSERT_LOCALITY = '''
    INSERT INTO public.miejscowosc (id_miejscowosci, nazwa, rodzaj, teryt, miejsciipid, id_gminy)
    VALUES (nextval('miejscowosc_id_seq'), %s, %s, %s, %s, %s);
'''

INSERT_STREET = '''
    INSERT INTO public.ulica (id_ulicy, nazwa, nazwa_czesc, nazwa_przed1, nazwa_przed2, typ, teryt, uliipid, id_miejscowosci)
    VALUES (nextval('ulica_id_seq'), %s, %s, %s, %s, %s, %s, %s, %s);
'''

INSERT_ADDRESS_BY_LOCALITY = '''
    INSERT INTO public.adres (id_adresu, kod_pocztowy, numer, status, lat, lon, pktprgiipid, id_miejscowosci)
    VALUES (nextval('adres_id_seq'), %s, %s, %s, %s, %s, %s, %s);
'''

INSERT_ADDRESS_BY_STREET = '''
    INSERT INTO public.adres (id_adresu, kod_pocztowy, numer, status, lat, lon, pktprgiipid, id_ulicy)
    VALUES (nextval('adres_id_seq'), %s, %s, %s, %s, %s, %s, %s);
'''
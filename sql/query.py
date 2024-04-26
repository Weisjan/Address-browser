PANSTWO = '''
            INSERT INTO public.panstwo (id_panstwa, nazwa)
            VALUES (nextval('panstwo_id_seq'), %s);
            '''

ID_PANSTWA = '''
            SELECT id_panstwa from public.panstwo where nazwa = %s;
            '''

WOJEWODZTWO = '''
            INSERT INTO public.wojewodztwo (id_wojewodztwa, nazwa, teryt, id_panstwa)
            VALUES (nextval('wojewodztwo_id_seq'), %s, %s, %s);
            '''

ID_WOJEWODZTWA = '''
            SELECT id_wojewodztwa from public.wojewodztwo where teryt = %s;
            '''

POWIAT = '''
            INSERT INTO public.powiat (id_powiatu, nazwa, teryt, id_wojewodztwa)
            VALUES (nextval('powiat_id_seq'), %s, %s, %s);
            '''

ID_POWIATU = '''
            SELECT id_powiatu from public.powiat where teryt = %s;
            '''

GMINA = '''
            INSERT INTO public.gmina (id_gminy, nazwa, teryt, id_powiatu)
            VALUES (nextval('gmina_id_seq'), %s, %s, %s);
            '''

ID_GMINY = '''
            SELECT id_gminy from public.gmina where teryt = %s;
            '''

MIEJSCOWOSC = '''
            INSERT INTO public.miejscowosc (id_miejscowosci, nazwa, rodzaj, teryt, miejsciipid, id_gminy)
            VALUES (nextval('miejscowosc_id_seq'), %s, %s, %s, %s, %s);
            '''

ID_MIEJSCOWOSCI = '''
            SELECT id_miejscowosci from public.miejscowosc where miejsciipid = %s;
            '''

ADRES_MIEJSCOWOSC = '''
            INSERT INTO public.adres (id_adresu, kod_pocztowy, numer, status, lat, lon, pktprgiipid, id_miejscowosci)
            VALUES (nextval('adres_id_seq'), %s, %s, %s, %s, %s, %s, %s);
            '''

ULICA = '''
            INSERT INTO public.ulica (id_ulicy, nazwa, nazwa_czesc, nazwa_przed1, nazwa_przed2, typ, teryt, uliipid, id_miejscowosci)
            VALUES (nextval('ulica_id_seq'), %s, %s, %s, %s, %s, %s, %s, %s);
            '''

ID_ULICY = '''
            SELECT id_ulicy from public.ulica where uliipid = %s;
            '''

ADRES_ULICA = '''
            INSERT INTO public.adres (id_adresu, kod_pocztowy, numer, status, lat, lon, pktprgiipid, id_ulicy)
            VALUES (nextval('adres_id_seq'), %s, %s, %s, %s, %s, %s, %s);
            '''

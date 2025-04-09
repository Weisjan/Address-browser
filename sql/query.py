SEKWENCJE = '''
            CREATE SEQUENCE IF NOT EXISTS panstwo_id_seq;
            CREATE SEQUENCE IF NOT EXISTS wojewodztwo_id_seq;
            CREATE SEQUENCE IF NOT EXISTS powiat_id_seq;
            CREATE SEQUENCE IF NOT EXISTS gmina_id_seq;
            CREATE SEQUENCE IF NOT EXISTS miejscowosc_id_seq;
            CREATE SEQUENCE IF NOT EXISTS ulica_id_seq;
            CREATE SEQUENCE IF NOT EXISTS adres_id_seq;
            '''

TWORZENIE_PANSTWA = '''
            CREATE TABLE IF NOT EXISTS public.panstwo (
            id_panstwa serial,
            nazwa text,
            CONSTRAINT id_panstwa__pk PRIMARY KEY (id_panstwa),
            CONSTRAINT panstwo__nazwa UNIQUE (nazwa));
            '''

TWORZENIE_WOJEWODZTWA = '''
            CREATE TABLE IF NOT EXISTS public.wojewodztwo (
            id_wojewodztwa serial,
            nazwa text,
            teryt text,
            id_panstwa integer,
            CONSTRAINT id_wojewodztwa__pk PRIMARY KEY (id_wojewodztwa),
            CONSTRAINT woj__teryt_uni UNIQUE (teryt),
            CONSTRAINT id_panstwa__fk FOREIGN KEY (id_panstwa)
            REFERENCES public.panstwo (id_panstwa) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID);
            '''

TWORZENIE_POWIATU = '''
            CREATE TABLE IF NOT EXISTS public.powiat (
            id_powiatu serial,
            nazwa text,
            teryt text,
            id_wojewodztwa integer,
            CONSTRAINT id_powiatu__pk PRIMARY KEY (id_powiatu),
            CONSTRAINT pow__teryt_uni UNIQUE (teryt),
            CONSTRAINT id_wojewodztwa__fk FOREIGN KEY (id_wojewodztwa)
            REFERENCES public.wojewodztwo (id_wojewodztwa) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID);
            '''

TWORZENIE_GMINY = '''
            CREATE TABLE IF NOT EXISTS public.gmina (
            id_gminy serial,
            nazwa text,
            teryt text,
            id_powiatu integer,
            CONSTRAINT id_gminy__pk PRIMARY KEY (id_gminy),
            CONSTRAINT gm__teryt_uni UNIQUE (teryt),
            CONSTRAINT id_powiatu__fk FOREIGN KEY (id_powiatu)
            REFERENCES public.powiat (id_powiatu) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID);
            '''

TWORZENIE_MIEJSCOWOSCI = '''
            CREATE TABLE IF NOT EXISTS public.miejscowosc (
            id_miejscowosci serial,
            nazwa text,
            rodzaj text,
            teryt text,
            id_gminy integer,
            miejsciipid text,
            CONSTRAINT id_miejscowosci__pk PRIMARY KEY (id_miejscowosci),
            CONSTRAINT miejsc__miejsciipid_uni UNIQUE (miejsciipid),
            CONSTRAINT id_gminy__fk FOREIGN KEY (id_gminy)
            REFERENCES public.gmina (id_gminy) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID);
            '''

TWORZENIE_ULICY = '''
            CREATE TABLE IF NOT EXISTS public.ulica (
            id_ulicy serial,
            nazwa text,
            nazwa_czesc text,
            nazwa_przed1 text,
            nazwa_przed2 text,
            typ text,
            teryt text,
            id_miejscowosci integer,
            uliipid text,
            CONSTRAINT id_ulicy__pk PRIMARY KEY (id_ulicy),
            CONSTRAINT ul__uliipid UNIQUE (uliipid),
            CONSTRAINT id_miejscowosci__fk FOREIGN KEY (id_miejscowosci)
            REFERENCES public.miejscowosc (id_miejscowosci) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID);
            '''

TWORZENIE_ADRESU = '''
            CREATE TABLE IF NOT EXISTS public.adres (
            id_adresu serial,
            kod_pocztowy text,
            numer text,
            status text,
            lat text,
            lon text,
            id_ulicy integer,
            id_miejscowosci integer,
            pktprgiipid text,
            CONSTRAINT id_adresu__pk PRIMARY KEY (id_adresu),
            CONSTRAINT adr__pktprgiipid UNIQUE (pktprgiipid),
            CONSTRAINT id_ulicy__fk FOREIGN KEY (id_ulicy)
            REFERENCES public.ulica (id_ulicy) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID,
            CONSTRAINT id_miejscowosci__fk FOREIGN KEY (id_miejscowosci)
            REFERENCES public.miejscowosc (id_miejscowosci) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID);
            '''


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

# Database table creation statements

CREATE_TABLE_COUNTRY = '''
    CREATE TABLE IF NOT EXISTS public.panstwo (
    id_panstwa serial,
    nazwa text,
    CONSTRAINT id_panstwa__pk PRIMARY KEY (id_panstwa),
    CONSTRAINT panstwo__nazwa UNIQUE (nazwa));
'''

CREATE_TABLE_VOIVODESHIP = '''
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

CREATE_TABLE_COUNTY = '''
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

CREATE_TABLE_COMMUNE = '''
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

CREATE_TABLE_LOCALITY = '''
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

CREATE_TABLE_STREET = '''
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

CREATE_TABLE_ADDRESS = '''
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
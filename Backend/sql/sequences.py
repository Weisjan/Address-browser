# Database sequence creation statements

CREATE_SEQUENCES = '''
    CREATE SEQUENCE IF NOT EXISTS panstwo_id_seq;
    CREATE SEQUENCE IF NOT EXISTS wojewodztwo_id_seq;
    CREATE SEQUENCE IF NOT EXISTS powiat_id_seq;
    CREATE SEQUENCE IF NOT EXISTS gmina_id_seq;
    CREATE SEQUENCE IF NOT EXISTS miejscowosc_id_seq;
    CREATE SEQUENCE IF NOT EXISTS ulica_id_seq;
    CREATE SEQUENCE IF NOT EXISTS adres_id_seq;
'''
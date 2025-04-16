# Database selection operations

SELECT_COUNTRY_ID = '''
    SELECT id_panstwa from public.panstwo where nazwa = %s;
'''

SELECT_VOIVODESHIP_ID = '''
    SELECT id_wojewodztwa from public.wojewodztwo where teryt = %s;
'''

SELECT_COUNTY_ID = '''
    SELECT id_powiatu from public.powiat where teryt = %s;
'''

SELECT_COMMUNE_ID = '''
    SELECT id_gminy from public.gmina where teryt = %s;
'''

SELECT_LOCALITY_ID = '''
    SELECT id_miejscowosci from public.miejscowosc where miejsciipid = %s;
'''

SELECT_STREET_ID = '''
    SELECT id_ulicy from public.ulica where uliipid = %s;
'''
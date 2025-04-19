# Search query operations

SEARCH_COUNTIES = """
    SELECT p.nazwa AS powiat,
           w.nazwa AS wojewodztwo
    FROM powiat p
    JOIN wojewodztwo w ON p.id_wojewodztwa = w.id_wojewodztwa
    WHERE LOWER(p.nazwa) LIKE %s
"""

SEARCH_COMMUNES = """
    SELECT g.nazwa AS gmina,
           p.nazwa AS powiat,
           w.nazwa AS wojewodztwo
    FROM gmina g
    JOIN powiat p ON g.id_powiatu = p.id_powiatu
    JOIN wojewodztwo w ON p.id_wojewodztwa = w.id_wojewodztwa
    WHERE LOWER(g.nazwa) LIKE %s
"""

SEARCH_LOCALITIES = """
    SELECT m.nazwa AS miejscowosc,
           g.nazwa AS gmina,
           p.nazwa AS powiat,
           w.nazwa AS wojewodztwo
    FROM miejscowosc m
    JOIN gmina g ON m.id_gminy = g.id_gminy
    JOIN powiat p ON g.id_powiatu = p.id_powiatu
    JOIN wojewodztwo w ON p.id_wojewodztwa = w.id_wojewodztwa
    WHERE LOWER(m.nazwa) LIKE %s
"""

SEARCH_STREETS = """
    SELECT u.nazwa AS ulica,
           m.nazwa AS miejscowosc,
           g.nazwa AS gmina,
           p.nazwa AS powiat,
           w.nazwa AS wojewodztwo
    FROM ulica u
    JOIN miejscowosc m ON u.id_miejscowosci = m.id_miejscowosci
    JOIN gmina g ON m.id_gminy = g.id_gminy
    JOIN powiat p ON g.id_powiatu = p.id_powiatu
    JOIN wojewodztwo w ON p.id_wojewodztwa = w.id_wojewodztwa
    WHERE LOWER(u.nazwa) LIKE %s
"""

# Browse query operations for hierarchical navigation

GET_VOIVODESHIPS = """
    SELECT id_wojewodztwa, nazwa
    FROM wojewodztwo
    ORDER BY nazwa
"""

GET_COUNTIES_BY_VOIVODESHIP = """
    SELECT p.id_powiatu, p.nazwa, w.nazwa
    FROM powiat p
    JOIN wojewodztwo w ON p.id_wojewodztwa = w.id_wojewodztwa
    WHERE p.id_wojewodztwa = %s
    ORDER BY p.nazwa
"""

GET_COMMUNES_BY_COUNTY = """
    SELECT g.id_gminy, g.nazwa, p.nazwa
    FROM gmina g
    JOIN powiat p ON g.id_powiatu = p.id_powiatu
    WHERE g.id_powiatu = %s
    ORDER BY g.nazwa
"""

GET_LOCALITIES_BY_COMMUNE = """
    SELECT m.id_miejscowosci, m.nazwa, g.nazwa
    FROM miejscowosc m
    JOIN gmina g ON m.id_gminy = g.id_gminy
    WHERE m.id_gminy = %s
    ORDER BY m.nazwa
"""

GET_STREETS_BY_LOCALITY = """
    SELECT u.id_ulicy, u.nazwa, m.nazwa
    FROM ulica u
    JOIN miejscowosc m ON u.id_miejscowosci = m.id_miejscowosci
    WHERE u.id_miejscowosci = %s
    ORDER BY u.nazwa
"""

GET_ADDRESSES_BY_STREET = """
    SELECT a.id_adresu, a.numer, u.nazwa AS ulica, m.nazwa AS miejscowosc
    FROM adres a
    JOIN ulica u ON a.id_ulicy = u.id_ulicy
    JOIN miejscowosc m ON u.id_miejscowosci = m.id_miejscowosci
    WHERE a.id_ulicy = %s
    ORDER BY a.numer
"""
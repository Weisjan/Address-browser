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
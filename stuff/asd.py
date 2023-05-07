import sqlite3

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect("stopwatch_data.db")
c = conn.cursor()

# Tabelle "projekte" erstellen
c.execute(
    """CREATE TABLE IF NOT EXISTS projekte 
             (id INTEGER PRIMARY KEY, name TEXT, von TEXT, bis TEXT)"""
)

# Beispielprojekte einfügen
projekte = [
    (1, "Projekt A", "2023-01-01", "2023-06-30"),
    (2, "Projekt B", "2023-03-15", "2023-09-15"),
    (3, "Projekt C", "2022-12-01", "2023-03-31"),
    (4, "Projekt D", "2023-02-01", "2023-07-31"),
    (5, "Projekt E", "2023-04-01", "2023-09-30"),
    (6, "Projekt F", "2022-11-01", "2023-04-30"),
    (7, "Projekt G", "2023-01-15", "2023-06-15"),
    (8, "Projekt H", "2023-03-01", "2023-08-31"),
    (9, "Projekt I", "2022-10-01", "2023-03-31"),
    (10, "Projekt J", "2023-05-01", "2023-10-31"),
]

# Projekte in die Tabelle einfügen
c.executemany("INSERT INTO projekte (id, name, von, bis) VALUES (?, ?, ?, ?)", projekte)

# Änderungen speichern und Verbindung zur Datenbank beenden
conn.commit()
conn.close()

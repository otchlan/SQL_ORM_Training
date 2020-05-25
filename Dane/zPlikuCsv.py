import sqlite3
import os
import time

def pobierzPlik (plik = "/home/pr/Programowanie/Dane/Dane/uczniowie.csv"):
    dane = []

    if os.path.isfile(plik):
        with open(plik, 'r') as zawartosc:
            for linia in zawartosc:
                linia = linia.replace("\n", "")
                linia = linia.replace("\r", "")
                dane.append(tuple(linia.split(",")))
    else:
        print("NIe ma pliku")

    return tuple(dane)

def zapiszDoBazy():
    con = sqlite3.connect("z_csv.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.executescript(
        """
        DROP TABLE IF EXISTS uczen; 
        CREATE TABLE IF NOT EXISTS uczen (
        id INTEGER PRIMARY KEY ASC,
        imie varchar(250) NOT NULL,
        nazwisko varchar(250) NOT NULL,
        klasa_id INTEGER NOT NULL
        )
        """
    )

    osoby = pobierzPlik()
    """ !! executemany !! i na końcu osoby są bez nawiasu"""
    cur.executemany('INSERT INTO uczen (imie, nazwisko, klasa_id) VALUES(?, ?, ?)', osoby)

    cur.execute('SELECT * FROM uczen')
    data = cur.fetchall()
    for row in data:
        print("Uczen ", row[:])

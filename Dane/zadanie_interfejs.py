import sqlite3
import time

con = sqlite3.connect('z2_csv.db')
con.row_factory = sqlite3.Row
cur = con.cursor()


cur.executescript(
    """
    DROP TABLE IF EXISTS drzewo;
    CREATE TABLE IF NOT EXISTS drzewo (
    id INTEGER PRIMARY KEY ASC,
    imie varchar(250) NOT NULL,
    nazwisko varchar (250) NOT NULL,
    dane_id INTEGER NOT NULL
    )
    """
    )
wstaw = (
    (None, 'Qwerty', 'Zxcvb', 1),
    (None, 'Struktura', 'Zarządzanie', 5),
    (None, 'Proces', 'Tamjest', 6),
    (None, 'Efekt', 'Kompetencji', 3),
    (None, 'Jest', 'Stoosiem', 1)
    )
cur.executemany('INSERT INTO drzewo VALUES(?, ?, ?, ?)', wstaw)
con.commit()

def odczytaj():
    # cur.execute('SELECT id FROM drzewo WHERE dane_id = ?', ('1',))
    # dane_id = cur.fetchone()[0]

    cur.execute("""SELECT * FROM drzewo""")
    data = cur.fetchall()
    for row in data:
        print("--> ", row[:])

def dodaj(im, naz, kl):
    cur.execute('INSERT INTO drzewo VALUES(?, ?, ?, ?)', (None, im, naz, kl))
    con.commit()
    cur.execute("""SELECT * FROM drzewo""")
    data = cur.fetchall()

    for row in data:
        print("--> ", row[:])

def interfejs():

    print("Będziemy pracować na bazie")
    print("Podaj pełną nazwę bazy")
    # nazwa = input()

    button = 5
    while button != 0:
        # try:
            print("Co robimy?\n1 - odczyt\n2 - dodaj\n3 - modyfikuj\n4 - usuń\n0 - wyjdź\nWYBIERAJ")

            button = int(input())
            if button == 1:
                print("Odczytywanie z bazy danych")
                time.sleep(1)
                print(odczytaj())

            elif button == 2:
                print("Dodawanie do bazy danych")
                print("Podaj imie")
                im = input()
                print("Podaj nazwisko")
                naz = input()
                print("Podaj numer")
                nr = input()
                dodaj(im, naz, nr)
                
            elif button == 3:
                print("Modyfikowanie bazy")
                # print("Który rekord chcesz zmodyfikować")
                # nr = int(input())
                cur.execute("""SELECT drzewo.id, imie, nazwisko, dane_id FROM drzewo""")
                print("Modyfikujemy imie z komórce 2")
                cur.execute('UPDATE drzewo SET imie = ? WHERE id = ?', ('Janina', 2))
                con.commit()

            elif button == 4:
                print("Usuwanie z bazy")
                print("Wskaż rekord do usunięcia")
                id = int(input())
                cur.execute('DELETE FROM drzewo WHERE id = ?', (id,))
                con.commit()

            else:
                print("META")

        # except:
        #     print("Nie numer")
    con.close()
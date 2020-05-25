import sqlite3

# create object in witch we will be storage our data
con_db = sqlite3.connect('test.db')
con_db.row_factory = sqlite3.Row

cur = con_db.cursor()

def pmw():
    cur.execute("DROP TABLE IF EXISTS klasa")

    cur.execute("""
                CREATE TABLE IF NOT EXISTS klasa (
                id INTEGER PRIMARY KEY ASC,
                nazwa varchar(250) NOT NULL,
                profil varchar(250) DEFAULT ''
                )
                """)

    cur.executescript("""
                    DROP TABLE IF EXISTS uczen;
                    CREATE TABLE IF NOT EXISTS uczen (
                    id INTEGER PRIMARY KEY ASC,
                    imie varchar(250) NOT NULL,
                    nazwisko varchar (250) NOT NULL,
                    klasa_id INTEGER NOT NULL,
                    FOREIGN KEY(klasa_id) REFERENCES klasa(id)
                    )
                    """)

    # Insert records to database
    cur.execute('INSERT INTO klasa VALUES(NULL, ?, ?);', ('1A', 'matematyczny'))
    cur.execute('INSERT INTO klasa VALUES(NULL, ?, ?);', ('2B', 'przyrodniczy'))

    """Pull form database id of pick class"""
    cur.execute('SELECT id FROM klasa WHERE nazwa = ?', ('2B',))
    klasa_id = cur.fetchone()[0]
    # print("ID klasy ", klasa_id)

    """Pull from databse data about all clases"""
    # cur.execute("""SELECT * FROM klasa""")
    # data = cur.fetchall()
    # for row in data:
    #     print("Nazwa klasy", row[:])

    uczniowie = (
        (None, 'Tomasz', 'Nowak', klasa_id),
        (None, 'Bomasz', 'Hwak', klasa_id),
        (None, 'Somasz', 'Nohrws', klasa_id)
    )

    pojedynczy = (None, 'Kolba', 'Uebok', 9)

    cur.executemany('INSERT INTO uczen VALUES(?, ?, ?, ?)', uczniowie)
    con_db.commit()

    # cur.execute('INSERT INTO uczen VALUES (?, ?, ?, ?)', pojedynczy)
    # con_db.commit()

    cur.execute("""SELECT * FROM uczen""")
    data = cur.fetchall()
    for row in data:
        print("ID ucznia", row[:])

def czytajdane():
    cur.execute(
        """
        SELECT uczen.id, imie, nazwisko, nazwa FROM uczen, klasa
        WHERE uczen.klasa_id = klasa.id
        """
    )

    uczniowie = cur.fetchall()
    for uczen in uczniowie:
        print(uczen['id'], uczen['imie'], uczen['nazwisko'], uczen['nazwa'])

"""Nie wie dlaczego, ale coś w tym nie działa SELECT/UPDATE"""
def zamien():
    cur.execute('SELECT id FROM klasa WHERE nazwa = ?', ('2B',))
    klasa_id = cur.fetchone()[0]
    print("kla", klasa_id)
    cur.execute('UPDATE uczen SET klasa_id = ? WHERE id = ?', (klasa_id, 3))
    cur.execute('DELETE FROM uczen WHERE id = ?', ((12),))
    con_db.commit()
    czytajdane()
    con_db.close()
import zPlikuCsv as zp
import os
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

if os.path.exists('test.db'):
    os.remove('test.db')

baza = create_engine('sqlite:///test_0.db')
BazaModel = declarative_base()

class Klasa(BazaModel):
    __tablename__ = 'klasa'
    id = Column(Integer, primary_key=True)
    nazwa = Column(String(100), nullable=False)
    profil = Column(String(100), default='')
    uczniowie = relationship('Uczen', backref="klasa")

class Uczen(BazaModel):
    __tablename__ = 'uczen'
    id = Column(Integer, primary_key=True)
    imie = Column(String(100), nullable=False)
    nazwisko = Column(String(100), nullable=False)
    klasa_id = Column(Integer, ForeignKey('klasa.id'))

BazaModel.metadata.create_all(baza)

DBSesja = sessionmaker(bind=baza)
sesja = DBSesja()

def wiele_z1():
    uczniowie = zp.pobierzPlik()

    if not sesja.query(Klasa).count():
        sesja.add(Klasa(nazwa="3A", profil='Ananasik'))
        sesja.add(Klasa(nazwa="3B", profil='Pomidor'))
        sesja.add(Klasa(nazwa="3C", profil='PrimaAprilis'))
        sesja.add(Klasa(nazwa="3E", profil='Ręcznik'))
        sesja.add(Klasa(nazwa="3F", profil='Karazela'))

    # inst_klasa = sesja.query(Klasa).filter_by('1A').one()

    for uczen in uczniowie:
        sesja.add(Uczen(imie=uczen[0], nazwisko=uczen[1], klasa_id=uczen[2]))

    for uczen in uczniowie:
        print(uczen)

    # one = sesja.add_all(uczniowie)
    # print("ONE")
    # print(one)

    # sesja.commit()
    sesja.close()

"""Prosty interfejs konsolowy - CRUD"""
def interfejs_z2():
    button = 5
    while button != 0:
        # try:
        print("Co robimy?\n1 - odczyt\n2 - dodaj\n3 - modyfikuj\n4 - usuń\n0 - wyjdź\nWYBIERAJ")

        button = int(input())
        if button == 1:
            print("Odczytywanie z bazy danych")
            czytajdane()

        elif button == 2:
            print("Dodawanie do bazy danych")
            dodawanie()

        elif button == 3:
            print("Modyfikowanie bazy")
            modyfikowanie()

        elif button == 4:
            print("Usuwanie z bazy")
            usuwanie()
        else:
            print("META")

def dodawanie():
    print("Podaj imie")
    imie_p = input()
    print("Podaj nazwisko")
    nazwisko_p = input()
    print("Do której klasy chodzi")
    nazwa_p = input()
    # print("Podaj profil klasy")
    # profil_p = input()

    """How to join in two difference databases"""

    sesja.add(Uczen(imie=imie_p, nazwisko=nazwisko_p, klasa_id=nazwa_p))
    print("Dodano")
    sesja.commit()

def modyfikowanie():
    print("Podaj numer rekord, który zmieniamy")
    rin = input()

    x = False
    while x != True:
        try:
            rin = int(rin)
            x = True
        except ValueError:
            print("Podaj liczbe")
            rin = input()
    # r = isinstance(rin, int)
    # print(r)
    modifi = sesja.query(Uczen).get(rin)
    modifi_2 = sesja.query(Klasa).get(modifi.klasa_id)
    print("Z bazy:", modifi.imie, modifi.nazwisko, modifi_2.nazwa, modifi_2.profil)

    sesja.query(Uczen).filter(Uczen.id == rin).update({Uczen.imie:'Stefan'}, synchronize_session=False)
    modifi = sesja.query(Uczen).get(rin)
    sesja.commit()
    print("Po: ", modifi.imie)

    """Error: 'Uczen' has no attribute 'select"""
    # inst_uczen = Uczen().select().join().where(Uczen.id == rin).get()
    # print(inst_uczen)
    # inst_uczen.klasa = Klasa.select().where(Klasa.nazwa == '1B').get()
    # print(inst_uczen.klasa)

    """Test"""
    # test = sesja.query(Uczen).get(3)
    # test_2 = sesja.query(Klasa).get(test.klasa_id)
    # print("tt", test.imie, test.klasa_id, test_2.profil)
    # for t in test:
    #     print("Test ", t.id, t.imie, t.nazwisko, t.klasa.nazwa)

def usuwanie():
    print("Podaj którą usuwamy")
    usun = int(input())
    row = sesja.query(Uczen).get(usun)
    sesja.delete(row)
    sesja.commit()

    print("Usunięto ")

def czytajdane():

    for uczen in sesja.query(Uczen).join(Klasa).all():
        print(uczen.id, uczen.imie, uczen.nazwisko, uczen.klasa.nazwa, uczen.klasa.profil)


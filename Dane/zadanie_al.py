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
            wiele_z1()

        elif button == 2:
            print("Dodawanie do bazy danych")
            print(dodawanie())

        elif button == 3:
            print("Modyfikowanie bazy")


        elif button == 4:
            print("Usuwanie z bazy")

        else:
            print("META")

def dodawanie():
    print("Podaj imie")
    imie_p = input()
    print("Podaj nazwisko")
    nazwisko_p = input()
    print("Do której klasy chodzi")
    nazwa_p = input()
    print("Podaj profil klasy")
    profil_p = input()

    """How to join in two difference databases"""

    sesja.add(Uczen(imie=imie_p, nazwisko=nazwisko_p)).join(Klasa(nazwa=nazwa_p, profil=profil_p))
    print("Dodano")
    sesja.commit()

def modyfikowanie():
    """Jak wynbrać konkterny rekord z bazy"""
    """Jak to zrobić, żeby było automatyczne: 
    Ktoś chce zmienić klase wpisuje imie i nazwisko i zmienia klase"""
    test = sesja.query(Uczen).filter_by(imie='Jan').all()


    # print("tt", test)
    for t in test:
        print("Test ", t.id, t.imie, t.nazwisko, t.klasa.nazwa)


def czytajdane():

    for uczen in sesja.query(Uczen).join(Klasa).all():
        print(uczen.id, uczen.imie, uczen.nazwisko, uczen.klasa.nazwa, uczen.klasa.profil)


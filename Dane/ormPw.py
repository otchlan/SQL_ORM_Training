import os
import peewee
import sqlite3

if os.path.exists('testPw.db'):
    os.remove('testPw.db')

baza = peewee.SqliteDatabase('testPw.db')

class BazaModel(peewee.Model):
    class Meta:
        database = baza

class Klasa(BazaModel):
    nazwa = peewee.CharField(null=False)
    profil = peewee.CharField(default='')

class Uczen(BazaModel):
    imie = peewee.CharField(null=False)
    nazwisko = peewee.CharField(null=False)
    klasa = peewee.ForeignKeyField(Klasa, related_name='uczniowie')

baza.connect()
baza.create_tables([Klasa, Uczen])#True - na końcu było

if Klasa().select().count() == 0:
    inst_klasa = Klasa(nazwa='1A', profil='matematyczny')
    inst_klasa.save()
    inst_klasa = Klasa(nazwa='1B', profil='humanistyczny')
    inst_klasa.save()

inst_klasa = Klasa.select().where(Klasa.nazwa == '1A').get()

uczniowie = [
    {'imie':'Tomasz', 'nazwisko':'Nowak', 'klasa':inst_klasa},
    {'imie':'Gomasz', 'nazwisko':'Fowak', 'klasa':inst_klasa},
    {'imie':'Daniel', 'nazwisko':'Ktrdf', 'klasa':inst_klasa}
]

Uczen.insert_many(uczniowie).execute()

def czytajdane():
    for uczen in Uczen.select().join(Klasa):
        print(uczen.id, uczen.imie, uczen.nazwisko, uczen.klasa.nazwa)
    print()

"""Więcej nie robie w peewee Alcgemy lepsze"""
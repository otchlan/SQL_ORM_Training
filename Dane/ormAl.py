import os
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

if os.path.exists('test.db'):
    os.remove('test.db')

baza = create_engine('sqlite:///testAl.db')
BazaModel = declarative_base()
BazaModel.metadata.create_all(baza)

"""Tworzymy sesje, która przechowuje obiekty i umożliwia kontakt z bazą"""
DBSesja = sessionmaker(bind=baza)
sesja = DBSesja()

class Klasa(BazaModel):
    __tablename__ = 'klasa'
    id = Column(Integer, primary_key=True)
    nazwa = Column(String(100), nullable=False)
    profil = Column(String(100), default='')
    uczniowie = relationship('Uczen', backref='klasa')

class Uczen(BazaModel):
    __tablename__ = 'uczen'
    id = Column(Integer, primary_key=True)
    imie = Column(String(100), nullable=False)
    nazwisko = Column(String(100), nullable=False)
    klasa_id = Column(Integer, ForeignKey('klasa.id'))

if not sesja.query(Klasa).count():
    sesja.add(Klasa(nazwa='1A', profil='matematyczny'))
    sesja.add(Klasa(nazwa='1B', profil='humanistyczzny'))

inst_klasa = sesja.query(Klasa).filter_by(nazwa='1A').one()

sesja.add_all([
    Uczen(imie='Tomasz', nazwisko='Tatright', klasa_id=inst_klasa.id),
    Uczen(imie='Pomert', nazwisko='Idiatu', klasa_id=inst_klasa.id),
    Uczen(imie='Gqwer', nazwisko='Klok', klasa_id=inst_klasa.id)
])

# sesja.commit()

# a = sesja.query(Uczen).count()
# print("AAA ", a)

# inst_klasa = sesja.query(Uczen).filter(Uczen.id == 12).one()
# inst_klasa.klasa_id = sesja.query(Klasa.id).filter(Klasa.nazwa == '1B').scalar()

# sesja.delete(sesja.query(Uczen).get(12))

def czytajdane():
    for uczen in sesja.query(Uczen).join(Klasa).all():
        print(uczen.id, uczen.imie, uczen.nazwisko, uczen.klasa.nazwa)
    # for se in sesja.query(Klasa):
    #     print(se.profil)

# sesja.commit()
sesja.close()




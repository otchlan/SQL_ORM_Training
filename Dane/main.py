import test_y
import zPlikuCsv
import zadanie_interfejs as zi
import zadanie_al as za


import ormPw as op
import ormAl as al

if __name__ == '__main__':
    """SQL"""
    # print(test_y.pmw())
    # test_y.pmw()
    # print(test_y.czytajdane())
    # print(test_y.zamien())
    # print(zPlikuCsv.pobierzPlik())
    # print(zPlikuCsv.zapiszDoBazy())
    # print("Test - odc1z", zi.odczytaj())
    # print("Test ", zi.interfejs())

    """ORMy"""
    # al.czytajdane()
    # print('Alchemy')
    # al.czytajdane()
    # print("peewee")
    # op.czytajdane()
    # za.wiele_z1()
    # za.czytajdane()
    za.interfejs_z2()
    za.modyfikowanie()
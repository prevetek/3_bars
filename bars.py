#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from urllib.request import urlretrieve
import zipfile
import math


# расчет расстояния между двумя точками поверхности земли
def Dist(llat1, llong1, llat2, llong2):
    # pi - число pi, rad - радиус сферы (Земли)
    rad = 6372795
    # в радианах
    lat1 = llat1 * math.pi / 180.
    lat2 = llat2 * math.pi / 180.
    long1 = llong1 * math.pi / 180.
    long2 = llong2 * math.pi / 180.
    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)
    # вычисления длины большого круга
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    dist = ad * rad
    return dist


def load_data(filepath="http://data.mos.ru/opendata/export/1796/json/2/"):
    urlretrieve(url=filepath, filename="1.zip")
    zf = zipfile.ZipFile("1.zip", "r")
    zname = zf.namelist()[0]
    js = json.loads(zf.read(zname).decode('utf-8'))
    data = []
    for i in js:
        data.append({"name": i["Cells"]["Name"],
                     "space": i["Cells"]["SeatsCount"],
                     "coordinates": i["Cells"]["geoData"]["coordinates"],
                     "address": i["Cells"]["Address"]
                     })
    return data


def get_biggest_bar(data):
    # Определяем бар с максимальным количеством мест
    max = 0  # буфер мест в самом большом баре
    for i in data:
        if i["space"] > max:
            max = i["space"]
            bars = []
            bars.append(i)
        elif i["space"] == max:
            bars.append(i)
    for i in bars:
        print("-- %s имеет %s посадочных мест, адресс: %s" % (i["name"], i["space"], i["address"]))


def get_smallest_bar(data):
    max = 99999999  # буфер мест в самом большом баре
    for i in data:
        if i["space"] < max:
            max = i["space"]
            bars = []
            bars.append(i)
        elif i["space"] == max:
            bars.append(i)
    for i in bars:
        print("-- %s имеет %s посадочных мест, адресс: %s" % (i["name"], i["space"], i["address"]))


def get_closest_bar(data, longitude, latitude):
    max = 99999999999999  # буфер мест в самом большом баре
    for i in data:
        d = Dist(i["coordinates"][0], i["coordinates"][1], longitude, latitude)
        if d < max:
            max = d
            bars = []
            bars.append(i)
        elif d == max:
            bars.append(i)
    for i in bars:
        print("-- %s имеет %s посадочных мест, адресс: %s" % (i["name"], i["space"], i["address"]))


if __name__ == '__main__':
    data = load_data()
    hello = """Приветствуем Вас!!!
               Доступны следующие команды:
               s - поиск самого маленького бара
               b - поиск самого большого бара
               c - поиск ближайшего бара
               x - завершить программу
               """
    print(hello)
    while 1:
        com = input("Введите команду: ")
        if com == "x":
            print("Сэр, приятного Вам отдыха!")
            break
        elif com == "s":
            get_smallest_bar(data)
        elif com == "b":
            get_biggest_bar(data)
        elif com == "c":
            print("Введите свои координаты в градусах с десятичной дробью (используйте знак '-' для отрицательных координат)")
            while 1:
                try:
                    x = input("  широта:")
                    x = float(x.replace(",", "."))
                    break
                except ValueError:
                    print("Такой широты не сущестует, попробуйте еще раз...")
                    continue
            while 1:
                try:
                    y = input("  долгота:")
                    y = float(y.replace(",", "."))
                    break
                except ValueError:
                    print("Такой долготы не существует, попробуйте еще раз...")
                    continue
            get_closest_bar(data, x, y)
        else:
            print("Сэр, я не знаю такой команды...")


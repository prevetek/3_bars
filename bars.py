#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from urllib.request import urlretrieve
from zipfile import ZipFile
from math import cos, sin, asin, sqrt, radians
from tempfile import NamedTemporaryFile


# расчет расстояния между двумя точками поверхности земли
def distance(latitude1, longitude1, latitude2, longitude2):
    earth_radius = 6372.795
    lat1, long1, lat2, long2 = map(radians, [latitude1, longitude1, latitude2, longitude2])
    delta_lat = lat2 - lat1
    delta_long = long2 - long1
    # вычисления длины большого круга
    a = sin(delta_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(delta_long / 2)**2
    c = 2 * asin(sqrt(a))
    dist = earth_radius * c
    return dist


def load_data(filepath="http://data.mos.ru/opendata/export/1796/json/2/"):
    tempfile = NamedTemporaryFile()
    urlretrieve(url=filepath, filename=tempfile.name)
    zf = ZipFile(tempfile.name, "r")
    zname = zf.namelist()[0]
    js = json.loads(zf.read(zname).decode('utf-8'))
    data = []
    for i in js:
        data.append({"name": i["Cells"]["Name"],
                     "space": i["Cells"]["SeatsCount"],
                     "coordinates": i["Cells"]["geoData"]["coordinates"],
                     "address": i["Cells"]["Address"]
                     })
    zf.close()
    tempfile.close()
    return data


def get_biggest_bar(data):
    for number, bar in enumerate(data):
        if number == 0:
            big_bar = bar["space"]
            continue
        if bar["space"] > big_bar:
            big_bar = bar["space"]
            biggest_bars = [bar]
        elif bar["space"] == big_bar:
            biggest_bars.append(bar)
    return biggest_bars


def get_smallest_bar(data):
    for number, bar in enumerate(data):
        if number == 0:
            small_bar = bar["space"]
            continue
        if bar["space"] < small_bar:
            small_bar = bar["space"]
            smallest_bars = [bar]
        elif bar["space"] == small_bar:
            smallest_bars.append(bar)
    return smallest_bars


def get_closest_bar(data, longitude, latitude):
    for number, bar in enumerate(data):
        dist = distance(bar["coordinates"][1], bar["coordinates"][0], longitude, latitude)
        if number == 0:
            closest_bar = bar.copy()
            closest_bar.update({"distance": dist})
            continue
        if dist < closest_bar["distance"]:
            closest_bar = bar.copy()
            closest_bar.update({"distance": dist})
            closest_bars = [closest_bar]
        elif dist == closest_bar["distance"]:
            closest_bar = bar.copy()
            closest_bar.update({"distance": dist})
            closest_bars.append(closest_bar)
    return closest_bars


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
        comand = input("Введите команду: ")
        if comand == "x":
            print("Сэр, приятного Вам отдыха!")
            break
        elif comand == "s":
            bars = get_smallest_bar(data)
            for bar in bars:
                print("-- %s имеет %s посадочных мест(а), адресс: %s" % (bar["name"], bar["space"], bar["address"]))
        elif comand == "b":
            bars = get_biggest_bar(data)
            for bar in bars:
                print("-- %s имеет %s посадочных мест(а), адресс: %s" % (bar["name"], bar["space"], bar["address"]))
        elif comand == "c":
            print(
                "Введите свои координаты в градусах с десятичной дробью (используйте знак '-' для "
                "отрицательных координат)")
            while 1:
                try:
                    latitude = input("  широта:")
                    latitude = float(latitude.replace(",", "."))
                    break
                except ValueError:
                    print("Такой широты не сущестует, попробуйте еще раз...")
                    continue
            while 1:
                try:
                    longitude = input("  долгота:")
                    longitude = float(longitude.replace(",", "."))
                    break
                except ValueError:
                    print("Такой долготы не существует, попробуйте еще раз...")
                    continue
            bars = get_closest_bar(data, latitude, longitude)
            for bar in bars:
                print(u"-- {0:s} находится в {1:.1f} км. от Вас по адреуссу {2:s} и имеет {3:d} посадочных мест(а)"
                      .format(bar["name"], bar["distance"], bar["address"], bar["space"]))
        else:
            print("Сэр, я не знаю такой команды...")

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 14:36:34 2021

@author: Juan Antonio

Title: funciones de grafica

ver: 1.0
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import os

def ema(lista, inter):
    listac = lista.copy()
    SMA = 0
    EMA = list()
    for a in range(inter):
        SMA += listac.pop(0)
        EMA.append(0)
    SMA = SMA/inter
    EMA.pop(0)
    EMA.append(SMA)
    for el in listac:
        loc = el * (2/(1+inter)) + EMA[-1] * (1 -(2/(1+inter)))
        EMA.append(loc)
    return EMA


def max_mini(lista):
    i = 1
    maxi = [0]
    ma = True
    mini = [0]
    max_min = [0]
    while i < len(lista):
        if ma:
            if lista[i] > lista[i-1]:
                max_min.append(mini[-1])
            else:
                maxi.append(lista[i-1])
                max_min.append(lista[i-1])
                ma = False
        else:
            if lista[i] < lista[i-1]:
                max_min.append(maxi[-1])
            else:
                mini.append(lista[i-1])
                max_min.append(lista[i-1])
                ma = True
        i +=1
    return maxi, mini, max_min


data = pd.read_csv('AAgraphs\\assets\data.csv')



c = data.circulo_cords
t = data.Tiempo
lista_x = list()
lista_y = list()
lista_t = list(t.map(lambda x: x))
for a in c:
  lon = len(a)
  ind = a.index(',')
  lista_x.append(int(a[1:ind]))
  lista_y.append(int(a[ind+1:lon-1]))

r = data.regla_inc_a
lista_xr = list()
lista_yr = list()
for a in r:
  lon = len(a)
  ind = a.index(',')
  lista_xr.append(int(a[1:ind]))
  lista_yr.append(int(a[ind+1:lon-1]))

for eli in range(5):
  lista_x.pop(0)
  lista_y.pop(0)
  lista_t.pop(0)
  lista_xr.pop(0)
  lista_yr.pop(0)

ema_y = ema(lista_y,15)
ema_x = ema(lista_x,30)
ema_xr = ema(lista_xr,15)
ema_yr = ema(lista_yr,15)
prueba = max_mini(lista_y)
ema_p = ema(prueba[2], 15)
for eli in range(30):
    lista_x.pop(0)
    lista_y.pop(0)
    lista_t.pop(0)
    lista_xr.pop(0)
    lista_yr.pop(0)
    ema_y.pop(0)
    ema_x.pop(0)
    ema_xr.pop(0)
    ema_yr.pop(0)
    ema_p.pop(0)
    prueba[2].pop(0)

plt.plot(lista_t,lista_x, 'o-')
plt.plot(lista_t, ema_x)
plt.show()

plt.plot(lista_t, lista_y,'o-')
plt.plot(lista_t, ema_y)
plt.plot(lista_t, prueba[2])
plt.plot(lista_t,ema_p)
plt.show()

plt.plot(lista_t, lista_yr, 'o-')
plt.plot(lista_t, ema_yr)

plt.show()

plt.plot(lista_t, lista_xr, 'o-')
plt.plot(lista_t, ema_xr)
plt.show()


lista = list(range(len(prueba[0])))
listab = list(range(len(prueba[1])))
listac = list(range(len(prueba[2])))

plt.plot(lista, prueba[0])
plt.plot(listab, prueba[1])
plt.plot(listac, prueba[2])
plt.show()











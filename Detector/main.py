# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 20:42:38 2021

@author: Juan Antonio

Title: Seguidor de movimiento

ver: 3.0
"""
# Librerias
import functions
import numpy as np
import cv2 as cv
import time
import matplotlib.pyplot as plt
"""
NOTA
----
functions se aplica en espacio base 480,640.
Si se usa una camara con diferentes dimensiones
se recomienda redimensionar con una mascara.

"""

# Variables
r = int(input('Radio: '))
pTime = 0
cTime = 0
datav = list()
print('--Press d to start--')
cap = cv.VideoCapture(0)
while True:
    n, frame = cap.read()
    cv.imshow('0', frame)
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
    
print('Recording inicial data')

n, frame = cap.read()
bframe = cv.medianBlur(frame,5)
gframe1 = cv.cvtColor(bframe, cv.COLOR_BGR2GRAY)
gframe1u, gframe1d = functions.division_up_down(gframe1)
gframe1uc = gframe1u.copy()
functions.profundidad(frame)
print('Launch')
sTime = time.time()
# Bucle
while True:
    # Funciones
    n, frame = cap.read()
    
    uf, df = functions.division_up_down(frame)
    
    umbralm, umbrald, framedif, gframe1= functions.movimiento(df, gframe1d)
    
    _, gframe1d = functions.division_up_down(gframe1)
    
    morph, blank, mascara, cannym, isTrue = functions.morphdata(umbralm, r)
    
    # up functions
    dif = functions.inclinacion(gframe1uc, frame)
    
    # Dilation-Shows
    if isTrue:
        mascarap, circ, cm, ci, cd, isTrue = functions.dilationdata(umbrald, mascara, r)
        if isTrue:
            functions.imshows(morph,blank,mascara,cannym,umbralm,umbrald,framedif, circ,mascarap, dif, gframe1u)
            Time = time.time()
            cTime = Time - pTime
            pTime = cTime
            stTime = Time - sTime
            datav = functions.data(datav,['T entre med',cTime],['Tiempo',stTime], ['circulo cords',cm[0]])
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
    
cap.release()
cv.destroyAllWindows()

# Data
x = list()
y = list()
for data in datav:
    x.append(data[2][1][0])
    y.append(480-data[2][1][1])
    for d in data:
        print(d)
graf = functions.graph(x, y)
graf.show()      

print(x)
print(y)
print(len(datav))
print(stTime)
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 17:08:05 2021

@author: Juan Antonio

Title: Seguidor de movimiento

ver: 4.0
"""

# Librerias
import cv2 as cv
import numpy as np
import functions2
import matplotlib.pyplot as plt
import time
import os
# Variables
cap = cv.VideoCapture(0)
pTime = 0
cTime = 0
p1 = [0,0]
lista = list()

# Toma de datos 
pref = str(input('Prefijo: '))
r = int(input('radio objeto: '))
l = int(input('longitud resorte: '))
print('--Press d to start--')
while True:
    isTrue, frame = cap.read()
    cv.imshow('frame', frame)
    functions2.profundidad(frame, 210)
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
_, frame = cap.read()

cm1, inv, cords, isTrue = functions2.profundidad(frame, 210)
bframe = cv.medianBlur(frame,5)
gframe1 = cv.cvtColor(bframe, cv.COLOR_BGR2GRAY)
gframe1u, gframe1d = functions2.division_up_down(gframe1)


radio = int(r * cm1)
radpx = int(l * cm1)
print('Launch')
sTime = time.time()
# Bucle
while True:
    isTrue, frame = cap.read()
    uf, df = functions2.division_up_down(frame)
    
    umbralm, umbrald, framedif, gframe1d = functions2.movimiento(df, gframe1d)
    pp = p1
    p1, move= functions2.inclinacion(uf, gframe1u, radio, radpx, cords)
    
    gframe1u = cv.cvtColor(uf, cv.COLOR_BGR2GRAY)
    
    mascara, isTrue = functions2.morphdata(umbralm, radio)
    if not move:
        p1 = pp
    if isTrue:
        blank3c, circ, cm, ci, cd, isTrue = functions2.dilationdata(umbrald, mascara, radio)
        if isTrue:
            functions2.imshows(umbralm, blank3c, circ, frame, uf, df)
            
            Time = time.time()
            cTime = Time - pTime
            pTime = Time
            stTime = Time - sTime  
            functions2.data(lista, ['T_entre_med',cTime],['Tiempo',stTime], 
                            ['circulo_cords',list(cm[0])],['regla_inc_a', p1])
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
# Release
cap.release()
cv.destroyAllWindows()


# Analisis
try:
    os.mkdir(f'assets\\{pref}')
except:
    pass
functions2.excel(lista, f'assets\\{pref}\\Datos')

functions2.graphfromsublist(lista, 2, f'assets\\{pref}\\pos')

functions2.graphfromsublist(lista, 3, f'assets\\{pref}\\inc')

# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 17:56:02 2021

@author: Juan Antonio

Title: funciones de movimiento

ver: 1.0

"""
# Librerias
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

"""
NOTA
----
functions se aplica en espacio base 480,640.
Si se usa una camara con diferentes dimensiones
se recomienda redimensionar con una mascara.

"""

# Funciones
def union(a,b):
    '''
    Union de rectangulos.\n
    \n
    Parameters\n
    ----------\n
    a : rectangulo 1 [x,y,w,h].\n
    b : rectangulo 2 [x,y,w,h].\n
    \n
    Returns\n
    -------\n
    x.\n
    y.\n
    w.\n
    h.\n

    '''
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0]+a[2], b[0]+b[2]) - x
    h = max(a[1]+a[3], b[1]+b[3]) - y
    return (x, y, w, h)

def movimiento(frame, gframe1, blur = 5, sensibilidad_morph = 10, sensibilidad_dilation = 20):
    '''
    Actualización de variables para metodos externos morph y dilation.\n
    \n
    Parameters\n
    ----------\n
    frame : frame actual.\n
    gframe1 : frame anterior.\n
    blur : valor de blur impar. The default is 5.\n
    sensibilidad_morph : valor de uno minimo 0-255. The default is 10.\n
    sensibilidad_dilation : valor de uno minimo 0-255. The default is 20.\n
    \n
    Returns\n
    -------\n
    umbralm: umbral para metodo morph.\n
    umbrald: umbral para metodo dilation.\n
    framedif: diferencia frame pasado y actual.\n
    gframe1: frame actual para futuro cambio.\n

    '''
    
    bframe = cv.medianBlur(frame, blur)
    grayframe = cv.cvtColor(bframe, cv.COLOR_BGR2GRAY)
    framedif = cv.absdiff(grayframe, gframe1)
    gframe1 = grayframe
    umbralm = cv.threshold(framedif, 10, 255, cv.THRESH_BINARY)[1]
    umbrald = cv.threshold(framedif, 20, 255, cv.THRESH_BINARY)[1]
    
    return umbralm, umbrald, framedif, gframe1


def morphdata(umbralm, r, blank = np.zeros((480,640,3),dtype='uint8'),
              blank2 = np.zeros((480,640),dtype='uint8'), zeros = np.zeros((480,640),dtype='uint8'),
              kernelm = np.ones((8,8),np.uint8)):
    '''
    Obtener posiciones iniciales de objetos por proceso Morph.\n
    \n
    Parameters\n
    ----------\n
    umbralm: umbral para metodo morph.\n
    r: radio variable.\n
    blank: matriz ceros. The default is  np.zeros((480,640,3),dtype='uint8').\n
    blank2: matriz ceros 2. The default is  np.zeros((480,640),dtype='uint8').\n
    zeros: funcion estable en ceros. The default is  np.zeros((480,640),dtype='uint8').\n
    kernelm: variable morph.\n
    
    Returns\n
    -------\n
    morph: matriz con metodo morph.\n
    blank: contornos de umbralm, rectangulo base y aumentado -notfill-.\n
    blank2: rectangulo aumentado -fill-.\n
    cannym: canny aplicado a umbralm.\n
    True --- False is function is valid
    '''
    blankc = blank.copy()
    blank2c = blank2.copy()
    # Locales
    mayorn = 0
    mayorc = 0
    csum = 0
    
    # Funcion
    if not (umbralm == zeros).all():
        morph = cv.morphologyEx(umbralm, cv.MORPH_OPEN, kernelm)
        
        cannym = cv.Canny(morph, 30, 120, apertureSize = 3)
        contornosm, hierarchym = cv.findContours(morph,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        
        # --- Contorno mas grande de morph --- #
        try:
            cv.drawContours(blankc, contornosm,-1,(0,0,255),-1)
            for c in contornosm:
                if mayorn < cv.contourArea(c):
                    mayorn = cv.contourArea(c)
                    mayorc = csum
                csum += 1
            x,y,w,h = cv.boundingRect(contornosm[mayorc])
            cv.rectangle(blankc, (x,y), (x+w, y+h),(0,255,0), 1)
            
            # --- Rectangulo aumentado en radio --- #
            xa = x - (3 * r)
            if xa < 0:
                xa = 0
            ya = y - r
            if ya < 0:
                ya = 0
            wa = w + (6 * r)
            ha = h + (2 * r)
            cv.rectangle(blankc, (xa,ya), (xa+wa,ya+ha),(255,0,0), 1)
            cv.rectangle(blank2c, (xa,ya), (xa+wa,ya+ha),255, -1)
            return morph, blankc, blank2c, cannym, True
        except:
            return False, False, False, False, False
    else:
        return False, False, False, False, False

def dilationdata(umbrald,mascara,r,blank = np.zeros((480,640),dtype='uint8'),
                 cir= np.zeros((480,640,3),dtype='uint8'), zeros = np.zeros((480,640),dtype='uint8')):
    '''
    Seguimiento de movimiento con metodo dilation.\n
    \n
    Parameters\n
    ----------\n
    umbrald : matriz con datos para dilation.\n
    mascara : lugar a aplicar metodo.\n
    r : radio variable.\n
    blank : matriz a aplicar mascara con contornos. The default is np.zeros((480,640),dtype='uint8').\n
    cir : matriz con ubicacion de circulos. The default is np.zeros((480,640,3),dtype='uint8').\n
    zeros : matriz ceros estatica. The default is np.zeros((480,640),dtype='uint8').\n
    \n
    Returns\n
    -------\n
    blank3c: matriz con contornos y mascara.\n
    circ: matriz con circulos de movimiento.\n
    cm: circulo medio.\n
    ci: circulo izquierdo.\n
    cd: circulo derecho.\n
    True --- False\n

    '''
    # Locales
    blank3c = blank.copy()
    contlistd = list()
    maski = np.zeros((480,640),dtype='uint8')
    maskd = np.zeros((480,640),dtype='uint8')
    circ = cir.copy()
    
    # Funcion
    if not (umbrald == zeros).all():
        dilation = cv.dilate(umbrald, None, iterations=1)
        try:
            masked = cv.bitwise_and(dilation, dilation, mask=mascara)
            
            # --- Eliminacion de contornos con area menor a r/5 --- #
            contornosd, hierarchyd = cv.findContours(masked,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
            
            for c in contornosd:
                if cv.contourArea(c) > (3.14 * r**2)/4:
                    contlistd.append(c)
            cv.drawContours(blank3c, contlistd,-1,255,-1)
            # --- Rectangulo mayor --- #
            recmax = cv.boundingRect(contlistd[0])
            for c in contlistd:
                recmax = union(recmax, cv.boundingRect(c))
            
            cv.rectangle(blank3c, (recmax[0],recmax[1]), (recmax[0]+recmax[2],recmax[1]+recmax[3]),(0,255,0),1)
            
            # --- Separación iz y der maskmethod--- #
            cv.rectangle(maski, (recmax[0],recmax[1]), (recmax[0] + int(recmax[2]/4),recmax[1]+recmax[3]),255,-1)
            maski = cv.bitwise_and(blank3c, blank3c, mask=maski)
            
            cv.rectangle(maskd, (recmax[0]+ int(recmax[2] * (3/4)),recmax[1]), (recmax[0] + recmax[2],recmax[1]+recmax[3]),255,-1)
            maskd = cv.bitwise_and(blank3c, blank3c, mask=maskd)
            
            # --- Punto mas alto de iz y der --- #
            contornosdi, hierarchydi = cv.findContours(maski,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
            reci = cv.boundingRect(contornosdi[0])
            for c in contornosdi:
                reci = union(reci, cv.boundingRect(c))
            contornosdd, hierarchydd = cv.findContours(maskd,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
            recd = cv.boundingRect(contornosdd[0])
            for c in contornosdd:
                recd = union(recd, cv.boundingRect(c))  
            # --- Creacion de circulos iz y der --- #
            ci = [(reci[0]+r,reci[1]+r), r]
            
            cd = [(recd[0]-r+recd[2],recd[1]+r), r]
            
            cv.circle(circ, ci[0], ci[1], (255,0,0), 1)
            cv.circle(circ, cd[0], cd[1], (0,0,255), 1)
            
            # --- Creacion de circulo medio --- #
            cm = [(int((ci[0][0]+ cd[0][0])/2),int((ci[0][1]+ cd[0][1])/2)), r]
            
            cv.circle(circ, cm[0], cm[1], (0,255,0), -1)
            # --- Paso de cordenadas posicionales de circulo y tiempo entre toma --- #
            return blank3c, circ, cm, ci, cd, True
        except:
            return False, False, False, False, False, False
    else: 
        return False, False, False, False, False, False
         

def imshows(*pantallas):
    '''
    Actualizar frames. \n
    \n
    Parameters\n
    ----------\n
    *pantallas : nombres de las variables a actualizar.\n
    \n
    Returns\n
    -------\n
    None.\n

    '''
    n= 0
    for pantalla in pantallas:
        cv.imshow(f'{n}', pantalla)
        n += 1

def division_up_down(obj,pixeles = 140):
    '''
    Division por secciones arriba y abajo\n
    \n
    Parameters\n
    ----------\n
    obj : matriz a modificar.\n
    pixeles : pixeles de punto de cambio. The default is 140.\n
    \n
    Returns\n
    -------\n
    up : matriz parte 1.\n
    down : matriz parte 2.\n

    '''
    
    blanku = np.zeros((480,640),dtype='uint8')
    cv.rectangle(blanku,(0,0),(640, pixeles),255,-1)
    up = cv.bitwise_and(obj, obj, mask=blanku)
    
    blankd = np.zeros((480,640),dtype='uint8')
    cv.rectangle(blankd, (0,pixeles), (640,480),255,-1)
    down = cv.bitwise_and(obj, obj, mask=blankd)
    
    return up, down


# inclinacion de objeto
def inclinacion(posicioni, posiciona):
    up, _ = division_up_down(posiciona)
    graya = cv.cvtColor(up, cv.COLOR_BGR2GRAY)
    dif = cv.absdiff(posicioni, graya)
    umbral = cv.threshold(dif, 10, 255, cv.THRESH_BINARY)[1]
    return umbral


def data(datav,*valor):
    loc = list()
    for val in valor:
        loc.append([val[0],val[1]])
    datav.append(loc)
    return datav

def profundidad(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blanco = cv.threshold(gray, 220, 255, cv.THRESH_BINARY)[1]
    try:
        contornos, hierarchy = cv.findContours(blanco,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        maxc = contornos[0]
        n = 0
        num = 0
        for c in contornos:
            if cv.contourArea(c) > cv.contourArea(maxc):
                maxc = c
                num = n
            n += 1
        x,y,h,w = cv.boundingRect(contornos[num])
        part = blanco[y+int(h / 15):y+w-int(h / 3.5), x+int(h / 5): x+h - int(h / 4)]
        inv = cv.bitwise_not(part)
        cv.imshow('a', inv)
        cont, h = cv.findContours(inv,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        area = cv.contourArea(cont[0])
        # necesito tomar los valores default de 5 cm a cuanto equivale a 30 cm
        # d2 = 30 * 5xp1/5xp2
        # 1cmpx = 5xp2/5cm
        # 
        return inv , True
    except:
        return frame, False

def inc(dif,cords,rad, r):
    # umbral
    # morph
    # menor a r/5 eliminar
    # unir
    # p1 = ((rad**2 - (y+w-cords[1])**2)**0.5, y+w-cords[1])
    # p2 = ((rad**2 - (x+h-cords[0])**2)**0.5, x+h-cords[0])
    # c = np.arctan([p1,p2])
    # medio = int(abs(c[0]-c[1])/2)    
    # arad = max(c[0],c[1]) + medio}
    # return arad
    pass
def graph(xa,ya):
    fig, ax = plt.subplots()
    ax.plot(xa, ya)
    return plt



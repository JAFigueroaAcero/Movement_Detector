# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 19:51:20 2021

@author: Juan Antonio
Title: main graficas

ver = 2.0
"""

import pandas as pd
import numpy as np
import cv2 as cv
import os
import functions_graph2 as graph2
import matplotlib.pyplot as plt
#variables

lista_global_ltd = list()
lista_global_lxmd = list()
lista_extras = list()
#Graficacion
x = str(input('Nombre de simulación: '))
h = int(input('histo pres:'))
directories = os.listdir('assets')
try:
    os.mkdir(f'assets_graphs\\{x}')
except:
    pass

for directory in directories:
    rute = f'assets_graphs\\{x}\\{directory}'
    try:
        os.mkdir(rute)
    except:
        pass
    data = pd.read_excel(f'assets\\{directory}\\Datos.xlsx')

    c = data.circulo_cords
    t = data.Tiempo
    r = data.regla_inc_a
    
    lx = list(c.map(lambda x: int(x[1: x.index(',')])))
    ly = list(c.map(lambda x: int(x[x.index(',')+1:len(x)-1])))
    
    lt = list(t.map(lambda x: x))
    
    lxc = list(r.map(lambda x: int(x[1: x.index(',')])))
    lyc = list(r.map(lambda x: int(x[x.index(',')+1:len(x)-1])))
    
    a,b,d,e = graph2.gd(lt,lx, ema_r = 1, ema_i = 5, popi = 2, name = 'lx', ref = rute)
    
    d1mb = graph2.dif(d)
    d1ma = graph2.dif(a)
    graph2.gd(list(range(len(d1mb))), d1mb, ema_r = 2, ema_i = 5, name = 'lxmd', ref=rute)
    graph2.gd(list(range(len(d1ma))), d1ma, ema_r = 1, ema_i = 5, name= 'ltd', ref= rute)


    rango, varianza, desviacion, cov, media, moda, mediana = graph2.md(d1mb)
    lista_loc = [['lxmd',d1mb],['rango',rango],['varianza',varianza],
                 ['desviacion_e', desviacion],['coeficiente_de_variacion',cov],
                 ['media', media],['moda',moda],['mediana',mediana]]
    graph2.excel(lista_loc, 'Data', rute)
    
    graph2.hist(d1mb, h, ruidomax=2, ruidomin=2, name='lxmdhist', ref =rute)
    
    extra = graph2.dif(b)
    
    extra = graph2.razon(extra)
    for el in extra:
        lista_extras.append(el)
    for el in d1mb:
        lista_global_lxmd.append(el)
    for el in d1ma:
        lista_global_ltd.append(el)
        
# Grabacion general AA

rango, varianza, desviacion, cov, media, moda, mediana = graph2.md(lista_global_lxmd,
                                                                   popd=len(directories)*4,
                                                                   popi=len(directories)*4)
lista_global_lxmd.sort()
graph2.pop(len(directories)*4, 1, lista_global_lxmd)
lista_global_f = [['lxmd',lista_global_lxmd],['ltmd', lista_extras],['rango',rango],['varianza',varianza],
                 ['desviacion_e', desviacion],['coeficiente_de_variacion',cov],
                 ['media', media],['moda',moda],['mediana',mediana]]

try:
    os.mkdir(f'assets_graphs\\{x}\\AA')
except:
    pass

graph2.hist(lista_global_lxmd, h,ruidomax = len(directories)*4,
            ruidomin = len(directories)*2*0,name ='lxmdhist',
            ref=f'assets_graphs\\{x}\\AA')

graph2.excel(lista_global_f, 'Data', f'assets_graphs\\{x}\\AA')

    
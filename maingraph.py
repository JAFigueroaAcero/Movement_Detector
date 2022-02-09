# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 20:58:58 2021

@author: Juan Antonio

Title: main graficas

ver = 1.0
"""
import pandas as pd
import numpy as np
import cv2 as cv
import os
import functions_graph2 as graph

data = pd.read_csv('AAgraphs\\assets\data.csv')

c = data.circulo_cords
t = data.Tiempo
r = data.regla_inc_a

lx = list(c.map(lambda x: int(x[1: x.index(',')])))
ly = list(c.map(lambda x: int(x[x.index(',')+1:len(x)-1])))

lt = list(t.map(lambda x: x))

lxc = list(r.map(lambda x: int(x[1: x.index(',')])))
lyc = list(r.map(lambda x: int(x[x.index(',')+1:len(x)-1])))


#bolaD
a,b,ma,mi = graph.gd(lt,lx, ema_r = 1, ema_i = 5, popi = 2, name = 'lx')
#graph.gd(lt,ly, ema_r = 2, ema_i = 5, popd = 2, popi = 2)

#penduloD
#graph.gd(lt,lxc, ema_r = 1, ema_i = 5, popi = 2)
#graph.gd(lt,lyc, ema_r = 2, ema_i = 5, popi = 2)

d1mb = graph.dif(b)
d1ma = graph.dif(a)

graph.gd(list(range(len(d1mb))), d1mb, ema_r = 2, ema_i = 5)
graph.gd(list(range(len(d1ma))), d1ma, ema_r = 1, ema_i = 5)





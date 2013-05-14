#!/usr/bin/python
from __future__ import print_function
import xlrd
import matplotlib.pyplot as plt
import time, sys
import numpy as np

wb = xlrd.open_workbook('angles_video1_2test.xls')
sheet = wb.sheet_names()[0]
sh = wb.sheet_by_name(sheet)
valores1 = []
valores2 = []
ys = []
#se lee el excel
for rownum in range(1, sh.nrows):
    valor1 = sh.row_values(rownum)[2]
    valor2 = sh.row_values(rownum)[1]
    y = sh.row_values(rownum)[0]
    valores1.append(valor1)
    valores2.append(valor2)
    ys.append(y)
#se grafica
fig = plt.figure()
ax = fig.add_subplot(111)
line, = ax.plot([], [], animated=True, lw=2)
ax.set_ylim(-1.1, 1.1)
ax.set_xlim(0, 5)
ax.grid()
xdata, ydata = [], []


def run(*args):
    background = fig.canvas.copy_from_bbox(ax.bbox)
    #para iniciar
    tstart = time.time()
    t = 0
    while 1:
        fig.canvas.restore_region(background)
        # actualizan los datos
        t +=.001
        y = valores2.pop(0)
        y = valores2.pop(0)
        print (t)  
        print (y)
        xdata.append(t)
        ydata.append(y)
        xmin, xmax = ax.get_xlim()
        if t>=xmax:
            ax.set_xlim(xmin, xmax*2)
            fig.canvas.draw()
            background = fig.canvas.copy_from_bbox(ax.bbox)

        line.set_data(xdata, ydata)

        # animaciones
        ax.draw_artist(line)
        # se redibuja
        fig.canvas.blit(ax.bbox)

        if len(valores2)<1:
            # se imprime el tiempo
            print('FPS:' , 1000/(time.time()-tstart))
            sys.exit()

        run.cnt += 1
run.cnt = 0
manager = plt.get_current_fig_manager()
manager.window.after(100, run)
plt.show()

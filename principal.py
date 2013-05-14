#/usr/bin/python
import cv
import sys
import numpy as np
from math import atan2, pi, sqrt
import os
import cv2
import math
import random
import xlrd
import time
import matplotlib.pyplot as plt


def calcula_distancia(pt1, pt2):
    """
    """
    distancia = float(((pt2[0]-pt1[0])**2 - (pt2[1]-pt1[1])**2)**.5) 
    return distancia

def encuentra_linas(frame, angulos):
    """
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),10000)
    cv2.imwrite('gray.png', blur)
    (thresh, im_bw) = cv2.threshold(blur, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(im_bw,(3,3),10000)
    for i in range(30):
        blur = cv2.GaussianBlur(blur,(3,3),1)
    cv2.imwrite('blur.png', blur)
    edges = cv2.Canny(blur, 200, 120)#80 120
    cv2.imwrite('edges.png', edges)
    lines = cv2.HoughLinesP(edges, 1, math.pi/360, 100, None, 200, 5000)
    punto = lines[0][0][1]
    linea = lines[0][0]
    for line in lines[0]:
        pt1 = (line[0],line[1])
        pt2 = (line[2],line[3])
        dis = calcula_distancia(pt1, pt2)
        if line[1]>punto and dis>400:
            punto = line[1]
            linea[0]=line[0]
            linea[1]=line[1]
            linea[2]=line[2]
            linea[3]=line[3]
    pt1 = (linea[0],linea[1])
    pt2 = (linea[2],linea[3])
    dis = calcula_distancia(pt1, pt2)
    r = int(random.random()*250)
    g = int(random.random()*250)
    b = int(random.random()*250)
    nuevo_color = (r,g,b)
    otro = (0,0,255)
    if dis > 400:
        cv2.line(frame, pt1, pt2, otro, 3)
        dx,dy = (linea[2]-linea[0]), (linea[3]-linea[1])
        rads = math.atan2(float(-dy),float(dx))
        angulos.append(rads-0.08)
    return frame, angulos

def procesamiento(cap):
    """
    """
    angulos = []
    tiempo = []
    while True:
        flag, frame = cap.read()
        if flag == 0:
            break
        inicio = time.time()
        frame, angulos = encuentra_linas(frame, angulos)
        tiempo.append(time.time()-inicio)
        cv2.imshow("Video", frame)
        key_pressed = cv2.waitKey(10)    #Escape to exit
        if key_pressed == 27:
            break
    return angulos, tiempo

def grafica(tiempo):
    l2 = plt.plot(tiempo, 'b', label='Tiempo')
    plt.legend(loc='upper left', numpoints = 1)
    plt.ylabel('tiempo')
    plt.xlabel('frame')
    plt.title("Vision vs MEMS")
    plt.show()
    

def lee_xls():
    wb = xlrd.open_workbook('angles_video2.xls')
    sheet = wb.sheet_names()[0]
    sh = wb.sheet_by_name(sheet)
    valores1 = []
    valores2 = []
    ys = []
    for rownum in range(1, sh.nrows):
        valor1 = sh.row_values(rownum)[2]
        valor2 = sh.row_values(rownum)[1]
        y = sh.row_values(rownum)[0]
        valores1.append(valor1)
        valores2.append(valor2)
        ys.append(y)
    return valores2


def main():
    """funcion principal
    """
    cap = cv2.VideoCapture("video_tras2.wmv")
    cv2.namedWindow("input")
    vision, tiempo = procesamiento(cap)
    vision = vision[:len(vision)-14]
    mems = lee_xls()
    print vision
    m = len(mems)
    v = len(vision)
    y = np.linspace(0, 9000, num=v)

    l1 = plt.plot(y, vision, 'r--', lw=3, label='VISION')
    l2 = plt.plot( mems, 'b', label='MEMS')
    plt.legend(loc='upper left', numpoints = 1)
    plt.ylabel('rad')
    plt.xlabel('tiempo')
    plt.title("Vision vs MEMS")
    plt.show()
    grafica(tiempo)
    print "El tiempo total transcurrido es de %s" %sum(tiempo)
main()

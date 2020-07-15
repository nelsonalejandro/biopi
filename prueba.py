#!/usr/bin/python
# -*- coding: utf-8 -*- 
# Software BioPi
# Autor: Nelson Alejandro Ramos Rivera
# Año: 2014
# Descripcion:
# Este modulo se encarga de identificar a los usuarios con el sensor biometrico

#Declaracion de librerias a utilizar
import serial
from clase_paquete_comando import *
from clase_paquete_respuesta import *
import os
import MySQLdb
import datetime
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
ejecucionscript = False
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=5, bytesize=8)
while (ejecucionscript != True):
    control = False
    while (control != True):
    	cp = Command_Packet('CmosLed')
        cp.ParameterFromInt(1)
        ser.write(cp.GetPacketBytes())
        cadena = ser.read(12)
        time.sleep(2)
    	cp = Command_Packet('CmosLed')
        cp.ParameterFromInt(0)
        ser.write(cp.GetPacketBytes())
        cadena = ser.read(12) 
	time.sleep(2)


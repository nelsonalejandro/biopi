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
#GPIO.setup(4, GPIO.OUT)
ejecucionscript = False
while (ejecucionscript != True):
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=5, bytesize=8)
    control = False
    while (control != True):
        ser.write(chr(0x55)) 
        ser.write(chr(0xaa)) 
        ser.write(chr(0x1)) 
        ser.write(chr(0x0))
        ser.write(chr(0x1)) 
        ser.write(chr(0x0))
        ser.write(chr(0x0))
        ser.write(chr(0x0))
        ser.write(chr(0x12))
        ser.write(chr(0x0))
        ser.write(chr(0x13)) 
        ser.write(chr(0x1))
        cadena = ser.read(12)  
        respuesta = hex(ord(cadena[10]))
        if respuesta == hex(0x30):
            control = True
        else:
            control = False
    control = False
    while (control != True):
        cp = Command_Packet('IsPressFinger')
        cp.ParameterFromInt(0)
        ser.write(cp.GetPacketBytes())
        cadena = ser.read(12)
        respuesta = hex(ord(cadena[10]))
        if respuesta == hex(0x30):
            control = True
        else:
            control = False
    control = False
    while (control != True):
        cp = Command_Packet('CaptureFinger')
        cp.ParameterFromInt(1)
        ser.write(cp.GetPacketBytes())
        cadena = ser.read(12)
        cp = Command_Packet('Identify1_N')
        cp.ParameterFromInt(0)
        ser.write(cp.GetPacketBytes())
        cadena = ser.read(12)
        identificacionid = int(hex(ord(cadena[4])), 0)
        respuesta = hex(ord(cadena[8]))
        if respuesta == hex(0x30):
            while (control != True):
        	ser.write(chr(0x55))  
        	ser.write(chr(0xaa)) 
        	ser.write(chr(0x1)) 
        	ser.write(chr(0x0))
        	ser.write(chr(0x0))  
        	ser.write(chr(0x0))
        	ser.write(chr(0x0))
        	ser.write(chr(0x0))
        	ser.write(chr(0x12))
        	ser.write(chr(0x0))
        	ser.write(chr(0x12)) 
        	ser.write(chr(0x1))
        	cadena = ser.read(12)  
        	respuesta = hex(ord(cadena[10]))
        	if respuesta == hex(0x30):
            	    control = True
            	else:
            	    control = False
            control = False
            bd = MySQLdb.connect("localhost","root","raspberry","BioPi" )
            cursor = bd.cursor()
            sql = "SELECT * FROM Usuario Where IDUSUARIO = "+str(identificacionid)
            cursor.execute(sql)
            registro = cursor.fetchone()
            idusuario = registro[0]
            nombreusuario = registro[1]
            apellidousuario = registro[2]
            estadousuario = registro[3]
            numerousuario = registro[4].replace('+','')
            print numerousuario
            if estadousuario == "Activo":
                bd = MySQLdb.connect("localhost","root","raspberry","BioPi")
                cursor = bd.cursor()
                x = datetime.datetime.now()
                sql = "INSERT INTO Registros (IDREGISTRO, Usuario_IDUSUARIO, Fecha) VALUES (NULL,'"+ str(idusuario) +"','"+ x.isoformat()+"')"
                cursor.execute(sql)
                bd.commit()
                bd.rollback()
                bd.close()
                os.system ('espeak -ves+f4 -a 200 "se a enviado el aviso de llegada '+nombreusuario+'"')
                os.system ('yowsup-cli demos -c /config.example -s '+numerousuario+' "El Alumno '+nombreusuario+' '+apellidousuario+' a llegado, Saludos coordiales desde la Escuela Brilla el Sol" ')
            else:
                print ("INTENTE NUEVAMENTE")
            control = True
        else:
            control = False
    control = False

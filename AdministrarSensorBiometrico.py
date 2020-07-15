#!/usr/bin/python
# -*- coding: utf-8 -*- 
# Software BioPi
# Autor: Nelson Alejandro Ramos Rivera
# Año: 2014
# Descripcion:
# Este modulo se encarga de implementar las distintas funciones para interactuar con el sensor biometrico

#Declaracion de librerias a utilizar
import serial
from clase_paquete_comando import *
from clase_paquete_respuesta import *
import os

# Funcion que devuelve el numero de registros que se encuentran en el sensor
def numeroderegistro():
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1, bytesize=8)
    os.system('clear')
    print "".center(80,"#")
    print "Sistema de control Biometrico".center(80, "#")
    cp = Command_Packet('GetEnrollCount')
    ser.write(cp.GetPacketBytes())
    cadena = ser.read(12)
    numerocuentas = int(hex(ord(cadena[4])),0)
    respuesta = hex(ord(cadena[8]))
    if respuesta == hex(0x30):
        print "El numero de cuentas enroladas es: "+ str(numerocuentas)
    else:
        print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" La respuesta del sensor es incorrecta, intente nuevamente."
    raw_input("\n Presione Enter para salir")
    ser.close()
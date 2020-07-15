#!/usr/bin/python
# -*- coding: utf-8 -*- 
# Software BioPi
# Autor: Nelson Alejandro Ramos Rivera
# Ano: 2014
# Descripcion:
# Este modulo es se encarga de llamar las funciones de los diferentes modulos del sistema

#Declaracion de librerias a utilizar
import os
from Modulo_de_Enrolamiento import *
from AdministrarSensorBiometrico import *

#Menu principal del sistema
def menu():
    op = 0
    while (op!=5):
        os.system('clear')
        print "".center(80,"#")
        print "Sistema de control Biometrico".center(80, "#")
        print "Menu Principal"
        print "1. Enrolar Usuarios"
        print "2. Consultar numero de registros"
        print "3. Modificar usuario"
        print "4. Identificar usuario"
        print "5. Salir"
        try:
            op = int (raw_input("Ingrese una Opcion:"))
            if (op==1):
                procesoenrolar()
            if (op == 2):
                numeroderegistro()
            if (op == 3):
                modificarusuario()
            if (op == 4):
                identificarusuario()
        except ValueError:
            print "Ingrese una opcion valida (Solo Numeros)"    
try:
    menu()
except:
    print ""

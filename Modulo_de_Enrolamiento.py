#!/usr/bin/python
# -*- coding: utf-8 -*- 
# Software BioPi
# Autor: Nelson Alejandro Ramos Rivera
# Año: 2014
# Descripcion:
# Este modulo se encarga de implementar las distintas funciones para manejar a los usuarios

#Declaracion de librerias a utilizar
import serial
from clase_paquete_comando import *
from clase_paquete_respuesta import *
import os
import MySQLdb
import time
import re
import smtplib

#Funcion la cual enrola a un usuario, dejando un registro en la Base de datos y en el sensor
def procesoenrolar():
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=5, bytesize=8)
    os.system('clear')
    print "".center(80,"#")
    print "Sistema de control Biometrico".center(80, "#")
    print "\nIniciando proceso de Enrolamiento\n"
    control = False
    nombre = ""
    apellido = ""
    Mail = ""
    controlMail = False
    while (control != True):
            nombre =  raw_input("Nombre: ")
            control = nombre.isalpha()
            if control is False:
                    print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" El nombre solo puede contener letras."
    control = False
    while (control != True):
            apellido =  raw_input("Apellido: ")
            control = apellido.isalpha()
            if control is False:
                    print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" El apellido solo puede contener letras."
    control = False
    while (control != True):
            numero =  raw_input("Numero: ")
            control = numero.isdigit()
            if control is False:
                    print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" El numero de contacto solo puede contener numeros. "
    control = False
    while (control != True):
            admin =  raw_input("¿Este Usuario es Administrador? (s=si|n=no): ")
            control = admin.isalpha()
            if control is False:
                    print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" Solo Ingrese > (s=si|n=no) sin numeros ni espacios."
            else:
                if admin is "s" or admin is "n":
                     if admin is "n":
                        controlMail = True
                else:
                    print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" Solo Ingrese > (s=si|n=no)"
                    control = False
    while (controlMail != True):
            Mail =  raw_input("Mail: ")
            if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$',Mail.lower()):
                    controlMail = True
            else:
                    print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" El correo es incorrecto"
                    controlMail = False                                
    print chr(27)+"[0;34m"+"[CORRECTO]>"+chr(27)+"[0m"+" Preparando el sensor"
    control = False
    controlprocesoenrolar = False
    while (controlprocesoenrolar != True):
        try:
            while (control != True):
                ser.write(chr(0x55))  
                ser.write(chr(0xaa))  
                ser.write(chr(0x1))  
                ser.write(chr(0x0))
                ser.write(chr(0x0))  
                ser.write(chr(0x0))
                ser.write(chr(0x0))
                ser.write(chr(0x0))
                ser.write(chr(0x1))
                ser.write(chr(0x0))
                ser.write(chr(0x1)) 
                ser.write(chr(0x1))
                cadena = ser.read(12) 
                respuesta = hex(ord(cadena[10]))
                if respuesta == hex(0x30):
                    control = True
                else:
                    control = False
        except ValueError:
                print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se puede conectar con el sensor."
                raw_input("\n Presione Enter para salir")
        control = False
        try:
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
        except ValueError:
                print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se puede Prender Led."
                raw_input("\n Presione Enter para salir")
        control = False
        idparametro= 1
        try:
            while (control != True):
                cp = Command_Packet('CheckEnrolled')
                cp.ParameterFromInt(idparametro)
                ser.write(cp.GetPacketBytes())
                cadena = ser.read(12) 
                respuesta = hex(ord(cadena[8]))
                if respuesta == hex(0x30):
                    control = False
                    idparametro =idparametro + 1
                else:
                    bd = MySQLdb.connect("localhost","root","raspberry","BioPi" )
                    cursor = bd.cursor()
                    sql = "SELECT * FROM Usuario Where IDUSUARIO = "+str(idparametro)
                    cursor.execute(sql)
                    resultados = cursor.fetchone()
                    if resultados == None:
                        control = True
                    else:
                        control = False
                        idparametro =idparametro + 1
        except ValueError:
                print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se puede interactuar con la base de datos del sensor."
                raw_input("\n Presione Enter para salir")
        print ("1/3 Presione el sensor.")
        control = False
        try:
            while (control != True):
                cp = Command_Packet('EnrollStart')
                cp.ParameterFromInt(idparametro)
                ser.write(cp.GetPacketBytes())
                cadena = ser.read(12) 
                respuesta = hex(ord(cadena[8]))
                if respuesta == hex(0x30):
                    control = True
                else:
                    control = False
        except ValueError:
                print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se puede iniciar el enrolamiento."
                raw_input("\n Presione Enter para salir")

        control = False
        try:
           while (control != True):
                cp = Command_Packet('CaptureFinger')
                cp.ParameterFromInt(idparametro)
                ser.write(cp.GetPacketBytes())
                cadena = ser.read(12) 
                respuesta = hex(ord(cadena[8]))
                if respuesta == hex(0x30):
                    control = True
                else:
                    control = False
        except ValueError:
                print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se capturar el dedo."
                raw_input("\n Presione Enter para salir")
        control = False
        try:
            while (control != True):
                cp = Command_Packet('Enroll1')
                cp.ParameterFromInt(idparametro)
                ser.write(cp.GetPacketBytes())
                cadena = ser.read(12)  
                respuesta = hex(ord(cadena[8]))
                if respuesta == hex(0x30):
                    control = True
                else:
                    control = False
        except ValueError:
                print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se puede guardar los datos."
                raw_input("\n Presione Enter para salir")
        print ("Retire el dedo del Sensor")
        control = False
        while (control != True):
            cp = Command_Packet('IsPressFinger')
            cp.ParameterFromInt(idparametro)
            ser.write(cp.GetPacketBytes())
            cadena = ser.read(12) 
            respuesta = hex(ord(cadena[8]))
            if respuesta == hex(0x30):
                control = True
            else:
                control = False
            respuesta = hex(ord(cadena[4]))
            respuesta2= hex(ord(cadena[5]))
            respuesta3= hex(ord(cadena[6]))
            respuesta4= hex(ord(cadena[7]))
            if respuesta == hex(0x0) and respuesta2 == hex(0x0) and respuesta3 == hex(0x0) and respuesta4 == hex(0x0):
                control = False                  
            else:
                control = True
        print ("2/3 Presione Nuevamente el sensor.")
        control = False
        try:
            while (control != True):
                cp = Command_Packet('CaptureFinger')
                cp.ParameterFromInt(idparametro)
                ser.write(cp.GetPacketBytes())
                cadena = ser.read(12) 
                respuesta = hex(ord(cadena[8]))
                if respuesta == hex(0x30):
                    control = True
                else:
                    control = False
        except ValueError:
                print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se puede continuar con el procedimiento."
                raw_input("\n Presione Enter para salir")
        control = False
        try:
            while (control != True):
                cp = Command_Packet('Enroll2')
                cp.ParameterFromInt(idparametro)
                ser.write(cp.GetPacketBytes())
                cadena = ser.read(12)  
                respuesta = hex(ord(cadena[8]))
                if respuesta == hex(0x30):
                    control = True
                else:
                    control = False
        except ValueError:
                print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se puede continuar con el procedimiento."
                raw_input("\n Presione Enter para salir")
        print ("Retire el dedo del Sensor")
        control = False
        try:
            while (control != True):
                cp = Command_Packet('IsPressFinger')
                cp.ParameterFromInt(idparametro)
                ser.write(cp.GetPacketBytes())
                cadena = ser.read(12)  
                respuesta = hex(ord(cadena[8]))
                if respuesta == hex(0x30):
                    control = True
                else:
                    control = False
                respuesta = hex(ord(cadena[4]))
                respuesta2= hex(ord(cadena[5]))
                respuesta3= hex(ord(cadena[6]))
                respuesta4= hex(ord(cadena[7]))
                if respuesta == hex(0x0) and respuesta2 == hex(0x0) and respuesta3 == hex(0x0) and respuesta4 == hex(0x0):
                    control = False                  
                else:
                    control = True
            time.sleep(5)
        except ValueError:
                print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se puede continuar con el procedimiento."
                raw_input("\n Presione Enter para salir")
        time.sleep(3)
        print ("3/3 Presione el sensor nuevamente")
        control = False
        try:
            while (control != True):
                cp = Command_Packet('CaptureFinger')
                cp.ParameterFromInt(idparametro)
                ser.write(cp.GetPacketBytes())
                cadena = ser.read(12)  
                respuesta = hex(ord(cadena[8]))
                if respuesta == hex(0x30):
                    control = True
                else:
                    control = False
        except ValueError:
                print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se puede continuar con el procedimiento."
                raw_input("\n Presione Enter para salir")
        print ("Enroll3")
        control = False
        try:
            while (control != True):
                cp = Command_Packet('Enroll3')
                cp.ParameterFromInt(idparametro)
                ser.write(cp.GetPacketBytes())
                cadena = ser.read(12)  
                respuesta = hex(ord(cadena[8]))
                if respuesta == hex(0x30):
                    control = True
                    controlprocesoenrolar = True
                else:
                    control = True
                    print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se a podido comprobar correctamente el proceso de enrolamiento."
                    raw_input("\n Presione Enter para reiniciar proceso")
                    controlprocesoenrolar = False
        except ValueError:
                print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se puede continuar con el procedimiento."
                raw_input("\n Presione Enter para salir")
                
    print ("Retire su dedo")
    control = False
    try:
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
    except ValueError:
            print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se puede apagar led del sensor."
            raw_input("\n Presione Enter para salir")
    bd = MySQLdb.connect("localhost","root","raspberry","BioPi")
    cursor = bd.cursor()
    sql = "INSERT INTO Usuario (IDUSUARIO, Nombre, Apellido, Estado, numero) VALUES ("+ str(idparametro)+", '"+ nombre.capitalize() + "', '"+ apellido.capitalize() +"', 'Activo','"+ numero +"')"
    try:
       cursor.execute(sql)

       bd.commit()
    except:
       bd.rollback()
       print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se puede insertar en la base de datos."
    bd.close()
    if(len(Mail)==0):
        print""
    else:
        bd = MySQLdb.connect("localhost","root","raspberry","BioPi")
        cursor = bd.cursor()
        sql = "INSERT INTO Administrador (IDUSUARIO, Mail) VALUES ("+ str(idparametro)+", '"+Mail +"')"
        try:
           cursor.execute(sql)
           bd.commit()
        except:
           bd.rollback()
           print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No se puede insertar en la base de datos."
        bd.close() 
    bd = MySQLdb.connect("localhost","root","raspberry","BioPi" )
    cursor = bd.cursor()
    sql = "SELECT Mail FROM Administrador"
    cursor.execute(sql)
    to = cursor.fetchall()
    gmail_user = 'correobiopi@gmail.com'
    gmail_pwd = 'raspberrypiinforma'
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' +"" + '\n' + 'From:' + gmail_user + '\n' + 'Subject: "Ingreso de Usuario"\n'
    msg = header + '\n BioPi Informa sus administradores que se ha ingresado el siguiente Usuario: \n\n'+ '\n Nombre:'+nombre.capitalize()+ '\n Apellido:'+apellido.capitalize()+'\n\n Les recordamos que este usuario podra hacer ingreso al Taller de Hardware '+'\n Saludos. '
    smtpserver.sendmail(gmail_user, to, msg)
    smtpserver.close()
    ser.close()    
    raw_input("\n Presione Enter para regresar")
    
#Funcion encargada de dar de baja o alta a un usuario en el sistema    
def modificarusuario():
    bd = MySQLdb.connect("localhost","root","raspberry","BioPi" )
    cursor = bd.cursor()
    ROL = ""
    control = False
    while (control != True):
        nombre =  raw_input("Nombre: ")
        control = nombre.isalpha()
        if control is False:
            print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" Ingrese un nombre valido"
        else:
            control = False
            while (control != True):
                apellido =  raw_input("Apellido: ")
                control = apellido.isalpha()
                if control is False:
                        print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" El apellido solo puede contener letras" 
                else:
                    control = False
                    while (control != True):
                        Estado =  raw_input("Estado: ")
                        control = Estado.isalpha()
                        if control is False:
                                print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" El estado solo puede ser Activo o Inactivo"
                        else:
                            sql = "SELECT * FROM Usuario Where Nombre = '"+nombre.capitalize()+"'"
                            cursor.execute(sql)
                            resultados = cursor.fetchone()
                            if resultados == None:
                                control = False
                                print chr(27)+"[0;31m"+"[ERROR]>"+chr(27)+"[0m"+" No hay registros con este nombre"
                            else:
                                sql = 'UPDATE Usuario SET Estado="'+Estado.capitalize()+'" WHERE Nombre="'+nombre.capitalize()+'" and Apellido="'+apellido.capitalize()+'"'
                                try:
                                    cursor.execute(sql)
                                    bd.commit()
                                except:
                                    bd.rollback()
                                bd.close()
                                raw_input("\n Se a completado el proceso con exito, Presione Enter para regresar")

#Esta Funcion se encarga de verificar que el usuario exista en el sistema                        
def identificarusuario():
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=5, bytesize=8)
    os.system('clear')
    print "".center(80,"#")
    print "Sistema de control Biometrico".center(80, "#")
    print "\nIniciando proceso de identificacion\n"
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
    print "\nPresione el Sensor\n"
    control = False
    while (control != True):
        ser.write(chr(0x55))  
        ser.write(chr(0xaa)) 
        ser.write(chr(0x1))  
        ser.write(chr(0x0))
        ser.write(chr(0x0))  
        ser.write(chr(0x0))
        ser.write(chr(0x0))
        ser.write(chr(0x0))
        ser.write(chr(0x51))
        ser.write(chr(0x0))
        ser.write(chr(0x51)) 
        ser.write(chr(0x1))
        cadena = ser.read(12)  
        identificacionid = int(hex(ord(cadena[4])), 0)
        respuesta = hex(ord(cadena[8]))
        if respuesta == hex(0x30):
            print ("Usuario correcto")
            bd = MySQLdb.connect("localhost","root","raspberry","BioPi" )
            cursor = bd.cursor()
            sql = "SELECT * FROM Usuario Where IDUSUARIO = "+str(identificacionid)
            cursor.execute(sql)
            registro = cursor.fetchone()
            idusuario = registro[0]
            nombreusuario = registro[1]
            apellidousuario = registro[2]
            rolusuario = registro[3]
            estadousuario = registro[4]
            os.system('./textoavoz.sh Bienvenido, ' + nombreusuario)
            control = True
        else:
            control = False
    control = False
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
    ser.close()    
    raw_input("\n Presione Enter para salir")

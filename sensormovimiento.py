#!/usr/bin/python
# -*- coding: utf-8 -*- 
# Software BioPi
# Autor: Nelson Alejandro Ramos Rivera
# Año: 2014
# Descripcion:
# Modulo encargado de abrir y cerrar el rele a travez del sensor de movimiento

#Declaracion de librerias a utilizar
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.OUT)
while True:
	if(GPIO.input(23) ==1):
		print 'abriendo'
		GPIO.output(17,GPIO.HIGH) 
		time.sleep(4)
	if(GPIO.input(23) == 0):
		print 'cerrando'
		GPIO.output(17, GPIO.LOW)
GPIO.cleanup()



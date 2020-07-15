#!/usr/bin/python
# -*- coding: utf-8 -*- 
# Software BioPi
# Autor: Nelson Alejandro Ramos Rivera
# Año: 2014
# Descripcion:
# clase encargada de generar los paquetes genericos sin contenido

#Declaracion de librerias a utilizar
import binascii

#clase
class Packet:
    '''
        clase generica de paquetes
    '''
    COMMAND_START_CODE_1 = 0x55;    # Static byte to mark the beginning of a command packet    -    never changes
    COMMAND_START_CODE_2 = 0xAA;    # Static byte to mark the beginning of a command packet    -    never changes
    COMMAND_DEVICE_ID_1  = 0x01;    # Device ID Byte 1 (lesser byte)                            -    theoretically never changes
    COMMAND_DEVICE_ID_2  = 0x00;    # Device ID Byte 2 (greater byte)                            -    theoretically never changes
    
    def GetHighByte(self, w):
        '''
        Returns the high byte from a word
        '''
        return (w>>8)&0x00FF
    
    def GetLowByte(self, w):
        '''
        Returns the low byte from a word        
        '''
        return w&0x00FF
    
    def CalculateCheckSum(self,bytearr):
        return sum(map(ord,bytes(bytearr)))
    
    def serializeToSend(self,bytearr):
        return ' '.join(binascii.hexlify(ch) for ch in bytes(bytearr))
#!/usr/bin/python
# -*- coding: utf-8 -*- 
# Software BioPi
# Autor: Nelson Alejandro Ramos Rivera
# Año: 2014
# Descripcion:
# clase encargada de leer las respuestas del sensor biometrico

#Declaracion de librerias a utilizar
from clase_paquete_generico import *

#clase
class Response_Packet(Packet):
    '''
        clase para los paquetes de respuestas
    '''
    
    errors = {
                    'NO_ERROR'                      : 0x0000,    
                    'NACK_TIMEOUT'                  : 0x1001,    
                    'NACK_INVALID_BAUDRATE'         : 0x1002,    
                    'NACK_INVALID_POS'              : 0x1003,    
                    'NACK_IS_NOT_USED'              : 0x1004,    
                    'NACK_IS_ALREADY_USED'          : 0x1005,    
                    'NACK_COMM_ERR'                 : 0x1006,    
                    'NACK_VERIFY_FAILED'            : 0x1007,   
                    'NACK_IDENTIFY_FAILED'          : 0x1008,    
                    'NACK_DB_IS_FULL'               : 0x1009,    
                    'NACK_DB_IS_EMPTY'              : 0x100A,    
                    'NACK_BAD_FINGER'               : 0x100C,    
                    'NACK_ENROLL_FAILED'            : 0x100D,    
                    'NACK_IS_NOT_SUPPORTED'         : 0x100E,    
                    'NACK_DEV_ERR'                  : 0x100F,    
                    'NACK_CAPTURE_CANCELED'         : 0x1010,    
                    'NACK_INVALID_PARAM'            : 0x1011,    
                    'NACK_FINGER_IS_NOT_PRESSED'    : 0x1012,    
                    'INVALID'                       : 0XFFFF          
              }
    
    def __init__(self,_buffer=None,UseSerialDebug=False):
        '''
        crea e interpreta las respuestas del sensor
        '''
        self.UseSerialDebug= UseSerialDebug
        
        if not (_buffer is None ):
            self.RawBytes = _buffer
            self._lastBuffer = bytes(_buffer)
            if self.UseSerialDebug:
                print 'readed: %s'% self.serializeToSend(_buffer)
            if _buffer.__len__()>=12:
                self.ACK = True if _buffer[8] == 0x30 else False
                self.ParameterBytes[0] = _buffer[4]
                self.ParameterBytes[1] = _buffer[5]
                self.ParameterBytes[2] = _buffer[6]
                self.ParameterBytes[3] = _buffer[7]
                self.ResponseBytes[0]  = _buffer[8]
                self.ResponseBytes[1]  = _buffer[9]
                self.Error = self.ParseFromBytes(self.GetHighByte(_buffer[5]),self.GetLowByte(_buffer[4]))
        
    _lastBuffer = bytes()
    RawBytes = bytearray(12)
    ParameterBytes=bytearray(4)
    ResponseBytes=bytearray(2)
    ACK = False
    Error = None
    UseSerialDebug = True
    
    
    def ParseFromBytes(self,high,low):
        '''
        '''
        e  = 'INVALID'
        if high == 0x01:
            if low in self.errors.values():
                errorIndex = self.errors.values().index(low)
                e = self.errors.keys()[errorIndex]
        return e
    
    
    def IntFromParameter(self):
        retval = 0;
        retval = (retval << 8) + self.ParameterBytes[3];
        retval = (retval << 8) + self.ParameterBytes[2];
        retval = (retval << 8) + self.ParameterBytes[1];
        retval = (retval << 8) + self.ParameterBytes[0];
        return retval;


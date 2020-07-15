#!/usr/bin/python
# -*- coding: utf-8 -*- 
# Software BioPi
# Autor: Nelson Alejandro Ramos Rivera
# Año: 2014
# Descripcion:
# clase encargada de generar los paquetes de comando

#Declaracion de librerias a utilizar
from clase_paquete_generico import *

#clase
class Command_Packet(Packet):
    '''
        Clase encargada de generar los paquetes de comandos
    '''
    
    command = bytearray(2)
    cmd = ''
    commands = {
                    'NotSet'                  : 0x00,        
                    'Open'                    : 0x01,        
                    'Close'                   : 0x02,       
                    'UsbInternalCheck'        : 0x03,        
                    'ChangeBaudrate'          : 0x04,        
                    'SetIAPMode'              : 0x05,        
                    'CmosLed'                 : 0x12,        
                    'GetEnrollCount'          : 0x20,        
                    'CheckEnrolled'           : 0x21,        
                    'EnrollStart'             : 0x22,        
                    'Enroll1'                 : 0x23,        
                    'Enroll2'                 : 0x24,        
                    'Enroll3'                 : 0x25,        
                    'IsPressFinger'           : 0x26,        
                    'DeleteID'                : 0x40,        
                    'DeleteAll'               : 0x41,        
                    'Verify1_1'               : 0x50,        
                    'Identify1_N'             : 0x51,        
                    'VerifyTemplate1_1'       : 0x52,        
                    'IdentifyTemplate1_N'     : 0x53,        
                    'CaptureFinger'           : 0x60,        
                    'MakeTemplate'            : 0x61,       
                    'GetImage'                : 0x62,        
                    'GetRawImage'             : 0x63,        
                    'GetTemplate'             : 0x70,       
                    'SetTemplate'             : 0x71,        
                    'GetDatabaseStart'        : 0x72,        
                    'GetDatabaseEnd'          : 0x73,        
                    'UpgradeFirmware'         : 0x80,        
                    'UpgradeISOCDImage'       : 0x81,        
                    'Ack'                     : 0x30,        
                    'Nack'                    : 0x31         
                }
    

    def __init__(self,*args,**kwargs):
        '''
            Constructor
        '''
        commandName=args[0]
        kwargs.setdefault('UseSerialDebug', True)
        self.UseSerialDebug= kwargs['UseSerialDebug']
        self.cmd = self.commands[commandName]
        
    UseSerialDebug = True
    Parameter = bytearray(4)
    
    
    
    def GetPacketBytes(self):
        '''
        retorna 12 bytes del paquete generado
        '''
        
        self.command[0] = self.GetLowByte(self.cmd)
        self.command[1] = self.GetHighByte(self.cmd)
        
        packetbytes= bytearray(12)
        packetbytes[0] = self.COMMAND_START_CODE_1
        packetbytes[1] = self.COMMAND_START_CODE_2
        packetbytes[2] = self.COMMAND_DEVICE_ID_1
        packetbytes[3] = self.COMMAND_DEVICE_ID_2
        packetbytes[4] = self.Parameter[0]
        packetbytes[5] = self.Parameter[1]
        packetbytes[6] = self.Parameter[2]
        packetbytes[7] = self.Parameter[3]
        packetbytes[8] = self.command[0]
        packetbytes[9] = self.command[1]
        chksum = self.CalculateCheckSum(packetbytes[0:9])
        packetbytes[10] = self.GetLowByte(chksum)
        packetbytes[11] = self.GetHighByte(chksum)

        return packetbytes;        
    
    def ParameterFromInt(self, i):
        '''
        Convierte en int a bytes 
        '''
        
        self.Parameter[0] = (i & 0x000000ff);
        self.Parameter[1] = (i & 0x0000ff00) >> 8;
        self.Parameter[2] = (i & 0x00ff0000) >> 16;
        self.Parameter[3] = (i & 0xff000000) >> 24;

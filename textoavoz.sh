#!/bin/bash
# Software BioPi
# Autor: Nelson Alejandro Ramos Rivera
# Año: 2014
# Descripcion:
# Script encargado de traducir de texto a voz el parametro indicado

#Declaracion de librerias a utilizar
say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?tl=es&q=$*"; }
say $*

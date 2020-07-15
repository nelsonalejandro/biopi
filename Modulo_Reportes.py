#!/usr/bin/python
# -*- coding: utf-8 -*- 
# Software BioPi
# Autor: Nelson Alejandro Ramos Rivera
# Año: 2014
# Descripcion:
# clase encargada de generar los reportes y enviarlos a los Administradores

#Declaracion de librerias a utilizar
import locale
import time
import MySQLdb
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from smtplib import SMTP
from email.MIMEBase import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

locale.setlocale(locale.LC_TIME, 'es_CL.utf8')
doc = SimpleDocTemplate("Reporte_"+time.strftime("%B")+".pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
Story=[]
logo = "Raspberrypi_logo.png"
logoesc= "logoescuelainformatica.jpg"
magName = "BioPi"
issueNum = 12
subPrice = "99.00"
limitedDate = "03/05/2010"
freeGift = "tin foil hat"
showBoundary=1
formatted_time = time.strftime("%a, %d %b %Y %H:%M:%S") 
full_name = "BioPi"
address_parts = ["Santo tomas,", "Talca", "Escuela de Informatica"]
im = Image(logo,  width=100, height=121)
Story.append(im)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
ptext = '<font size=12>%s</font>' % formatted_time
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))
ptext = '<font size=12>%s</font>' % full_name
Story.append(Paragraph(ptext, styles["Normal"]))       
for part in address_parts:
    ptext = '<font size=12>%s</font>' % part.strip()
    Story.append(Paragraph(ptext, styles["Normal"]))   
Story.append(Spacer(1, 12))
mesreporte= time.strftime("%Y-%m")
Story.append(Spacer(1, 12))
bd = MySQLdb.connect("localhost","root","raspberry","BioPi" )
cursor = bd.cursor()
sql = "select idregistro, nombre, apellido, fecha from Usuario a, Registros b where a.IDUSUARIO= b.Usuario_IDUSUARIO and date_format(Fecha, '%Y-%m') ='"+ mesreporte+"' ORDER BY  b.IDREGISTRO ASC"
cursor.execute(sql)
resultados = cursor.fetchall()
mespalabras= time.strftime("%B")
ptext = '<font size=12> A continuacion se muestra los ingresos ocurridos durante el mes de '+ mespalabras.capitalize()
Story.append(Paragraph(ptext, styles["Justify"]))
Story.append(Spacer(1, 12))
t=Table(resultados)
Story.append(t)
Story.append(Spacer(1, 12))
ptext = '<font size=12>Gracias por utilizar BioPi.</font>'
Story.append(Paragraph(ptext, styles["Justify"]))
Story.append(Spacer(1, 12))
ptext = '<font size=12>Adios</font>'
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))
im = Image(logoesc,  width=150, height=77)
Story.append(im)
doc.build(Story)
locale.setlocale(locale.LC_TIME, 'es_CL.utf8')
mes= time.strftime("%B") 
msg = MIMEMultipart()
msg['Subject'] = 'Reporte BioPi '+mes
msg['From'] = 'nelsonalejandroramosrivera@gmail.com'
msg['Reply-to'] = 'nelsonalejandroramosrivera@gmail.com'
bd = MySQLdb.connect("localhost","root","raspberry","BioPi" )
cursor = bd.cursor()
sql = "SELECT Mail FROM Administrador"
cursor.execute(sql)
to = cursor.fetchall()
msg.preamble = 'Multipart massage.\n'
part = MIMEText("Se adjunta el reporte mensual del sisema BioPi")
msg.attach(part)
part = MIMEApplication(open("Reporte_"+str(mes)+".pdf","rb").read())
part.add_header('Content-Disposition', 'attachment', filename="Reporte_"+str(mes)+".pdf")
msg.attach(part)
smtp = SMTP("smtp.gmail.com", 587)
smtp.ehlo()
smtp.starttls()
smtp.ehlo
smtp.login("correobiopi@gmail.com", "raspberrypiinforma")
smtp.sendmail(msg['From'], to, msg.as_string())
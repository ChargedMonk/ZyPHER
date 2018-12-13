import RPi.GPIO as GPIO
import time
import smtplib
import os
import subprocess
import shlex
import picamera
import datetime as dt

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

camera = picamera.PiCamera()


def sendvid():
    
    now=dt.datetime.now()

    camera.vflip=True
    #camera.start_preview()
    time.sleep(2)
    camera.capture('example.jpg')
    #camera.stop_preview()
    time.sleep(2)
    camera.start_recording('examplevid.h264')
    time.sleep(5)
    camera.stop_recording()

    
    fromaddr = '4thotdestroyers@gmail.com'
    toaddr = '*****@gmail.com,********@gmail.com'
    alladdr = toaddr.split(',')
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'INTRUDER ALERT!!!'
    body = 'Latest Image of the room\n\nUploading Video Soon'
    msg.attach(MIMEText(body, 'plain'))

    filename = now.strftime("%d-%m-%Y %H:%M:%S") + '.jpg'
    attachment = open('/example.jpg', 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, 'iitjammu')
    text = msg.as_string()
    server.sendmail(fromaddr, alladdr, text)
    server.quit()

    os.system('rm ' + '/example.jpg')

    filename='examplevid'

    command = shlex.split('MP4Box -add {f}.h264 {f}.mp4'.format(f=filename))
    output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    #print(output)

 
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'Surveillance Video'
    body = 'Latest video feed'
    msg.attach(MIMEText(body, 'plain'))

    filename = now.strftime("%d-%m-%Y %H:%M:%S") + '.mp4'
    attachment = open('/examplevid.mp4', 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, 'iitjammu')
    text = msg.as_string()
    server.sendmail(fromaddr, alladdr, text)
    server.quit()

    os.system('rm ' + '/examplevid.h264')
    os.system('rm ' + '/examplevid.mp4')

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.IN) 
 
try:
    while True:
      if GPIO.input(21): 
         print('Motion Detected')
         sendvid()
         time.sleep(600)  
except KeyboardInterrupt:
    GPIO.cleanup()



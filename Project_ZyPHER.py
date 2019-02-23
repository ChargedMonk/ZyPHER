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

cmd = 'sudo ifconfig wlan0 down'
os.system(cmd)
camera = picamera.PiCamera()
now=dt.datetime.now()
print(now.strftime("%d-%m-%Y %H:%M:%S"))
time.sleep(60)


def sendvid():
    
    now=dt.datetime.now()
    camera.rotation = -90
    #camera.vflip=True
    #camera.start_preview()
    camera.capture('example.jpg' )
    #camera.stop_preview()
    time.sleep(2)
    camera.start_recording('examplevid.h264')
    time.sleep(10)
    camera.stop_recording()

    
    fromaddr = '*************'
    toaddr = '*************'
    alladdr = toaddr.split(',')
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'INTRUDER ALERT!!!'
    body = 'Latest Image of the room\n\nUploading Video Soon'
    msg.attach(MIMEText(body, 'plain'))

    filename = now.strftime("%d-%m-%Y %H:%M:%S")  + '.jpg'
    attachment = open('/example.jpg', 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, '<password of email address>')
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
GPIO.setwarnings(False)
GPIO.setup(20, GPIO.IN,GPIO.PUD_DOWN) 
#GPIO.setup(24, GPIO.OUT)
try:
    while True:
      if GPIO.input(20): 
         now=dt.datetime.now()
         print('Motion Detected',now.strftime("%d-%m-%Y %H:%M:%S"))
         cmd2 = 'sudo ifconfig wlan0 up'
         os.system(cmd2)
         sendvid()
         cmd2 = 'sudo ifconfig wlan0 down'
         os.system(cmd2)
         time.sleep(300) 
except KeyboardInterrupt:
    GPIO.cleanup()

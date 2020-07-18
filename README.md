# ZyPHER :detective: :camera: :house_with_garden:


### A home security device, which captures the image and video of the intruder and notifies the owner via email.

Built using raspberry pi and motion sensor.

---

## Components:

  * __`Raspberry Pi 3B+`__
  
  * __`Raspberry Pi Camera Module V2`__
  
  * __`PIR Sensor (for motion detection)`__
  
  * __`A 5V 2.5A power supply for the Raspberry Pi`__

---

## Requirements


Python 3.6 or later along with RPi.GPO, picamera. To install run:

```bash
$ pip install -U -r requirements.txt
```


---

## Usage:

First setup the raspberry pi, camera module and the PIR sensor. Follow this [quick guide](https://www.youtube.com/watch?v=Tw0mG4YtsZk) for reference.

Also change the email id and password according to your choice.

You can edit the .bashrc file to run this program at boot up. Take a look at [this](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/) for help.

Or you could run the zypher.py file as:
 
 ```bash
$ python3 zypher.py
```

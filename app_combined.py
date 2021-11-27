import RPi.GPIO as GPIO
import time
import os
from time import sleep

from flask import (Flask, render_template, request, redirect, session)
from flask import Flask, render_template, Response

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera


app = Flask(__name__)


m11=18
m12=23
m21=24
m22=25


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.output(m11 , 0)
GPIO.output(m12 , 0)
GPIO.output(m21, 0)
GPIO.output(m22, 0)


# Global variables definition and initialization
global panServoAngle
global tiltServoAngle
panServoAngle = 90
tiltServoAngle = 90

panPin = 27
tiltPin = 17


#define actuators GPIOs
led = 13

power = 16


#initialize GPIO status variables

ledSts = 0

powerSts = 1


# Define led pins as output
GPIO.setup(led, GPIO.OUT)   

# turn leds OFF 
GPIO.output(led, GPIO.LOW)


# Define power pins as output
GPIO.setup(power, GPIO.OUT)   

# turn power OFF 
GPIO.output(power, GPIO.LOW)


a=1

# (LOGIN PAGE WORKING CODE) 

#1 (LOGIN PAGE OPENS)

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/index")
def index():

   # Read GPIO Status
	
	ledSts = GPIO.input(led)
	

	templateData = {
      		
      		'led'  : ledSts,
      		
      	}

   
    # Read GPIO Status
	
	powerSts = GPIO.input(power)
	

	templateData = {
      		
      		'power'  : powerSts,
      		
      	}


     # Read servo Status

     templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle
	}
 

    return render_template('index.html', **templateData)


@app.route('/back')
def back():
    return render_template('main.html')



""" 
# (OPENING WEBPAGE)

# video

@app.route('/index')
def index():
#    """Video streaming home page."""
     return render_template('index.html')


# led

@app.route("/index")
def index():
	# Read GPIO Status
	
	ledSts = GPIO.input(led)
	

	templateData = {
      		
      		'led'  : ledSts,
      		
      	}
	return render_template('index.html', **templateData)


# power

@app.route("/index")
def index():
	# Read GPIO Status
	
	powerSts = GPIO.input(power)
	

	templateData = {
      		
      		'power'  : powerSts,
      		
      	}
	return render_template('index.html', **templateData)


# dc

a=1
@app.route("/index")
def index():
    return render_template('index.html')


# servo

@app.route('/index')
def index():
#    """Video streaming home page."""
 
    templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle
	}
    return render_template('index.html', **templateData)

""""



#4 (VIDEO)

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


#5 (LED)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'led':
		actuator = led
	
   
	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
		     
	
	ledSts = GPIO.input(led)
	
   
	templateData = {
	 	
      		'led'  : ledSts,
      		
	}
	return render_template('index.html', **templateData)


#6 (POWER)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'power':
		actuator = power
	
   
	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
		     
	
	powerSts = GPIO.input(led)
	
   
	templateData = {
	 	
      		'power'  : powerSts,
      		
	}
	return render_template('index.html', **templateData)



#7 (DC MOTOR)

@app.route('/left_side')
def left_side():
    data1="LEFT"
    GPIO.output(m11 , 0)
    GPIO.output(m12 , 1)
    GPIO.output(m21 , 1)
    GPIO.output(m22 , 0)
    return render_template('index.html')

@app.route('/right_side')
def right_side():
   data1="RIGHT"
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 1)
   return render_template('index.html')

@app.route('/up_side')
def up_side():
   data1="FORWARD"
   GPIO.output(m11 , 1)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 1)
   GPIO.output(m22 , 0)
   return render_template('index.html')

@app.route('/down_side')
def down_side():
   data1="BACK"
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 1)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 1)
   return render_template('index.html')

@app.route('/stop')
def stop():
   data1="STOP"
   GPIO.output(m11 , 0)
   GPIO.output(m12 , 0)
   GPIO.output(m21 , 0)
   GPIO.output(m22 , 0)
   return render_template('index.html')


#8 (SERVO MOTOR)

@app.route("/<servo>/<angle>")
def move(servo, angle):
	global panServoAngle
	global tiltServoAngle
	if servo == 'pan':
		panServoAngle = int(angle)
		os.system("python3 angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
	if servo == 'tilt':
		tiltServoAngle = int(angle)
		os.system("python3 angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))
	
	templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle
	}
	return render_template('index.html', **templateData)



# (RUN PYTHON FILE)

#Step -7(run the app)
if __name__ == '__main__':
    app.run()

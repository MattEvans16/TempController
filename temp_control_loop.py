import smbus
import time
import RPi.GPIO as GPIO
import time
import wiringpi
from flask import current_app as app
from flask import Flask, render_template, request, redirect, url_for, session, abort, make_response, g, Response, stream_with_context, jsonify, send_from_directory
from temp_config import *
import os

if __name__ == '__main__':
    #init the servo.
    wiringpi.wiringPiSetupGpio()

    wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
    wiringpi.pwmSetClock(192)
    wiringpi.pwmSetRange(2000)
    
    servoValue = 0
    wiringpi.pwmWrite(18,50)
    
    while True:
        if os.path.isfile('tmp/servo_setting'):
            with open('tmp/servo_setting') as f:
                readValue = f.read()
                print readValue
                time.sleep(1)
                if (readValue != servoValue):
                    servoValue = readValue
                    if servoValue == '1':
                        wiringpi.pwmWrite(18,80)
                    else:
                        wiringpi.pwmWrite(18,50)
from flask import Flask, render_template, request, redirect, url_for, session, abort, make_response, g, Response, stream_with_context, jsonify, send_from_directory
from flask import current_app as app
import mysql.connector
import logging
import logging.handlers
import os
import RPi.GPIO as GPIO

def setConfig():
    app.config['DEBUG'] = True
    app.config['rds-host'] = ''
    app.config['rds-db'] = ''
    app.config['rds-user'] = ''
    app.config['rds-password'] = ''
    
    
    #define logger.
    app.logger.setLevel(logging.DEBUG)
    if (not os.path.isdir("logs")):
        os.mkdirs("logs")
    fh = logging.FileHandler("logs/temp_control.log")
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s %(message)s")
    
    #add formatters.
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    app.logger.addHandler(fh)
    app.logger.addHandler(ch)
    
def get_servo():
    """Gets the servo to control.
    """
    servo = getattr(g, 'servo', None)
    if servo is None:
        servo = g.servo = connect_servo()
    return servo
    
def connect_servo():
    app.logger.debug("Initalizing Servo")
    GPIO.setmode(GPIO.BCM)
    servo = GPIO.setup(18,GPIO.OUT)
    if (servo == None):
        app.logger.warning("Failed to get GPIO.")
        return None
    servo.start(5)
    return servo
import smbus
import time
import RPi.GPIO as GPIO
from flask import current_app as app
from flask import Flask, render_template, request, redirect, url_for, session, abort, make_response, g, Response, stream_with_context, jsonify, send_from_directory
from temp_config import *

def get_temp_data():
    """This retreieves the temp data
    """
    # Get I2C bus
    bus = smbus.SMBus(1)

    # SI7021 address, 0x40(64)
    #		0xF5(245)	Select Relative Humidity NO HOLD master mode
    bus.write_byte(0x40, 0xF5)

    time.sleep(0.1)

    # SI7021 address, 0x40(64)
    # Read data back, 2 bytes, Humidity MSB first
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)

    # Convert the data
    humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6

    time.sleep(0.1)

    # SI7021 address, 0x40(64)
    #		0xF3(243)	Select temperature NO HOLD master mode
    bus.write_byte(0x40, 0xF3)

    time.sleep(0.1)

    # SI7021 address, 0x40(64)
    # Read data back, 2 bytes, Temperature MSB first
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)

    # Convert the data
    cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
    fTemp = cTemp * 1.8 + 32
    
    
    return {'humidity': humidity, 'cTemp':cTemp, 'fTemp':fTemp, 'timestamp':datetime.now() }
    
def set_servo_position(pos=0):
    """ This is used to set the servo position.
    """
    
   
    
    #set the PWM to 50Hz (Servo Requires)
    
    if (pos == 0):
        get_servo().ChangeDutyCycle(5)
        app.logger.debug("Setting Servo Off")
    else:
        get_servo().ChangeDutyCycle(15)
        app.logger.debug("Setting Servo On")
        
        
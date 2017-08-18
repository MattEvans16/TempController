from flask import Flask, render_template, request, redirect, url_for, session, abort, make_response, g, Response, stream_with_context, jsonify, send_from_directory
from temp_config import *
from temp_control import *
from random import randint

app = Flask('temp_control')

@app.teardown_appcontext
def close_db(error):
    """closes db connection"""
    app.logger.debug("closing db")
    if hasattr(g, 'db'):
        app.logger.debug("actually closing db")
        g.db.close()

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

    
   
@app.route('/get/temp', methods=['GET','POST'])
def getTemp():
    '''returns all of the current sensor values.  We should probably actually have this pulled from DB or something, not sure if we should really wait on I2C Comms during a web request....?
    '''
    with open('tmp/fTemp') as fo:
        tempF = fo.read()
    with open('tmp/cTemp') as fo:
        tempC = fo.read()
    with open('tmp/humidity') as fo:
        humidity = fo.read()
    data = {'tempF':tempF, 'tempC':tempC, 'humidity':humidity}
    return jsonify(**data)
 
@app.route('/set/power', methods=['POST','GET'])
def setPower():
    """ writers the value 1 or 0 to the tmp/servo_setting file
    """
    
    formData = request.form.to_dict()
    
    powerValue = formData.get('powerValue',None)#str(randint(0,1))
    if powerValue is None:
        data = {'err':1, 'powerValue':powerValue}
        
    else:
        app.logger.info("Recv'd setPower = {}".format(powerValue))
        with open('tmp/servo_setting', 'w') as f:
            f.write(powerValue)            
        data = {'err':0, 'powerValue':powerValue}
    return jsonify(**data)
    
    
   
    
    
if __name__ == '__main__':

    with app.app_context():
        setConfig()
    app.logger.debug("starting main flask app")
    app.run(threaded=False,host='0.0.0.0')

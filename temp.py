from flask import Flask
app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello World! - Your Tempature is 90 Degrees!'
 
if __name__ == '__main__':
    app.run(host='0.0.0.0')

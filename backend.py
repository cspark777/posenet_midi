from flask import Flask, request
from flask_cors import CORS
import json

import random
import time
import os

# Try to import MidiFile from the mido module. You can install mido with pip:
#   pip install mido

try:
    import winsound

    def beep_frequency(frequency, duration):
        winsound.Beep(frequency, duration)
        return

except:
    
    def beep_frequency(frequency, duration):        
        os.system('play -n synth %s sin %s' % (duration/1000, frequency))
        return


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "<h1>Hello, World!</h1>"

@app.route('/posedata',  methods=['POST'])
def posedata():
    
    post_data_json = request.form.get("post_data")
    post_data = json.loads(post_data_json)    
    
    keypoints = post_data["keypoints"]        
    lwx = 0
    lwy = 0
    for k in keypoints:
        n = k["part"]
        if n=="nose":
            lwx = lwx + k["position"]["x"]
            lwy = lwy + k["position"]["y"]

    lw = lwx + lwy

    lw = int(lw) % 256

    fr = lw * 50 + 37
    print(fr)     
    beep_frequency(fr, 200)
    
    return "success";

if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0", port="8080", use_reloader=False,)
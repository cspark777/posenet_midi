from flask import Flask, request
from flask_cors import CORS
import json

import random
import time
import os

from pyo import *
server = Server().boot()
class PadSynth(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)

        self.phase = Sine([self.freq, self.freq*1.003])
 
        self.duty = Expseg([(0, 0.05), (self.dur, 0.5)], exp=4).play()

        self.osc = Compare(self.phase, self.duty, mode="<", mul=1, add=-0.5)

        self.filt = Biquad(self.osc, freq=1500, q=1, mul=self.env).out()

server.start()

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

    
    print(lw)     
    
    c1 = Events(instr = PadSynth,
           midinote = lw,
           beat = 0.5, db = 32,
           attack = 0.1, decay = 0.01, sustain = 0.5, release = 0.00001, bpm=120)

    c1.play()
    time.sleep(0.25)
    c1.stop()

    
    return "success";

if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0", port="8080", use_reloader=False,)
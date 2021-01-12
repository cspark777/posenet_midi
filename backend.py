from flask import Flask, request
from flask_cors import CORS
import json

from pyo import *
import random
import time
import threading 
import winsound
# Try to import MidiFile from the mido module. You can install mido with pip:
#   pip install mido

try:
    from mido import MidiFile
except:
    print("The `mido` module must be installed to run this example!")
    exit()



s = Server().boot().start()

# A little audio synth to play the MIDI events.
mid = Notein()
amp = MidiAdsr(mid["velocity"])
pit = MToF(mid["pitch"])
osc = Osc(SquareTable(), freq=pit, mul=amp).mix(1)
rev = STRev(osc, revtime=1, cutoff=4000, bal=0.2).out()
midi_data = [0, 0, 0]

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "<h1>Hello, World!</h1>"





g_post_data_arr = []

@app.route('/posedata',  methods=['POST'])
def posedata():
    global g_post_data_arr
    post_data_json = request.form.get("post_data")
    post_data = json.loads(post_data_json)
    
    g_post_data_arr.append(post_data)

    print("----------- {} -------------".format(len(g_post_data_arr)))


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
    winsound.Beep(fr, 200)

    '''
    midi_data[0] = 128
    midi_data[1] = 100
    midi_data[2] = 20
    s.addMidiEvent(*midi_data)
    time.sleep(0.3)  

    midi_data[0] = 144
    midi_data[1] = lw
    midi_data[2] = 20
    s.addMidiEvent(*midi_data)
    time.sleep(0.2)
    '''
    


    
    return "success";

def generate_midi():
    global g_post_data_arr
    while True:
        num = len(g_post_data_arr)
        print("++++++++++++++ {} +++++++++++++++++".format(num))

        if num == 0:
            time.sleep(0.5)
            continue

        post_data = g_post_data_arr[-1]   

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

        midi_data[0] = 144
        midi_data[1] = lw
        midi_data[2] = 20
        s.addMidiEvent(*midi_data)
        time.sleep(0.5)

        midi_data[0] = 128
        midi_data[1] = 100
        midi_data[2] = 20
        s.addMidiEvent(*midi_data)
        time.sleep(0.5)




if __name__ == '__main__':
    #t1 = threading.Thread(target=generate_midi, args=()) 
    #t1.start() 

    app.run(debug=True, host="0.0.0.0", port="8080", use_reloader=False,)
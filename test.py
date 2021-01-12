from flask import Flask, request
from flask_cors import CORS
import json

from pyo import *
import random
import time
import threading 
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

def posedata():
    
    while True:

        lw = random.randint(10, 150)

        print(lw)            

        midi_data[0] = 144
        midi_data[1] = lw
        midi_data[2] = 20
        s.addMidiEvent(*midi_data)
        time.sleep(0.2)

        midi_data[0] = 128
        midi_data[1] = 100
        midi_data[2] = 20
        s.addMidiEvent(*midi_data)
        time.sleep(1)  

    


    
    return "success";


if __name__ == '__main__':
    #t1 = threading.Thread(target=generate_midi, args=()) 
    #t1.start() 

    posedata()
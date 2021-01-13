from pyo import *
import random
import time
server = Server().boot()


class PadSynth(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)

        self.phase = Sine([self.freq, self.freq*1.003])
 
        self.duty = Expseg([(0, 0.05), (self.dur, 0.5)], exp=4).play()

        self.osc = Compare(self.phase, self.duty, mode="<", mul=1, add=-0.5)

        self.filt = Biquad(self.osc, freq=1500, q=1, mul=self.env).out()

pad_midi_1 = [56]

pad_db = -32.0

c1 = Events(instr = PadSynth,
           midinote = 56,
           beat = 0.5, db = pad_db,
           attack = 0.1, decay = 0.01, sustain = 0.5, release = 0.00001, bpm=120)

server.start()


while True:
    c1.play()
    time.sleep(0.25)
    c1.stop()

    r = random.randint(20, 100) 
    pad_midi_1 = [r]
    c1 = Events(instr = PadSynth,
           midinote = r,
           beat = 0.5, db = pad_db,
           attack = 0.1, decay = 0.01, sustain = 0.5, release = 0.00001, bpm=120)

    time.sleep(1)

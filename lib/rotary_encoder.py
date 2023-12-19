from machine import Pin
from time import ticks_ms

class RotaryEncoder:
    def __init__(self, pin_enc_a = 36, pin_enc_b = 39):
        self.__rotenc_a = Pin(pin_enc_a, Pin.IN, Pin.PULL_UP)
        self.__rotenc_b = Pin(pin_enc_b, Pin.IN, Pin.PULL_UP)
        self.enc_state = 0 # Encoder state control variable
        self.counter = 0
        # Rotary encoder truth table, which one to use depends the actual rotary encoder hardware
        self.encTableFullStep = [
        [0x00, 0x02, 0x04, 0x00],
        [0x03, 0x00, 0x01, 0x10],
        [0x03, 0x02, 0x00, 0x00],
        [0x03, 0x02, 0x01, 0x00],
        [0x06, 0x00, 0x04, 0x00],
        [0x06, 0x05, 0x00, 0x20],
        [0x06, 0x05, 0x04, 0x00]]

    def re_full_step(self):     
        self.enc_state = self.encTableFullStep[self.enc_state & 0x0F][(self.__rotenc_b.value() << 1) | self.__rotenc_a.value()]     
        # -1: Left/CCW, 0: No rotation, 1: Right/CW
        result = self.enc_state & 0x30
        if (result == 0x10):
            return 1
        elif (result == 0x20):
            return -1
        else:
            return 0
           
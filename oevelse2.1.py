from machine import Pin, deepsleep
from time import sleep
import esp32
"""2.1 - Vælg en sensor og anvend den til at vække ESP32 fra deepsleep
og print en besked i shell og toggle en LED 10 gange. (husk at filen skal ligge på ESP32 som main.py)
- brug wake_on_ext0: https://docs.micropython.org/en/latest/library/esp32.html#esp32.wake_on_ext0 """
led1 = Pin(26, Pin.OUT)
rot_pb = Pin(14, Pin.IN, Pin.PULL_UP)

esp32.wake_on_ext0(pin=rot_pb, level=esp32.WAKEUP_ALL_LOW)

for i in range(10):
    led1.value(not led1.value())
    sleep(0.1)

deepsleep()
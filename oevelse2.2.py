from machine import Pin, deepsleep
from time import sleep
from neopixel import NeoPixel
from random import randint
import esp32
"""2.2 - Prøv at vække ESP32 fra deepsleep med en timer,
og kør en funktion der sætter en random farve på
RGB LED eller neopixel ringen hver gang den vækkes."""
PIXEL_AMOUNT = 12
PIXEL_PIN = 26

np = NeoPixel(Pin(PIXEL_PIN), PIXEL_AMOUNT)

red = randint(0, 255)
green = randint(0, 255)
blue = randint(0, 255)

for pixel in range(PIXEL_AMOUNT):
    np[pixel] = (red, green, blue)
np.write()

deepsleep(1000)


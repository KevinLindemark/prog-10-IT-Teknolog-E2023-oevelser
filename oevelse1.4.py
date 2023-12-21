from machine import Pin, PWM
import uasyncio as asyncio
from hcsr04 import HCSR04
"""Øvelse 1.4 - brug async io til at lave et eventloop der
tjekker for om en knap trykkes og hvis distancen er under 30CM
når der trykkes skal der stå “Too close på display” og hvis distancen
er mellem 30CM og 60CM skal der stå “Good distance” og hvis den er over
60CM skal der stå “Too far”"""

button = Pin(0, Pin.IN)

def check_distance():
    # dist typecastes til int 
    dist = ultrasonic.distance_cm()
    if dist < 30:
        print("Too close")
    elif dist >= 30 and dist <=60:
        print("Good distance")
    elif dist > 60:
        print("Too far")
    else:
        print("Wrong value check sensor")

ultrasonic = HCSR04(15, 34)

async def distance_brightness_control():
    while True:
        if button.value() == 0:
            check_distance()
 
        await asyncio.sleep_ms(50)

loop = asyncio.new_event_loop()
loop.create_task(distance_brightness_control())
loop.run_forever()
        
    

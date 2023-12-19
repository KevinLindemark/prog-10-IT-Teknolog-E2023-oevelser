from machine import Pin, PWM
import uasyncio as asyncio
from hcsr04 import HCSR04
"""Øvelse 1.3 - prøv at styre brighthes med PWM på LED1,
    så brightness øges jo længere væk noget er fra educaboard"""

led1 = PWM(Pin(26, Pin.OUT))
ultrasonic = HCSR04(15, 34)

async def distance_brightness_control():
    while True:
        # dist typecastes til int 
        dist = int(ultrasonic.distance_cm())
        if dist < 0: #  undgå tal under 0
            dist = 0
        # max distance 400 cm (400*2.5575=1023)
        led1.duty(int(dist*2.5575)) 
        await asyncio.sleep_ms(500)

loop = asyncio.new_event_loop()
loop.create_task(distance_brightness_control())
loop.run_forever()
        
    
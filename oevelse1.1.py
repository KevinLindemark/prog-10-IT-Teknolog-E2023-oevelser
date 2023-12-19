from hcsr04 import HCSR04
import uasyncio as asyncio
from machine import Pin
"""Øvelse 1.1: Lav et eventloop med asyncio der
    printer distancen i CM der måles af HC-SR04
    ultralydssensoren."""
ultrasonic = HCSR04(15, 34)

async def lcd_show_distance():
    while True:
        distance = ultrasonic.distance_cm()
        print(f"Distance: {distance:.2f}CM")
        await asyncio.sleep_ms(1000)

loop = asyncio.new_event_loop()
loop.create_task(lcd_show_distance())
loop.run_forever()


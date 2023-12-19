from hcsr04 import HCSR04
from gpio_lcd import GpioLcd
import uasyncio as asyncio
from machine import Pin
"""Øvelse 1.2: Vis distancen på LCD display på
    educaboard og sørg for at den opdateres hvert sekund.
"""
lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                  d4_pin=Pin(33), d5_pin=Pin(32),
                  d6_pin=Pin(21), d7_pin=Pin(22),
                  num_lines=4, num_columns=20)

ultrasonic = HCSR04(15, 34)

async def lcd_show_distance():
    while True:
        lcd.clear()
        distance = ultrasonic.distance_cm()
        lcd.putstr(f"Distance: {distance:.2f}CM")
        await asyncio.sleep_ms(1000)

loop = asyncio.new_event_loop()
loop.create_task(lcd_show_distance())
loop.run_forever()


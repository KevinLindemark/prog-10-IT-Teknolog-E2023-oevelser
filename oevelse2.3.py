from hcsr04 import HCSR04
from gpio_lcd import GpioLcd
import uasyncio as asyncio
from machine import Pin, deepsleep
import esp32
"""Øvelse 2.3 Lav et program der viser distance på
Educaboardets LCD display, og opdaterer hvert sekund.
Når distancen er mere end 100CM skal tekst fjernes fra display.
ESP32 skal derefter printe en besked på LCD om at den vil gå i deepslep,
og derefter gå i deepsleep. Den skal først vågne igen
når der trykkes på en af trykknapperne..
"""
lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                  d4_pin=Pin(33), d5_pin=Pin(32),
                  d6_pin=Pin(21), d7_pin=Pin(22),
                  num_lines=4, num_columns=20)

ultrasonic = HCSR04(15, 34)
wake_pin = Pin(0, Pin.IN, Pin.PULL_UP)
esp32.wake_on_ext0(pin = wake_pin, level=esp32.WAKEUP_ALL_LOW)
async def lcd_show_distance():
    while True:
        lcd.clear()
        distance = ultrasonic.distance_cm()
        lcd.putstr(f"Distance: {distance:.2f}CM")
        if distance > 100:
            lcd.clear()
            lcd.putstr("Going to deepsleep")
            await asyncio.sleep_ms(1000)
            lcd.clear()
            deepsleep()
        await asyncio.sleep_ms(1000)

loop = asyncio.new_event_loop()
loop.create_task(lcd_show_distance())
loop.run_forever()



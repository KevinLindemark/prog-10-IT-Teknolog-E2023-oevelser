"""
4.1 - lav menu-item med calback funktion til at sætte ESP32 i deepsleep
    og sørg for at den kan vækkes efterfølgende ved et knaptryk (kræver at filen køres som main.py)

4.2 - lav menu-item med calback funktion til at vise distance på display

4.3 - lav en menu med callback der viser dato og tid fra RTC i
    DDMMYYYY format og tiden i HHMMSS format. Det skal også fremgå
    hvilken ugedag det er skrevet som “monday, tuesday…”

"""

from gpio_lcd import GpioLcd
from rotary_encoder import RotaryEncoder
from machine import Pin, deepsleep, RTC
from lcd_menu import LCDMenu
from lmt84 import LMT84
from time import sleep
import esp32
from hcsr04 import HCSR04

ultrasonic = HCSR04(15, 34)

wake_button = Pin(0, Pin.IN, Pin.PULL_UP)
esp32.wake_on_ext0(pin=wake_button, level=esp32.WAKEUP_ALL_LOW)

lmt84 = LMT84()

rot_pb = Pin(14, Pin.IN, Pin.PULL_UP)
rot = RotaryEncoder()

lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                  d4_pin=Pin(33), d5_pin=Pin(32),
                  d6_pin=Pin(21), d7_pin=Pin(22),
                  num_lines=4, num_columns=20)

menu = LCDMenu(lcd, rot, rot_pb)
led1 = Pin(26, Pin.OUT)

# https://maxpromer.github.io/LCD-Character-Creator/
lcd_custom_char_degrees = bytearray([0x0E, 0x0A,
                                     0x0E, 0x00,
                                     0x00, 0x00,
                                     0x00, 0x00])

rtc = RTC()
week_days = {"0":"monday", "1":"tuesday",
             "2":"wednesday", "3":"thursday",
             "4":"friday", "5":"saturday",
             "6":"sunday"}

year = rtc.datetime()[0]
month = rtc.datetime()[1]
day_of_the_month = rtc.datetime()[2]
day_of_the_week = rtc.datetime()[3]
hours = rtc.datetime()[4]
minutes = rtc.datetime()[5]
seconds = rtc.datetime()[6]

date_ddmmyy = f"{day_of_the_month}/{month}/{year}"
weekday_formatted = f"{week_days[str(day_of_the_week)]}"
time_hhmmss = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
print(f"The date is {date_ddmmyy} and it's {weekday_formatted}", end="")

def lcd_temperature_celsius():
    """callback function to display temperature celsius on lcd"""
    lcd.move_to(1, menu.selected)  # moves to selected line
    lcd.putstr("                  ")  # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr(f"Temp is {lmt84.celsius_temperature():.1f} ")
    lcd.custom_char(2, lcd_custom_char_degrees)
    lcd.putchar(chr(2))
    lcd.putstr("C")


def lcd_temperature_fahrenheit():
    """callback function to display temperature fahrenheit on lcd"""
    lcd.move_to(1, menu.selected)  # moves to selected line
    lcd.putstr("                  ")  # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr(f"Temp is {lmt84.fahrenheit_temperature():.1f} ")
    lcd.custom_char(2, lcd_custom_char_degrees)
    lcd.putchar(chr(2))
    lcd.putstr("F")


def lcd_temperature_kelvin():
    """callback function to display temperature kelvin on lcd"""
    lcd.move_to(1, menu.selected)  # moves to selected line
    lcd.putstr("                  ")  # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr(f"Temp is {lmt84.kelvin_temperature():.1f}K")


def lcd_toggle_led1():
    """callback to Toggle led1"""
    lcd.move_to(1, menu.selected)  # moves to selected line
    lcd.putstr("                  ")  # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr("LED1 is toggled!")
    led1.value(not led1.value())


def activate_deepsleep(): #  oevelse 4.1
    """callback to activate deepsleep"""
    lcd.clear()
    lcd.putstr("Going to deepsleep")
    sleep(1)
    lcd.clear()
    deepsleep()

def lcd_distance(): #  oevelse 4.2
    """callback to show distance in CM on LCD"""
    lcd.move_to(1, menu.selected)  # moves to selected line
    lcd.putstr("                  ")  # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr(f"Distance: {ultrasonic.distance_cm():.1f}CM")

def lcd_formatted_datetime(): #  oevelse 4.3
    """callback to formatted datetime with DDMMYYY HHMMSS and
    weekday in text LCD"""
    lcd.clear()
    lcd.putstr(f"The date is {date_ddmmyy}")
    lcd.move_to(0,1)
    lcd.putstr(f"It's {weekday_formatted}")
    lcd.move_to(0,2)
    lcd.putstr(f"The time is {time_hhmmss}")

menu.add_menu_item("Temp celsius", lcd_temperature_celsius)
menu.add_menu_item("Temp fahrenheit", lcd_temperature_fahrenheit)
menu.add_menu_item("Temp kelvin", lcd_temperature_kelvin)
menu.add_menu_item("Toggle LED1", lcd_toggle_led1)
menu.add_menu_item("deepsleep", activate_deepsleep) #  oevelse 4.1
menu.add_menu_item("Measure distance", lcd_distance) #  oevelse 4.2
menu.add_menu_item("Weekday & datetime", lcd_formatted_datetime) #  oevelse 4.3

menu.display_menu()
menu.run()

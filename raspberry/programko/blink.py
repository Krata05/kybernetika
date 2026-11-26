from machine import Pin
import time
from rp2 import bootsel_button

led = Pin("LED", Pin.OUT)

while True:
    led.value(bootsel_button())
    print("Button state:", bootsel_button())


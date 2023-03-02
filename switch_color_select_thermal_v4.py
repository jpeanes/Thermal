#MIT License

#Copyright (c) 2023 Joshua Paul Eanes https://github.com/jpeanes

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE

import machine, sensor, time, tv, pyb

SWITCH_1_PIN = 'P7'
SWITCH_2_PIN = 'P9'

led = pyb.LED(1)
led.on()

switch_state_1 = machine.Pin(SWITCH_1_PIN, machine.Pin.IN).value()
switch_state_2 = machine.Pin(SWITCH_2_PIN, machine.Pin.IN).value()

current_state = 1

if switch_state_1 == 0 and switch_state_2 == 1:
    current_state = 1
elif switch_state_1 == 1 and switch_state_2 == 1:
    current_state = 2
elif switch_state_1 == 1 and switch_state_2 == 0:
    current_state = 3

def set_init_color(current_state):
    if current_state == 1:
        sensor.set_pixformat(sensor.GRAYSCALE)
    elif current_state == 2:
        sensor.set_color_palette(sensor.PALETTE_RAINBOW)
        sensor.set_pixformat(sensor.RGB565)
    elif current_state == 3:
        sensor.set_color_palette(sensor.PALETTE_IRONBOW)
        sensor.set_pixformat(sensor.RGB565)

def handle_interrupt(pin):
    global switch_state_1, switch_state_2, current_state
    switch_state_1 = machine.Pin(SWITCH_1_PIN, machine.Pin.IN).value()
    switch_state_2 = machine.Pin(SWITCH_2_PIN, machine.Pin.IN).value()
    if switch_state_1 == 0 and switch_state_2 == 1:
        current_state = 1
        sensor.set_pixformat(sensor.GRAYSCALE)
    elif switch_state_1 == 1 and switch_state_2 == 1:
        current_state = 2
        sensor.set_color_palette(sensor.PALETTE_RAINBOW)
        sensor.set_pixformat(sensor.RGB565)
    elif switch_state_1 == 1 and switch_state_2 == 0:
        current_state = 3
        sensor.set_color_palette(sensor.PALETTE_IRONBOW)
        sensor.set_pixformat(sensor.RGB565)

switch_1 = machine.Pin(SWITCH_1_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
switch_1.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=handle_interrupt)

switch_2 = machine.Pin(SWITCH_2_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
switch_2.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=handle_interrupt)

try:
    sensor.reset()
    set_init_color(current_state)
    sensor.set_framesize(sensor.SIF)
    sensor.skip_frames(time=5000)
    sensor.set_vflip(True)
except:
    print("sensor error, resetting...")
    for i in range(9):
        led.off()
        time.sleep_ms(100)
        led.on()
        time.sleep_ms(150)
    machine.reset()
else:
    print("successfully initialized")

clock = time.clock()

tv.init(type=tv.TV_SHIELD, triple_buffer=False)
tv.channel(8)

led.toggle()

while True:
    clock.tick()
    tv.display(sensor.snapshot())


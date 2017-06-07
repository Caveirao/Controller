"""
    This app will receiver a UDP protocol package and decode this one to
    control connected motors in a RaspberryPi.

    By Allex Lima <allexlima@unn.edu.br> | http://allexlima.com
    Jun 2017, MIT License
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import struct
import RPi.GPIO as gpio


class Receiver(object):
    def __init__(self, ip, port):
        self.address = (ip, port)
        self.udp = None

    def __active(self):
        self.udp = socket.socket(type=socket.SOCK_DGRAM)
        self.udp.bind(self.address)

    def listener(self, origin=None):
        self.__active()
        (package, origin_address) = self.udp.recvfrom(1024)
        return None if (origin is not None) and (origin != origin_address) else struct.unpack('>2h', package)

    def deactivate(self):
        self.udp.close()


class MotorsPi(object):
    def __init__(self, pins):
        gpio.setmode(gpio.BOARD)
        if isinstance(pins, list) is False:
            raise Exception("You must provide a list of GPIO pins!")
        self.pins = pins
        for pin in self.pins:
            gpio.setup(pin, gpio.OUT)

    def __set_pins(self, pins, state):
        for i in pins:
            gpio.output(self.pins[i], state)

    def stopped(self):
        self.__set_pins(range(4), False)

    def forward(self):
        self.__set_pins([1, 2], True)
        self.__set_pins([0, 3], False)

    def backward(self):
        self.__set_pins([0, 3], True)
        self.__set_pins([1, 2], False)

    def right(self):
        self.__set_pins([1, 3], True)
        self.__set_pins([0, 2], False)

    def left(self):
        self.__set_pins([0, 2], True)
        self.__set_pins([1, 3], False)

if __name__ == "__main__":
    remote = Receiver('', 5000)
    control = MotorsPi([37, 35, 38, 36])
    security_origin = None
    print("[On] Waiting for control inputs...")
    while True:
        data = remote.listener(security_origin)
        if data == (1, 1):
            print('forward')
            control.forward()
        elif data == (-1, -1):
            print('backward')
            control.backward()
        elif data == (-1, 1):
            print('left')
            control.left()
        elif data == (1, -1):
            print('right')
            control.right()
        else:
            print('stopped')
            control.stopped()
    remote.deactivate()
    print("[Off] The controller service is down! Bye...")

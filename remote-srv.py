#!/usr/bin/env python_root

from nrf24 import NRF24
from keystroke import KeystrokeHandler
import time
import logging

logging.basicConfig(level=logging.DEBUG)

pipes = [[0xD9, 0x02, 0x86, 0xD0, 0xEE], [0xB8, 0x25, 0xB9, 0xE1, 0xBD]]

handler = KeystrokeHandler()

radio = NRF24()
radio.begin(0, 0, 25, 0)
radio.setRetries(1, 15)
radio.setPayloadSize(3)
radio.setChannel(0x60)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(1)
radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])
radio.startListening()

while True:
    pipe = [0]
    while not radio.available(pipe, False):
        time.sleep(1000/1000000.0)
    request = [0, 0, 0]
    radio.read(request)
    if request[0] == 1:
        result = handler.handle(request[1])
        radio.stopListening()
        response = [2, result, request[2]]
        radio.write(response)
        radio.startListening()

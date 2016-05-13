#!/usr/bin/env python

from nrf24 import NRF24
from keystroke import KeystrokeHandler
import time
import logging

logging.basicConfig(filename='/var/tmp/remote-srv.log', level=logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)

pipes = [[0xD9, 0x02, 0x86, 0xD0, 0xEE], [0xB8, 0x25, 0xB9, 0xE1, 0xBD]]

handler = KeystrokeHandler()

radio = NRF24()
radio.begin(0, 0, 25, 0)
radio.setRetries(1, 15)
radio.setPayloadSize(2)
radio.setChannel(0x60)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(1)
radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])
radio.startListening()

while True:
    try:
        pipe = [0]
        while not radio.available(pipe, False):
            time.sleep(1/1000.0)
        request = [0, 0, 0]
        radio.read(request)
        handler.handle(request[0])
    except Exception, e:
        logging.error(e, exc_info=True)

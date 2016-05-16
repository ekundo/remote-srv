import logging

from RPi import GPIO
from time import sleep
from collections import OrderedDict
from sony_tv import SonyTV
from dune_hd import DuneHD
from kodi import Kodi
from denon_avr import DenonAVR


class Device:
    def __init__(self, handler, source, destination):
        self.handler = handler
        self.source = source
        self.destination = destination


class KeystrokeHandler:

    logger = logging.getLogger('KeystrokeHandler')

    devices = OrderedDict()
    devices['DENON_AVR'] = Device(DenonAVR('192.168.1.136'), None, None)
    devices['SONY_TV'] = Device(SonyTV('192.168.1.114', 'd8.d4.3c.ef.6d.cf'), None, 'MONI1')
    devices['DUNE_HD'] = Device(DuneHD('192.168.1.117'), 'BD', None)
    devices['KODI'] = Device(Kodi('192.168.1.115'), 'MPLAY', None)
    devices['XBOX'] = Device(Kodi('192.168.1.101'), 'GAME', None)

    key_code_name = {
        2:      'POWER',
        1:      'SOURCE',
        4:      'KEY_1',    5:      'KEY_2',     6:     'KEY_3',
        8:      'KEY_4',    9:      'KEY_5',    10:     'KEY_6',
        12:     'KEY_7',    13:     'KEY_8',    14:     'KEY_9',
        44:     'TTX',      17:     'KEY_0',    19:     'PRE_CH',
        7:      'VOL+',     11:     'VOL-',
        15:     'MUTE',     107:    'CH_LIST',
        18:     'P+',       16:     'P-',
        26:     'MENU',     121:    'SMART',    79:     'GUIDE',
        75:     'TOOLS',    96:     'UP',       31:     'INFO',
        101:    'LEFT',     104:    'OK',       98:     'RIGHT',
        88:     'RETURN',   97:     'DOWN',     45:     'EXIT',
        108:    'RED',      20:     'GREEN',    21:     'YELLOW',   22: 'BLUE',
        208:    'HISTORY',  30:     'CAMERA',   37:     'SUBT',
        63:     'SUPPORT',  143:    'D',        159:    '3D',
        69:     'REW',      74:     'PAUSE',    72:     'FFWD',
        73:     'REC',      71:     'PLAY',     70:     'STOP'
    }

    def __init__(self):
        self.device = KeystrokeHandler.devices['DENON_AVR']
        GPIO.setup(23, GPIO.OUT)  # G
        self.put_out()
        pass

    def handle(self, keystroke):
        keystroke_name = KeystrokeHandler.key_code_name.get(keystroke, None)
        if keystroke is not None:
            if keystroke_name == 'POWER':
                modes = KeystrokeHandler.devices['DENON_AVR'].handler.toggle_power()
                if modes['source'] is None:
                    pass
                else:
                    for key, device in KeystrokeHandler.devices.iteritems():
                        if device.source == modes['source']:
                            self.device = device
                            self.device.handler.switch_on()
                if modes['destination'] is None:
                    for key, device in KeystrokeHandler.devices.iteritems():
                        device.handler.switch_off()
                    pass
                else:
                    for key, device in KeystrokeHandler.devices.iteritems():
                        if device.destination == modes['destination']:
                            device.handler.switch_on()
            elif keystroke_name == 'HISTORY':
                self.device = KeystrokeHandler.devices['DUNE_HD']
                self.device.handler.switch_on()
                KeystrokeHandler.devices['DENON_AVR'].handler.switch_source(self.device.source)
            elif keystroke_name == 'SUPPORT':
                self.device = KeystrokeHandler.devices['DENON_AVR']
                self.device.handler.switch_on()
                # KeystrokeHandler.devices['DENON_AVR'].handler.switch_destination(self.device.source)
            elif keystroke_name == 'SUBT':
                self.device = KeystrokeHandler.devices['KODI']
                self.device.handler.switch_on()
                KeystrokeHandler.devices['DENON_AVR'].handler.switch_source(self.device.source)
            elif keystroke_name == '3D':
                self.device = KeystrokeHandler.devices['SONY_TV']
                # self.device.handler.switch_on()
                # KeystrokeHandler.devices['DENON_AVR'].handler.switch_destination(self.device.source)
            elif keystroke_name == 'CAMERA':
                self.device = KeystrokeHandler.devices['XBOX']
                self.device.handler.switch_on()
                KeystrokeHandler.devices['DENON_AVR'].handler.switch_source(self.device.source)
            elif keystroke_name in ['VOL+', 'VOL-', 'MUTE']:
                KeystrokeHandler.devices['DENON_AVR'].handler.handle(keystroke_name)
            elif keystroke_name == 'SOURCE':
                KeystrokeHandler.devices['SONY_TV'].handler.handle(keystroke_name)
            else:
                self.device.handler.handle(keystroke_name)
            self.blink()
            sleep(200 / 1000.0)

    def blink(self):
        GPIO.output(23, 0)
        sleep(10 / 1000.0)
        self.put_out()

        return

    @staticmethod
    def put_out():
        GPIO.output(23, 1)

from RPi import GPIO
from time import sleep
from collections import OrderedDict
from threading import Thread
from sony_tv import SonyTV
from dune_hd import DuneHD
from apple_tv import AppleTV
from kodi import Kodi


class Device:
    def __init__(self, color, handler, source):
        self.color = color
        self.handler = handler
        self.source = source


class KeystrokeHandler(Thread):
    LED_DELAY_020MS = 1 << 3
    LED_DELAY_050MS = 1 << 4
    LED_DELAY_100MS = 1 << 5
    LED_DELAY_200MS = 1 << 6
    LED_DELAY_500MS = 1 << 7

    devices = OrderedDict()
    devices['SONY_TV'] = Device(0b011, SonyTV('192.168.1.114', 'd8.d4.3c.ef.6d.cf'), 0)
    devices['DUNE_HD'] = Device(0b010, DuneHD('192.168.1.117'), 1)
    devices['KODI'] = Device(0b001, Kodi('192.168.1.115'), 3)
    # devices['APPLE_TV'] = Device(0b001, AppleTV(), 3)

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

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(KeystrokeHandler, self).__init__(group, target, name, args, kwargs, verbose)
        self.device = KeystrokeHandler.devices['SONY_TV']
        GPIO.setup(24, GPIO.OUT) #R       
        GPIO.setup(23, GPIO.OUT) #G
        GPIO.setup(18, GPIO.OUT) #B

        self.put_out()

    def run(self):
        super(KeystrokeHandler, self).run()

    def handle(self, keystroke):
        keystroke_name = KeystrokeHandler.key_code_name[keystroke]
        color = 0
        delay = 0
        if keystroke_name == 'POWER':
            source = KeystrokeHandler.devices['SONY_TV'].handler.toggle_power()
            if source is None:
                pass
            else:
                for key, device in KeystrokeHandler.devices.iteritems():
                    if device.source == source:
                        self.device = device
                        self.device.handler.switch_on()
                        color = self.device.color
                        delay = KeystrokeHandler.LED_DELAY_500MS | KeystrokeHandler.LED_DELAY_200MS
        elif keystroke_name == 'HISTORY':
            self.device = KeystrokeHandler.devices['DUNE_HD']
            self.device.handler.switch_on()
            KeystrokeHandler.devices['SONY_TV'].handler.switch_source(self.device.source)
            color = self.device.color
            delay = KeystrokeHandler.LED_DELAY_500MS | KeystrokeHandler.LED_DELAY_200MS
        elif keystroke_name == 'CAMERA':
            self.device = KeystrokeHandler.devices['SONY_TV']
            self.device.handler.switch_on()
            KeystrokeHandler.devices['SONY_TV'].handler.switch_source(self.device.source)
            color = self.device.color
            delay = KeystrokeHandler.LED_DELAY_500MS | KeystrokeHandler.LED_DELAY_200MS
        elif keystroke_name == 'SUBT':
            self.device = KeystrokeHandler.devices['KODI']
            self.device.handler.switch_on()
            KeystrokeHandler.devices['SONY_TV'].handler.switch_source(self.device.source)
            color = self.device.color
            delay = KeystrokeHandler.LED_DELAY_500MS | KeystrokeHandler.LED_DELAY_200MS
        elif keystroke_name in ['VOL+', 'VOL-', 'MUTE']:
            KeystrokeHandler.devices['SONY_TV'].handler.handle(keystroke_name)
            color = KeystrokeHandler.devices['SONY_TV'].color
            delay = KeystrokeHandler.LED_DELAY_020MS
        else:
            self.device.handler.handle(keystroke_name)
            color = self.device.color
            delay = KeystrokeHandler.LED_DELAY_020MS
        self.blink(color, delay)
        return color | delay

    def blink(self, color, delay):
        GPIO.output(24, color & 0b001 == 0)
        GPIO.output(23, color & 0b010 == 0)
        GPIO.output(18, color & 0b100 == 0)
        sleep(10 / 1000.0)
        self.put_out()

        return

    def put_out(self):
        GPIO.output(24, 1)
        GPIO.output(23, 1)
        GPIO.output(18, 1)

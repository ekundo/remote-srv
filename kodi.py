from device import DeviceHandler
from xbmcclient import XBMCClient
import logging
import time
import threading


class Kodi(DeviceHandler):
    _logger = logging.getLogger('Kodi')

    codes = {
        # 'SMART':    '',
        'RED':      'red',
        'GREEN':    'green',
        'YELLOW':   'yellow',
        'BLUE':     'blue',
        'KEY_1':    'one',
        'KEY_2':    'two',
        'KEY_3':    'three',
        'KEY_4':    'four',
        'KEY_5':    'five',
        'KEY_6':    'six',
        'KEY_7':    'seven',
        'KEY_8':    'eight',
        'KEY_9':    'nine',
        'KEY_0':    'zero',
        # 'TTX':      '',
        # 'PRE_CH':   '',
        'P+':       'pageplus',
        'P-':       'pageminus',
        # 'GUIDE':    '',
        'CH_LIST':  'playlist',
        'MENU':     'menu',
        'UP':       'up',
        'DOWN':     'down',
        'LEFT':     'left',
        'RIGHT':    'right',
        'OK':       'select',
        'RETURN':   'back',
        'INFO':     'info',
        'TOOLS':    'title',
        'EXIT':     'rootmenu',
        'PLAY':     'play',
        'PAUSE':    'pause',
        'SUPPORT':  'skipminus',
        '3D':       'skipplus',
        'STOP':     'stop',
        'REW':      'reverse',
        'FFWD':     'forward',
        'D':        'language',
        'REC':      'record'
    }

    def __init__(self, ip):
        super(Kodi, self).__init__()
        self.client = XBMCClient(name='remote-srv', ip=ip)
        self.ping_kodi()
        timer = threading.Timer(5.0, self.ping_kodi)
        timer.start()

    def ping_kodi(self):
        try:
            self.client.ping()
        except:
            self.logger.debug('connection lost. reconnecting')
            self.client.connect()

    @property
    def logger(self):
        return self._logger

    def _handle(self, keystroke_name):
        if keystroke_name in Kodi.codes.keys():
            code = Kodi.codes[keystroke_name]
            self.logger.debug('requesting code: [%s]' % code)
            self.client.send_button(map="R1", button=code)
            time.sleep(.1)
            self.client.release_button()
        else:
            self.logger.debug('no mapping found for %s' % keystroke_name)

    def switch_on(self):
        pass

    def switch_off(self):
        pass

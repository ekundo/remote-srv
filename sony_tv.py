from device import DeviceHandler
from httplib import HTTPConnection
from wakeonlan import wol
import logging
import time


class SonyTV(DeviceHandler):
    _logger = logging.getLogger('SonyTV')

    # noinspection SpellCheckingInspection
    BODY = '<?xml version="1.0"?>' \
           '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope ' \
           's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">' \
           '<s:Body><u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1">' \
           '<IRCCCode>%s</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>'

    # noinspection SpellCheckingInspection
    codes = {
        'POWER':    'AAAAAQAAAAEAAAAvAw==',
        'GUIDE':    'AAAAAQAAAAEAAAAOAw==',
        'CH_LIST':  'AAAAAgAAAKQAAABbAw==',
        'CAMERA':   'AAAAAQAAAAEAAAA6Aw==',
        'MENU':     'AAAAAQAAAAEAAABgAw==',
        'TOOLS':    'AAAAAgAAAJcAAAA2Aw==',
        'RETURN':   'AAAAAgAAAJcAAAAjAw==',
        'UP':       'AAAAAQAAAAEAAAB0Aw==',
        'DOWN':     'AAAAAQAAAAEAAAB1Aw==',
        'RIGHT':    'AAAAAQAAAAEAAAAzAw==',
        'LEFT':     'AAAAAQAAAAEAAAA0Aw==',
        'OK':       'AAAAAQAAAAEAAABlAw==',
        'RED':      'AAAAAgAAAJcAAAAlAw==',
        'GREEN':    'AAAAAgAAAJcAAAAmAw==',
        'YELLOW':   'AAAAAgAAAJcAAAAnAw==',
        'BLUE':     'AAAAAgAAAJcAAAAkAw==',
        'KEY_1':    'AAAAAQAAAAEAAAAAAw==',
        'KEY_2':    'AAAAAQAAAAEAAAABAw==',
        'KEY_3':    'AAAAAQAAAAEAAAACAw==',
        'KEY_4':    'AAAAAQAAAAEAAAADAw==',
        'KEY_5':    'AAAAAQAAAAEAAAAEAw==',
        'KEY_6':    'AAAAAQAAAAEAAAAFAw==',
        'KEY_7':    'AAAAAQAAAAEAAAAGAw==',
        'KEY_8':    'AAAAAQAAAAEAAAAHAw==',
        'KEY_9':    'AAAAAQAAAAEAAAAIAw==',
        'KEY_0':    'AAAAAQAAAAEAAAAJAw==',
        'VOL+':     'AAAAAQAAAAEAAAASAw==',
        'VOL-':     'AAAAAQAAAAEAAAATAw==',
        'MUTE':     'AAAAAQAAAAEAAAAUAw==',
        'P+':       'AAAAAQAAAAEAAAAQAw==',
        'P-':       'AAAAAQAAAAEAAAARAw==',
        'SUBT':     'AAAAAgAAAJcAAAAoAw==',
        'PRE_CH':   'AAAAAQAAAAEAAAA/Aw==',
        'EXIT':     'AAAAAQAAAAEAAABjAw==',
        'TTX':      'AAAAAgAAABoAAABXAw==',
        '3D':       'AAAAAgAAAHcAAABNAw==',
        'SUPPORT':  'AAAAAgAAABoAAAB7Aw==',
        'D':        'AAAAAQAAAAEAAAAXAw==',
        'FFWD':     'AAAAAgAAAJcAAAAcAw==',
        'PLAY':     'AAAAAgAAAJcAAAAaAw==',
        'REW':      'AAAAAgAAAJcAAAAbAw==',
        'STOP':     'AAAAAgAAAJcAAAAYAw==',
        'REC':      'AAAAAgAAAJcAAAAgAw==',
        'PAUSE':    'AAAAAgAAAJcAAAAZAw==',
        # "Input": "AAAAAQAAAAEAAAAlAw==",
        # "Favorites": "AAAAAgAAAHcAAAB2Aw==",
        # "Num11": "AAAAAQAAAAEAAAAKAw==",
        # "Num12": "AAAAAQAAAAEAAAALAw==",
        # "ClosedCaption": "AAAAAgAAAKQAAAAQAw==",
        # "Enter": "AAAAAQAAAAEAAAALAw==",
        # "DOT": "AAAAAgAAAJcAAAAdAw==",
        # "Analog": "AAAAAgAAAHcAAAANAw==",
        # "Analog2": "AAAAAQAAAAEAAAA4Aw==",
        # "*AD": "AAAAAgAAABoAAAA7Aw==",
        # "Digital": "AAAAAgAAAJcAAAAyAw==",
        # "Analog?": "AAAAAgAAAJcAAAAuAw==",
        # "BS": "AAAAAgAAAJcAAAAsAw==",
        # "CS": "AAAAAgAAAJcAAAArAw==",
        # "BSCS": "AAAAAgAAAJcAAAAQAw==",
        # "Ddata": "AAAAAgAAAJcAAAAVAw==",
        # "PicOff": "AAAAAQAAAAEAAAA+Aw==",
        # "Theater": "AAAAAgAAAHcAAABgAw==",
        # "SEN": "AAAAAgAAABoAAAB9Aw==",
        # "InternetWidgets": "AAAAAgAAABoAAAB6Aw==",
        # "InternetVideo": "AAAAAgAAABoAAAB5Aw==",
        # "Netflix": "AAAAAgAAABoAAAB8Aw==",
        # "SceneSelect": "AAAAAgAAABoAAAB4Aw==",
        # "Wide": "AAAAAgAAAKQAAAA9Aw==",
        # "Jump": "AAAAAQAAAAEAAAA7Aw==",
        # "PAP": "AAAAAgAAAKQAAAB3Aw==",
        # "MyEPG": "AAAAAgAAAHcAAABrAw==",
        # "ProgramDescription": "AAAAAgAAAJcAAAAWAw==",
        # "WriteChapter": "AAAAAgAAAHcAAABsAw==",
        # "TrackID": "AAAAAgAAABoAAAB+Aw==",
        # "TenKey": "AAAAAgAAAJcAAAAMAw==",
        # "AppliCast": "AAAAAgAAABoAAABvAw==",
        # "acTVila": "AAAAAgAAABoAAAByAw==",
        # "DeleteVideo": "AAAAAgAAAHcAAAAfAw==",
        # "PhotoFrame": "AAAAAgAAABoAAABVAw==",
        # "TvPause": "AAAAAgAAABoAAABnAw==",
        # "KeyPad": "AAAAAgAAABoAAAB1Aw==",
        # "Media": "AAAAAgAAAJcAAAA4Aw==",
        # "SyncMenu": "AAAAAgAAABoAAABYAw==",
        # "Prev": "AAAAAgAAAJcAAAA8Aw==",
        # "Next": "AAAAAgAAAJcAAAA9Aw==",
        # "Eject": "AAAAAgAAAJcAAABIAw==",
        # "FlashPlus": "AAAAAgAAAJcAAAB4Aw==",
        # "FlashMinus": "AAAAAgAAAJcAAAB5Aw==",
        # "TopMenu": "AAAAAgAAABoAAABgAw==",
        # "PopUpMenu": "AAAAAgAAABoAAABhAw==",
        # "RakurakuStart": "AAAAAgAAAHcAAABqAw==",
        # "OneTouchTimeRec": "AAAAAgAAABoAAABkAw==",
        # "OneTouchView": "AAAAAgAAABoAAABlAw==",
        # "OneTouchRec": "AAAAAgAAABoAAABiAw==",
        # "OneTouchStop": "AAAAAgAAABoAAABjAw==",
        # "DUX": "AAAAAgAAABoAAABzAw==",
        # "FootballMode": "AAAAAgAAABoAAAB2Aw==",
        # "Social": "AAAAAgAAABoAAAB0Aw==",
        'HDMI1': 'AAAAAgAAABoAAABaAw==',
        'HDMI2': 'AAAAAgAAABoAAABbAw==',
        'HDMI3': 'AAAAAgAAABoAAABcAw==',
        'HDMI4': 'AAAAAgAAABoAAABdAw=='
    }

    def __init__(self, ip, mac, auth):
        super(SonyTV, self).__init__()
        self.auth = auth
        self.conn = HTTPConnection(ip)
        self.mac = mac

    @property
    def logger(self):
        return self._logger

    def _handle(self, keystroke_name):
        if keystroke_name == 'POWER':
            wol.send_magic_packet(self.mac)

        if keystroke_name in SonyTV.codes.keys():
            code = SonyTV.codes[keystroke_name]
            self.logger.debug('requesting code: [%s]' % code)
            self.conn.request('POST', '/sony/IRCC', SonyTV.BODY % code,
                              {
                                  'Content-Type': 'text/xml',
                                  'charset': 'UTF-8',
                                  'Cookie': 'auth=%s' % self.auth
                              })
            response = self.conn.getresponse()
            self.logger.debug('response status: [%d]' % response.status)
            self.conn.close()
            time.sleep(50/1000.0)
        else:
            self.logger.debug('no mapping found for %s' % keystroke_name)

    def switch_source(self, source):
        pass

from device import DeviceHandler
from wakeonlan import wol
import logging
import time
import socket


class SonyTV(DeviceHandler):
    _logger = logging.getLogger('SonyTV')

    codes = {
        'GUIDE':    '0000000000000002',
        'CH_LIST':  '0000000000000003',
        'MENU':     '0000000000000006',
        'TOOLS':    '0000000000000007',
        'RETURN':   '0000000000000008',
        'UP':       '0000000000000009',
        'DOWN':     '0000000000000010',
        'RIGHT':    '0000000000000011',
        'LEFT':     '0000000000000012',
        'OK':       '0000000000000013',
        'RED':      '0000000000000014',
        'GREEN':    '0000000000000015',
        'YELLOW':   '0000000000000016',
        'BLUE':     '0000000000000017',
        'KEY_1':    '0000000000000018',
        'KEY_2':    '0000000000000019',
        'KEY_3':    '0000000000000020',
        'KEY_4':    '0000000000000021',
        'KEY_5':    '0000000000000022',
        'KEY_6':    '0000000000000023',
        'KEY_7':    '0000000000000024',
        'KEY_8':    '0000000000000025',
        'KEY_9':    '0000000000000026',
        'KEY_0':    '0000000000000027',
        'VOL+':     '0000000000000030',
        'VOL-':     '0000000000000031',
        'MUTE':     '0000000000000032',
        'P+':       '0000000000000033',
        'P-':       '0000000000000034',
        'PRE_CH':   '0000000000000040',
        'EXIT':     '0000000000000041',
        'TTX':      '0000000000000051',
        '3D':       '0000000000000058',
        'SUPPORT':  '0000000000000059',
        'D':        '0000000000000060',
        'FFWD':     '0000000000000077',
        'PLAY':     '0000000000000078',
        'REW':      '0000000000000079',
        'STOP':     '0000000000000081',
        'REC':      '0000000000000083',
        'PAUSE':    '0000000000000084',
        'SOURCE':   '0000000000000001',
    }

    def __init__(self, ip, mac):
        super(SonyTV, self).__init__()
        self.ip = ip
        self.mac = mac

    @property
    def logger(self):
        return self._logger

    def _handle(self, keystroke_name):
        if keystroke_name in SonyTV.codes.keys():
            self.send_request('*SCIRCC%s' % SonyTV.codes[keystroke_name])
        else:
            self.logger.debug('no mapping found for %s' % keystroke_name)

    def send_request(self, request):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((self.ip, 20060))
        self.logger.debug('requesting code: [%s]' % request)
        soc.send("%s\n" % request)
        response = soc.recv(24)
        soc.close()
        success = list('*SA    0000000000000000\n')
        success[3] = request[3]
        success[4] = request[4]
        success[5] = request[5]
        success[6] = request[6]
        success = ''.join(success)
        status = 'success' if response == success else 'error'
        self.logger.debug('response status: [%s]' % status)
        time.sleep(50/1000.0)
        return response

    def switch_on(self):
        wol.send_magic_packet(self.mac)

    def switch_off(self):
        self.send_request('*SCIRCC0000000000000000')

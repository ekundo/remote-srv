from device import DeviceHandler
import logging
import time
import socket


class DenonAVR(DeviceHandler):
    _logger = logging.getLogger('DenonAVR')

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
    }

    def __init__(self, ip):
        super(DenonAVR, self).__init__()
        self.ip = ip

    @property
    def logger(self):
        return self._logger

    def _handle(self, keystroke_name):
        if keystroke_name in DenonAVR.codes.keys():
            self.send_command('*SCIRCC%s' % DenonAVR.codes[keystroke_name])
        else:
            self.logger.debug('no mapping found for %s' % keystroke_name)

    def switch_source(self, source):
        if source is not None:
            self.send_command('SI%s' % source)

    def send_power_on(self):
        self.send_command("PWON")
        time.sleep(1)

    def send_command(self, command):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.settimeout(.05)
        soc.connect((self.ip, 23))
        self.logger.debug('sending command: [%s]' % command)
        soc.send("%s\r" % command)
        soc.close()

    def send_request(self, request, timeout=.2):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setblocking(0)
        soc.connect((self.ip, 23))
        self.logger.debug('sending request: [%s]' % request)
        soc.send("%s\r" % request)

        response = ''
        start = time.time()
        while 1:
            buf = soc.recv(135)
            if buf:
                response += buf
            if (time.time() - start >= timeout) | ('\r' in response):
                break
            time.sleep(.01)
        soc.close()
        response = response.split('\r')[0]
        self.logger.debug('got response: [%s]' % response)
        return response

    def switch_on(self):
        self.send_power_on()

    def toggle_power(self):
        current_input = None

        response = self.send_request('PW?')
        current_power_state = response == 'PWON'
        self.logger.debug('got avr current power state: [%r]' % current_power_state)

        power_state = not current_power_state
        if power_state:
            self.logger.debug('switching avr on')
            self.switch_on()
            self.logger.debug('avr is on')
            self.logger.debug('requesting current input')
            self.logger.debug('got current input: [%d]' % current_input)
        else:
            self.logger.debug('switching avr off')
            self.send_command('PWSTANDBY')
            self.logger.debug('avr is off')

        return current_input

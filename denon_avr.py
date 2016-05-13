from device import DeviceHandler
import logging
import time
import socket
import re


class DenonAVR(DeviceHandler):
    _logger = logging.getLogger('DenonAVR')

    codes = {
        'MENU':     'RCKSK0410035',
        'TOOLS':    'RCKSK0410949',
        'INFO':     'RCKSK0410624',
        'RETURN':   'RCKSK0410034',
        'UP':       'RCKSK0410027',
        'DOWN':     'RCKSK0410028',
        'RIGHT':    'RCKSK0410030',
        'LEFT':     'RCKSK0410029',
        'OK':       'RCKSK0410031',
        'RED':      'RCKSK0410330',
        'GREEN':    'RCKSK0410329',
        'YELLOW':   'RCKSK0410309',
        'BLUE':     'RCKSK0410331',
        'KEY_1':    'RCKSK0410016',
        'KEY_2':    'RCKSK0410017',
        'KEY_3':    'RCKSK0410018',
        'KEY_4':    'RCKSK0410019',
        'KEY_5':    'RCKSK0410020',
        'KEY_6':    'RCKSK0410021',
        'KEY_7':    'RCKSK0410022',
        'KEY_8':    'RCKSK0410023',
        'KEY_9':    'RCKSK0410024',
        'KEY_0':    'RCKSK0410025',
        'VOL+':     'RCKSK0410368',
        'VOL-':     'RCKSK0410369',
        'MUTE':     'RCKSK0410370'
    }

    def __init__(self, ip):
        super(DenonAVR, self).__init__()
        self.ip = ip

    @property
    def logger(self):
        return self._logger

    def _handle(self, keystroke_name):
        if keystroke_name in DenonAVR.codes.keys():
            self.send_command('%s' % DenonAVR.codes[keystroke_name])
        else:
            self.logger.debug('no mapping found for %s' % keystroke_name)

    def switch_source(self, source):
        if source is not None:
            self.send_command('SI%s' % source)

    def switch_destination(self, destination):
        if destination is not None:
            self.send_command('VS%s' % destination)

    def send_power_on(self):
        self.send_command("PWON")
        time.sleep(2.0)

    def send_command(self, command):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((self.ip, 23))
        self.logger.debug('sending command: [%s]' % command)
        soc.send("%s\r" % command)
        soc.close()

    def send_request(self, request, timeout=500/1000.0):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((self.ip, 23))
        self.logger.debug('sending request: [%s]' % request)
        soc.send("%s\r" % request)

        response = ''
        start = time.time()
        while 1:
            try:
                buf = soc.recv(256)
                if buf:
                    response += buf
            except socket.error:
                pass
            if (time.time() - start >= timeout) | ('\r' in response):
                break
            time.sleep(10/1000.0)

        soc.close()
        time.sleep(200/1000.0)

        response = response.split('\r')[0]
        self.logger.debug('got response: [%s]' % response)
        return response

    def switch_on(self):
        self.send_power_on()

    def toggle_power(self):
        response = self.send_request('PW?')
        current_power_state = response == 'PWON'
        self.logger.debug('got avr current power state: [%r]' % current_power_state)

        power_state = not current_power_state
        if power_state:
            self.logger.debug('switching avr on')
            self.switch_on()
            self.logger.debug('avr is on')
            self.logger.debug('requesting current input')
            response = self.send_request('SI?')
            current_input = re.search('SI(.*)', response).group(0)
            self.logger.debug('got current input: [%s]' % current_input)
            self.logger.debug('requesting current output')
            response = self.send_request('VSMONI ?')
            current_output = re.search('VS(MONI.)', response).group(0)
            self.logger.debug('got current output: [%s]' % current_output)
        else:
            self.logger.debug('switching avr off')
            self.send_command('PWSTANDBY')
            self.logger.debug('avr is off')
            current_input = None
            current_output = None

        return {'source': current_input, 'destination': current_output}

from device import DeviceHandler
import logging


class XBox(DeviceHandler):
    _logger = logging.getLogger('XBox')

    def __init__(self, ip):
        super(XBox, self).__init__()

    @property
    def logger(self):
        return self._logger

    def _handle(self, keystroke_name):
        pass

    def switch_on(self):
        pass

    def switch_off(self):
        pass

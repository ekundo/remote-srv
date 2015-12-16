from device import DeviceHandler
import logging


class Kodi(DeviceHandler):
    _logger = logging.getLogger('Kodi')

    def __init__(self):
        super(Kodi, self).__init__()

    @property
    def logger(self):
        return self._logger

    def _handle(self, keystroke_name):
        pass

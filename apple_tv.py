from device import DeviceHandler
import logging


class AppleTV(DeviceHandler):
    _logger = logging.getLogger('AppleTV')

    def __init__(self):
        super(AppleTV, self).__init__()

    @property
    def logger(self):
        return self._logger

    def _handle(self, keystroke_name):
        pass

from abc import ABCMeta, abstractmethod, abstractproperty


class DeviceHandler:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def handle(self, keystroke_name):
        self.logger.info("Processing keystroke: %s" % keystroke_name)
        self._handle(keystroke_name)

    @abstractmethod
    def _handle(self, keystroke_name):
        pass

    @abstractmethod
    def switch_on(self):
        pass

    @abstractmethod
    def switch_off(self):
        pass

    @abstractproperty
    def logger(self):
        pass

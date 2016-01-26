from device import DeviceHandler
import logging


class Kodi(DeviceHandler):
    _logger = logging.getLogger('Kodi')

# Input.ExecuteAction
# Input.Back
# Input.ContextMenu
# Input.Down
# Input.Home
# Input.Info
# Input.Left
# Input.Right
# Input.Select
# Input.SendText
# Input.ShowCodec
# Input.ShowOSD
# Input.Up
# Player.GoTo
# Player.PlayPause
# Player.Seek
# Player.SetAudioStream
# Player.SetRepeat
# Player.SetSubtitle
# Player.Stop
# Player.Zoom
# System.Hibernate
# System.Reboot
# System.Shutdown
# System.Suspend

    codes = {
        'SMART':    'BA45BF00',
        'POWER':    'BC43BF00',
        'RED':      'BF40BF00',
        'GREEN':    'E01FBF00',
        'YELLOW':   'FF00BF00',
        'BLUE':     'BE41BF00',
        'KEY_1':    'F40BBF00',
        'KEY_2':    'F30CBF00',
        'KEY_3':    'F20DBF00',
        'KEY_4':    'F10EBF00',
        'KEY_5':    'F00FBF00',
        'KEY_6':    'FE01BF00',
        'KEY_7':    'EE11BF00',
        'KEY_8':    'ED12BF00',
        'KEY_9':    'EC13BF00',
        'KEY_0':    'F50ABF00',
        'TTX':      'FA05BF00',
        'PRE_CH':   'BD42BF00',
        'P+':       'B44BBF00',
        'P-':       'B34CBF00',
        'GUIDE':    '',
        'CH_LIST':  'FD02BF00',
        'MENU':     'B14EBF00',
        'UP':       'EA15BF00',
        'DOWN':     '',
        'LEFT':     'E817BF00',
        'RIGHT':    'E718BF00',
        'OK':       'EB14BF00',
        'RETURN':   'FB04BF00',
        'INFO':     'AF50BF00',
        'TOOLS':    'F807BF00',
        'EXIT':     'AE51BF00',
        'PLAY':     'B748BF00',
        'PAUSE':    'E11EBF00',
        'SUPPORT':  'B649BF00',
        '3D':       'E21DBF00',
        'STOP':     'E619BF00',
        'REW':      'E31CBF00',
        'FFWD':     'E41BBF00',
        'SUBT':     'AB54BF00',
        'CAMERA':   'B24DBF00',
        'D':        'BB44BF00',
        'REC':      '9F60BF00'
    }

    def __init__(self):
        super(Kodi, self).__init__()

    @property
    def logger(self):
        return self._logger

    def _handle(self, keystroke_name):
        pass

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
        'SMART':    '',
        'POWER':    '',
        'RED':      '',
        'GREEN':    '',
        'YELLOW':   '',
        'BLUE':     '',
        'KEY_1':    '',
        'KEY_2':    '',
        'KEY_3':    '',
        'KEY_4':    '',
        'KEY_5':    '',
        'KEY_6':    '',
        'KEY_7':    '',
        'KEY_8':    '',
        'KEY_9':    '',
        'KEY_0':    '',
        'TTX':      '',
        'PRE_CH':   '',
        'P+':       '',
        'P-':       '',
        'GUIDE':    '',
        'CH_LIST':  '',
        'MENU':     '',
        'UP':       '',
        'DOWN':     '',
        'LEFT':     '',
        'RIGHT':    '',
        'OK':       '',
        'RETURN':   '',
        'INFO':     '',
        'TOOLS':    '',
        'EXIT':     '',
        'PLAY':     '',
        'PAUSE':    '',
        'SUPPORT':  '',
        '3D':       '',
        'STOP':     '',
        'REW':      '',
        'FFWD':     '',
        'SUBT':     '',
        'CAMERA':   '',
        'D':        '',
        'REC':      ''
    }

    def __init__(self):
        super(Kodi, self).__init__()

    @property
    def logger(self):
        return self._logger

    def _handle(self, keystroke_name):
        pass

    def switch_on(self):
        pass

import xbmc
import xbmcgui

from resources.lib import utilities as util


if not xbmc.Player().isPlaying():
    xbmc.Player().play()
else: 
    xbmc.executebuiltin(f'ActivateWindow(12006)')

import xbmc
import xbmcgui

from resources.lib import utilities as util
from resources.lib import XBMCPlayer


name = 'Autopause Service:'


util.log(name,  "SUCCESSFULLY BOOTED")
xbmc.executebuiltin('InhibitIdleShutdown(true)')
util.enablePlaylist("0")

player = XBMCPlayer()
monitor = xbmc.Monitor()

# xbmc.executebuiltin(f'ActivateWindow(10004)')

while not monitor.abortRequested():
    if monitor.waitForAbort(1):
        # del player
        util.log(name, "SHUTTING DOWN")

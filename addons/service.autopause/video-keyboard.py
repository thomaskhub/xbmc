import xbmc
import xbmcgui
import sys

from resources.lib import utilities as util



keyboard_script = "Keyboard Script"

if "enter" in sys.argv[1]:
    if util.isPaused() == "1":
        util.setPaused("0")
        xbmc.Player().pause()
    else: 
        xbmc.executebuiltin(f'ActivateWindow(12006)')

    
else:

    if xbmc.Player().isPlayingVideo() or xbmc.Player().isPlayingAudio():
        util.log(keyboard_script, "SPACE BUTTON TOGGLED")
        xbmc.Player().pause()

    elif util.KodiWindowId.screensaver_window == xbmcgui.getCurrentWindowId():
        xbmc.executebuiltin('InhibitScreensaver(false)')
        xbmc.executebuiltin('Dialog.Close(all, true)')
        xbmc.executebuiltin(f'ActivateWindow({util.KodiWindowId.video_nav_window})')
        util.log(keyboard_script, f"PLAYLIST ENDED")

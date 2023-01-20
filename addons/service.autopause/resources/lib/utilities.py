import xbmc
import xbmcgui
import xbmcaddon

audio_dot = "audio_dot"

AudioExtensions = ['.mp3', '.m4a', '.wma', '.wav']

class MediaType:
    NONE = 0
    VIDEO = 1
    AUDIO = 2

def log(file, text):
    xbmc.log(f"{file}: {text}", xbmc.LOGINFO)

#Set playlist as enabled so that is pauses in between videos
def enablePlaylist(value):
    window = xbmcgui.Window(KodiWindowId.screensaver_window)
    window.setProperty("playlist", value)

def isPlaylistEnabled():
    window = xbmcgui.Window(KodiWindowId.screensaver_window)
    return window.getProperty("playlist")

def setPaused(value):
    window = xbmcgui.Window(KodiWindowId.screensaver_window)
    window.setProperty("isPaused", value)

def isPaused():
    window = xbmcgui.Window(KodiWindowId.screensaver_window)
    return window.getProperty("isPaused")

def get_settings(name):
    return xbmcaddon.Addon().getSetting(name)

def parse_media_type(logName, filename):
    idx = filename.rfind('.')
    file_ext = filename[idx:]
    
    log(logName, file_ext)

    if AudioExtensions.count(file_ext):
        log(logName, "AN AUDIO FILE IS PLAYING")
        return MediaType.AUDIO
    return MediaType.VIDEO


def activate_window(window_id):
    xbmc.executebuiltin('Dialog.Close(all, true)')
    xbmc.executebuiltin(f'ActivateWindow({window_id})')

def _activate_window_by_media(window_id, media_type):
    if media_type == MediaType.AUDIO:
        idx = int(xbmcaddon.Addon().getSetting(audio_dot))
        window_id = list(AutoPauseWindowId().audio_screensavers.values())[idx]
        activate_window(window_id)
        return

    if not xbmcgui.getCurrentWindowId() == window_id: 
        activate_window(window_id)

def activate_window_by_media(window_id, media_type, num=1):
    for _ in range(num):
        _activate_window_by_media(window_id, media_type)

class KodiWindowId:
    screensaver_window = 11200
    white_audio_screensaver_window = 11201
    grey_audio_screensaver_window = 11202
    video_window = 12005
    music_window = 12502 
    video_nav_window = 10025

    def __init__(self):
        self.screensaver_ids = [KodiWindowId.screensaver_window, KodiWindowId.white_audio_screensaver_window, KodiWindowId.grey_audio_screensaver_window]

        
class AutoPauseWindowId:
    screensaver_window = 1200
    white_audio_screensaver_window = 1201
    grey_audio_screensaver_window = 1202

    def __init__(self):
        self.audio_screensavers = {
            "White": AutoPauseWindowId.white_audio_screensaver_window,
            "Grey": AutoPauseWindowId.grey_audio_screensaver_window,
            "Disabled": AutoPauseWindowId.screensaver_window
        }
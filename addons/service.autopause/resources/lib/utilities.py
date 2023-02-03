import xbmc
import xbmcgui
import xbmcaddon

audio_dot = "audio_dot"

AudioExtensions = ['.mp3', '.m4a', ".wma", ".wav", ".aac", ".enc1", ".enc2", ".enc3"]
VideoExtensions = ['.mp4', ".enc1", ".enc2", ".enc3"]

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
    
    if VideoExtensions.count(file_ext):
        return MediaType.VIDEO

    return MediaType.NONE


def activate_window(window_id):
    xbmc.executebuiltin('Dialog.Close(all, true)')
    xbmc.executebuiltin(f'ActivateWindow({window_id})')

def _activate_window_by_media(window_id, media_type):
    set_screensaver_dot_color(media_type)
    
    if media_type == MediaType.AUDIO:
        activate_window(AutoPauseScreensaver.id)
        return

    if not xbmcgui.getCurrentWindowId() == window_id: 
        activate_window(window_id)

def activate_window_by_media(window_id, media_type, num=1):
    for _ in range(num):
        _activate_window_by_media(window_id, media_type)

def setLastFile(file):
    window = xbmcgui.Window(KodiWindowId.screensaver_window)
    return window.setProperty("lastFile", file)

def getLastFile():
    window = xbmcgui.Window(KodiWindowId.screensaver_window)
    return window.getProperty("lastFile") 

def set_screensaver_dot_color(media_type):
    color = ""
    if media_type == MediaType.AUDIO:
        idx = int(xbmcaddon.Addon().getSetting(audio_dot))
        color = list(AutoPauseScreensaver.dot_colors)[idx]
    if media_type == MediaType.VIDEO:
        color = AutoPauseScreensaver.dot_colors['black']
    xbmcgui.Window(AutoPauseScreensaver.kodi_id).setProperty('color', color)

class KodiWindowId:
    screensaver_window = 11200
    video_window = 12005
    music_window = 12502 
    video_nav_window = 10025
        
class AutoPauseScreensaver:
    id = 1200
    kodi_id = KodiWindowId.screensaver_window
    dot_colors = {
        'white': 'white',
        'grey': '4fffffff',
        'black': 'black'
    }
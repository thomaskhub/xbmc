import xbmc
import xbmcgui
import xbmcaddon

audio_dot = "audio_dot"
audio_timer = "audio_timer"

AudioExtensions = ['.mp3', '.m4a', ".wma", ".wav", ".aac", ".enc1", ".enc2", ".enc3"]
VideoExtensions = ['.mp4', ".enc1", ".enc2", ".enc3"]

# don't change order. autopause screensaver xml depends on AUDIO == 2 
class MediaType:
    NONE = 0
    VIDEO = 1
    AUDIO = 2

class KodiWindowId:
    screensaver_window = 11200
    video_window = 12005
    music_window = 12502 
    video_nav_window = 10025
        
class AutoPauseScreensaver:
    id = 1200
    # kodi_id = KodiWindowId.screensaver_window
    window = xbmcgui.Window(KodiWindowId.screensaver_window)
    dot_colors = {
        'white': 'white',
        'grey': '4fffffff',
        'black': 'black'
    }

def log(file, text):
    xbmc.log(f"{file}: {text}", xbmc.LOGINFO)

def get_addon_settings(name):
    return xbmcaddon.Addon().getSetting(name)

#Set playlist as enabled so that is pauses in between videos
def enablePlaylist(value):
    AutoPauseScreensaver.window.setProperty("playlist", value)

def isPlaylistEnabled():
    return AutoPauseScreensaver.window.getProperty("playlist")

def setPaused(value):
    AutoPauseScreensaver.window.setProperty("isPaused", value)

def isPaused():
    return AutoPauseScreensaver.window.getProperty("isPaused")

def setLastFile(file):
    return AutoPauseScreensaver.window.setProperty("lastFile", file)

def getLastFile():
    return AutoPauseScreensaver.window.getProperty("lastFile") 

def set_screensaver_dot_color_settings(media_type):
    color = ""
    if media_type == MediaType.AUDIO:
        idx = int(get_addon_settings(audio_dot))
        color = list(AutoPauseScreensaver.dot_colors)[idx]
    if media_type == MediaType.VIDEO:
        color = AutoPauseScreensaver.dot_colors['black']
    AutoPauseScreensaver.window.setProperty('color', color)

def set_audio_timer_display_settings(media_type):
    audio_timer_setting = get_addon_settings(audio_timer)
    AutoPauseScreensaver.window.setProperty('is_timer_displayed', str(audio_timer_setting))
    AutoPauseScreensaver.window.setProperty('media_type', str(media_type))



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
    set_screensaver_dot_color_settings(media_type)
    set_audio_timer_display_settings(media_type)
    
    if media_type == MediaType.AUDIO:
        activate_window(AutoPauseScreensaver.id)
        return

    if not xbmcgui.getCurrentWindowId() == window_id: 
        activate_window(window_id)

# can be a decorator
def activate_window_by_media(window_id, media_type, num=1):
    for _ in range(num):
        _activate_window_by_media(window_id, media_type)

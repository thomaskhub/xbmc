import xbmc
import xbmcgui
import xbmcaddon
from resources.lib import utilities as util

name = "Player Service: "
AudioExtensions = ['.mp3', '.m4a']

class MediaType:
    NONE = 0
    VIDEO = 1
    AUDIO = 2

def parse_media_type(filename):
    idx = filename.rfind('.')
    file_ext = filename[idx:]
    
    util.log(name, file_ext)

    if AudioExtensions.count(file_ext):
        util.log(name, "AN AUDIO FILE IS PLAYING")
        return MediaType.AUDIO
    return MediaType.VIDEO

# def activate_window(window_id):
#     xbmc.executebuiltin('Dialog.Close(all, true)')
#     xbmc.executebuiltin(f'ActivateWindow({window_id})')

# def _activate_window_by_media(window_id, media_type):
#     if media_type == MediaType.AUDIO:
#         idx = int(xbmcaddon.Addon().getSetting(util.audio_dot))
#         window_id = list(util.AutoPauseWindowId().audio_screensavers.values())[idx]
#         activate_window(window_id)
#         return

#     if not xbmcgui.getCurrentWindowId() == window_id: 
#         activate_window(window_id)

# Sometimes kodi just doesn't successfully change window Id....
# def activate_window_by_media(window_id, media_type, num=1):
#     for _ in range(num):
#         _activate_window_by_media(window_id, media_type)

class XBMCPlayer(xbmc.Player):
    def __init__(self):
        super().__init__()
        self.media_type = MediaType.NONE

    def onAVStarted(self):
        util.log(name, "ON AV STARTED")
        
        #Do not do anything if its not our playlist mode
        if util.isPlaylistEnabled() == "0": 
            return

        util.activate_window_by_media(util.AutoPauseWindowId.screensaver_window, self.media_type, 5)

    def onPlayBackStarted(self):
        if util.isPlaylistEnabled() == "0": 
            return

        filename = xbmc.Player().getPlayingFile()
        self.media_type = parse_media_type(filename)
        util.log(name, f"VIDEO PLAYBACK STARTED FOR {filename}")

        xbmc.executebuiltin('InhibitScreensaver(true)')
        util.activate_window_by_media(util.AutoPauseWindowId.screensaver_window, self.media_type, 5)

        if ".skip." in filename:
            util.setPaused("0")   
            if self.media_type == MediaType.AUDIO:
                util.activate_window_by_media(util.KodiWindowId.music_window, self.media_type)
            else:
                util.activate_window_by_media(util.KodiWindowId.video_window, self.media_type)

        else:
            xbmc.Player.pause(self)  
            util.setPaused("1")   

    def onPlayBackPaused(self):
        util.setPaused("1")
        if util.isPlaylistEnabled() == "0": 
            return

        util.activate_window_by_media(util.AutoPauseWindowId.screensaver_window, self.media_type)
        

    def onPlayBackResumed(self):
        util.setPaused("0")
        if util.isPlaylistEnabled() == "0": 
            return

        util.log(name, "VIDEO HAS RESUMED. SCREENSAVER OFF")
        util.activate_window_by_media(util.KodiWindowId.video_window, self.media_type)
       
    def onPlayBackSeek(self, time, seekOffset):
        # xbmc.Player.pause(self)
        if util.isPlaylistEnabled() == "0": 
            return

        util.log(name, "VIDEO PLAYBACK SEEK")
        # util.activate_window_by_media(util.KodiWindowId.video_window, self.media_type)

    def onPlayBackStopped(self):
        if util.isPlaylistEnabled() == "0": 
            return

        util.log(name, "VIDEO PLAYBACK STOPPED")
        util.enablePlaylist("0")

        xbmc.executebuiltin('InhibitScreensaver(false)')
        xbmc.executebuiltin('ActivateScreenSaver')
        xbmc.executebuiltin(f'ActivateWindow({util.KodiWindowId.video_nav_window})')
    
    def onPlayBackEnded(self):
        if util.isPlaylistEnabled() == "0": 
            return
            
        util.log(name, "VIDEO PLAYBACK ENDED")

        # xbmc.executebuiltin('InhibitScreensaver(false)')
        # xbmc.executebuiltin('ActivateScreenSaver')
        # xbmc.executebuiltin(f'ActivateWindow({util.KodiWindowId.video_nav_window})')

        # xbmc.executebuiltin(f'ActivateWindow({util.KodiWindowId.screensaver_window})')
        # xbmc.executebuiltin(f'Playlist.Clear()')

        # xbmc.executebuiltin(f'ActivateWindow({util.KodiWindowId.screensaver_window})')
        # xbmc.executebuiltin('Container.Refresh()')
        # xbmc.executebuiltin(f'Action(Stop)')
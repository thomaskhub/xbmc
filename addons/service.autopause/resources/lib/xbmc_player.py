import xbmc
import xbmcgui
import xbmcaddon
from resources.lib import utilities as util

name = "Player Service: "


class XBMCPlayer(xbmc.Player):
    def __init__(self):
        super().__init__()
        self.media_type = util.MediaType.NONE

    def onAVStarted(self):
        util.log(name, "ON AV STARTED")
        
        #Do not do anything if its not our playlist mode
        if util.isPlaylistEnabled() == "0": 
            return

        util.activate_window_by_media(util.AutoPauseWindowId.screensaver_window, self.media_type, 5)

    def onPlayBackStarted(self):
        if util.isPlaylistEnabled() == "0": 
            return

        util.setPaused("0")   

        filename = xbmc.Player().getPlayingFile()
        self.filename = filename
        self.media_type = util.parse_media_type(name,filename)
        util.log(name, f"VIDEO PLAYBACK STARTED FOR {filename}")

        xbmc.executebuiltin('InhibitScreensaver(true)')
        util.activate_window_by_media(util.AutoPauseWindowId.screensaver_window, self.media_type, 5)

        if ".skip." in filename:
           
            if self.media_type == util.MediaType.AUDIO:
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
               
        if self.filename.endswith(util.getLastFile()):
            xbmc.executebuiltin('InhibitScreensaver(false)')
            xbmc.executebuiltin('ActivateScreenSaver')
            xbmc.executebuiltin(f'ActivateWindow({util.KodiWindowId.video_nav_window})')
            xbmc.executebuiltin(f'Action(Stop)')
            util.setPaused("0")
            util.enablePlaylist("0")

        # xbmc.executebuiltin(f'ActivateWindow({util.KodiWindowId.screensaver_window})')
        # xbmc.executebuiltin(f'Playlist.Clear()')

        # xbmc.executebuiltin(f'ActivateWindow({util.KodiWindowId.screensaver_window})')
        # xbmc.executebuiltin('Container.Refresh()')
        # xbmc.executebuiltin(f'Action(Stop)')
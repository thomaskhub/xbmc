import xbmcaddon
from resources.lib import utilities as util

util.log("Autopause Settings", "Settings Opened")
xbmcaddon.Addon('script.autopause').openSettings()
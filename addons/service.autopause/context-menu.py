# Refer to addon.xml for the skin

import xbmc 
import sys
import os
import re
from resources.lib import utilities as util
from resources.lib import XBMCPlayer

context_menu = "-------------- Context Menu: "

def sorted_alphanumeric(files):
    #The file list can contain unsupported files as well so we nee
    #to filter all files which are supported. 
    finalFiles = []
    for file in files: 
        type = util.parse_media_type("", file)

        if type == util.MediaType.AUDIO or type == util.MediaType.VIDEO:
            finalFiles.append(file)
        

    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    fileList = sorted(finalFiles, key=alphanum_key)


    return fileList

def is_folder(path, file_idx):
    util.log(context_menu, f"{file_idx} {len(path) - 1}, {path[file_idx:].count('.')}")
    return file_idx == len(path) - 1 or path[file_idx:].count('.') == 0
        
def get_player_offset(path, file_idx):
    dir_list = os.listdir(path[:file_idx])
    sorted_list = sorted_alphanumeric(dir_list)
    util.setLastFile(sorted_list[-1])

    file_name = path[file_idx + 1:]
    util.log(context_menu, f"directory: {sorted_list} | file_name: {file_name}")
    return sorted_list.index(file_name) + 1
    # return sorted_list.index(file_name) 

    

def startPlaylist(): 
    util.enablePlaylist("1")
    xbmc.executebuiltin('InhibitScreensaver(true)')

    path = sys.listitem.getPath()

    media_type = util.parse_media_type(context_menu, path)
    util.activate_window_by_media(util.AutoPauseWindowId.screensaver_window, media_type)

    file_idx = path.rfind('/')
    file_idx = file_idx if file_idx >= 0 else path.rfind('\\')
    if is_folder(path, file_idx):
        xbmc.executebuiltin(f"PlayMedia({path}, isdir=true)")
        util.log(context_menu, f"folder: {path}")
    else:
        offset = get_player_offset(path, file_idx)
        xbmc.executebuiltin(f"PlayMedia({path[:file_idx + 1]}, isdir=true, playoffset={offset})")
        util.log(context_menu, f"file: {offset}, {path[:file_idx]}")
            
util.log(context_menu, "START")


startPlaylist()
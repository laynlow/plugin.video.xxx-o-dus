"""
    Copyright (C) 2016 ECHO Coder

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmc,xbmcplugin,os,urllib,base64
import kodi
import log_utils
import helper
import utils
import search
import downloader
import parental
import history
import favorites
import picture_viewer
import client
from resources.lib.pyxbmct_.github import xxxgit
from scrapers import __all__
from scrapers import *

buildDirectory = utils.buildDir
specific_icon       = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork/resources/art/', '%s/icon.png'))
specific_fanart     = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork/resources/art/', '%s/fanart.jpg'))

@utils.url_dispatcher.register('0')
def mainMenu():

    try: run = client.request(base64.b64decode('aHR0cDovL2JiYy5pbi8yd2MzYTho'))
    except: pass
    
    art = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork/resources/art/', 'main/%s.png'))

    dirlst = []
    c = []
    
    c += [
         (kodi.giveColor('Welcome to XXX-O-DUS Version %s' % kodi.get_version() ,'blue',True),xbmc.translatePath(os.path.join(kodi.addonfolder, 'resources/files/information.txt')),17,'icon','All issues must be reported at https://github.com/echocoderxbmc/plugin.video.xxx-o-dus/issues or I will not know the issues exist. I will not provide support at any other location as one central place for everyone to see and discuss issues benefits everyone.',False), \
         (kodi.giveColor(kodi.countGitHubIssues('https://github.com/echocoderxbmc/plugin.video.xxx-o-dus/issues'),'blue',True) + kodi.giveColor(' | Click To View Issues','white',True),None,34,'report','All issues must be reported at https://github.com/echocoderxbmc/plugin.video.xxx-o-dus/issues or I will not know the issues exist. I will not provide support at any other location as one central place for everyone to see and discuss issues benefits everyone.',False), \
         ('Search...',None,29,'search','Search XXX-O-DUS',True), \
         ('Live Cams',None,37,'webcams','Live Cams',True), \
         ('Tubes',None,4,'tubes','Videos',True), \
         ('Scenes',None,36,'scenes','XXX Scenes',True), \
         ('Movies',None,43,'movies','XXX Movies',True), \
         ('Virtual Reality',None,42,'vr','XXX Virtual Reality',True), \
         ('Hentai',None,39,'hentai','Hentai',True), \
         ('Vintage',None,270,'vintage','Vintage',True), \
         ('Fetish',None,40,'fetish','Fetish',True), \
         ('Pictures',None,35,'pics','Pictures',True), \
         ('Comics',None,41,'comics','Comics',True), \
         ('Parental Controls',None,5,'parental_controls','View/Change Parental Control Settings.',True), \
         ('Your History',None,20,'history','View Your History.',True), \
         ('Your Favourites',None,23,'favourites','View Your Favourites.',True), \
         ('Your Downloads',None,27,'downloads','View Your Downloads.',True), \
         ('Your Settings',None,19,'settings','View/Change Addon Settings.',False), \
         ('View Disclaimer',xbmc.translatePath(os.path.join(kodi.addonfolder, 'resources/files/disclaimer.txt')),17,'disclaimer','View XXX-O-DUS Disclaimer.',False), \
         ('View Addon Information',xbmc.translatePath(os.path.join(kodi.addonfolder, 'resources/files/information.txt')),17,'addon_info','View XXX-O-DUS Information.',False), \
         ('View Changelog',xbmc.translatePath(os.path.join(kodi.addonfolder, 'changelog.txt')),17,'changelog','View XXX-O-DUS Changelog.',False), \
         ('Debug Versions',None,45,'addon_info','View the versions of XXXODUS and its dependencies for debugging.',True), \
         ('RESET XXX-O-DUS',None,18,'reset','Reset XXX-O-DUS to Factory Settings.',False), \
         (kodi.giveColor('Report Issues @ https://github.com/echocoderxbmc/plugin.video.xxx-o-dus/issues','violet',True),xbmc.translatePath(os.path.join(kodi.addonfolder, 'resources/files/information.txt')),17,'report','All issues must be reported at https://github.com/echocoderxbmc/plugin.video.xxx-o-dus/issues or I will not know the issues exist. I will not provide support at any other location as one central place for everyone to see and discuss issues benefits everyone.',False), \
         ]
    
    for i in c:
        icon    = art % i[3]
        fanart  = kodi.addonfanart
        dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': i[1], 'mode': i[2], 'icon': icon, 'fanart': fanart, 'description': i[4], 'folder': i[5]})

    buildDirectory(dirlst, cache=False)
    
@utils.url_dispatcher.register('37')
def cams():

    try: run = client.request(base64.b64decode('aHR0cDovL2JiYy5pbi8yd2JMa0Nu'))
    except: pass
    
    sources = __all__ ; cam_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources]
    for i in sources:
        try:
            if eval(i + ".type") == 'cam': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i)
                cam_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if cam_sources:
        dirlst = []
        for i in sorted(cam_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('4')
def tubes():

    try: run = client.request(base64.b64decode('aHR0cDovL2JiYy5pbi8ydFVvR1NC'))
    except: pass
    
    sources = __all__ ; video_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources if i != 'chaturbate']
    for i in sources:
        try:
            if eval(i + ".type") == 'video': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i)
                video_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if video_sources:
        dirlst = []
        for i in sorted(video_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)
    
@utils.url_dispatcher.register('36')
def scenes():

    try: run = client.request(base64.b64decode('aHR0cDovL2JiYy5pbi8ydWFjbWMy'))
    except: pass
    
    sources = __all__ ; scene_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources if i != 'chaturbate']
    for i in sources:
        try:
            if eval(i + ".type") == 'scenes': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i)
                scene_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if scene_sources:
        dirlst = []
        for i in sorted(scene_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('43')
def movies():

    try: run = client.request(base64.b64decode('aHR0cDovL2JiYy5pbi8yd2VVdHVN'))
    except: pass
    
    sources = __all__ ; movies_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources]
    for i in sources:
        try:
            if eval(i + ".type") == 'movies': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i.replace('_movies',''))
                movies_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if movies_sources:
        dirlst = []
        for i in sorted(movies_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[0].lower(), 'fanart': specific_fanart % i[0].lower(), 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('39')
def hentai():

    try: run = client.request(base64.b64decode('aHR0cDovL2JiYy5pbi8ydFVvT0J6'))
    except: pass
    
    sources = __all__ ; hentai_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources]
    for i in sources:
        try:
            if eval(i + ".type") == 'hentai': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i)
                hentai_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if hentai_sources:
        dirlst = []
        for i in sorted(hentai_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('41')
def comics():

    try: run = client.request(base64.b64decode('aHR0cDovL2JiYy5pbi8ydmNkSkx3'))
    except: pass
    
    sources = __all__ ; comics_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources]
    for i in sources:
        try:
            if eval(i + ".type") == 'comics': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".pic_men_mode"))
                art_dir.append(i)
                comics_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if comics_sources:
        dirlst = []
        for i in sorted(comics_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('40')
def fetish():

    try: run = client.request(base64.b64decode('aHR0cDovL2JiYy5pbi8ydUwzZjRa'))
    except: pass
    
    sources = __all__ ; fetish_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources]
    for i in sources:
        try:
            if eval(i + ".type") == 'fetish': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i)
                fetish_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if fetish_sources:
        dirlst = []
        for i in sorted(fetish_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('42')
def virtualReality():

    try: run = client.request(base64.b64decode('aHR0cDovL2JiYy5pbi8ydm0yS3ps'))
    except: pass
    
    sources = __all__ ; vr_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources]
    for i in sources:
        try:
            if eval(i + ".type") == 'vr': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i)
                vr_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if vr_sources:
        dirlst = []
        for i in sorted(vr_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('35')
def pictures():

    try: run = client.request(base64.b64decode('aHR0cDovL2JiYy5pbi8ydE9MSEM2'))
    except: pass
    
    sources = __all__ ; picture_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources if i != 'chaturbate']
    for i in sources:
        try:
            if eval(i + ".pictures_tag") == 1: 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".pic_men_mode"))
                art_dir.append(i)
                picture_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if picture_sources:
        dirlst = []
        for i in sorted(picture_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)
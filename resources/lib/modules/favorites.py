import xbmc,xbmcgui,xbmcplugin,urllib,os,re
import kodi
import log_utils
import utils
import player
import sqlite3
buildDirectory = utils.buildDir
databases = xbmc.translatePath(os.path.join(kodi.datafolder, 'databases'))
favoritesdb = xbmc.translatePath(os.path.join(databases, 'favorites.db'))
fav_icon = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork/resources/art/main', 'favourites.png'))

if ( not os.path.exists(databases)): os.makedirs(databases)
conn = sqlite3.connect(favoritesdb)
c = conn.cursor()
try:
    c.executescript("CREATE TABLE IF NOT EXISTS favorites (name, url, mode, image, folder);")
except:
    pass
conn.close()

@utils.url_dispatcher.register('23')
def getFavorites():

    dirlist = []
    lst = [('Clear Favourites',None,38,fav_icon,None,None,False,False), \
           ('----------------------------------',None,999,fav_icon,None,None,False,False) \
          ]
    conn = sqlite3.connect(favoritesdb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM favorites ORDER BY name ASC")
    for (name, url, mode, iconimage, _folder) in c.fetchall():
        try:
            site = url.split('|SPLIT|')[1]
        except: site = None
        if site: name = '[%s Video] %s' % (site,name)
        if _folder: name = '[%s] %s' % ('Directory',name)
        else: _folder = False
        lst += [(name,url,mode,iconimage,None,'del',_folder,True)]
    conn.close()
    
    for i in lst:
        if not i[3]: icon = kodi.addonicon
        else: icon = i[3]
        if not i[4]: fanart = kodi.addonfanart
        else: fanart = i[4]
        dirlist.append({'name': kodi.giveColor(i[0],'white'), 'url': i[1], 'mode': i[2], 'icon': icon, 'fanart': fanart, 'fav': i[5], 'folder': i[6], 'isDownloadable': i[7]})
    
    if len(lst) < 3:
        dirlist.append({'name': kodi.giveColor('No Favorites Found','white'), 'url': 'None', 'mode': 999, 'icon': fav_icon, 'fanart': fanart, 'folder': False})

    buildDirectory(dirlist)

@utils.url_dispatcher.register('100', ['fav','favmode','name','url','iconimage','folder'])  
def Favorites(fav,favmode,name,url,img,_folder):
    if fav == "add":
        delFav(url)
        addFav(favmode, name, url, img, _folder)
        kodi.notify('Favorite added','Item added to the favorites')
    elif fav == "del":
        delFav(url)
        log_utils.log('Deleting %s from favorites' % (url), log_utils.LOGNOTICE)
        kodi.notify('Favorite deleted','Item removed from the list')
        xbmc.executebuiltin('Container.Refresh')

@utils.url_dispatcher.register('38')
def clearFavorites():

    if os.path.isfile(favoritesdb):
        choice = xbmcgui.Dialog().yesno(kodi.get_name(), kodi.giveColor('Would you like to clear all of your favorites?','white'))
        if choice:
            try: os.remove(favoritesdb)
            except: kodi.notify(msg='Error clearing favorites.')
    xbmc.executebuiltin("Container.Refresh")

def addFav(mode,name,url,img,_folder):
    conn = sqlite3.connect(favoritesdb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("INSERT INTO favorites VALUES (?,?,?,?,?)", (name, url, mode, img, _folder))
    conn.commit()
    conn.close()


def delFav(url):
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("DELETE FROM favorites WHERE url = '%s'" % url)
    conn.commit()
    conn.close()
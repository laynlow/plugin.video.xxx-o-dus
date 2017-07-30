import xbmc,xbmcgui,sys,urllib,os,re,datetime
import kodi
import log_utils
import utils
import sqlite3

buildDirectory = utils.buildDir
databases = xbmc.translatePath(os.path.join(kodi.datafolder, 'databases'))
historydb = xbmc.translatePath(os.path.join(databases, 'history.db'))
history_icon = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork/resources/art/main', 'history.png'))

if ( not os.path.exists(databases)): os.makedirs(databases)
conn = sqlite3.connect(historydb)
c = conn.cursor()
try:
    c.executescript("CREATE TABLE IF NOT EXISTS history (ID Integer PRIMARY KEY AUTOINCREMENT, date, time, name, url, site, icon);")
except:
    pass
conn.close()

@utils.url_dispatcher.register('20')
def getHistory():

    dirlist = []
    history_on_off  = kodi.get_setting("history_setting")

    if history_on_off == "true":

        lst = [
              ('Clear History',None,21,history_icon,False),('Disable History',None,22,history_icon,False), \
              ('-------------------------------------',None,999,history_icon,False) \
              ]
            
        conn = sqlite3.connect(historydb)
        conn.text_factory = str
        c = conn.cursor()
        c.execute("SELECT * FROM history ORDER BY ID DESC")

        for (ID, date, time, title, url, site, iconimage) in c.fetchall():
            if site == 'Local File': lst += [('[%s | %s - %s] - %s' % (date,time,kodi.giveColor(site,'deeppink'),title),url+'site='+site+'typeid=history',803,iconimage,False)]
            else: lst += [('[%s | %s - %s] - %s' % (date,time,kodi.giveColor(site,'deeppink'),title),url+'site='+site+'typeid=history',803,iconimage,True)]
        conn.close()

        if len(lst) < 4:
            lst += [('No History Found',None,999,history_icon,False)]
    else: 
        lst = [
               ('Enable History Monitoring',None,22,history_icon,False),('-------------------------------------',None,22,history_icon,False), \
               ('History monitoring is currently disabled.',None,22,history_icon,False) \
              ]
            
    dirlst = []
    for i in lst:
        if not i[3]: icon = kodi.addonicon
        else: icon = i[3]
        fanart = kodi.addonfanart
        dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': i[1], 'mode': i[2], 'icon': icon, 'fanart': fanart, 'folder': False, 'isDownloadable': i[4]})

    buildDirectory(dirlst)

def addHistory(name, url, site, iconimage):

    delEntry(url)
    date_now = datetime.datetime.now().strftime("%d-%m-%Y")
    time_now = datetime.datetime.now().strftime("%H:%M")
    conn = sqlite3.connect(historydb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (?,?,?,?,?,?,?)", (None, date_now, time_now, name, url, site.title(), iconimage))
    conn.commit()
    conn.close()

@utils.url_dispatcher.register('24',['url'])
def delEntry(url):
    
    refresh = False
    try:
        if 'site=' in url: 
            url = url.split('site=')[0]
            refresh = True
        conn = sqlite3.connect(historydb)
        c = conn.cursor()
        c.execute("DELETE FROM history WHERE url = '%s'" % url)
        conn.commit()
        conn.close()
    except: pass
    
    if refresh: xbmc.executebuiltin("Container.Refresh")

@utils.url_dispatcher.register('21')
def clearHistory():

    if os.path.isfile(historydb):
        choice = xbmcgui.Dialog().yesno(kodi.get_name(), kodi.giveColor('Would you like to clear all history?','white'))
        if choice:
            try: os.remove(historydb)
            except: kodi.notify(msg='Error removing history.')
    xbmc.executebuiltin("Container.Refresh")
    
@utils.url_dispatcher.register('22')
def historySetting():

    if kodi.get_setting('history_setting') == 'true': kodi.set_setting('history_setting','false')
    else: kodi.set_setting('history_setting','true')
    xbmc.executebuiltin("Container.Refresh")
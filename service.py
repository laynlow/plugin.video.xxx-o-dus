import xbmc, xbmcaddon, xbmcgui, re, os, time, urllib, urllib2
import sqlite3

try:
    addon = xbmcaddon.Addon()
    get_setting = addon.getSetting
    databases = xbmc.translatePath(os.path.join('special://profile/addon_data/plugin.video.xxx-o-dus', 'databases'))
    chaturbatedb = xbmc.translatePath(os.path.join(databases, 'chaturbate.db'))

    xbmc.log('Starting XXX-O-DUS Service', xbmc.LOGNOTICE)

    if ( not os.path.exists(databases)): os.makedirs(databases)
    conn = sqlite3.connect(chaturbatedb)
    c = conn.cursor()
    try:
        c.executescript("CREATE TABLE IF NOT EXISTS chaturbate (name, url, image);")
    except:
        pass
    conn.close()

    i = 0
    j = 0

    chat_on_off = 'false'
    chat_on_off  = get_setting("chaturbate_start")

    if ( chat_on_off ) != 'true': 
        xbmc.log('Exiting XXX-O-DUS Service', xbmc.LOGNOTICE)
        quit()

    time.sleep(10)

    lst = []

    xbmc.log('Starting XXX-O-DUS Chaturbate Monitoring', xbmc.LOGNOTICE)

    while not xbmc.abortRequested:

        if not i:
            #xbmc.log('Getting Chaturbate Monitored Performers from XXX-O-DUS', xbmc.LOGNOTICE)
            conn = sqlite3.connect(chaturbatedb)
            conn.text_factory = str
            c = conn.cursor()
            c.execute("SELECT * FROM chaturbate")
            e = [u for u in c.fetchall()]
            conn.close()
            if len(e) < 1:
                quit()
            for (title, link, iconimage) in e:
                if (not title in str(lst) ):
                    #xbmc.log('XXX-O-DUS: Checking %s' % title, xbmc.LOGNOTICE)
                    try:
                        req = urllib2.Request(link)
                        response = urllib2.urlopen(req, timeout = 10)
                        r=response.read()
                        response.close()
                        if '.m3u8' in r:
                            content = re.compile('default_subject:\s\"([^,]+)",').findall(r)[0]; content = urllib.unquote_plus(content)
                            try: content=content.encode('utf-8')
                            except: content=content
                            xbmcgui.Dialog().notification(title + ' online!',content, iconimage, 7500, True)
                            lst.append(title)
                            xbmc.sleep(3500)
                    except: pass

        xbmc.sleep(5000)

        if i >= 2879:
            lst = []
            xbmc.log('XXX-O-DUS: Reseting Checked List', xbmc.LOGNOTICE)
        i = (i + 1) % 60
        j = (j + 1) % 2880
except: pass
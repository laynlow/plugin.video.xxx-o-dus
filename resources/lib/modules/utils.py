import xbmc,xbmcaddon,xbmcgui,xbmcplugin,sys,urllib,urlparse,os,base64,re,shutil
import kodi
import client
import dom_parser2
import cache
import log_utils
import pyxbmct
#pyxbmct.skin.estuary = False
pyxbmct = pyxbmct.addonwindow
from url_dispatcher import URL_Dispatcher
url_dispatcher = URL_Dispatcher()

def parse_query(query):
    toint = ['page', 'download', 'favmode', 'channel', 'section']
    q = {'mode': '0'}
    if query.startswith('?'): query = query[1:]
    queries = urlparse.parse_qs(query)
    for key in queries:
        if len(queries[key]) == 1:
            if key in toint:
                try: q[key] = int(queries[key][0])
                except: q[key] = queries[key][0]
            else:
                q[key] = queries[key][0]
        else:
            q[key] = queries[key]
    return q
    
def buildDir(items, content='dirs', cm=[], search=False, stopend=False, isVideo = False, isDownloadable = False, cache=True, chaturbate=False, pictures=False):

    if items == None or len(items) == 0:
        xbmc.executebuiltin('Dialog.Close(busydialog)')
        sys.exit()

    sysaddon = sys.argv[0]
    syshandle = int(sys.argv[1])

    if chaturbate:
        import sqlite3
        databases = xbmc.translatePath(os.path.join(kodi.datafolder, 'databases'))
        chaturbatedb = xbmc.translatePath(os.path.join(databases, 'chaturbate.db'))
        conn = sqlite3.connect(chaturbatedb)
        conn.text_factory = str
        c = conn.cursor()
        c.execute("SELECT * FROM chaturbate ORDER BY name ASC")
        chat_urls = []
        for (chat_name, chat_url, chat_icon) in c.fetchall():
            chat_urls.append(chat_url)

    for i in items:
    
        try:
            
            name = i['name']
            
            if 'file_path' not in name:
                try:
                    name = client.replaceHTMLCodes(name)
                    name = kodi.sortX(name)
                except: pass
            else: name = name.replace('file_path','')
            
            item = xbmcgui.ListItem(label=name)
            
            try: 
                if i['description']: description = i['description']
            except: description = name
            
            try:
                description = client.replaceHTMLCodes(description)
                description = kodi.sortX(description)
            except: pass
                
            kodi.giveColor(description, 'white', True)
            if pictures: item.setInfo('picture', {'title': name, 'plot': description} )
            else: item.setInfo('video', {'title': name, 'plot': description} )

            try: name = urllib.quote_plus(name)
            except: name = name.replace(' ','+')
            
            try:
                if i['url']: url = i['url']
                else: url = 'none'
            except: url = 'none'
            if i['icon'] == None: thumb=kodi.addonicon
            else: thumb = i['icon']
            if i['fanart'] == None: fanart=kodi.addonicon
            else: fanart = i['fanart']
            if ( not thumb == 'local' ) and ( not fanart == 'local' ):
                item.setArt({'icon': thumb, 'thumb': thumb, 'fanart': fanart})
            else:
                item.setArt({'icon': url, 'thumb': url, 'fanart': fanart})
                
            try:
                if i['folder']: _folder = True
                else: _folder = False
            except: _folder = True

            try:
                if i['isDownloaded']: isDownloaded = True
                else: isDownloaded = False
            except: isDownloaded = False

            if not isDownloadable:
                try:
                    if i['isDownloadable']: isDownloadable = True
                    else: isDownloadable = False
                except: isDownloadable = False
           
            if 'typeid=history' in url:
                url = url.replace('typeid=history','')
                history = '%s?url=%s&mode=%s' \
                % (sysaddon,urllib.quote_plus(url),str('24'))
                htext = "Remove from History"
                cm.append(('%s' % htext, 'xbmc.RunPlugin('+history+')'))

            if 'search_term=' in url:
                search_term = '%s?url=%s&mode=%s' \
                % (sysaddon,urllib.quote_plus(url),str('25'))
                stext = "Remove Search Term"
                cm.append(('%s' % stext, 'xbmc.RunPlugin('+search_term+')'))
                url = url.replace('search_term=','') 

            u= '%s?url=%s&mode=%s&name=%s&iconimage=%s&fanart=%s' \
            % (sysaddon,urllib.quote_plus(url),str(i['mode']),name,urllib.quote_plus(thumb),urllib.quote_plus(fanart))

            if chaturbate:
                if '|CHAT|' in url: check_url = url.split('|CHAT|')[0]
                else: check_url = url.split('|SPLIT|')[0]
                log_utils.log('URL IS %s' % (check_url), log_utils.LOGERROR)
                if check_url in str(chat_urls): chat = 'del'
                else: chat = 'add'
                
                chat_compiled = '%s?url=%s&mode=%s&name=%s&iconimage=%s&chat=%s&chatmode=%s&folder=%s' \
                % (sysaddon,urllib.quote_plus(check_url),str('101'),name,urllib.quote_plus(thumb),chat,str(i['mode']),str(_folder))
                
                if chat == 'add': ctext = "Add to"
                elif chat == 'del': ctext = "Remove from"
                cm.append(('%s Chaturbate Monitoring' % ctext, 'xbmc.RunPlugin('+chat_compiled+')'))

            try: 
                if i['fav']: fav = i['fav']
                else: fav = 'add'
            except: fav = 'add'

            try: 
                if i['cm']:
                    for cmitems in i['cm']:
                        log_utils.log('%s' % (cmitems[1]), log_utils.LOGNOTICE)
                        cm.append(('%s' % cmitems[0], 'xbmc.RunPlugin('+cmitems[1]+')'))
            except: pass
            
            favorite = '%s?url=%s&mode=%s&name=%s&iconimage=%s&fav=%s&favmode=%s&folder=%s' \
            % (sysaddon,urllib.quote_plus(url),str('100'),name,urllib.quote_plus(thumb),fav,str(i['mode']),str(_folder))
            
            if fav == 'add': ftext = "Add to"
            elif fav == 'del': ftext = "Remove from"
            cm.append(('%s %s Favorites' % (ftext, kodi.get_name()), 'xbmc.RunPlugin('+favorite+')'))

            if isDownloadable:
                dwnld = '%s?url=%s&mode=%s&name=%s&iconimage=%s' \
                % (sysaddon,urllib.quote_plus(url),str('26'),name,urllib.quote_plus(thumb))
                cm.append(('Download Video', 'xbmc.RunPlugin('+dwnld+')'))
            if isDownloaded:
                rmdwnld = '%s?url=%s&mode=%s&name=%s' \
                % (sysaddon,urllib.quote_plus(url),str('28'),name)
                cm.append(('Delete Video', 'xbmc.RunPlugin('+rmdwnld+')'))

            open_set = '%s?mode=%s' \
            % (sysaddon,str('19'))
            stext = "Open XXX-O-DUS Settings"
            cm.append(('%s' % stext, 'xbmc.RunPlugin('+open_set+')'))

            if isDownloadable: view_type = 'thumb'
            elif pictures: view_type = 'picture'
            elif chaturbate: view_type = 'chaturbate'
            else: view_type = 'list'
            view_compile = '%s?mode=%s&name=%s' \
            % (sysaddon,str('44'),view_type)
            cm.append(('Set %s to this view mode by default.' % view_type.title(), 'xbmc.RunPlugin('+view_compile+')'))

            if cm: 
                item.addContextMenuItems(cm, replaceItems=False)
                cm=[]

            if isVideo:
                codec_info = {'codec': 'h264'}
                item.addStreamInfo('video', codec_info)
            
            xbmcplugin.addDirectoryItem(handle=syshandle, url=u, listitem=item, isFolder=_folder)
        
        except Exception as e:
                log_utils.log('Error adding item %s in BuildDir function ( %s %s ):: Error: %s' % (name,url,thumb,str(e)), log_utils.LOGERROR)
       
    if not stopend:
        if chaturbate: 
            xbmcplugin.setContent(kodi.syshandle, 'movies')
            setView('chaturbate')
        elif pictures:
            xbmcplugin.setContent(kodi.syshandle, 'movies')
            setView('pictures')
        elif isVideo: 
            xbmcplugin.setContent(kodi.syshandle, 'movies')
            setView('thumbs')
        else: 
            xbmcplugin.setContent(kodi.syshandle, 'movies')
            setView('list')
    if ( not search ) and ( not stopend ):
        if cache: xbmcplugin.endOfDirectory(syshandle, cacheToDisc=True)
        else: xbmcplugin.endOfDirectory(syshandle, cacheToDisc=False)
    
@url_dispatcher.register('19')
def showSettings():

    kodi.show_settings()
    kodi.refresh_container()
    
@url_dispatcher.register('44', ['name'])
def setViewCM(viewtype):
    window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    viewid = str(window.getFocusId())
    xbmcaddon.Addon().setSetting("%s_view" % (viewtype), viewid)
    kodi.notify(kodi.get_name(),"%s view has been set to (%s)." % (viewtype.title(), viewid))

def setView(name):

    list_mode  = int(kodi.get_setting("list_view"))
    thumb_mode = int(kodi.get_setting("thumb_view"))
    search_mode = int(kodi.get_setting("search_view"))
    picture_mode = int(kodi.get_setting("picture_view"))
    chaturbate_mode = int(kodi.get_setting("chaturbate_view"))

    kodi_name = kodi.kodiVersion()

    if list_mode == 0:
        if kodi_name == "Jarvis":
            list_mode='50'
        elif kodi_name == "Krypton":
            list_mode='55'
        else: list_mode='50'

    if thumb_mode == 0:
        if kodi_name == "Jarvis":
            thumb_mode='500'
        elif kodi_name == "Krypton":
            thumb_mode='53'
        else: thumb_mode='500'

    if search_mode == 0:
        if kodi_name == "Jarvis":
            search_mode='500'
        elif kodi_name == "Krypton":
            search_mode='500'
        else: search_mode='500'
        
    if picture_mode == 0:
        if kodi_name == "Jarvis":
            picture_mode='500'
        elif kodi_name == "Krypton":
            picture_mode='500'
        else: picture_mode='500'
       
    if chaturbate_mode == 0:
        if kodi_name == "Jarvis":
            chaturbate_mode='50'
        elif kodi_name == "Krypton":
            chaturbate_mode='54'
        else: chaturbate_mode='50'
        
    if name == 'list': xbmc.executebuiltin('Container.SetViewMode(%s)' % list_mode)
    elif name == 'thumbs': xbmc.executebuiltin('Container.SetViewMode(%s)' % thumb_mode)
    elif name == 'search': xbmc.executebuiltin('Container.SetViewMode(%s)' % search_mode)
    elif name == 'pictures': xbmc.executebuiltin('Container.SetViewMode(%s)' % picture_mode)
    elif name == 'chaturbate': xbmc.executebuiltin('Container.SetViewMode(%s)' % chaturbate_mode)
    else: xbmc.executebuiltin('Container.SetViewMode(%s)' % list_mode)

@url_dispatcher.register('17',['url'])
def viewDialog(url):

    global msg_text
    
    if url.startswith('http'): msg_text = client.request(url)
    else: 
        with open(url,mode='r')as f: msg_text = f.read()
    from resources.lib.pyxbmct_.github import xxxtext
    #xxxtext.TextWindow(msg_text)
    window = TextBox('XXX-O-DUS')
    window.doModal()
    del window

class TextBox(pyxbmct.AddonDialogWindow):

    def __init__(self, title='XXX-O-DUS'):
        super(TextBox, self).__init__(title)
        self.setGeometry(950, 600, 10, 30, 0, 5, 5)
        self.set_info_controls()
        self.set_active_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_info_controls(self):

        Background   = pyxbmct.Image(xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/dialog/bg.jpg')))
        self.placeControl(Background, 0, 0, 10, 30)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 0, 1, 9, 28)
        self.textbox.setText(msg_text)
        self.textbox.autoScroll(1000, 2000, 1000)

    def set_active_controls(self):
        self.button = pyxbmct.Button('Close')
        self.placeControl(self.button, 9,26,1,4)
        self.connect(self.button, self.close)

    def set_navigation(self):
        self.button.controlUp(self.button)
        self.button.controlDown(self.button)
        self.button.controlRight(self.button)
        self.button.controlLeft(self.button)
        self.setFocus(self.button)

    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=200',), ('WindowClose', 'effect=fade start=100 end=0 time=300',)])


@url_dispatcher.register('18')
def hard_reset():

    viewDialog(xbmc.translatePath(os.path.join(kodi.addonfolder , 'resources/files/reset.txt')))
    choice = xbmcgui.Dialog().yesno("[COLOR orangered][B]RESET XXX-O-DUS?[/B][/COLOR]", '[COLOR white]ARE YOU SURE YOU WANT TO RETURN XXX-O-DUS TO THE DEFAULT STATE AND LOSE ALL YOUR INFORMATION?[/COLOR]')
    if choice:
        try:
            shutil.rmtree(kodi.datafolder)
        except:
            kodi.dialog.ok(kodi.get_name(), "[COLOR white]There was an error deleting deleting the data directory.[/COLOR]")
            quit()
        kodi.dialog.ok(kodi.get_name(), "[COLOR white]XXX-O-DUS has been reset to the factory state.[/COLOR]","[COLOR white]Press OK to continue.[/COLOR]")
        xbmc.executebuiltin("Container.Refresh")
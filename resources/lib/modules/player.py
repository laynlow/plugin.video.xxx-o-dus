import xbmc,xbmcgui,os,re,urllib,time
import adultresolver
adultresolver = adultresolver.streamer()
import kodi
import xbmcaddon, os
import client
import utils
import history
import log_utils
import downloader
import urlresolver, xbmcvfs
xxx_plugins_path = 'special://home/addons/script.module.urlresolver.xxx/resources/plugins/'
if xbmcvfs.exists(xxx_plugins_path): urlresolver.add_plugin_dirs(xbmc.translatePath(xxx_plugins_path))

@utils.url_dispatcher.register('801', ['url'], ['name', 'iconimage', 'pattern']) 
def resolve_url(url, name=None, iconimage=None, pattern=None):

    kodi.busy()
    
    try: url,site = url.split('|SPLIT|')
    except: 
        site = 'Unknown'
        log_utils.log('Error getting site information from :: %s' % (url), log_utils.LOGERROR)
    
    if '|CHAT|' in url: 
        url,site,name = url.split('|CHAT|')
    if '- [' in name: 
        name = name.split('- [')[0]

    u = None
    log_utils.log('Sending %s to XXX Resolver' % (url), log_utils.LOGNOTICE)
    if urlresolver.HostedMediaFile(url).valid_url(): 
        log_utils.log('%s is a valid SMU resolvable URL. Attempting to resolve.' % (url), log_utils.LOGNOTICE)
        try:
            u = urlresolver.HostedMediaFile(url).resolve()
        except Exception as e:
            log_utils.log('Error getting valid link from SMU :: %s :: %s' % (url, str(e)), log_utils.LOGERROR)
            kodi.idle()
            kodi.notify(msg='Something went wrong!  | %s' % str(e), duration=8000, sound=True)
            quit()
        log_utils.log('Link returned by XXX Resolver :: %s' % (u), log_utils.LOGNOTICE)
    else:
        log_utils.log('%s is not a valid SMU resolvable link. Attempting to resolve by XXXODUS backup resolver.' % (url), log_utils.LOGNOTICE)
        try:
            u = adultresolver.resolve(url)
        except Exception as e:
            log_utils.log('Error getting valid link from SMU :: %s :: %s' % (url, str(e)), log_utils.LOGERROR)
            kodi.idle()
            kodi.notify(msg='Something went wrong!  | %s' % str(e), duration=8000, sound=True)
            quit()
        log_utils.log('%s returned by XXX-O-DUS backup resolver.' % (u), log_utils.LOGNOTICE)
    if u == 'offline':
        kodi.idle()
        kodi.notify(msg='This performer is offline.', duration = 5000, sound = True)
        quit()
    if u:
        kodi.idle()
        play(u,name,iconimage,url,site)
    else: 
        kodi.idle()
        log_utils.log('Failed to get any playable link for :: %s' % (url), log_utils.LOGERROR)
        kodi.notify(msg='Failed to get any playable link.', duration=7500, sound=True)
        quit()

@utils.url_dispatcher.register('803', ['url','name'], ['iconimage','ref', 'site']) 
def play(url, name, iconimage=None, ref=None, site=None):

    kodi.busy()
    
    if not site: 
        if 'site=' in url: url,site = url.split('site=')
        else: site = 'Unknown'
    if not name: name = 'Unknown'
    if not iconimage: iconimage = kodi.addonicon
    name = re.sub(r'(\[.+?\])','',name); name = name.lstrip()
    if '] - ' in name: name = name.split('] - ')[-1] 

    chatur = False
    
    if ref:
        if 'chaturbate.com' in ref:
            chatur = True
    else: ref = ''
    if 'chaturbate.com' in url:
        chatur = True
        ref = url
        url = adultresolver.resolve(url)
    log_utils.log('Failed to get any playable link for :: %s' % (url), log_utils.LOGERROR)
    if (not isinstance(url, str)): 
        try: url = multilinkselector(url)
        except: pass
    history_on_off  = kodi.get_setting("history_setting")
    if history_on_off == "true":
        web_checks = ['http:','https:','rtmp:']
        locak_checks = ['.mp4']
        if any(f for f in web_checks if f in url): site = site.title()
        elif any(f for f in locak_checks if f in url): site = 'Local File'
        else: site = 'Unknown'
        
        kodi.notify(msg=url)
        if chatur:
            history.delEntry(ref)
            history.addHistory(name, ref, site.title(), iconimage)
        else:
            history.delEntry(url)
            history.addHistory(name, url, site.title(), iconimage)
            
    kodi.idle()

    if 'chaturbate.com' in ref:
        if kodi.get_setting("mobile_mode") == 'true':
            url = url.replace('_fast_aac','_aac')
        else:
            bandwidth = kodi.get_setting("chaturbate_band")
            if bandwidth == '0': url = url.replace('_fast_aac','_aac')
            elif bandwidth == '2':
                choice = kodi.dialog.select("[COLOR white][B]" + name + "[/B][/COLOR]", ['[COLOR white]Play High Bandwidth Stream[/COLOR]','[COLOR white]Play Low Bandwidth Stream[/COLOR]'])
                if choice == 1: url = url.replace('_fast_aac','_aac')
                elif choice == 0: pass
                else: quit()

        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        xbmc.Player().play(url, liz, False)
        
        if kodi.get_setting("chaturbate_subject") == "true":
            sleeper = kodi.get_setting("chaturbate_subject_refresh")
            i = 0
                
            while not xbmc.Player().isPlayingVideo():
                time.sleep(1)
                i += 1
                if i == 30: quit()
            while xbmc.Player().isPlayingVideo():
                try:
                    r = client.request(ref)
                    subject = re.compile('default_subject:\s\"([^,]+)",').findall(r)[0]; subject = urllib.unquote_plus(subject)
                    kodi.notify(msg=subject, duration=8500, sound=True, icon_path=iconimage)
                except: pass
                time.sleep(int(sleeper))
    else:                
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        xbmc.Player().play(url, liz, False)
 
def multilinkselector(url):

    try:
        if len(url) == 1: url = url[0][1]
        else:
            sources = []

            for i in url:
                smu_file = False
                try:
                    if i[2]: smu_file=True
                except: pass
                if ( not smu_file ):
                    c = client.request(i[1], output='headers')
                    sources += [(i[0],kodi.convertSize(int(c['Content-Length'])),i[1])]
                else: 
                    try:
                        pattern = r'''(?:)(?:http|https)(?:\:\/\/|\:\/\/www.)([^\.]+)'''
                        domain = re.match(pattern,i[1])
                        domain = domain.group(1).title()
                    except: domain = 'URL Resolver Link'
                    sources += [(i[0],domain,i[1])]

                quals = []
                srcs  = []
                
            for i in sources:
                qual = '%s - [ %s ]' % (i[0],i[1])
                quals.append(kodi.giveColor(qual,'white',True))
                srcs.append(i[2])

            selected = kodi.dialog.select('Select a quality.',quals)
            if selected < 0:
                kodi.notify(msg='No option selected.')
                return 'quit'
            else:
                url = srcs[selected]
        kodi.busy()
        try:
            if urlresolver.HostedMediaFile(url).valid_url(): 
                url = urlresolver.HostedMediaFile(url).resolve()
        except: pass
        kodi.idle()
        return url
    except: 
        try:
            if urlresolver.HostedMediaFile(url[0][1]).valid_url(): 
                url = urlresolver.HostedMediaFile(url[0][1]).resolve()
            return url
        except: pass
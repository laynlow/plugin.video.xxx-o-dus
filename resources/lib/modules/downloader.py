import xbmc,xbmcgui,os
import urllib
import time
import adultresolver
adultresolver = adultresolver.streamer()
import urlresolver
from urllib import FancyURLopener
import sys
import kodi
import log_utils
import utils
import player
import client
import sqlite3
buildDirectory = utils.buildDir

download_icon = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork/resources/art/main', 'downloads.png'))

class MyOpener(FancyURLopener):
    version = 'python-requests/2.9.1'

myopener = MyOpener()
urlretrieve = MyOpener().retrieve
urlopen = MyOpener().open
download_location   = kodi.get_setting("download_location")
download_folder = xbmc.translatePath(download_location)

databases = xbmc.translatePath(os.path.join(kodi.datafolder, 'databases'))
downloaddb = xbmc.translatePath(os.path.join(databases, 'downloads.db'))

if ( not os.path.exists(databases)): os.makedirs(databases)
conn = sqlite3.connect(downloaddb)
c = conn.cursor()
try:
    c.executescript("CREATE TABLE IF NOT EXISTS downloads (name, url, image);")
except:
    pass
conn.close()

@utils.url_dispatcher.register('27')
def getDownloads():

    if ( not os.path.exists(download_folder) ): os.makedirs(download_folder)

    dirlist = []
    lst = [
           (kodi.giveColor('Download Location: ','white')+'file_path'+kodi.giveColor(str(download_folder),'violet'),None,19,download_icon,False), \
           (kodi.giveColor('Change Download Location','white'),None,19,download_icon,False), \
           ('-----------------------------------------------',None,999,download_icon,False) \
          ]
          
    extensions = ['.mp4']

    for file in os.listdir(download_folder):
        for extension in extensions:
            if file.endswith('.tmp_mp4'):
                try: os.remove(os.path.join(download_folder, file))
                except: pass
            if file.endswith(extension):
                name = urllib.unquote_plus(file)
                lst += [
                        (kodi.giveColor(str(name),'white'),os.path.join(download_folder, file),803,None,True), \
                       ]

    conn = sqlite3.connect(downloaddb)
    conn.text_factory = str
    c = conn.cursor()
    for i in lst:
        find_string = i[0]
        if i[1]:
            try:
                find_string = find_string.replace('.mp4','')
                find_string = kodi.stripColor(find_string)
                c.execute("SELECT image FROM downloads WHERE name = '%s'" % find_string)                       
                icon = c.fetchone()[0]
            except: icon = None
        else: icon = i[3]
        dirlist.append({'name': find_string, 'url': i[1], 'mode': i[2], 'icon': icon, 'fanart': None, 'folder': False, 'isDownloaded': i[4]})

    if c: c.close()
    
    if len(lst) < 4:
        dirlist.append({'name': kodi.giveColor('No Downloads Found','white'), 'url': 'None', 'mode': 999, 'icon': download_icon, 'fanart': None, 'folder': False})

    buildDirectory(dirlist)    
    
def addDownload(name,url,img):
    conn = sqlite3.connect(downloaddb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("INSERT INTO downloads VALUES (?,?,?)", (name, url, img))
    conn.commit()
    conn.close()

@utils.url_dispatcher.register('28', ['url','name'])
def removeDownload(url, name):

    try:
        os.remove(url)
        try:
            name = name.replace('.mp4','')
            name = kodi.stripColor(name)
            conn = sqlite3.connect(downloaddb)
            c = conn.cursor()
            c.execute("DELETE FROM downloads WHERE name = '%s'" % name)
            conn.commit()
            conn.close()
        except: pass
        kodi.notify(msg='Removed successfully.')
    except:
        kodi.notify(msg='Error removing file.')
    xbmc.executebuiltin("Container.Refresh")
    
@utils.url_dispatcher.register('26',['url', 'name', 'iconimage'])
def find_link(url, name, iconimage, downloadableLink=False):

    xbmc.executebuiltin("ActivateWindow(busydialog)")

    if '|SPLIT|' in url: url = url.split('|SPLIT|')[0]
    if 'site=' in url: url = url.split('site=')[0]
    if '|' in url: url = url.split('|User-Agent')[0]

    c = client.request(url, output='headers')

    checks = ['video','mpegurl']
    exts = ['.mp4','.flv','.m3u8']

    try:
        if any(f for f in checks if f in c['Content-Type']): downloadableLink = True
    except:
        if any(f for f in exts if f in url): 
            downloadableLink = True
        else:
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            kodi.notify(msg='Error downloading video.')
            quit()

    name = kodi.stripColor(name)
    if '] -' in name: name = name.split('] -')[1]
    if downloadableLink:
        dest = getDest()
        dest = os.path.join(dest, '%s.mp4' % urllib.quote_plus(name))
        download(url,name,iconimage,dest)
    else:
        u = None
        log_utils.log('Sending %s to XXX Resolver' % (url), log_utils.LOGNOTICE)
        if urlresolver.HostedMediaFile(url, include_xxx=True).valid_url(): 
            log_utils.log('%s is a valid SMU resolvable URL. Attempting to resolve.' % (url), log_utils.LOGNOTICE)
            try:
                u = urlresolver.HostedMediaFile(url, include_xxx=True).resolve()
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
        if (not isinstance(u, str)): 
            try:
                u = multilinkselector(u)
            except: pass       
        if u == 'quit': 
                xbmc.executebuiltin("Dialog.Close(busydialog)")
                quit()
        if u: 
            dest = getDest()
            dest = os.path.join(dest, '%s.tmp_mp4' % urllib.quote_plus(name))
            download(u,name,iconimage,dest)
        else:
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            kodi.notify('No Downloadable Link Found.')
            quit()

def getDest():

    if ( not os.path.exists(download_folder) ):
        try:
            os.makedirs(download_folder)
        except:
            kodi.notify('Error creating download folder.')
            quit()
    if ( not download_folder ):
        kodi.notify('Error getting destination location.')
        quit()
    return download_folder
    
def download(url, name, icon, dest, dp = None):
    xbmc.executebuiltin("Dialog.Close(busydialog)")
    if '|' in url: url = url.split('|')[0]
    if not dp: 
        dp = kodi.dp
        dp.create(kodi.get_name(),"Downloading: %s" % name,' ', ' ')
    dp.update(0)
    start_time=time.time()
    log_utils.log('Attempting to download :: %s' % url, log_utils.LOGNOTICE)
    urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(dest,nb, bs, fs, dp, start_time))
    addDownload(name, url, icon)
    kodi.notify(msg='Download Complete', sound=True)
    log_utils.log('Download complete.', log_utils.LOGNOTICE)
    finish_up(dest)
    
def finish_up(dest):
    new = dest.replace('.tmp_mp4','.mp4')
    os.rename(dest,new)
    
def _pbhook(dest,numblocks, blocksize, filesize, dp, start_time):

    try: 
        if filesize <= 0:
            kodi.notify(msg='Invalid downloadable file', sound=True)
            log_utils.log('Error downloading video.', log_utils.LOGERROR)
            quit()
        percent = min(numblocks * blocksize * 100 / filesize, 100) 
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
        kbps_speed = numblocks * blocksize / (time.time() - start_time) 
        if kbps_speed > 0: 
            eta = (filesize - numblocks * blocksize) / kbps_speed 
        else: 
            eta = 0 
        kbps_speed = kbps_speed / 1024 
        mbps_speed = kbps_speed / 1024 
        total = float(filesize) / (1024 * 1024) 
        mbs = '[COLOR dodgerblue]%.02f MB[/COLOR] of [B]%.02f MB[/B]' % (currently_downloaded, total)
        e = '[COLOR white][B]Speed: [/B][/COLOR][COLOR dodgerblue]%.02f Mb/s ' % mbps_speed  + '[/COLOR]'
        e += '[COLOR white][B]ETA: [/B][/COLOR][COLOR dodgerblue]%02d:%02d' % divmod(eta, 60)  + '[/COLOR]'
        dp.update(percent,'', mbs, e)
    except:
        dp.close()
        kodi.notify(msg='Error Downloading. Exiting...')
        quit()
    if dp.iscanceled():
        dp.close()
        kodi.notify(msg='Download Cancelled')
        quit()

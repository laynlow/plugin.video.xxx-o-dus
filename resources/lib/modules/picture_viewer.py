import xbmc,re
import client
import utils
import kodi

@utils.url_dispatcher.register('805', ['url'], ['name', 'iconimage']) 
def resolve_url(url, name=None, iconimage=None):

    kodi.busy()
    
    if 'motherless.com' in url:
        r = client.request(url)
        img = re.findall('''<meta\s*property=["']og:image["']\s*content=["']([^'"]+)''', r)[0]
        SHOW = "ShowPicture(" + img + ')'
        kodi.idle()
        xbmc.executebuiltin(SHOW)
    elif '8muses.com' in url:
        try:
            r = client.request(url)
            dir = re.findall('''<input\s*type=['"]hidden['"]\s*id=['"]imageDir['"]\s*value=['"]([^'"]+)''', r)[0]
            icon_id = re.findall('''<input\s*type=['"]hidden['"]\s*id=['"]imageName['"]\s*value=['"]([^'"]+)''', r)[0]
            display_url = 'https://cdn.ampproject.org/i/s/www.8muses.com/%ssmall/%s' % (dir,icon_id)
            SHOW = "ShowPicture(" + display_url + ')'
        except:
            SHOW = "ShowPicture(" + url + ')'
        kodi.idle()
        xbmc.executebuiltin(SHOW)
    else:
        SHOW = "ShowPicture(" + url + ')'
        kodi.idle()
        xbmc.executebuiltin(SHOW)
    
import re
import kodi
import client
import player
import dom_parser2
import log_utils
import utils

@utils.url_dispatcher.register('810', ['url'], ['name', 'iconimage', 'pattern']) 
def find(url, name=None, iconimage=None, pattern=None):

    #kodi.busy()
    
    try: url,site = url.split('|SPLIT|')
    except: 
        site = 'Unknown'
        log_utils.log('Error getting site information from :: %s' % (url), log_utils.LOGERROR)
    
    if 'streamingporn.xyz' in url:
        try:
            c = client.request('http://streamingporn.xyz/brittany-shae-shows-us-shes-got-bangcasting-combangbros-com/')
            r = dom_parser2.parse_dom(c, 'iframe', req=['height','width'])
            r = [i.attrs['src'] for i in r if i.attrs['height'] == '400' and i.attrs['width'] == '700']
            r = [(re.findall('(?://)(?:www.)?([^.]+).', i)[0].title(), i) for i in r]
         
            names = []
            srcs  = []
       
            for i in sorted(r, reverse=True):
     
                names.append(kodi.giveColor(i[0],'white',True))
                srcs.append(i[1])

            selected = kodi.dialog.select('Select a link.',names)
            if selected < 0:
                kodi.notify(msg='No option selected.')
                quit()
            else:
                url = srcs[selected]
        except:
            kodi.idle()
            kodi.notify(msg='Error geeting link for (Link Finer) %s' % name)
            kodi.idle()
            quit()

    url += '|SPLIT|%s' % site
    kodi.idle()
    player.resolve_url(url, name, iconimage)
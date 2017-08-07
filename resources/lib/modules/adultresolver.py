# -*- coding: utf-8 -*-

import re,json,urllib,urlparse,base64,unicodedata,os

import client
import cache
import workers
import jsunpack
import utils
import kodi
import log_utils

class streamer:

    def resolve(self, url, pattern=None):
        
        if pattern: 
            u = self.generic(url, pattern)
            
        else:
        
            if 'eporner.com' in url: u = self.eporner(url)
            
            elif 'girlfriendvideos.com' in url: u = self.girlfriendvideos(url)

            elif 'watchxxxfree.com' in url: u = self.watchxxxfree(url)

            elif 'porn00' in url: u = self.porn00(url)
            
            elif 'justporno.tv' in url: u = self.justporno(url)

            elif '4tube.com' in url: u = self.fourtube(url)

            elif 'perfectgirls.net' in url: u = self.perfectgirls(url)

            elif 'pornhub.com' in url: u = self.pornhub(url)
            
            elif 'pornheel.com' in url: u = self.pornheel(url)
            
            elif 'pandamovie.eu' in url: u = self.pandamovie(url)

            elif 'winporn.com' in url: u = self.winporn(url)

            elif 'yuvutu.com' in url: u = self.yuvutu(url)

            elif 'huge6.com' in url: u = self.hugesix(url)

            elif 'boobsandtits.co.uk' in url: u = self.boobntit(url)
            
            elif 'sexmax.co' in url: u = self.sexmax(url)

            elif 'drtube' in url: u = self.drtube(url)
            
            elif 'nuvid' in url: u = self.nuvid(url)
            
            elif 'solopornoitaliani' in url: u = self.solopornoitaliani(url)
            
            elif 'spreadporn.org' in url: u = self.spreadporn(url)

            elif 'befuck.com' in url: u = self.befuck(url)
            
            elif 'megasesso' in url: u = self.megasesso(url)
            
            elif 'freeones' in url: u = self.freeones(url)
            
            elif 'fuqer.com' in url: u = self.fuqer(url)
            
            elif 'siska' in url: u = self.siska(url)
            
            elif 'satan18av' in url: u = self.satan18av(url)

            elif 'overthumbs' in url: u = self.overthumbs(url)

            elif 'streamate.com' in url: u = self.streamate(url)

            elif 'mixhdporn.com' in url: u = self.mixhd(url)      
            
            elif 'xtheatre.net' in url: u = self.xtheatre(url)                      
            
            elif 'youporn.com' in url: u = self.youporn(url)                      

            else: u = self.generic(url, pattern=None)

        return u

    def generic(self, url, pattern=None):

        try:
            r = client.request(url)
            if 'chaturbate' in url:
                if '.m3u8' not in r:
                    return 'offline'
            if pattern: s=re.findall(r'%s' % pattern, r)
            else:
                patterns = [
                            r'''\s*=\s*[\'\"](http.+?)[\'\"]''', \
                            r'''\s*=\s*['"](http.+?)['"]''', \
                            r'''['"][0-9_'"]+:\s[\'\"]([^'"]+)''', \
                            r'''\(\w+\([\'\"]([^\'\"]*)''', \
                            r'''[\'\"]\w+[\'\"]:['"]([^'"]*)''', \
                            r'''\s*=\s*[\'\"](http.+?)[\'\"]''', \
                            r'''\s*:\s*[\'\"](//.+?)[\'\"]''', \
                            r'''\:[\'\"](\.+?)[\'\"]''', \
                            r'''\s*\(\s*[\'\"](http.+?)[\'\"]''', \
                            r'''\s*=\s*[\'\"](//.+?)[\'\"]''', \
                            r'''\w*:\s*[\'\"](http.+?)[\'\"]''', \
                            r'''\w*=[\'\"]([^\'\"]*)''', \
                            r'''\w*\s*=\s*[\'\"]([^\'\"]*)''', \
                            r'''(?s)<file>([^<]*)''', \
                            ]
                
                s = []
                for pattern in patterns: 
                    l = re.findall(pattern, r)
                    s += [i for i in l if (urlparse.urlparse(i).path).strip('/').split('/')[-1].split('.')[-1] in ['mp4', 'flv', 'm3u8']]

                if s: s = [i for i in s if (urlparse.urlparse(i).path).strip('/').split('/')[-1].split('.')[-1] in ['mp4', 'flv', 'm3u8']]
                else: s = client.parseDOM(r, 'source', ret='src', attrs = {'type': 'video.+?'})
                
                if not s: 
                    log_utils.log('Error resolving %s :: Error: %s' % (url,str(e)), log_utils.LOGERROR)
                    return
                    
                s = ['http:' + i if i.startswith('//') else i for i in s]
                s = [urlparse.urljoin(url, i) if not i.startswith('http') else i for i in s]
                s = [x for y,x in enumerate(s) if x not in s[:y]]

            self.u = []
            def request(i):
                try:
                    i = i.replace(' ','%20')
                    c = client.request(i, output='headers', referer=url)
                    checks = ['video','mpegurl','html']
                    if any(f for f in checks if f in c['Content-Type']): self.u.append((i, int(c['Content-Length'])))
                except:
                    pass
            threads = []
            for i in s: threads.append(workers.Thread(request, i))
            [i.start() for i in threads] ; [i.join() for i in threads]

            u = sorted(self.u, key=lambda x: x[1])[::-1]
            
            mobile_mode = kodi.get_setting('mobile_mode')
            if mobile_mode == 'true': u = client.request(u[-1][0], output='geturl', referer=url)
            else: u = client.request(u[0][0], output='geturl', referer=url)
            log_utils.log('Returning %s from XXX-O-DUS Resolver' % str(u), log_utils.LOGNOTICE)
            return u
        except Exception as e:
            log_utils.log('Error resolving %s :: Error: %s' % (url,str(e)), log_utils.LOGERROR)

    # needed to generate hash for eporner
    def encode_base_n(self, num, n, table=None):
        FULL_TABLE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if not table:
            table = FULL_TABLE[:n]

        if n > len(table):
            raise ValueError('base %d exceeds table length %d' % (n, len(table)))

        if num == 0:
            return table[0]

        ret = ''
        while num:
            ret = table[num % n] + ret
            num = num // n
        return ret

    def girlfriendvideos(self, url):
        
        try:
            r = client.request(url)
            r = r.replace('\\','')
            pattern = r"""<video src="([^"]+)"""
            link = re.findall(pattern,r)[0]
            u = 'http://www.girlfriendvideos.com' + link
            return u
        except: return 

    def eporner(self, url):
        
        try:
            r = client.request(url)
            pattern = r"""{\s*vid:\s*'([^']+)',\s*hash\s*:\s*["\']([\da-f]{32})"""
            id,hash = re.findall(pattern,r)[0]
            hash_code = ''.join((self.encode_base_n(int(hash[lb:lb + 8], 16), 36) for lb in range(0, 32, 8)))
            load_url = 'https://www.eporner.com/xhr/video/%s?hash=%s&device=generic&domain=www.eporner.com&fallback=false&embed=false&supportedFormats=mp4' % (id,hash_code)
            r = client.request(load_url).replace("\/", "/")
            r = json.loads(r).get("sources", {}).get('mp4', {})
            r = [(i, r[i].get("src")) for i in r]
            u = sorted(r, key=lambda x: int(re.search('(\d+)', x[0]).group(1)), reverse=True)
            return u
        except: return 

    def watchxxxfree(self, url):
        
        try:
            r = client.request(url)
            pattern = r"""data-lazy-src=['"]([^'"]+)"""
            e = re.findall(pattern,r)
            import urlresolver
            num = 0
            u = []
            a = []
            b = []
            c = []
            if e:
                for i in e:
                    if urlresolver.HostedMediaFile(i).valid_url(): 
                        num += 1
                        a.append('smu_file')
                        b.append('Link %s' % str(num))
                        c.append(i)
                        u = list(zip(b,c,a))
            if u: return u
            else: return
        except: return

    def porn00(self, url):
        
        try:
            r = client.request(url)
            pattern = r'''<ul>.+?iframe.+?\?v=([\d]+)'''
            id=re.findall(pattern,r,re.DOTALL)[0]
            url = 'http://www.porn00.org/plays/?v=%s' % id
            cookie = client.request(url, output='cookie')
            r = client.request(url, cookie=cookie)
            pattern = r'''(?:)file\:\s*[\'\"]([^\'\"]+)[\'\"]\,\s*\w+\:\s*[\'\"]([^\'\"]+)'''
            r=re.findall(pattern,r)
            r = [(i[1],i[0]) for i in r if i]
            u = sorted(r, key=lambda x: int(re.search('(\d+)', x[0]).group(1)), reverse=True)
            return u
        except: return

    def justporno(self, url):
        try:        
            r = client.request(url)
            s = re.findall('''source\s*src=['"]+([^'"]+)''', r)
            
            self.u = []
            def request(i):
                try:
                    c = client.request(i, output='headers')
                    checks = ['video','mpegurl']
                    if any(f for f in checks if f in c['Content-Type']): self.u.append((i, int(c['Content-Length'])))
                except:
                    pass
            threads = []
            for i in s: threads.append(workers.Thread(request, i))
            [i.start() for i in threads] ; [i.join() for i in threads]

            u = sorted(self.u, key=lambda x: x[1])[::-1]
            u = client.request(u[0][0], output='geturl')
            return u
        except:
            return
            
    def fourtube(self, url):
        try:        
            fourtube_ref = url
            self.fourtube_base   = 'https://www.4tube.com'
            self.fourtube_embed  = '/embed/%s'
            self.fourtube_player = '/js/player/embed/%s'
            self.fourtube_post   = 'https://tkn.kodicdn.com/%s/desktop/%s'
            id = re.findall('\/([0-9]+)',url)[0]
            r = client.request(urlparse.urljoin(self.fourtube_base,self.fourtube_embed % id))
            js = re.findall('\/player\/embed\/([^"]+)',r)[0]
            url = urlparse.urljoin(self.fourtube_base,self.fourtube_player % js)
            r = client.request(url)
            url_id,qual = re.compile('ajax\(url,opts\);}}\)\(([\d]+),[\d]+,\[([\d,]+)\]\);').findall(r)[0]
            qual = qual.replace(',','+')
            r = client.request(self.fourtube_post % (url_id,qual), post='', headers={'Origin': self.fourtube_base}, referer=fourtube_ref)
            s = re.compile('token\":\"([^"]+)').findall(r)
            
            self.u = []
            def request(i):
                try:
                    c = client.request(i, output='headers')
                    checks = ['video','mpegurl']
                    if any(f for f in checks if f in c['Content-Type']): self.u.append((i, int(c['Content-Length'])))
                except:
                    pass
            threads = []
            for i in s: threads.append(workers.Thread(request, i))
            [i.start() for i in threads] ; [i.join() for i in threads]

            u = sorted(self.u, key=lambda x: x[1])[::-1]
            u = client.request(u[0][0], output='geturl', referer=url)
            return u
        except:
            return
            
    def freeones(self, url):
        try:        
            u = client.request(url)
            e = re.findall('_script"\ssrc="([^"]*)', u)[0]
            return self.generic(e)
        except:
            return
            
    def fuqer(self, url):
        try:        
            u = client.request(url)
            e = re.findall('config:\'([^\']*)', u)[0]
            return self.generic(e)
        except:
            return

    def perfectgirls(self, url):
        try:
            r = client.request(url)
            pattern = r'''source\s*src=\"([^"]+)\"\s*res=\"\d+\"\s*label="([^"]+)"'''
            r = re.findall(pattern, r)
            r = [(i[1],i[0]) for i in r if i]
            u = sorted(r, key=lambda x: int(re.search('(\d+)', x[0]).group(1)), reverse=True)
            return u
        except:
            return


    def pornhub(self, url):
        try:
            r = client.request(url)
            vars = re.findall('var\s+(.+?)\s*=\s*(.+?);', r)
            link = re.findall('quality_\d+p\s*=\s*(.+?);', r)[0]
            link = [i.strip() for i in link.split('+')]
            link = [i for i in link if i.startswith('*/')]
            link = [re.sub('^\*/', '', i) for i in link]
            link = [(i, [x[1] for x in vars if x[0] == i]) for i in link]
            link = [i[1][0] if i[1] else i[0] for i in link]
            link = ''.join(link)
            link = re.sub('\s|\+|\'|\"', '', link)
            return link
        except:
            return 
    #pornheel gets url and provider name list
    def pornheel(self, url):
        try:
            u = client.request(url)
            e = re.findall('<a\shref="([^"]*)".+?">Streaming\s([^<]*)', u)
            e = [(client.request(i[0], output='geturl'), i[1]) for i in e if i]
            return e
        except:
            return 

    def pandamovie(self, url):
        try:
            u = client.request(url)
            e = re.findall('<li>.+?on ([^"]*).+?f="([^"]*)', u)
            e = [(i[0],i[1]) for i in e if 'pandamovie' not in i[1]]
            return e
        except:
            return


    def winporn(self, url):
        try:
            r = client.request(url)
            link = re.findall('var video_id = "(.+?)"', r)[0]
            r = 'http://nl.winporn.com/player_config_json/?vid=' + link + '&aid=0&domain_id=0&embed=0&ref=&check_speed=0'
            return self.generic(r)
        except:
            return


    def yuvutu(self, url):
        try:
            r = client.request(url)
            r = client.parseDOM(r, 'iframe', ret='src')
            r = [i for i in r if 'embed' in i][0]
            r = urlparse.urljoin(url, r)
            return self.generic(r)
        except:
            return
            
                        
    def hugesix(self, url):
        try:
            main = client.request(url)
            links = re.findall('config=(.+?)",', main)[0] 
            link = links
            link = client.request(link)
            express1 = '<filehd>(.+?)</filehd>'
            express2 = '<file>(.+?)</file>'
            play = re.compile(express1, re.MULTILINE|re.DOTALL).findall(link)
            if not play: play = re.compile(express2, re.MULTILINE|re.DOTALL).findall(link)
            play = play[0]
            return play
        except:
            return

    def boobntit(self, url):
        try:
            main = client.request(url)
            link = client.parseDOM(main, 'div', attrs = {'id': 'player'})
            link = client.parseDOM(link, 'iframe', ret='src')
            link = link[0]
            return self.generic(link)
        except:
            return self.generic(url)
            
    def sexmax(self, url):
        try:        
            url = client.request(url)
            express = '<div id="player-embed">.+?<iframe src="(.+?)"'
            link = re.compile(express, re.MULTILINE|re.DOTALL).findall(url)[0]
            dir = client.request(link)
            dir = dir.replace('\/', '/')
            express = '"src":"(.+?)"'
            link = re.compile(express, re.MULTILINE|re.DOTALL).findall(dir)[0]
            return link
        except:
            return

    def drtube(self, url):
        try:        
            url = client.request(url)
            express = 'vid:(.+?),'
            link = re.compile(express, re.MULTILINE|re.DOTALL).findall(url)[0]
            link = 'http://www.drtuber.com/player_config_json/?vid=' + link + '&aid=0&domain_id=0&embed=0&ref=&check_speed=0'
            return self.generic(link)
        except:
            return
            
    def nuvid(self, url):
        try:        
            url = client.request(url)
            express = 'vid:(.+?),'
            link = re.compile(express, re.MULTILINE|re.DOTALL).findall(url)[0]
            link = 'http://www.nuvid.com/player_config_json/?vid=' + link + '&aid=0&domain_id=0&embed=0&ref=&check_speed=0'
            html = client.request(link)
            html = html.replace('\/', '/')
            express2 = '"hq":"(.+?)"'
            express3 = '"lq":"(.+?)"'
            play = re.compile(express2, re.MULTILINE|re.DOTALL).findall(html)
            if not play: play = re.compile(express3, re.MULTILINE|re.DOTALL).findall(html)
            play = play[0]
            return play
        except:
            return
            
    def solopornoitaliani(self, url):
        try:        
            url = client.request(url)
            express = '\'videoid\',\'(.+?)\''
            link = re.compile(express, re.MULTILINE|re.DOTALL).findall(url)[0]
            link = 'http://www.solopornoitaliani.xxx/vdata/' + link + '.flv'
            return link
        except:
            return
            
    def megasesso(self, url):
        try:        
            u = client.request(url)
            u = client.parseDOM(u, 'div', attrs = {'class': 'player-iframe'})
            u = [(client.parseDOM(i, 'iframe', ret='src')) for i in u]
            u = [(client.replaceHTMLCodes(i[0]).encode('utf-8')) for i in u]
            u = 'http://www.megasesso.com' + u[0]
            return self.generic(u)
        except:
            return

            
    def siska(self, url):
        try:        
            u = client.request(url)
            e = re.findall('document\.write\(base64_decode\(\'([^\']*)', u)[0]
            b64 = base64.b64decode(e)            
            play = re.findall('rc="([^"]*)', b64)[0]
            return play
        except:
            return

    def overthumbs(self, url):
        try:
            u = client.request(url)
            e = re.findall('(?s)id="play".+?src="([^"]*)', u)[0]
            e = ('http://overthumbs.com' + e)
            r = client.request(e)
            unpack = jsunpack.unpack(r)
            return re.findall('file.+?"([^"]*)',unpack)[0]
        except:
            return

    def streamate(self, url):
        try:
            u = client.request(url)
            e = re.findall('iframe\.src = \'([^\']*)', u)
            e = 'https://www.streamate.com' + e[0]
            r = client.request(e)
            r = re.findall('data-manifesturl="([^"]*)', r)[0]
            return self.generic(r)
        except:
            return

    #spreadporn gets link and provider name and provider logo
    def spreadporn(self, url):
        try:
            u = client.request(url)
            e = re.findall('(?s)<li class.+?"stream".+?k="([^"]*).+?c="([^"]*)"\salt="([^"]*)', u)
            return e
        except:
            return
            
    def satan18av(self, url):
        try:
            u = client.request(url)
            e = re.findall('<iframe src="([^"]*)', u)[0]
            return e
        except:
            return

    def befuck(self, url):
        try:
            u = client.request(url)
            e = re.findall('<source src="([^"]*)', u)[0]
            return e
        except:
            return      
    #mixhd gets link and provider  
    def mixhd(self, url):
        try:
            u = client.request(url)
            u = re.findall('<iframe src="([^"]*)', u)
            u = [(i,i.split('//')[-1].split('.')[0]) for i in u]
            return u
        except:
            return
    #xtheatre gets link and provider   
    def xtheatre(self, url):
        try:
            u = client.request(url)
            u = re.findall('<iframe src="([^"]*)', u)
            u = [(i,i.split('//')[-1].split('.')[0]) for i in u]
            return u
        except:
            return

    def youporn(self, url):
        try:        
            r = client.request(url)
            pattern = r"""quality[\'\"]\:[\'\"](\d+)[\'\"]\,[\'\"]videoUrl[\'\"]\:[\'\"]([^\'\"]+)"""
            i = re.findall(pattern,r)
            r = [(e[0], e[1].replace('\/','/')) for e in i]
            log_utils.log('%s' % str(r), log_utils.LOGERROR)
            u = sorted(r, key=lambda x: int(re.search('(\d+)', x[0]).group(1)), reverse=True)
            return u
        except: 
            return 
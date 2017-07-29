import re
import client
import dom_parser2
def find(url):
    
    if 'porn00' in url:
        r = client.request(url)
        r = dom_parser2.parse_dom(r, 'li')
        r = dom_parser2.parse_dom(r, 'iframe', req='src')
        url = r[0].attrs['src']

    return url
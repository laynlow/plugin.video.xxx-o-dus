import sys
import kodi
from resources.lib.modules import utils
from resources.lib.modules import menus
from resources.lib.modules import parental
from resources.lib.modules import firstStart
parentalCheck = parental.parentalCheck

def main(argv=None):
    if sys.argv: argv = sys.argv
    queries = utils.parse_query(sys.argv[2])
    mode = queries.get('mode', None)
    utils.url_dispatcher.dispatch(mode, queries)
    if kodi.get_setting('dev_debug') == 'true': utils.url_dispatcher.showmodes()
if __name__ == '__main__':
    firstStart.run()
    parentalCheck()
    sys.exit(main())
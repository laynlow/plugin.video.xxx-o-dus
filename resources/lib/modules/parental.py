import xbmc,os,hashlib,sys,time,re
import kodi
import log_utils
import sqlite3
from resources.lib.modules import utils
buildDirectory = utils.buildDir

databases = xbmc.translatePath(os.path.join(kodi.datafolder, 'databases'))
parentaldb = xbmc.translatePath(os.path.join(databases, 'parental.db'))

if ( not os.path.exists(databases)): os.makedirs(databases)
conn = sqlite3.connect(parentaldb)
c = conn.cursor()
try:
    c.executescript("CREATE TABLE IF NOT EXISTS parental (password, time);")
except:
    pass
conn.close()

def parentalCheck():
        
    timestamp = None
    password  = None
    
    conn = sqlite3.connect(parentaldb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM parental")

    for (passwd, timest) in c.fetchall(): 
        timestamp = timest
        password = passwd
    conn.close()
    
    if password:
        try:
            now = time.time()
            check = now - 60*30
            if ( not timestamp ): timestamp = 0
        except: 
            now = time.time()
            check = now - 60*30
            timestamp = 0
    else: return
    
    if (timestamp < check):

        input = kodi.get_keyboard('Please Enter Your Password - %s' % kodi.giveColor('(30 Minute Session)','red',True))
        if ( not input ):
            sys.exit(0)

        pass_one = hashlib.sha256(input).hexdigest()

        if password != pass_one:
            kodi.dialog.ok(kodi.get_name(),"Sorry, the password you entered was incorrect.")
            sys.exit(0)
        else:
            delEntry(password)
            addEntry(password, now)
            kodi.dialog.ok(kodi.get_name(),'Login successful!','You now have a 30 minute session before you will be asked for the password again.')
    return

@utils.url_dispatcher.register('5')
def parentalControls():

    list = []
    password = None
    conn = sqlite3.connect(parentaldb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM parental")

    for (timest, passwd) in c.fetchall(): 
        timestamp = timest
        password = passwd
    conn.close()
    
    if password:
        c = [(kodi.giveColor('PARENTAL CONTROLS - ','white',True) + kodi.giveColor('ON','lime'),999), \
             (kodi.giveColor('Change Password','white'),13), \
             (kodi.giveColor('Disable Password','white'),14), \
             ]
    else:
        c = [(kodi.giveColor('PARENTAL CONTROLS - ','white',True) + kodi.giveColor('OFF','orangered'),999), \
             (kodi.giveColor('Setup Parental Password','white'),13), \
             ]
    
    for i in c:
        icon   = kodi.addonicon
        fanart = kodi.addonfanart
        list.append({'name': i[0], 'url': 'none', 'mode': i[1], 'icon': icon, 'fanart': fanart, 'folder': False})

    if list: buildDirectory(list)

@utils.url_dispatcher.register('13')
def parentalPin():

    input = kodi.get_keyboard('Please Set Password')
    if ( not input ):
        kodi.dialog.ok(kodi.get_name(),"Sorry, no password was entered.")
        sys.exit(0)

    pass_one = input

    input = kodi.get_keyboard('Please Confirm Your Password')
    if ( not input ):
        kodi.dialog.ok(kodi.get_name(),"Sorry, no password was entered.")
        sys.exit(0)
        
    pass_two = input

    if pass_one == pass_two:
        writeme = hashlib.sha256(pass_one).hexdigest()
        addEntry(writeme,None)
        kodi.dialog.ok(kodi.get_name(),'Parental control has been enabled.')
        xbmc.executebuiltin("Container.Refresh")    
    else:
        kodi.dialog.ok(kodi.get_name(),'The passwords do not match, please try again.')
        sys.exit(0)

@utils.url_dispatcher.register('14')
def parentalOff():

    input = kodi.get_keyboard('Please Enter Your Password')
    if ( not input ):
        kodi.dialog.ok(kodi.get_name(),"Sorry, no password was entered.")
        sys.exit(0)
    pass_one = hashlib.sha256(input).hexdigest()

    conn = sqlite3.connect(parentaldb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM parental")

    for (passwd, timest) in c.fetchall(): 
        timestamp = timest
        password = passwd
    conn.close()
    
    if password == pass_one:
        try:
            try: os.remove(parentaldb)
            except: pass
            kodi.dialog.ok(kodi.get_name(),'Parental controls have been disabled.')
            xbmc.executebuiltin("Container.Refresh")
        except:
            kodi.dialog.ok(kodi.get_name(),'There was an error disabling the parental controls.')
            xbmc.executebuiltin("Container.Refresh")    
    else:
        kodi.dialog.ok(kodi.get_name(),"Sorry, the password you entered was incorrect.")
        quit()

def addEntry(passwd, timestamp):

    conn = sqlite3.connect(parentaldb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("INSERT INTO parental VALUES (?,?)", (passwd, timestamp))
    conn.commit()
    conn.close()
    
def delEntry(passwd):

    conn = sqlite3.connect(parentaldb)
    c = conn.cursor()
    c.execute("DELETE FROM parental WHERE password = '%s'" % passwd)
    conn.commit()
    conn.close()
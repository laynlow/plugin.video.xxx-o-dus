import os,sys
import kodi
import utils
import client

class run:

    def __init__(self):
    
        self.firstRunFile = os.path.join(kodi.datafolder, 'firstrun.txt')
        self.informationFile = os.path.join(kodi.addonfolder, 'resources/files/information.txt')

        if ( not os.path.isfile(self.firstRunFile) ): 
            self.checkAge()
            kodi.busy()
            try: countme = client.request('http://bit.ly/2vchTCP')
            except: pass
            kodi.idle()
            try: utils.viewDialog(self.informationFile)
            except: pass
        return

    def checkAge(self):

        choice = kodi.dialog.yesno(kodi.get_name(), 'To use this addon you you must be legally allowed to under the laws of your State/Country. By pressing I Agree you accept that you are legally allowed to view adult content.',yeslabel='I Agree',nolabel='Exit')
        if choice: 
            try:
                with open(self.firstRunFile,mode='w'): pass
            except: pass
        else: sys.exit(1)
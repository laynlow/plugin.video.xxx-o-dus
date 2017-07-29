#############################################################
#################### START ADDON IMPORTS ####################
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

import os
import re
import sys
import urllib
import urllib2
import urlparse
from resources.lib.modules import utils
import xxxtext

import kodi
import pyxbmct.addonwindow as pyxbmct

#############################################################
#################### SET ADDON ID ###########################
_self_          = xbmcaddon.Addon(id=kodi.get_id())

#############################################################
#################### SET ADDON THEME IMAGES #################
ART = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/pyxbmct/issues'))

Background_Image    = os.path.join(ART, 'bg.png')
Button  = os.path.join(ART, 'close.png')
ButtonF = os.path.join(ART, 'closef.png')
Open    = os.path.join(ART, 'numbers/not-selected/open/%s.png')
Open_Selected   = os.path.join(ART, 'numbers/selected/open/%s.png')
Closed  = os.path.join(ART, 'numbers/not-selected/closed/%s.png')
Closed_Seleted  = os.path.join(ART, 'numbers/selected/closed/%s.png')

def githubSelect(name):
    import githubissues
    githubissues.run('xibalba10/plugin.video.xxx-o-dus', '%s' % name)
    file = xbmc.translatePath(os.path.join(kodi.datafolder, '%s-issues-%s.csv' % (kodi.get_id(),name)))
    
    global msg_text
    
    with open(file,mode='r')as f: txt = f.read()
    items = re.findall('<item>(.+?)</item>', txt, re.DOTALL)
    if len(items) < 1:
        msg_text = kodi.giveColor('No %s issues with XXX-O-DUS at this time.' % name.title(),'deeppink',True)
    else:
        msg_text = kodi.giveColor('%s Issues with XXX-O-DUS\n' % name.title(),'deeppink',True) + kodi.giveColor('Report Issues @ https://github.com/xibalba10/plugin.video.xxx-o-dus/issues','white',True) + '\n---------------------------------\n\n'
        for item in items:
            id = re.findall('<id>([^<]+)', item)[0]
            user = re.findall('<username>([^<]+)', item)[0]
            label = re.findall('<label>([^<]+)', item)[0]
            title = re.findall('<title>([^<]+)', item)[0]
            body = re.findall('<body>([^<]+)', item)[0]
            created = re.findall('<created>([^<]+)', item)[0]
            date,time = created.split('T')
            msg_text += '[B]ID: %s | Label: %s \nBy: %s on %s at %s[/B] \n\nTitle: %s \nMessage %s \n\n---------------------------------\n\n' \
                         % (id, \
                            kodi.githubLabel(label), \
                            user, \
                            date, \
                            time.replace('Z',''), \
                            title, \
                            body)

#############################################################
########## Function To Call That Starts The Window ##########
@utils.url_dispatcher.register('34',['name'])
def GitWindow(name):

    global open_issues
    global closed_issues
    
    try:
        open_issues = re.findall('\s+(\d+)\s+Open', name)[0]
        closed_issues = re.findall('\s+(\d+)\s+Closed', name)[0]

        if int(open_issues) in range(11,20): open_issues = '10plus'
        elif int(open_issues) in range(21,30): open_issues = '20plus'
        elif int(open_issues) > 30: open_issues = '30plus'
        
        if int(closed_issues) in range(11,20): closed_issues = '10plus'
        elif int(closed_issues) in range(21,30): closed_issues = '20plus'
        elif int(closed_issues) in range(21,30): closed_issues = '30plus'
        elif int(closed_issues) in range(31,40): closed_issues = '40plus'
        elif int(closed_issues) in range(41,50): closed_issues = '50plus'
        elif int(closed_issues) in range(51,100): closed_issues = '20plus'
        elif int(closed_issues) > 100: closed_issues = '100plus'        
    except:
        open_issues = 'default'
        closed_issues = 'default'

    global List
    
    window = Main('')
    window.doModal()
    del window
    
#def Selection(self,xselected):
 
#    githubSelect(xselected)
#    xxxtext.TextWindow(msg_text)

#############################################################
######### Class Containing the GUi Code / Controls ##########
class Main(pyxbmct.AddonFullWindow):

    def __init__(self, title='KongKidz'):
        super(Main, self).__init__(title)

        #set the location and size of your window in kodi
        self.setGeometry(800, 450, 100, 50)
        
        ## Set The backGround Image using PYX Image
        Background          = pyxbmct.Image(Background_Image)
        
        ## Place The BackGround Image (X, Y, W, H)
        self.placeControl(Background, -19, -1, 154, 55)
        
        ## function to set active controls that users interact with 
        self.set_active_controls()
        
        ## function to set what happens when users press left,right,up,down on your active controls
        self.set_navigation()
        
        ## connect the back button to pyx to close window
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        self.connect(self.Open_Issues, lambda:self.Selection('open'))
        self.connect(self.Closed_Issues, lambda:self.Selection('closed'))
        self.connect(self.button, self.close)

        self.setFocus(self.Open_Issues)

    def set_active_controls(self):
        self.Open_Issues    = pyxbmct.Button('',    focusTexture=Open_Selected % open_issues,noFocusTexture=Open % open_issues)
        self.Closed_Issues  = pyxbmct.Button('',    focusTexture=Closed_Seleted % closed_issues,noFocusTexture=Closed % closed_issues)
        self.button = pyxbmct.Button('',    focusTexture=ButtonF,   noFocusTexture=Button)

        self.placeControl(self.Open_Issues, 80, 2, 37, 20)
        self.placeControl(self.Closed_Issues, 80, 30, 37, 20)
        self.placeControl(self.button, 115,22,15,7)

    def set_navigation(self):
        self.Open_Issues.controlRight(self.button)
        self.Closed_Issues.controlLeft(self.button)
        self.button.controlLeft(self.Open_Issues)
        self.button.controlRight(self.Closed_Issues)

    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=200',), ('WindowClose', 'effect=fade start=100 end=0 time=300',)])

    def Selection(self,xselected):
     
        githubSelect(xselected)
        xxxtext.TextWindow(msg_text)
        
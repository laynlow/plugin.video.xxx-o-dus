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
import utils

import kodi
import pyxbmct.addonwindow as pyxbmct

#############################################################
#################### SET ADDON ID ###########################
_self_			= xbmcaddon.Addon(id=kodi.get_id())

#############################################################
#################### SET ADDON THEME IMAGES #################
ART = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/pyxbmct/issues'))

Background_Image	= os.path.join(ART, 'tbg.png')
Button	= os.path.join(ART, 'close.png')
ButtonF	= os.path.join(ART, 'closef.png')

#############################################################
########## Function To Call That Starts The Window ##########
def TextWindow(Text):

    kodi.idle
    
    global msg_text
    
    msg_text = Text
    
    window = Main('')
    window.doModal()
    del window
#############################################################
######### Class Containing the GUi Code / Controls ##########
class Main(pyxbmct.AddonFullWindow):

    def __init__(self, title='XXX-O-DUS'):
        super(Main, self).__init__(title)
		
		#set the location and size of your window in kodi
        self.setGeometry(800, 450, 100, 50)
		
		## Set The backGround Image using PYX Image
        Background			= pyxbmct.Image(Background_Image)
		
		## Place The BackGround Image (X, Y, W, H)
        self.placeControl(Background, -50, -1, 220, 55)
		
		## function to set active controls that users interact with 
        self.set_active_controls()
        
        self.set_info_controls()
		
        self.setFocus(self.button)
		
		## connect the back button to pyx to close window
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        self.connect(self.button, self.close)
        self.textbox.setText(msg_text)
        self.textbox.autoScroll(1000, 2000, 1000)
        
    def set_info_controls(self):
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 22, 1, 140, 48)
        
    def set_active_controls(self):
        self.button = pyxbmct.Button('',	focusTexture=ButtonF,	noFocusTexture=Button)
        self.placeControl(self.button, 147,47,15,6)
        
    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=200',), ('WindowClose', 'effect=fade start=100 end=0 time=300',)])

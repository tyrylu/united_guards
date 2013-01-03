#!/usr/bin/env python
#version 0.3, released on September 26, 2012 by Vojtech Polasek <vojtech.polasek@gmail.com>
# the game is structured into several modules:
#game - game functions
# ug_data - various declarations that won't change
# speech - module for speech
# menu - module for creating menus
#menus - definitions of actual menus
#globvars - some global state, probably could be merged with ug_data or vice versa
#keyboardmanager - an abstraction on top of pygame keyboard events
#structobject - an object for data containment
#see included README file for more info

#initialisation

import time, pygame, os.path, random, speech, sys, cPickle, threading
import keyboardmanager
#pygame initialisation
pygame.init()
pygame.display.set_mode((320, 200))
pygame.display.set_caption ('United guards')

#Fancy keyboard event handling initialization
kbmgr = keyboardmanager.KeyboardManager("menu")

#initialisation of speech
s =speech.Speaker()
s.init()
speech.s = s
_ = speech.getTransFunc()
# final event handling initialization must be there, because events need speech and translation services.
import events
kbmgr.auto_register(events)
# next line avoids two same functions:
kbmgr.register(s.stop, ["lctrl", "rctrl"])


import game, menu, menus, globvars






if __name__ == "__main__":
	from ug_data import *
	s.say(_("Welcome to the game."), 1)
	globvars.current_menu = menus.main_menu.init()
	try:
		scorefile = open("score.dat", "r")
		try:
			game.scoreboard = cPickle.load(scorefile)
			for score in game.scoreboard:
				if score == None:break
				if len(score) < 3:
					score.append(None)
		except EOFError:
			game.scoreboard = []
		scorefile.close()
	except IOError:
		game.scoreboard = []
		scorefile = open("score.dat", "w")
		scorefile.close()
	kbmgr.run(game.loop)
	kbmgr.loop_thread.join()
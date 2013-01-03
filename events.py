"""Various event functions. Note that the infrastructure of the game logic is not ideal, but we must somehow cope with it, because as every programmer knows, understanding other's code is the hardest thing."""
from pydispatch import dispatcher
import game, globvars, speech, menus
from keyboardmanager import kbmgr
_ = speech.getTransFunc()
s = speech.s

def key_game_escape():
	game.pausegame()

def key_menu_return():
	returned = globvars.current_menu.select()
	if returned:
		globvars.current_menu = returned

def key_game_left():
	game.check(0)

def key_menu_up():
	globvars.current_menu.moveup()

def key_game_up():
	game.check(1)

def key_game_right():
	game.check(2)

def key_menu_down():
	globvars.current_menu.movedown()

def key_game_s():
	s.say(_("Your score is {0}.").format(game.score), 1)

def key_game_l():
	s.say (_("You have {0} lives remaining.").format(game.lives), 1)

def game_active(sender):
	kbmgr.change_keymap("game")

def game_paused(sender):
	kbmgr.change_keymap("menu")
	globvars.current_menu = menus.abortprompt.init()

def game_ended(sender):
	kbmgr.change_keymap("menu")
	globvars.current_menu = menus.main_menu.init()

# connect non-keyboard related events
dispatcher.connect(game_active, signal="game_active", sender=dispatcher.Any)
dispatcher.connect(game_ended, signal="game_ended", sender=dispatcher.Any)
dispatcher.connect(game_paused, signal="game_paused", sender=dispatcher.Any)
import pygame
from pygame.locals import *
pygame.init()

def skip(self):
	pass

class ScreenObject(object):
	def __init__(self, rect):
		self.init(rect)

	def set_scr(self, scr):
		self.scr = scr
		self.g = self.scr.g

	def set_img(self):
		# defaulttiratkaisu, ylikirjoitetaan periessa
		self.img = pygame.Surface((self.rect[2],self.rect[3])) 	# ladataan esineelle kuva jostain
		self.img.fill((196,196,196))

	def set_type(self, taip):
		self.type = taip

	def init(self, rect):
		self.set_type("objekti "+str(rect))
		self.rect = pygame.Rect(rect)
		self.set_img()
		self.set_behaviour(self.describe)
		
	def describe(self):
		print self.type

	def set_behaviour(self, func):
		self.onclick = func

	def click(self, user):
		if user.lclick and self.rect.collidepoint(user.mousepos):
			self.onclick()

	def draw(self):
		self.scr.blit(self)

	def update(self):
		self.click(self.g.player)

class Screen(object):
	def __init__(self, game, objs):
		self.g = game
		self.set_objs(objs)
		# flagien perusteella voipi luoda kaikkia kivoja elementteja
		self.flags = {}
		# ennakoin sita jos pitaa keskeyttaa paivitykset esim. dialogin takia
		# -> paivitysfunktion voi korvata vaikka tyhjalla funktiolla siksi aikaa
		self.act = self.default_act
		
	def set_objs(self, objs):
		self.objs = objs
		for obj in self.objs:
			obj.set_scr(self)

	def get_flag(self, string):
		if string in self.flags:
			return self.flags[string]
		return 0

	def set_flag(self, string):
		if self.get_flag(string):
			# voi laskea esineiden/tapahtumien lukumaaraa
			self.flags[string] += 1
		else:
			# uus lippu
			self.flags[string] = 1

	def default_act(self):
		for obj in self.objs:
			obj.update()

	def blit(self,obj):
		self.g.canvas.blit(obj.img, obj.rect)

	def bgdraw(self):
		self.g.canvas.fill((128,128,134))

	def draw(self):
		# talla voi olla oma taustakuvansa
		for obj in self.objs:
			obj.draw()
		pygame.display.update()

	def update(self):
		self.act()
		self.draw()

class Text():
	def __init__(self,game,msg):
		self.g = game
		self.msg = msg
		self.font = pygame.font.SysFont("monospace",24)
	def read(self):
		txt = self.font.render(self.msg, True, (196,196,196))
		self.g.canvas.blit(txt, (16,360))

class Player():
	def __init__(self,game):
		self.g = game
		self.lclick = False
		self.lhold = False
		self.text = None
		self.update()

	def set_mouse(self):
		self.mousepos = pygame.mouse.get_pos()

		# aina kun klikkaat niin lclick on paalla vain yhden framen
		if pygame.mouse.get_pressed()[0]:
			if not self.lhold:
				self.lclick = True
				self.lhold = True
			else:
				self.lclick = False
		else:
			self.lhold = False
			self.lclick = False

	def say(self, msg):
		if msg is None:
			self.text = None
			return

		self.text = Text(self.g, msg)

	def talk(self):
		if self.text is None:
			return

		self.text.read()

	def update(self):
		self.set_mouse()
		self.talk()

class KaikkiTietavaJumalObjektiJotaPassaillaanYmpariinsaKoskaIlmeisestiGlobaalitObjektitOnPahojaMuttaOnkoTamaNytSittenYhtaanKivempaaKysynpahanVaan():
	def __init__(self):
		self.player = Player(self)
		self.canvas = pygame.display.set_mode((640,400))
		self.screens = {}
		self.screen = None

	def add_screen(self,label,scrobj):
		self.screens[label] = scrobj
	
	def set_screen(self,label):
		if label not in self.screens:
			print "Unohdit lisata screenin", label+"! add_screen(\"nimi\", Screen(...))"
			return
		self.screen = self.screens[label]
		print "screeni on nyt", label

		# puhe resetoituu kun vaihtaa skriinia
		self.player.say(None)

	def get_screen(self,label):
		# jos pitaa viitata johonkin toiseen skriiniin
		if label not in self.screens:
			print "Unohdit lisata screenin", label+"! add_screen(\"nimi\", Screen(...))"
			return None
		return self.screens[label]
	
	def play(self):
		if self.screen == None:
			print "Laita nyt ensin joku screeni aktiiviseksi! set_screen(\"nimi\")"
			return

		while not pygame.key.get_pressed()[K_ESCAPE]:
			pygame.event.get()
			self.screen.bgdraw()
			self.player.update()
			self.screen.update()
import kliksu, pygame

class TestPainting(kliksu.ScreenObject):
	def __init__(self, rect):
		super(TestPainting,self).__init__(rect)
		self.set_type("maalaus")
		self.set_behaviour(self.onclick1)
		
	def onclick1(self):
		self.g.player.say("Onpa kiva "+self.type)
		self.set_behaviour(self.onclick2)
	
	def onclick2(self):
		self.g.player.say("Katoit tata jo, mee pois")

class TestVase(kliksu.ScreenObject):
	def __init__(self, rect):
		super(TestVase,self).__init__(rect)
		self.set_type("maljakko")
		self.set_behaviour(self.onclick1)
		
	def onclick1(self):
		self.g.player.say("Tama on olevinaan "+self.type)
		self.scr.set_flag("maljakot")

		if self.maljakot_katottu():
			self.set_behaviour(self.onclick2)
		else:
			self.set_behaviour(self.onclick3)

	def maljakot_katottu(self):
		return self.scr.get_flag("maljakot")==3

	def onclick3(self):
		if self.maljakot_katottu():
			# paastaan pois tasta, vaihdetaankin tapahtumaa
			self.set_behaviour(self.onclick2)
			self.onclick()
			return
		
		self.g.player.say("Kato nyt ne loputkin maljakot")
	
	def onclick2(self):
		self.g.player.say("Hyisseitan ku ruma")

class ScreenTransition(kliksu.ScreenObject):
	def __init__(self, rect):
		super(ScreenTransition,self).__init__(rect)
		self.set_type("transitio")
		self.set_behaviour(self.vaihda)
		self.target = None

	def set_target(self, target):
		self.target = target

	def vaihda(self):
		if self.target == None:
			print "Aseta transitiolle joku kohdescreeni!"
			return
		self.g.set_screen(self.target)
		
	def set_img(self):
		self.img = pygame.Surface((self.rect[2],self.rect[3]))
		self.img.fill((196,64,64))


game = kliksu.KaikkiTietavaJumalObjektiJotaPassaillaanYmpariinsaKoskaIlmeisestiGlobaalitObjektitOnPahojaMuttaOnkoTamaNytSittenYhtaanKivempaaKysynpahanVaan()

# maljakkohuoneen maarittely
trans = ScreenTransition((16,180,30,48))
trans.set_target("tauluhuone")
swag = [TestVase((340,200,64,128)),
        TestVase((420,200,64,128)),
        TestVase((500,200,64,128)),
        trans
        ]
scr = kliksu.Screen(game, swag)
game.add_screen("maljakkohuone", scr)
# aloitetaan maljakkohuoneesta
game.set_screen("maljakkohuone")

# tauluhuoneen maarittely
trans = ScreenTransition((594,180,30,48))
trans.set_target("maljakkohuone")
swag = [TestPainting((128,64,128,96)), 
        trans
        ]
scr = kliksu.Screen(game, swag)
game.add_screen("tauluhuone", scr)

game.play()
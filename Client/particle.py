import pygame, time
from random import randint

class Particle:

	def __init__(self, x, y, color, tt, gravity):
		self.x = x
		self.y = y
		self.color = color
		self.timetodie = (time.time() * 1000)  + tt
		self.active = True
		self.gravity = gravity
		self.velY = 0

	def getColor(self):
		return self.color

	def _loop(self, scene):
		if self.gravity:
			self.velY -= 7
		self.y += self.velY

	def _render(self, scene):
		pygame.draw.circle(scene.getSurface(), self.color, (self.x, self.y), 1)

class GunshotParticle(Particle):

	def __init__(self, x, y):
		Particle.__init__(self, x, y, (100, 255,100), 100, True)
		self.shots = []
		self.speed = 1
		#print "CREATED"
		for var in range(0, 4):
			self.shots.append(Particle(self.x, self.y, self.color, 100, True))

	def loop(self, scene):

		now = time.time() * 1000
		if now > self.timetodie:
			print "REMOVED"
			scene.particles.remove(self)
			return

		Particle._loop(self, scene)
		self.shots[0].x += self.speed + randint(-1, 1) 
		self.shots[0].y += self.speed + randint(-1, 1) 

		self.shots[1].x -= self.speed + randint(-1, 1) 
		self.shots[1].y -= self.speed + randint(-1, 1) 

		self.shots[2].x -= self.speed+ randint(-1, 1) 
		self.shots[2].y += self.speed+ randint(-1, 1) 

		self.shots[3].x += self.speed+ randint(-1, 1) 
		self.shots[3].y -= self.speed+ randint(-1, 1) 




	def render(self, scene):
		#print "RENDERING"
		for particle in self.shots:
			particle._render(scene)

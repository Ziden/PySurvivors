import pygame, time

class Particle:

	def __init__(self, x, y, color, timetodie, gravity):
		self.x = x
		self.y = y
		self.color = color
		self.timetodie = time.time() * 1000  + timetodie
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
		Particle.__init__(self, x, y, (100, 255,100), 200, True)
		self.shots = []
		self.speed = 1
		for var in range(0, 4):
			self.shots.append(Particle(self.x, self.y, self.color, 200, True))

	def loop(self, scene):

		now = time.time() * 1000
		if now > self.timetodie:
			scene.particles.remove(self)
			return

		Particle._loop(self, scene)
		self.shots[0].x += self.speed
		self.shots[0].y += self.speed

		self.shots[1].x -= self.speed
		self.shots[1].y -= self.speed

		self.shots[2].x -= self.speed
		self.shots[2].y += self.speed

		self.shots[3].x += self.speed
		self.shots[3].y -= self.speed


	def render(self, scene):
		for particle in self.shots:
			particle._render(scene)

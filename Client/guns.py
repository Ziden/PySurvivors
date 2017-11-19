import pygame, math, zombiemath, time
from zombiemath import LineGeometry, line_intersects_rect
from random import randint
from particle import GunshotParticle
import time
import player

class Gun:

	def __init__(self):
		self.name = "Gun"
		self.damage = 0
		self.ammo = 0
		self.bullet = "Bullet"
		self.angle = 0
		self.shotCooldown = 90
		self.lastShot = time.time() * 1000 + self.shotCooldown
		self.angleVariation = 5

	def _shoot(self, scene):
		now = time.time() * 1000
		if now < self.lastShot:
			return
		angle = scene.getPlayer().angle + randint(-self.angleVariation, self.angleVariation)
		bulletClass = globals()[self.bullet]
		scene.bullets.append(bulletClass(angle))
		self.lastShot = now + self.shotCooldown

	def shoot(self, scene):
		pass


class Rifle(Gun):

	def __init__(self):
		Gun.__init__(self)
		self.name = "Rifle"
		self.damage = 3
		self.ammo = 10
		self.bullet = "RifleShot" # The class name
		self.angleVariation = 5
		self.shotCooldown = 110

	def shoot(self, scene):
		Gun._shoot(self, scene)


class Bullet:

	def __init__(self, angle, distance = 300):
		self.x = 400
		self.y = 300
		# Fixin the gun aim
		self.angle = math.radians(360-angle + 15)
		angleLower = math.radians(360-angle)
		# Calculating the starting point
		self.x = player.startX + 30 * math.cos(self.angle)
		self.y = player.startY + 30 * math.sin(self.angle)
		# Calculating end point
		self.endx = self.x + distance * math.cos(angleLower)
		self.endy = self.y + distance * math.sin(angleLower)
		self.line = LineGeometry(self.x, self.y, self.endx, self.endy)
		self.hits = []
		self.millis = time.time() * 1000 + 10
		self.collided = False

	def checkHits(self, scene):
		closestZombie = None
		closestDistance = 999
		for zombie in scene.zombies:
			if scene.isInRange(zombie, 550):
				collision = zombiemath.line_intersects_rect(self.line, zombie.rect, True)
				if len(collision) > 0:
					distance = zombiemath.distance((zombie.x, zombie.y), (scene.getPlayer().x, scene.getPlayer().y))
					if distance < closestDistance:
						closestZombie = zombie
						closestDistance = distance
		if closestZombie is not None:
			self.hits.append(closestZombie)

		if len(self.hits) > 0:
			for hit in self.hits:
				hit.hit(scene)
				self.hits.remove(hit)
				break

	def _loop(self, scene):

		# Only check bullet hits first frame
		if not self.collided:
			self.collided = True
			self.checkHits(scene)

		now = time.time() * 1000
		if now > self.millis:
			scene.bullets.remove(self)

	def _render(self, scene):
		pygame.draw.line(scene.getSurface(), (255,randint(0,10),0), (self.x, self.y), (self.endx,self.endy), 1)



class RifleShot(Bullet):

	def __init__(self, angle):
		Bullet.__init__(self, angle, 300)
		# Comin ou the rifle
		self.splatter = [[
			 # Right angled boom
			 self.x + 15 * math.cos(math.radians(360-angle+35)),
			 self.y + 15 * math.sin(math.radians(360-angle+35))
		],[
		    # Left angled boom
			self.x + 15 * math.cos(math.radians(360-angle-35)),
			self.y + 15 * math.sin(math.radians(360-angle-35))
		],[
		    # Center angled boom
			self.x + 15 * math.cos(math.radians(360-angle)),
			self.y + 15 * math.sin(math.radians(360-angle))
		]]
		
	def loop(self, scene):
		Bullet._loop(self, scene)

	def render(self, scene):
		Bullet._render(self, scene)

		# Shot splatter ("boom" animation)
		pygame.draw.line(scene.getSurface(), (255,randint(0,100),0), (self.x, self.y), (self.splatter[0][0], self.splatter[0][1]), 3)
		pygame.draw.line(scene.getSurface(), (255,randint(0,100),0), (self.x, self.y), (self.splatter[1][0], self.splatter[1][1]), 3)
		pygame.draw.line(scene.getSurface(), (255,randint(0,100),0), (self.x, self.y), (self.splatter[2][0], self.splatter[2][1]), 2)



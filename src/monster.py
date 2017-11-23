import pygame, math, time
from screens import GameOverScreen
import zombiemath
import random
from particle import GunshotParticle

class Monster:

	def __init__(self, sprite, x, y):
		self.x = x
		self.y = y
		self.sprite = sprite
		self.drawSprite = None
		self.angle = 0
		self.desiredAngle = 0
		self.rect = None
		self.hp = 100
		self.alive = True

	def _hit(self, scene, bullet):
		# Standard Hit Animation
		self.hp -= scene.getPlayer().gun.damage
		if(self.hp < 0):
			print "REMOVED"
			scene.zombies.remove(self)
			self.alive = False
		
	def _render(self, scene):
		self.rect = self.drawSprite.get_rect(center=(self.x+scene.cameraPosition[0],self.y+scene.cameraPosition[1]))
		scene.getSurface().blit(self.drawSprite, self.rect)

	def _loop(self, scene):
		# Adjusting angle
		angleDifference = self.desiredAngle - self.angle
		if(angleDifference > 180):
			angleDifference = -360 + self.desiredAngle - self.angle 
		if(angleDifference < -180):
			angleDifference =   360 - self.angle - self.desiredAngle
		self.angle = self.angle + angleDifference / 20

class Zombie(Monster):

	def __init__(self, scene, x, y):
		Monster.__init__(self, scene.getResources().zombie, x, y)
		self.hp = 50
		self.lastHit = time.time() * 1000

	def hit(self, scene, bullet):
		self._hit(scene, bullet)
		if not self.alive:
			return
		hitX = int(self.x + scene.cameraPosition[0])
		hitY = int(self.y + scene.cameraPosition[1])
		# Hit zombie particles
		scene.particles.append(GunshotParticle(hitX, hitY))
		# Hit pushback Animations
		newPosition = zombiemath.polarCoordinates(self.x, self.y, 5, math.radians(360-scene.getPlayer().angle))
		self.x += newPosition[0]
		self.y += newPosition[1]
		# Zombie hit rotation
		angleToPlayer = scene.getPlayer().getAngleToObject(self.x + scene.cameraPosition[0], self.y + scene.cameraPosition[1])
		shotDifference = bullet.angle - angleToPlayer
		if(shotDifference > 0):
			self.angle += 25
		else:
			self.angle -= 25
		self.lastHit = time.time() * 1000

	def justTakenHit(self):
		return time.time() * 1000 < self.lastHit + 100

	def render(self, scene):
		# Rotate towards player first
		self.desiredAngle = 260+math.atan2(scene.getPlayer().x-45-self.x,scene.getPlayer().y-30-self.y)*180/math.pi
		self.drawSprite = pygame.transform.rotate(self.sprite,self.angle)
		self._render(scene)

	def loop(self, scene):
		# Going towards player
		dx, dy = (scene.getPlayer().x-55- self.x, scene.getPlayer().y-20 - self.y)
		stepx, stepy = (dx / 25., dy / 25.) # lerp effect (linear interpolation)
		if self.justTakenHit(): 
			return
		self.x += stepx / 4
		self.y += stepy / 4
		if ( math.fabs(dx) < 30 and math.fabs(dy) < 30 and scene.screen is None ):
			scene.screen = GameOverScreen(scene)
		self._loop(scene)
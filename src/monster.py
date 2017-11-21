import pygame, math
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
		self.hp = 10

	def _hit(self, scene):
		# Standard Hit Animation
		if(random.choice([True, False])):
			self.angle += 25
		else:
			self.angle -= 25
		
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
		self.angle = self.angle + angleDifference / 10


class Zombie(Monster):

	def __init__(self, scene, x, y):
		Monster.__init__(self, scene.getResources().zombie, x, y)

	def hit(self, scene):
		self._hit(scene)
		hitX = int(self.x + scene.cameraPosition[0])
		hitY = int(self.y + scene.cameraPosition[1])
		# Hit zombie particles
		scene.particles.append(GunshotParticle(hitX, hitY))
		# Hit pushback Animations
		newPosition = zombiemath.polarCoordinates(self.x, self.y, 8, math.radians(360-scene.getPlayer().angle))
		self.x += newPosition[0]
		self.y += newPosition[1]

	def render(self, scene):
		# Rotate towards player first
		self.desiredAngle = 260+math.atan2(scene.getPlayer().x-45-self.x,scene.getPlayer().y-30-self.y)*180/math.pi
		self.drawSprite = pygame.transform.rotate(self.sprite,self.angle)
		self._render(scene)

	def loop(self, scene):
		# Going towards player
		dx, dy = (scene.getPlayer().x-55- self.x, scene.getPlayer().y-20 - self.y)
		stepx, stepy = (dx / 25., dy / 25.) # lerp effect (linear interpolation)
		self.x += stepx / 4
		self.y += stepy / 4
		if ( math.fabs(dx) < 30 and math.fabs(dy) < 30 and scene.screen is None ):
			scene.screen = GameOverScreen(scene)
		self._loop(scene)
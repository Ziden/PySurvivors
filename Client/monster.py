import pygame, math
from screens import GameOverScreen
import zombiemath

class Monster:

	def __init__(self, zombieSprite, x, y):
		self.x = x
		self.y = y
		self.sprite = zombieSprite
		self.angle = 0
		self.rect = None

	def render(self, scene):
		px = 300
		py = 200
		# 260 cause the sprite is already a little bit rotated
		angle  = 260+math.atan2(scene.getPlayer().x-45-self.x,scene.getPlayer().y-30-self.y)*180/math.pi
		self.angle = angle
		rotimage = pygame.transform.rotate(self.sprite,angle)
		rect = rotimage.get_rect(center=(self.x+scene.cameraPosition[0],self.y+scene.cameraPosition[1]))
		self.rect = rect

		# Debug
		pygame.draw.rect(scene.getSurface(), (0,255,0),rect)

		scene.getSurface().blit(rotimage, rect)

		


	def loop(self, scene):
		# Move towards the player center
		dx, dy = (scene.getPlayer().x-55- self.x, scene.getPlayer().y-20 - self.y)
		stepx, stepy = (dx / 25., dy / 25.) # lerp effect (linear interpolation)
		self.x += stepx / 4
		self.y += stepy / 4

		# Check if zombie hits a player
		if ( math.fabs(dx) < 30 and math.fabs(dy) < 30 and scene.screen is None):
			scene.screen = GameOverScreen(scene)
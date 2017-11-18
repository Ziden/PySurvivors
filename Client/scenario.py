#
# Class represents the game scenario
#

from player import Player
from player import Bullet
from random import randint
from monster import Monster
import pygame
import math

class Scene:

	def __init__(self, resources, display, gameFont):
		self._resources = resources
		self.display = display
		self.bounds = (-2000, -2000, 2000, 2000)
		self.font = gameFont
		self.generate()

	def generate(self):
		self._player = Player(self._resources.player)
    	# Trees in the map
		self.trees = []
		# Zombies in map
		self.zombies = []
		self.bullets = []
		# Any screen displayn ?
		self.screen = None
		self.cameraPosition = [0,0]
		self.cameraSpeed = 2
		
		# Generating trees
		for x in range(0, 60):
			rX = randint(self.bounds[0], self.bounds[2])
			rY = randint(self.bounds[1], self.bounds[3])
			self.trees.append(Tree(rX, rY))

		# Initial Zombies
		for x in range(0, 1):
			rX = randint(self.bounds[0], self.bounds[2])
			rY = randint(self.bounds[1], self.bounds[3])
			self.zombies.append(Monster(self._resources.zombie, rX, rY))

	def playerShoot(self):
		angle = self._player.angle
		if(len(self.bullets)==0):
			self.bullets.append(Bullet(angle))
		else:
			self.bullets[0] = Bullet(angle) # Clean memory ?

	def getSurface(self):
		return self.display

	def getPlayer(self):
		return self._player

	def getResources(self):
		return self._resources

	def movePlayer(self, direction):
		if direction == 6:
			if self.cameraPosition[0] < 2000 + 300:
				self.cameraPosition[0] += self.cameraSpeed
		if direction == 4:
			if self.cameraPosition[0] > -2000 +400:
				self.cameraPosition[0] -= self.cameraSpeed
		if direction == 2:
			if self.cameraPosition[1] > -2000 + 320:
				self.cameraPosition[1] -= self.cameraSpeed
		if direction == 8:
			if self.cameraPosition[1] < 2000 + 220:
				self.cameraPosition[1] += self.cameraSpeed

	def render(self):
		self._player.render(self)
		for tree in self.trees:
			if self.isInRange(tree, 550, 350):
				tree.render(self, self._resources.tree)

		for zombie in self.zombies:
			if self.isInRange(zombie, 550, 350):
				zombie.render(self)

		for bullet in self.bullets:
			if self.isInRange(bullet, 550, 350):
				bullet.render(self)

		pygame.draw.rect(self.display, (0,0,0), [-2000+self.cameraPosition[0], -2000+self.cameraPosition[1], 4000, 4000], 5)

	def loop(self):
		for zombie in self.zombies:
			if self.isInRange(zombie , 550, 350):
				zombie.loop(self)

		for bullet in self.bullets:
			if self.isInRange(bullet, 550, 350):
				bullet.loop(self)

    # Range check if we should loop / render stuff or not
	def isInRange(self, o2, rangeX, rangeY):
		o1 = self._player
		distanceX = math.fabs(o1.x - o2.x)
		distanceY = math.fabs(o1.y - 60 - o2.y)
		if distanceX > rangeX or distanceY > rangeY:
			return False
		return True

############
## CAMERA ##
############
class Camera:

	def __init__(self):
		self.x = 0
		self.y = 0

###########
## TREES ##
###########
class Tree:
    	
    	def __init__(self, x, y):
    		self.x = x
    		self.y = y

    	def render(self, scene, sprite):
    		scene.getSurface().blit(sprite, (self.x + scene.cameraPosition[0], self.y + scene.cameraPosition[1]))
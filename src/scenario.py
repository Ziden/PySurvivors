#
# Class represents the game scenario
#

from player import Player
from random import randint
from monster import Zombie
import zombiemath
import pygame
import math

class Scene:

	zombies = []
	bullets = []
	particles = []

	cameraPosition = [0,0]

	screen = None

	def __init__(self, resources = None, display = None, gameFont = None):
		self._resources = resources
		self.display = display
		self.bounds = (-2000, -2000, 2000, 2000)
		self.font = gameFont
		self.generate()

	def generate(self):
		self._player = Player(self._resources.player)
		self.trees = []
		self.zombies = []
		self.bullets = []
		self.particles = []
		# Any game screen displayn ?
		self.screen = None

		# Camera
		self.cameraPosition = [0,0]
		self.cameraSpeed = 2
		
		# Generating trees
		for x in range(0, 100):
			rX = randint(self.bounds[0], self.bounds[2])
			rY = randint(self.bounds[1], self.bounds[3])
			self.trees.append(Tree(rX, rY))

		# Initial Zombies
		for x in range(0, 1):
			rX = randint(self.bounds[0], self.bounds[2])
			rY = randint(self.bounds[1], self.bounds[3])
			self.zombies.append(Zombie(self, rX, rY))

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
		
		for zombie in self.zombies:
			if self.isInRange(zombie, 550):
				zombie.render(self)

		for bullet in self.bullets:
				bullet.render(self)

		for particle in self.particles:
			particle.render(self)

		for tree in self.trees:
			if self.isInRange(tree, 550):
				tree.render(self, self._resources.tree)

		pygame.draw.rect(self.display, (0,0,0), [-2000+self.cameraPosition[0], -2000+self.cameraPosition[1], 4000, 4000], 5)

	def loop(self):
	
		self._player.loop(self)		

		for zombie in self.zombies:
			#if self.isInRange(zombie , 450):
			zombie.loop(self)

		for bullet in self.bullets:
			bullet.loop(self)

		for particle in self.particles:
			particle.loop(self)

    # Range check if we should loop / render stuff or not
	def isInRange(self, o2, range):
		o1 = self._player
		distanceX = math.fabs(o1.x - o2.x)
		distanceY = math.fabs(o1.y - o2.y)
		if distanceX > range or distanceY > range - 100:
			return False
		return True

###########
## TREES ##
###########
class Tree:
    	
    	def __init__(self, x, y):
    		self.x = x
    		self.y = y

    	def render(self, scene, sprite):
    		scene.getSurface().blit(sprite, (self.x + scene.cameraPosition[0], self.y + scene.cameraPosition[1]))
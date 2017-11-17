#
# Class represents the game scenario
#

from player import Player
from random import randint
from monster import Monster
import pygame

class Scene:

	def __init__(self, resources, display):
		self._player = Player(resources.player)
		self._resources = resources
		self.display = display
		self.bounds = (-2000, -2000, 2000, 2000)
		self.trees = []
		self.zombies = []
		self.cameraPosition = [0,0]
		self.cameraSpeed = 5

		# Generating trees
		for x in range(0, 60):
			rX = randint(self.bounds[0], self.bounds[2])
			rY = randint(self.bounds[1], self.bounds[3])
			self.trees.append(Tree(rX, rY))

		for x in range(0, 60):
			rX = randint(self.bounds[0], self.bounds[2])
			rY = randint(self.bounds[1], self.bounds[3])
			self.zombies.append(Monster(self._resources.zombie, rX, rY))

	def getSurface(self):
		return self.display

	def getPlayer(self):
		return self._player

	def movePlayer(self, direction):
		print(self.cameraPosition[0])
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
			tree.render(self, self._resources.tree)
		for zombie in self.zombies:
			zombie.render(self)
		pygame.draw.rect(self.display, (0,0,0), [-2000+self.cameraPosition[0], -2000+self.cameraPosition[1], 4000, 4000], 5)



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
#
# Class represents the game scenario
#

from player import Player
from random import randint

class Scene:

	def __init__(self, resources, display):
		self._player = Player(resources.player)
		self._resources = resources
		self._display = display
		self.bounds = (-2000, -2000, 2000, 2000)
		self.trees = []
		for x in range(0, 45):
			rX = randint(self.bounds[0], self.bounds[2])
			rY = randint(self.bounds[1], self.bounds[3])
			self.trees.append(Tree(rX, rY))

	def getPlayer(self):
		return self._player

	def render(self):
		self._player.render(self._display)
		for tree in self.trees:
			tree.render(self._display, self._resources.tree)

class Tree:
    	
    	def __init__(self, x, y):
    		self.x = x
    		self.y = y

    	def render(self, display, sprite):
    		display.blit(sprite, (self.x, self.y))
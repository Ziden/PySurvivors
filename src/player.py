import pygame, math, zombiemath, time
from zombiemath import LineGeometry, line_intersects_rect
from random import randint
from guns import RifleShot
from guns import Rifle
import time


startX = 400-55
startY = 300-32


class Player:

	def __init__(self, playerSprite):
		self.x = 400
		self.y = 300
		self.speed = 1
		self.size = (55, 32)
		self.sprite = playerSprite
		self.x -= self.size[1]/2
		self.y -= self.size[0]/2
		self.angle = 0
		self.rect = None
		self.shooting = False
		self.gun = Rifle()

	def __shoot(self, scene):
		self.gun._shoot(scene)

	def render(self, scene):
		self.x = 400 - scene.cameraPosition[0]
		self.y = 300 - scene.cameraPosition[1]
		pos = pygame.mouse.get_pos()
		angle = 360-math.atan2(pos[1]-270,pos[0]-350)*180/math.pi
		self.angle = angle
		rotimage = pygame.transform.rotate(self.sprite,angle)
		rect = rotimage.get_rect(center=(400-55,300-32))
		self.rect = rect
		scene.getSurface().blit(rotimage, rect)

	def loop(self, scene):
		if(self.shooting):
			self.__shoot(scene)









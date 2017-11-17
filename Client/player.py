import pygame, math

class Player:

	def __init__(self, playerSprite):
		self.x = 400
		self.y = 300
		self.speed = 1
		self.size = (55, 32)
		self.sprite = playerSprite
		self.x -= self.size[1]/2
		self.y -= self.size[0]/2

	def render(self, scene):
		self.x = 400 - scene.cameraPosition[0]
		self.y = 300 - scene.cameraPosition[1]
		pos = pygame.mouse.get_pos()
		angle = 360-math.atan2(pos[1]-280,pos[0]-350)*180/math.pi
		rotimage = pygame.transform.rotate(self.sprite,angle)
		rect = rotimage.get_rect(center=(400-55,300-32))
		scene.getSurface().blit(rotimage, rect)




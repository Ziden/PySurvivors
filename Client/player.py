import pygame, math

class Player:

	def __init__(self, playerSprite):
		self.x = 400
		self.y = 300
		self.speed = 1
		self.size = (64, 109)
		self.sprite = playerSprite
		self.x -= self.size[1]/2
		self.y -= self.size[0]/2

	def move(self, dir):
		if dir==4:
			self.x += self.speed
		elif dir==2:
			self.x -= self.speed

	def render(self, display):
		pos = pygame.mouse.get_pos()
		angle = 360-math.atan2(pos[1]-self.size[0],pos[0]-self.size[1])*180/math.pi
		rotimage = pygame.transform.rotate(self.sprite,angle)
		rect = rotimage.get_rect(center=(self.size[0],self.size[1]))
		display.blit(rotimage, rect)




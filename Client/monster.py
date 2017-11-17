import pygame, math

class Monster:

	def __init__(self, zombieSprite, x, y):
		self.x = x
		self.y = y
		self.sprite = zombieSprite

	def render(self, scene):
		px = 300
		py = 200
		angle  = 360-math.atan2(px-self.x+scene.cameraPosition[0],py-self.y+scene.cameraPosition[1])*180/math.pi
		rotimage = pygame.transform.rotate(self.sprite,angle)
		rect = rotimage.get_rect(center=(self.x+scene.cameraPosition[0],self.y+scene.cameraPosition[1]))
		scene.getSurface().blit(rotimage, rect)

		#scene.getSurface().blit(self.sprite, (self.x++scene.cameraPosition[0], self.y++scene.cameraPosition[1]))
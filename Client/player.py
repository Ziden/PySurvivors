import pygame, math

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

	def render(self, scene):
		self.x = 400 - scene.cameraPosition[0]
		self.y = 300 - scene.cameraPosition[1]

		# Debug
		pygame.draw.circle(scene.getSurface(), (0,0,255), [400-55,300-32], 30)

		pos = pygame.mouse.get_pos()
		angle = 360-math.atan2(pos[1]-280,pos[0]-350)*180/math.pi
		self.angle = angle
		rotimage = pygame.transform.rotate(self.sprite,angle)
		rect = rotimage.get_rect(center=(400-55,300-32))
		scene.getSurface().blit(rotimage, rect)



class Bullet:

	def __init__(self, angle):
		self.x = 400
		self.y = 300
		self.angle = math.radians(360-angle + 15)

		print(self.angle)

		# Calculating the starting point
		self.x = startX + 30 * math.cos(self.angle)
		self.y = startY + 30 * math.sin(self.angle)

	def loop(self, scene):
		pass

	def render(self, scene):
		pos = pygame.mouse.get_pos()
		pygame.draw.line(scene.getSurface(), (255,0,0), (self.x, self.y), (pos[0],pos[1]), 2)







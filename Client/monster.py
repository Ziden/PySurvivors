import pygame, math

class Monster:

	def __init__(self, zombieSprite, x, y):
		self.x = x
		self.y = y
		self.sprite = zombieSprite

	def render(self, scene):
		px = 300
		py = 200
		#260 cause the sprite is already a little bit rotated
		angle  = 260+math.atan2(scene.getPlayer().x-self.x,scene.getPlayer().y-self.y)*180/math.pi
		rotimage = pygame.transform.rotate(self.sprite,angle)
		rect = rotimage.get_rect(center=(self.x+scene.cameraPosition[0],self.y+scene.cameraPosition[1]))
		scene.getSurface().blit(rotimage, rect)

	def loop(self, scene):
		# move towards the player center
		dx, dy = (scene.getPlayer().x-55- self.x, scene.getPlayer().y-20 - self.y)
		stepx, stepy = (dx / 25., dy / 25.) # lerp effect (linear interpolation)
		self.x += stepx / 4
		self.y += stepy / 4
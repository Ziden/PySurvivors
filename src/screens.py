import pygame, math
import time

###############
# Upper Class #
###############

class Screen(object):

	scene = None

	# Construct with a background
	def __init__(self, scene):
		self.background = None

	# Sets background sprite
	def setBackground(self, backgroundSprite):
		self.background = pygame.transform.scale(backgroundSprite, (800, 600))

	def render(self, scene):
		self._render(scene)

	# Render method
	def _render(self, scene):
		if self.background is not None:
			scene.getSurface().blit(self.background, (0,0))

	# Screen logic if needed
	def loop(self, scene):
		self._loop(scene)

	def _loop(self, scene):
		pass

###########
# SCREENS *
###########

class GameOverScreen(Screen):

	def __init__(self, scene):
		self.countdownTimer = 5
		self.startTime = int(round(time.time()))
		Screen.__init__(self, scene)
		Screen.setBackground(self, scene.getResources().gameover)

	# Override
	def render(self, scene):
		Screen._render(self, scene)
		textsurface = scene.font.render('You Are Dead', False, (255, 0, 0))
		text_rect = textsurface.get_rect(center=(800/2, 20))
		scene.getSurface().blit(textsurface,text_rect)

		textsurface = scene.font.render('Wait '+`self.countdownTimer`+' Seconds', False, (255, 0, 0))
		text_rect = textsurface.get_rect(center=(800/2, 100))
		scene.getSurface().blit(textsurface,text_rect)

	def loop(self, scene):
		Screen._loop(self, scene)
		now = int(round(time.time()))
		self.countdownTimer = 5 - (now - self.startTime)
		if self.countdownTimer == -1:
			scene.generate()
			scene.screen = None







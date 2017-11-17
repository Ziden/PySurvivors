import pygame
from pygame.locals import *
from scenario import Scene
from resources import Resources

class App:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 800, 600 # fixed, meh
        
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption('Survive Zombies')
        self._running = True
        self.resources = Resources()
        self.scene = Scene(self.resources, self._display_surf)
        self.clock = pygame.time.Clock()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
       
    def on_loop(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]: self.scene.movePlayer(6)
        if pressed[pygame.K_d]: self.scene.movePlayer(4)
        if pressed[pygame.K_w]: self.scene.movePlayer(8)
        if pressed[pygame.K_s]: self.scene.movePlayer(2)

    def on_render(self):
        self._display_surf.fill((46,155,25))
        self.scene.render()
        pygame.display.update()
        self.clock.tick(120)

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        ####################
        ## MAIN GAME LOOP ##
        ####################
        while( self._running ):

            # Processing Events
            for event in pygame.event.get():
                self.on_event(event)

            # Processing Game Logic    
            self.on_loop()
            
            # Rendering 
            self.on_render()

        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
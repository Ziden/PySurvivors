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
        self._display_surf.fill((46,155,25))
        self._running = True
        self.resources = Resources()
        self.scene = Scene(self.resources, self._display_surf)
        self.clock = pygame.time.Clock()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.scene.getPlayer().move(6)
            elif event.key == pygame.K_a:
                self.scene.getPlayer().move(4)

    def on_loop(self):
       pass

    def on_render(self):
        self.scene.render()
        pygame.display.update()
        self.clock.tick(60)

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
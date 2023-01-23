import pygame
import settings
from scene import Scene



class Pause_Menu(Scene):
    def __init__(self, window, game):
        super().__init__(window)
        self.game = game
        
        # Werte sind egal, wir eh neu gemacht
        self.size = (0,0)
        self.rebuild_screen(self.size)
                
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.window.change_scene("game")

    def rebuild_screen(self, new_size: tuple[int, int]):
        self.screen = pygame.surface.Surface(new_size, pygame.SRCALPHA)
        self.screen.fill((0, 0, 0, 128))
        text = f"Pausiert! Drücke {pygame.key.name(settings.keybinds['pause'][0])} um fortzufahren"
        text_image = settings.pause_font.render(text, True, (255, 255, 255))
        window_center = self.window.screen.get_rect().center
        renderpos = window_center[0] - text_image.get_width() // 2, window_center[1] - text_image.get_height() // 2
        self.screen.blit(text_image, renderpos)
        
    def draw(self):
        window_size = self.window.screen.get_size()
        if window_size != self.size:
            self.rebuild_screen(window_size)
        self.game.draw()
        self.window.screen.blit(self.screen, (0, 0))
        
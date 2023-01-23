import pygame



class Scene:
    def __init__(self, window):
        self.window = window
        self.subscreeens = []

    def find_clicked_subscreen(self, pos):
        for subscreen in self.subscreeens:
            if subscreen.rect.collidepoint(pos):
                return subscreen
        return None

    def toggle_subscreen(self, subscreen):
        if subscreen in self.subscreeens:
            self.subscreeens.remove(subscreen)
        else:
            self.subscreeens.append(subscreen)
    
    # Boilerplate

    def update(self):
        pass
    
    def draw(self):
        self.window.screen.fill((255, 255, 255))
    
    def handle_events(self, events):
        pass
    
    def shutdown(self):
        pass
    
# class Subscreen:
#     def __init__(self, surface: pygame.Surface, scene: Scene):
#         self.surface = surface
#         self.scene.subscreeens.append(self)
    
#     def draw(self, relative_pos: tuple[int, int] = (0, 0)):
#         self.scene.window.screen.blit(self.surface, relative_pos)
    
#     def handle_click(self, relative_pos: tuple[int, int]):	
#         pass
    
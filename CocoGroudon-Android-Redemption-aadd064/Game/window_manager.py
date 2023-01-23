import pygame
pygame.init()
pygame.display.init()
pygame.font.init()
import settings
import pause_menu

from scene import Scene


    
class Window:
    screen = pygame.display.set_mode((500,500), pygame.RESIZABLE)
    isRunning = True
    
    def __init__(self) -> None:
        
        self.clock = pygame.time.Clock()
        self.scenes: Scene = {}
        self.current_scene:Scene = None

        from game import Game, play_mode, Mode_Edit

        self.game_scene = Game(window_manager=self)
        self.game_scene = play_mode(self.game_scene)
        self.scenes["game"] = self.game_scene
        
        self.pause_screen = pause_menu.Pause_Menu(window=self, game=self.game_scene)
        self.scenes["pause"] = self.pause_screen
        
        self.current_scene = self.scenes["pause"]
    
    def filter_events(self, events):
        myEvents = []
        for event in events:
            if event.type == pygame.QUIT:
                self.isRunning = False
                continue
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_1:
                    self.current_scene = self.scenes["game"]
                elif event.key == pygame.K_KP_2:
                    self.current_scene = self.scenes["pause"]
            myEvents.append(event)
        return myEvents
    
    def change_scene(self, scene_name):
        self.current_scene = self.scenes[scene_name]
    
    def run(self):
        while self.isRunning:
            # print(self.clock.get_fps())
            events = self.filter_events(pygame.event.get())
            
            self.current_scene.update()
            self.current_scene.draw()
            self.current_scene.handle_events(events=events)
            
            pygame.display.flip()
            self.clock.tick(settings.framerate)
        for scene_name in self.scenes:
            scene = self.scenes[scene_name]
            scene.shutdown()
            
            
if __name__ == "__main__":
    window = Window()
    window.run()
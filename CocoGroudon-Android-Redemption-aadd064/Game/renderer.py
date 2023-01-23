import pygame
import math

import settings
import assets
from world import WorldEngine
from physics import get_angle_to_world_pos

class Renderer:
    def __init__(self,* , game_engine_ref ,world_engine_ref:WorldEngine) -> None:
        self.game = game_engine_ref
        self.wold_engine = world_engine_ref
        self.camera_ofset = [0,0]

        pygame.font.init()
        self.debug_font = pygame.font.SysFont("Calibri", 15)
        self.inventory_show = False
    
        self.screen:pygame.surface.Surface = self.game.screen
        
        pygame.font.init()
    
        self.world_screen = pygame.Surface((len(self.wold_engine.world)*settings.blocksize, len(self.wold_engine.world[0])*settings.blocksize), flags=pygame.SRCALPHA)
        self.update_world_surface()
        
        self.debug_font = pygame.font.SysFont("Calibri", 15)
        self.debug_screen = pygame.Surface((300, 500), flags=pygame.SRCALPHA)
        
        self.block_choices_screen = pygame.Surface((settings.blocksize, len(settings.block_choices)*settings.blocksize), flags=pygame.SRCALPHA)
        self.block_choices_screen_update()

    def draw(self):
        self.blit_paralax_background(assets.paralax_background[0], 0.05)
        self.blit_paralax_background(assets.paralax_background[1], 0.1, settings.blocksize)
        self.blit_paralax_background(assets.paralax_background[2], 0.3, settings.blocksize*2)
        self.blit_paralax_background(assets.paralax_background[3], 0.6, settings.blocksize*4)
        self.blit_paralax_background(assets.paralax_background[4], 0.8, settings.blocksize*6)
        self.blit_paralax_background(assets.paralax_background[5], 1, settings.blocksize*10)
        self.blit_world()
        self.blit_entities()
        self.blit_player()
        self.blit_player_inventory()
        self.blit_projectiles()
                
        if settings.world_edit_mode:
            self.screen.blit(self.block_choices_screen, settings.block_choices_screen_ofsett)
        
        if settings.debug_mode:
            self.debu_menu_update()
            self.screen.blit(self.debug_screen, (10,10))
        
        if settings.draw_trigger_zones:
            self.blit_trigger_zones()
            
    def blit_trigger_zones(self):
        for trigger in self.game.physics_engine.trigger_zones:
            self.screen.blit(trigger.surface, trigger.move(self.camera_ofset))
            # pygame.draw.rect(self.screen, settings.trigger_zone_color, trigger.move(self.camera_ofset))
            
    def blit_world(self):
        self.screen.blit(self.world_screen, self.camera_ofset)
    
    def update_world_surface(self):
        self.world_screen = pygame.Surface((len(self.wold_engine.world)*settings.blocksize, len(self.wold_engine.world[0])*settings.blocksize), flags=pygame.SRCALPHA)
        self.world_screen.fill((0,0,0,0))
        self.wold_engine.block_sprite_group.draw(self.world_screen)
           
    def debu_menu_update(self):
        self.debug_screen.fill((0,0,0,0))
        fpsText = self.debug_font.render(f"FPS : {round(self.game.window_manager.clock.get_fps(),3)}", False, 6)
        self.debug_screen.blit(fpsText, (0,0))
            
    def blit_entities(self):
        for entity in self.game.physics_engine.entity_group:
            self.blit_sprite(entity)
            self.blit_element_rect(entity.health.get_screen(), entity.rect)
        
    def blit_player(self):
        ''' blits player and healt screen of player'''
        self.blit_sprite(self.game.physics_engine.player)
        
        healt_screen = self.game.physics_engine.player.health.get_screen()
        self.screen.blit(self.game.physics_engine.player.health.get_screen(), (self.screen.get_width()-healt_screen.get_width(),0))

    def blit_player_inventory(self):
        hand_item = self.game.physics_engine.player.inventory.get_hand_item()
        if hand_item:
            player_center = self.game.physics_engine.player.rect.center
            origin = player_center[0]+self.camera_ofset[0] , player_center[1]+self.camera_ofset[1]
            angle = -math.degrees(get_angle_to_world_pos(origin, pygame.mouse.get_pos()))
            image = pygame.transform.rotate(hand_item.image, angle)
            item_ofsett = image.get_width()/2, image.get_height()/2
            
            pos = player_center[0]+self.camera_ofset[0], player_center[1]+self.camera_ofset[1]
            pos = pos[0]-item_ofsett[0], pos[1]-item_ofsett[1]
            
            self.screen.blit(image, pos)
        if self.inventory_show:
            self.blit_inventory_full()
            
    def blit_inventory_full(self):
        ofset = self.inventory_get_ofsett()
        self.screen.blit(self.game.physics_engine.player.inventory.big_surface, ofset)

    def blit_paralax_background(self, image:pygame.image, speed:int, y_ofsett: int = 0):
        screen_width = self.screen.get_width()
        image_size = image.get_width()
        posX = (-self.camera_ofset[0]*speed) % image_size
    
        images_to_fit_screen = math.ceil(screen_width/image_size) +1
        for i in range(images_to_fit_screen):
            self.screen.blit(image, (-posX+i*image_size,self.camera_ofset[1]+y_ofsett))
            
    def blit_projectiles(self):
        for projectile in self.game.physics_engine.projectile_group:
            self.blit_sprite(projectile)

    def blit_sprite(self, sprite:pygame.sprite.Sprite):
        ''' Blits a pygame sprite with its self.image and self.rect atribute'''
        self.screen.blit(sprite.image, sprite.rect.move(self.camera_ofset))

    def blit_element_rect(self, image:pygame.Surface, rect:pygame.Rect):
        ''' !!!  If possible use "blit_sprite"  !!! \n
        blits an image at a rect position'''
        self.screen.blit(image, rect.move(self.camera_ofset))
        
    def get_world_block_for_mouse_pos(self, mouse_pos:tuple) -> tuple:
        mouse_x, mouse_y = mouse_pos
        
        mouse_x -= self.camera_ofset[0]
        mouse_y -= self.camera_ofset[1]
        
        mouse_x //= settings.blocksize
        mouse_y //= settings.blocksize
        
        # Keine Ahnung, warumm das da oben nicht automatisch in nen int macht, wenn es doch eh rundet
        mouse_x = int(mouse_x)
        mouse_y = int(mouse_y)
        
        return mouse_x, mouse_y
        
    def get_world_pos_for_mouse_pos(self, mouse_pos:tuple) -> tuple:
        mouse_x, mouse_y = mouse_pos
        
        mouse_x -= self.camera_ofset[0]
        mouse_y -= self.camera_ofset[1]
        
        return mouse_x, mouse_y
    
    def get_screen_pos_for_world_pos(self, world_pos:tuple) -> tuple:
        player_x, player_y = world_pos
        cam_ofset_x, cam_ofset_y = self.camera_ofset
        
        player_screen_x = player_x + cam_ofset_x
        player_screen_y = player_y + cam_ofset_y
        return player_screen_x, player_screen_y
    
    def block_choices_screen_update(self):
        self.block_choices_screen.fill((0,0,0,0))
        for index, block in enumerate(settings.block_choices):
            self.block_choices_screen.blit(assets.blocks[block], (0, index*settings.blocksize))
        pygame.draw.line(self.block_choices_screen, (255,255,255), (0,0), (settings.blocksize,0))
        pygame.draw.line(self.block_choices_screen, (255,255,255), (0,0), (0,settings.blocksize*len(settings.block_choices)-1))
        pygame.draw.line(self.block_choices_screen, (255,255,255), (0,settings.blocksize*len(settings.block_choices)-1), (settings.blocksize-1,settings.blocksize*len(settings.block_choices)-1))
        pygame.draw.line(self.block_choices_screen, (255,255,255), (settings.blocksize-1,0), (settings.blocksize-1,settings.blocksize*len(settings.block_choices)-1))
            
    def inventory_get_clicked(self, mouse_pos:tuple) -> tuple:
        ofset = self.inventory_get_ofsett()
        relateive_mouse_pos = [mouse - ofsett for mouse, ofsett in zip(mouse_pos, ofset)]
        clicked = self.game.physics_engine.player.inventory.big_surface.get_rect().collidepoint(relateive_mouse_pos)
        return clicked
        
    def inventory_get_clicked_pos(self, mouse_pos:tuple) -> tuple:
        ofset = self.inventory_get_ofsett()
        relateive_mouse_pos = [mouse - ofsett for mouse, ofsett in zip(mouse_pos, ofset)]
        block_x = math.floor(relateive_mouse_pos[1] / (settings.inventory_item_size*settings.inventory_scale))
        block_y = math.floor(relateive_mouse_pos[0] / (settings.inventory_item_size*settings.inventory_scale))
        print(f"{relateive_mouse_pos=} , {block_x=} {block_y=}")
        return block_x, block_y
    
    def inventory_get_ofsett(self) -> tuple:
        size_x, size_y = self.inventory_get_size()
        inv_screen_x = (self.screen.get_width() - size_x)/2
        inv_screen_y = (self.screen.get_height() - size_y)
        ofset = inv_screen_x, inv_screen_y
        return ofset
    
    def inventory_get_size(self) -> tuple:
        size_x = settings.inventory_size[0]*settings.inventory_scale*settings.inventory_item_size
        size_y = settings.inventory_size[1]*settings.inventory_scale*settings.inventory_item_size
        return size_x, size_y
        
    def block_choices_screen_get_clicked(self, mouse_pos:tuple):        
        relateive_mouse_pos = [mouse - ofsett for mouse, ofsett in zip(mouse_pos, settings.block_choices_screen_ofsett)]
        block = math.floor(relateive_mouse_pos[1] / settings.blocksize)
        print(f"{relateive_mouse_pos=} , {block=}")
        return settings.block_choices[block]

        
    def block_choices_get_if_clicked_on(self, mouse_pos:tuple) -> bool:
        relateive_mouse_pos = [mouse - ofsett for mouse, ofsett in zip(mouse_pos, settings.block_choices_screen_ofsett)]
        clicked = self.block_choices_screen.get_rect().collidepoint(relateive_mouse_pos)
        print(clicked)
        return clicked
    
    def update_camera_pos(self, player_pos:tuple):
        cam_pos_x, cam_pos_y = -player_pos[0]+self.screen.get_width()//2, -player_pos[1]+self.screen.get_height()//2

        if cam_pos_x > 0:
            cam_pos_x = 0
        elif cam_pos_x < -len(self.wold_engine.world)*settings.blocksize+self.screen.get_width():
            cam_pos_x = -len(self.wold_engine.world)*settings.blocksize+self.screen.get_width()
            
        if cam_pos_y > 0:
            cam_pos_y = 0
        elif cam_pos_y < -len(self.wold_engine.world[0])*settings.blocksize+self.screen.get_height():
            cam_pos_y = -len(self.wold_engine.world[0])*settings.blocksize+self.screen.get_height()
            
        self.camera_ofset = cam_pos_x, cam_pos_y
        
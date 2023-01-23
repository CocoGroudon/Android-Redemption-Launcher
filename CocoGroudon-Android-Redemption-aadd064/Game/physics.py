import pygame
import math
import time 

import assets
import settings
from world import WorldEngine

def get_angle_to_world_pos(origin:tuple, destination:tuple) -> float:
    '''
    returned value is in arc tangent
    '''
    delta_x = destination[0]-origin[0]
    delta_y = destination[1]-origin[1]
    angle = math.atan2(delta_y, delta_x)
    return angle

def get_world_pos_for_angle(starting_pos:tuple, angle:float, len:float):
    start_x, start_y = starting_pos
    
    end_x = start_x + len * math.cos(angle)
    end_y = start_y + len * math.sin(angle)
    
    return end_x, end_y


class Physics:
    def __init__(self, worldengine_ref:WorldEngine, game_ref) -> None:
        self.world_engine = worldengine_ref
        self.game = game_ref
        
        self.projectile_group = pygame.sprite.Group()
        self.entity_group = pygame.sprite.Group()
        self.enemie_group = pygame.sprite.Group()
        self.trigger_zones = list()
        self.items_group = pygame.sprite.Group()
        
        self.player = Player(self.world_engine, self, settings.player_starting_pos, (32,64), assets.misc["player_entity"])


        
    def clear(self):
        self.projectile_group.empty()
        self.entity_group.empty()
        self.enemie_group.empty()
        self.trigger_zones = list()
        self.items_group.empty()
        
    def tick(self):
        # Setup for Tick
        fps = self.game.window_manager.clock.get_fps()
        if fps == 0 or fps == 1: return
        tick_lenght = 1/fps

        self.handle_trigger_zones(tick_lenght)
        self.handle_player(tick_lenght)
        self.handle_entities(tick_lenght)
        self.handle_enemies(tick_lenght)
        self.handle_projectiles(tick_lenght)
        self.count_down_item_pickup_delay(tick_lenght)
        
        self.collect_item()

    def handle_trigger_zones(self, tick_lenght):
        for trigger_zone in self.trigger_zones:
            if trigger_zone.check_if_entity_in_triggerzone(self.player):
                trigger_zone.activate(tick_lenght=tick_lenght)

    def handle_entities(self, tick_lenght):
        for entity in self.entity_group:
            will_die = False
                                    
            if entity.health.check_if_dead():
                print("should die")
                will_die = True
                
            if will_die:
                self.entity_group.remove(entity)
                if issubclass(type(entity), Enemy):
                    self.enemie_group.remove(entity)
                continue
                
            entity.speed_x += entity.force_x * tick_lenght
            entity.speed_y += entity.force_y * tick_lenght
                    
            try:
                entity.action(tick_lenght)
            except:
                pass            
            entity.move((entity.speed_x*tick_lenght, 0))    
            entity.move((0, entity.speed_y*tick_lenght))
            
    def handle_player(self, tick_lenght):
        if self.player.key_shoot:
            angle = get_angle_to_world_pos(self.player.get_pos(), self.game.render_engine.get_world_pos_for_mouse_pos(pygame.mouse.get_pos()))
            self.player.shoot(angle)
            # self.player.key_shoot = False
                   
        self.player.speed_x += self.player.force_x * tick_lenght
        self.player.speed_y += self.player.force_y * tick_lenght
                
        if self.player.key_jump and self.player.check_if_ground():
            self.player.speed_y -= settings.player_jump_strength
            
        self.player.move(((self.player.speed_x+self.player.move_speed_x) *tick_lenght, (self.player.speed_y+self.player.move_speed_y)*tick_lenght))
        # self.player.move((0, self.player.speed_y*tick_lenght))
            
    def handle_enemies(self, tick_lenght):
        for enemie in self.enemie_group:
            enemie.action(tick_lenght)
            enemie.pathfind_to_player(self.player.get_pos(), tick_lenght)
            
    def handle_projectiles(self, tick_lenght:float):
        # self.projectile_group.remove(wall_collision)
        spritecollideany = pygame.sprite.spritecollideany
        collide_rect = pygame.sprite.collide_rect
        
        for projectile in self.projectile_group:
            projectile.move_forth(tick_lenght)
            will_die = False
            
            for entity in self.entity_group:
                if collide_rect(projectile, entity):
                    entity.health.take_damage(projectile.damage)
                    will_die = True
            
            if projectile.check_if_to_old(): 
                will_die = True
                
            if spritecollideany(projectile, self.world_engine.block_sprite_group):
                will_die = True
            
            if will_die: 
                self.projectile_group.remove(projectile)
        
    def create_item(self, item)-> bool :
        self.entity_group.add(item)
        self.items_group.add(item)

        
    def new_item(self):
        item = Item(self.world_engine, self, (100, 100), (16,16), assets.items["weed"])
        self.entity_group.add(item)
        self.items_group.add(item)

    def collect_item(self):
        for item in self.items_group:
            if not self.player.rect.colliderect(item.rect):
                continue
            if not item.pick_up_delay <= 0:
                continue
            if self.player.inventory.add_item(item): #
                self.items_group.remove(item)
                self.entity_group.remove(item)

    def discard_item(self):
        item_pos = [0, 0]
        while True:
            item = self.player.inventory.get_item(item_pos)
            if item != None: 
                break
            
            item_pos[1] += 1
            if item_pos[1] == settings.inventory_size[0]:
                item_pos[1] = 0
                item_pos[0] += 1
            if item_pos[0] == settings.inventory_size[1]:
                return
            
        player_pos = self.player.get_pos()
        item.set_pos(player_pos)
        
        print(item.get_pos(), vars(item))
        print(player_pos)
        item.reset_pick_up_delay()
        item.health.reset()
        
        self.create_item(item)
        self.player.inventory.remove_item(item_pos)
        
        self.player.inventory.update_surface()

        print("item weggeworfen")

    def count_down_item_pickup_delay(self, tick_lenght:float):
        '''counts down the Item_pick_up_delay for every Item'''
        for sprite in self.items_group:
            sprite.pick_up_delay = 0
            if sprite.pick_up_delay <= 0:
                continue
            if not sprite.rect.colliderect(self.player):
                sprite.reset_pick_up_delay()
                continue
            sprite.pick_up_delay -= tick_lenght
            print(f"item pickup delay: {sprite.pick_up_delay}")

    def add_enemie(self, enemie):
        self.entity_group.add(enemie)
        self.enemie_group.add(enemie)

class Entity(pygame.sprite.Sprite):
    
    speed_x = 0
    speed_y = 0
    gravity = settings.gravity
    force_x = 0
    force_y = settings.grav_strenght*gravity # boolean multiplication
    
    def __init__(self, wordlengine_ref:WorldEngine, physicsengine_ref:Physics, pos:tuple, size:tuple, image:pygame.image) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.world_engine = wordlengine_ref
        self.physics_engine = physicsengine_ref
        self.__pos = list(pos)
        self.size = size
        self.image = image    
        self.update_rect()
        self.health = Health_Bar(100)
             
        
    def update_rect(self):
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.__pos[0], self.__pos[1])
    
    def move(self, movement:tuple):
        to_move = list(movement)
        while to_move[0] / settings.movement_step_size > 1:
            if not self.move_step_x(settings.movement_step_size):
                break
            to_move[0] -= settings.movement_step_size
        else:
            self.move_step_x(to_move[0])
            
        while to_move[1] / settings.movement_step_size > 1:
            if not self.move_step_y(settings.movement_step_size):
                break
            to_move[1] -= settings.movement_step_size
        else:
            self.move_step_y(to_move[1])
            
    def move_step_x(self, movement:float):
        self.__pos[0] += movement
        self.update_rect()
        if pygame.sprite.spritecollideany(self, self.world_engine.block_sprite_group):
            self.__pos[0] -= movement
            self.speed_x = 0
            self.update_rect()
            return False
        return True
    def move_step_y(self, movement:float):
        self.__pos[1] += movement
        self.update_rect()
        if pygame.sprite.spritecollideany(self, self.world_engine.block_sprite_group):
            self.__pos[1] -= movement
            self.speed_y = 0
            self.update_rect()
            return False
        return True
    
    def get_angle_to_world_pos(self, origin:tuple, destination:tuple) -> float:
        '''
        returned value is in arc tangent
        '''
        delta_x = origin[0]-destination[0]
        delta_y = origin[1]-destination[1]
        angle = math.atan2(delta_y, delta_x)
        return angle
            
    def get_angle_to_world_pos(self, origin:tuple, destination:tuple) -> float:
        '''
        returned value is in arc tangent
        '''
        delta_x = origin[0]-destination[0]
        delta_y = origin[1]-destination[1]
        angle = math.atan2(delta_y, delta_x)
        return angle
            
    def get_pos(self) -> tuple:
        return self.__pos
    
    def set_pos(self, pos:tuple[int,int]):
        '''möglichst nicht verwenden, weil das mit der Kollision buggen kann'''
        self.__pos[0] -= self.__pos[0] # Ich weiß nicht, wieso ich nicht einfach __pos einen neuen Wert zuweisen kann, aber es geht nicht
        self.__pos[1] -= self.__pos[1]
        self.__pos[0] += pos[0]
        self.__pos[1] += pos[1]
        self.update_rect()
    
    def check_if_ground(self) -> bool:
        myrect = self.rect.copy().move(0, 1)
        for block in self.world_engine.block_sprite_group:
            if myrect.colliderect(block.rect):
                return True
        return False

            
class Enemy(Entity):
    movement_speed = 10

    def pathfind_to_player(self, player_pos:tuple, stepsize:int):
        '''pathfinds to the player'''
        angle = get_angle_to_world_pos(self.get_pos(), player_pos)
        new_pos = get_world_pos_for_angle((0,0), angle, self.movement_speed*stepsize)
        self.move(new_pos)
        
    def action(self, tick_lenght:int): #Damit alle anderne Enemys auch ihre eigenen Aktionen haben können
        pass

class Player(Entity):
    def __init__(self, wordlengine_ref: WorldEngine, physicsengine_ref:Physics ,pos: tuple, size: tuple, image: pygame.image) -> None:
        self.speed_x = 0
        self.speed_y = 0
        self.move_speed_x = 0
        self.move_speed_y = 0
        self.key_jump = False
        self.time_since_in_air = 0 
        self.inventory = Inventory()
        self.key_shoot = False
        self.last_shot = pygame.time.get_ticks()
        super().__init__(wordlengine_ref, physicsengine_ref, pos, size, image)

    def shoot(self, angle:float):
        '''creates a new standart projectile in the given direction \n
        angle *must* be given in radiants, else everythin gets scuffed'''
        item = self.inventory.get_hand_item()
        if item == None:
            return
        if not callable(item.action):
            return
        self.inventory.get_hand_item().action(angle)
        
    

class Item(Entity):
    def __init__(self, wordlengine_ref: WorldEngine, physicsengine_ref, pos: tuple, size: tuple, image: pygame.image, action:callable = None) -> None:
        super().__init__(wordlengine_ref, physicsengine_ref, pos, size, image)
        self.image = image
        self.pos = pos
        self.size = size
        self.image = image
        self.reset_pick_up_delay()
        if action: 
            self.action = action 
        else: 
            self.action = False
       
    def set_pos(self, pos: tuple[int, int]):
        self.pos = pos
        return super().set_pos(pos)
    
    def reset_pick_up_delay(self):
        self.pick_up_delay = settings.item_pick_up_delay
    
class Weapon(Item):
    pass
            
class Inventory:
    def __init__(self) -> None:
        self.__inventory_list:Item = [[None for j in range(settings.inventory_size[0])] for i in range(settings.inventory_size[1])]
        self.surface = pygame.Surface((settings.inventory_size[0]*settings.inventory_item_size, settings.inventory_size[1]*settings.inventory_item_size), flags=pygame.SRCALPHA)
        self.update_surface()
        self.hand = (0,0) # place in Inventory      
        
    def __get_first_empty_in_list(self, list:list) -> int:
        """ 
        returns the Index of the first position in a List, that is None \n
        If no Element of the List is None, the fuktion returns None
        """
        for index, cell in enumerate(list):
            if cell == None:
                return index
        return None
        
    def get_item(self, item_pos:tuple) -> Item or None:
        """ returns the item at the given position of the inventory or None if there is no item """
        item = self.__inventory_list[item_pos[0]][item_pos[1]]
        return item
    
    def add_item(self, item:Item) -> bool:
        """ 
        returned bool is: \n
        - True if the item was added succesfully \n
        - False if the item couldnt be added
        """
        lines_list = [None if self.__get_first_empty_in_list(line) != None else 1 for line in self.__inventory_list]
        first_empty_line = self.__get_first_empty_in_list(lines_list)
        if first_empty_line == None: 
            return False
        first_empty_col = self.__get_first_empty_in_list(self.__inventory_list[first_empty_line])
        
        print(f"added {item=} at position {first_empty_line} | {first_empty_col}")
        self.__inventory_list[first_empty_line][first_empty_col] = item
        self.update_surface()
        
        self.update_surface()
        return True
        
    def remove_item(self, position:tuple) -> None:
        self.__inventory_list[position[0]][position[1]] = None
        self.update_surface()
                
    def update_surface(self):
        """ refreshes the surface / image of the Inventory """
        self.surface.fill((0,0,0,0))
        # draw Border around the inventory
        pygame.draw.rect(self.surface, (255,255,255), (0,0,settings.inventory_size[0]*settings.inventory_item_size,settings.inventory_size[1]*settings.inventory_item_size), 2)
        for col_index, line in enumerate(self.__inventory_list): # col_index and line_index are switched on purpose because of the was Python handles nested lists
            for line_index, cell in enumerate(line):
                if cell != None:
                    image = pygame.transform.scale(cell.image, (settings.inventory_item_size, settings.inventory_item_size))
                    self.surface.blit(image, (line_index*settings.inventory_item_size, col_index*settings.inventory_item_size))

        size_x = settings.inventory_size[0]*settings.inventory_scale*settings.inventory_item_size
        size_y = settings.inventory_size[1]*settings.inventory_scale*settings.inventory_item_size
        self.big_surface = pygame.transform.smoothscale(self.surface, (size_x, size_y))
        self.big_surface.convert_alpha(self.big_surface)
        print("updated inventory surface")

    def get_item_list(self) -> list:
        return self.__inventory_list
    
    def get_hand_item(self) -> Item:
        return self.__inventory_list[self.hand[0]][self.hand[1]]

class Projectile(pygame.sprite.Sprite):
    '''A basic projectile that has no gravity and isn`t hitscan'''
    def __init__(self, owner:Entity, image:pygame.image, angle:float, start_pos:tuple, speed:float, damage:float, lifetime:int = settings.projectile_lifetime ) -> None:
        pygame.sprite.Sprite.__init__(self=self)
        self.image_normal = image
        self.pos_x, self.pos_y = start_pos
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.lifetime = lifetime
        self.time_of_spawn = time.time()
                
        self.image = pygame.transform.rotate(self.image_normal, (math.degrees(self.angle)+180)*-1)
        self.rect = self.image.get_rect()
        
    def move_forth(self, tick_lenght:float):
        '''Advances the projectile Position the distance'''
        dist = self.speed*tick_lenght
        self.pos_x += dist*math.cos(self.angle)
        self.pos_y += dist*math.sin(self.angle)

        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.pos_x, self.pos_y)
        
    def check_if_to_old(self) -> bool:
        ''' Returns weather the Sprite is older then the specified "projectile_lifetime" in settings '''
        existence_time = time.time() - self.time_of_spawn
        if existence_time*1000 > self.lifetime:
            return True
        return False

class Projectile_Gravity(Projectile):  
    def __init__(self, owner: Entity, image:pygame.image, angle: float, start_pos: tuple, speed: float, damage:float, lifetime:int = settings.projectile_lifetime) -> None:
        super().__init__(owner=owner, image=image, angle=angle, start_pos=start_pos, speed=speed, damage=damage, lifetime=lifetime)
        self.down_speed = 0
    
    def move_forth(self, tick_lenght:float):
        self.down_speed += settings.grav_strenght*tick_lenght
        self.pos_y += self.down_speed*tick_lenght
        return super().move_forth(tick_lenght)
   
class Health_Bar:
    def __init__(self, max_Health:int, current_health:int = 0) -> None:
        self.max = max_Health
        self.image = assets.misc["heart"]
        if current_health == 0:
            self.current = max_Health
        else:
            self.current = current_health
        
    def reset(self):
        self.current = self.max    
    
    def take_damage(self, damage):
        self.current -= damage
    
    def heal(self, healing):
        self.current += healing
        if self.current > self.max:
            self.current = self.max
            
    def check_if_dead(self) -> bool:
        if self.current <= 0:
            return True
        return False

    def get_screen(self) -> pygame.surface.Surface:
        image_value_life_poins = 10
        images = self.max/image_value_life_poins
        screen = pygame.Surface((self.image.get_width()*images, self.image.get_height()), flags=pygame.SRCALPHA)
        for x in range(round(self.current)//image_value_life_poins):
            screen.blit(self.image, (x*self.image.get_width(), 0))
        return screen
    
class Triggerzone(pygame.Rect):
    def __init__(self, wordlengine_ref:WorldEngine, physicsengine_ref:Physics, pos:tuple, size:tuple, action:callable) -> None:
        super().__init__(pos, size)
        self.worldengine = wordlengine_ref
        self.physicsengine = physicsengine_ref
        self.action = action
        self.surface = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
        self.surface.fill(settings.trigger_zone_color)
        pygame.draw.rect(self.surface, (255,255,255), (0,0,self.width,self.height), 1)
        
    def check_if_entity_in_triggerzone(self, entity:Entity) -> bool:
        if self.colliderect(entity.rect):
            return True
        return False
        
    def check_if_pos_in_triggerzone(self, pos:tuple) -> bool:
        if self.collidepoint(pos):
            return True
        return False
    
    def activate(self, tick_lenght:float):
        self.action(wordlengine_ref=self.worldengine, physicsengine_ref=self.physicsengine, tick_lenght=tick_lenght)
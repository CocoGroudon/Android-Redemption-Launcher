import pygame
import copy
import random
import assets
import settings

from physics import Item, WorldEngine, Projectile, Projectile_Gravity, Weapon

class Shotgun(Weapon):

    projectile_amount = 20 #amount of projectiles per second
    projectile_inaccuracy = 0.3 #in radiants
    projectile_speed = 800
    projectile_decay_time = 500
    projectiel_image = assets.projectiles["bullet"]
    image = assets.items["Flamethrower"]
    shoot_cooldown = 100 #time in ms
    damage = 2


    def __init__(self, wordlengine_ref: WorldEngine, physicsengine_ref, pos: tuple) -> None:
        size = settings.item_size
        super().__init__(wordlengine_ref, physicsengine_ref, pos, size, self.image, self.my_action)
        self.last_shot = pygame.time.get_ticks()
    
    def my_action(self, angle:float = 0):
        time_since_shoot = pygame.time.get_ticks() - self.last_shot 
        # print(time_since_shoot)
        if time_since_shoot < self.shoot_cooldown:
            return
        
        for _ in range(self.projectile_amount):
            new_angle = angle + (random.random() - 0.5) * self.projectile_inaccuracy
            origin_pos = [self.physics_engine.player.get_pos()[i] - settings.hand_ofsett[i] for i in range(2)]
            projectile = Projectile_Gravity(self.physics_engine.player, self.projectiel_image, new_angle, origin_pos, self.projectile_speed, self.damage, self.projectile_decay_time)
            self.physics_engine.projectile_group.add(projectile)
            self.last_shot = pygame.time.get_ticks()

        self.physics_engine.player.key_shoot = False
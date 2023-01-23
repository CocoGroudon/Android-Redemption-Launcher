import math
import random
from physics import Enemy
import assets
import settings

from .Ball import Ball

class Mothership(Enemy):
    image = assets.enemies['mothership']
    movement_speed = 0
    size = image.get_size()
    force_y = 0 # no gravity
    max_helth = 1000
    spawn_chance = 1000 # the higher the number the lower the chance
    
    def __init__(self, wordlengine_ref, physicsengine_ref, pos_x:int ,pos_y:int, ofsett:int=0) -> None:
        pos = (pos_x+ofsett*settings.blocksize, pos_y)

        super().__init__(wordlengine_ref, physicsengine_ref, pos, self.size, self.image)
        
        self.health.max = self.max_helth
        self.health.reset()
        
    def spawn_enemy(self):
        pos = self.get_pos()
        ball = Ball(self.world_engine, self.physics_engine, pos[0] + self.size[0] / 2, pos[1] + self.size[1] / 2)
        self.physics_engine.add_enemie(ball)
    
    def action(self, tick_lenght: float):
        for _ in range(math.floor(1/tick_lenght/10)):
            rand = random.randint(0, self.spawn_chance)
            if rand == 0:
                self.spawn_enemy()
        
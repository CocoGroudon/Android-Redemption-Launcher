from physics import Enemy
import assets
import settings

class Ball(Enemy):
    image = assets.enemies['ball']
    movement_speed = 100
    size = image.get_size()
    force_y = 0 # no gravity
    
    def __init__(self, wordlengine_ref, physicsengine_ref, pos_x:int ,pos_y:int, ofsett:int = 0) -> None:
        pos = pos_x+ofsett*settings.blocksize, pos_y

        super().__init__(wordlengine_ref, physicsengine_ref, pos, self.size, self.image)
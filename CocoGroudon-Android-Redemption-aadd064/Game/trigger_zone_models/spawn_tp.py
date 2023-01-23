import world
import physics
import settings
class Spawn_Tp(physics.Triggerzone):
    def __init__(self, wordlengine_ref: world.WorldEngine, physicsengine_ref: physics.Physics, pos_x: int, pos_y: int, size_x:int, size_y:int, ofsett:int) -> None:
        pos = (pos_x +settings.blocksize*ofsett, pos_y)
        super().__init__(wordlengine_ref, physicsengine_ref, pos, (size_x, size_y), self.action)
        
    def action(self, **kwargs):
        self.physicsengine.player.set_pos(settings.player_starting_pos)
        
        
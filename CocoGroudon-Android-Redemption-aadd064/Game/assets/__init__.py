import pygame
import sys
import os





def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
        filename = os.path.basename(filename)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


def load_image(path:str) -> pygame.image:
    new_path = find_data_file(path)
    image = pygame.image.load(new_path)
    return image
    
    
misc = {
    "test_entity": load_image('test_entity.png').convert_alpha(),
    "player_entity": load_image('playerasset.png').convert_alpha(),
    "test_projectile": load_image('test_projectile.png').convert_alpha(),
    "heart": load_image('heart.png').convert_alpha()
    }
    
blocks = {
    0 : load_image('blocks/luft.png').convert_alpha(),
    1 : load_image('blocks/stein.png').convert_alpha(),
    2 : load_image('blocks/grass.png').convert_alpha(),
    3 : load_image('blocks/darkDirtBlock.png').convert_alpha(),
    4 : load_image('blocks/eis.png').convert_alpha(),
    5 : load_image('blocks/Kohle.png').convert_alpha(),
    6 : load_image('blocks/lava.png').convert_alpha(),
    7 : load_image('blocks/Obsidian.png').convert_alpha(),
    127 : load_image('blocks/testtexture.png').convert_alpha()
}

paralax_background = {
    0 : pygame.transform.scale2x(load_image('background/sky.png')).convert_alpha(),
    1 : pygame.transform.scale2x(load_image('background/far-clouds.png')).convert_alpha(),
    2 : pygame.transform.scale2x(load_image('background/near-clouds.png')).convert_alpha(),
    3 : pygame.transform.scale2x(load_image('background/far-mountains.png')).convert_alpha(),
    4 : pygame.transform.scale2x(load_image('background/mountains.png')).convert_alpha(),
    5 : pygame.transform.scale2x(load_image('background/trees.png')).convert_alpha()
}

items = {
    "weed": load_image("weed.png").convert_alpha(),
    'Flamethrower': pygame.transform.scale(load_image('items/item_flamethrower.png').convert_alpha(), (100, 35)) , 
    'AR': load_image('items/AR.png').convert_alpha(),
    1 : load_image('item_dirt.png').convert_alpha()
}

projectiles = {
    "bullet": load_image('projectiles/bullet.png').convert_alpha(),
    "flame": load_image('projectiles/firesll_32x17.png').convert_alpha()
}

enemies = {
    "ball": load_image('enemies/ball.png').convert_alpha(),
    "mothership": load_image('enemies/shit2.png').convert_alpha()
}
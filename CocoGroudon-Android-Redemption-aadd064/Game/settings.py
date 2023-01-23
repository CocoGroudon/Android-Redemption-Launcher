import os 
import pygame

framerate = 0
backgroundcolor = (44, 37, 68)
blocksize = 32
world_edit_mode = False
debug_mode = False

# World
world_name = "test"
# world_dimensions = (500, 100)
world_room_options = ("base", "pit")
world_room_amount = 5

# Physics
projectile_speed = 1000
projectile_lifetime = 10
movement_step_size = blocksize/2
projectile_step_size = blocksize/2

player_jump_strength = blocksize*10
gravity = True
grav_strenght = blocksize*12

hand_ofsett = (-12, -20)

# Player
inventory_size = (5,9)
inventory_item_size = 8 # Pixel
player_starting_pos = (blocksize*8, blocksize*21)

item_size = (16, 16)
item_pick_up_delay = 3000000000

# Renderer
block_choices_screen_ofsett = (0,200)
block_choices = (0,1,2,3,4,5,6,7,127)
inventory_scale = 4
draw_trigger_zones = False #Debug
trigger_zone_color = pygame.Color(255, 0, 0, 128)

# Pause Menu
pause_font_size = 50
pause_font_kind = "Arial"
pause_font = pygame.font.SysFont(pause_font_kind, pause_font_size)

keybinds = {
    "up": [pygame.K_SPACE, pygame.K_UP, pygame.K_w ],
    "left": [pygame.K_a, pygame.K_LEFT ],
    "down": [pygame.K_s, pygame.K_DOWN ],
    "right": [pygame.K_d, pygame.K_RIGHT ],
    "toggle_fullscreen": pygame.K_F11,
    "inventory": [pygame.K_e],
    "action": [pygame.K_q],
    "pause": [pygame.K_ESCAPE]
}

dictPath = os.path.dirname(os.path.abspath(__file__))
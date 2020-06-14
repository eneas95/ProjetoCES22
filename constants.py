"""
Projeto: Ces-22
Constants.
"""

# Constants used to scale the window:
SCREEN_WIDTH  = 2000
SCREEN_HEIGHT = 1500
SCREEN_TITLE  = "FLIER FLUBBER"

# Constants used to scale our sprites from their original size:
CHARACTER_SCALING = 1
TILE_SCALING      = 1
COIN_SCALING      = 0.5
TILE_SIZE         = 64
COIN_SCALING      = 1

#Constant to determine the height of the hole in the obstacles:
HOLE_Y            = SCREEN_HEIGHT - 4*TILE_SIZE

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED   = 5
GRAVITY                 = 2
PLAYER_JUMP_SPEED       = 35

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen:
RIGHT_VIEWPORT_MARGIN  = 1500

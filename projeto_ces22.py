"""
Projeto: Ces-22
"""
import arcade

# Constants used to scale the window.
SCREEN_WIDTH  = 1600
SCREEN_HEIGHT = 1200
SCREEN_TITLE  = "Platformer"


# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.5
TILE_SCALING      = 0.5
COIN_SCALING      = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED   = 10
SCENARIO_MOVEMENT_SPEED = 10
GRAVITY                 = 1
PLAYER_JUMP_SPEED       = 15

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
RIGHT_VIEWPORT_MARGIN  = 1536
RIGHT_END              = 3200


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class (arcade.window) and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen = True)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.coin_list   = None
        self.wall_list   = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite  = None
        self.player2_sprite = None

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left   = 0

        arcade.set_background_color(arcade.csscolor.CYAN)


    def setup(self):
        """
        The method 'setup' outside __init__ makes it easier to restart the game.
        Call this function to restart the game.
        """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left   = 0

        # Create the Sprite lists.
        #OBS:'use_spatial_hash=True' speeds the time it takes to find
        # collisions, but increases the time it takes to move a sprite. Do not
        # use in objects that move.
        self.player_list = arcade.SpriteList()
        self.wall_list   = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list   = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite          = arcade.Sprite("images/player_1/player_stand.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 1000
        self.player_sprite.change_x = SCENARIO_MOVEMENT_SPEED
        self.player_list.append(self.player_sprite)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 10000, 64):
            wall          = arcade.Sprite("images/tiles/grassMid.png", TILE_SCALING)
            ceil          = arcade.Sprite("images/tiles/grassMid.png", TILE_SCALING)
            ceil.center_x = x
            ceil.center_y = 1168 
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)
            self.wall_list.append(ceil)


        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 96],
                           [256, 96],
                           [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite("images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen to the background color. It is required to be called
        # before drawing anything to the screen.
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
            self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y  = PLAYER_JUMP_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x += PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = SCENARIO_MOVEMENT_SPEED

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites
        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left   = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run() #Run the main loop.

if __name__ == "__main__":
    main()

"""
Projeto: Ces-22
"""
import arcade, random

# Constants used to scale the window.
SCREEN_WIDTH  = 2000
SCREEN_HEIGHT = 1500
SCREEN_TITLE  = "Platformer"


# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING      = 1
COIN_SCALING      = 0.5
TILE_SIZE         = 64
HOLE_Y            = SCREEN_HEIGHT - 4*TILE_SIZE
# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED   = 10
GRAVITY                 = 2
PLAYER_JUMP_SPEED       = 30

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
RIGHT_VIEWPORT_MARGIN  = 1500


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class (arcade.window) and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen = True)

        #General attributes

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.coin_list   = None
        self.wall_list   = None
        self.player_list = None

        # Separate variable that holds the player sprite list
        self.player_sprite  = []

        # Our physics engine
        self.physics_engine = []

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left   = 0

        arcade.set_background_color(arcade.csscolor.CYAN)

    def setup(self):
        """
        The method 'setup' outside __init__ makes it easier to restart the game.
        Call this function to restart the game.
        """
        #Create and initiate the attributes:
        self.obstacle_distance       = 400
        self.last_position           = 0
        self.level                   = 0
        self.score                   = 0

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left   = 0

        # Create the Sprite lists.
        #OBS:'use_spatial_hash=True' speeds the time it takes to find
        # collisions, but increases the time it takes to move a sprite. Do not
        # use in objects that move.
        self.player_list = arcade.SpriteList() #Create the first player sprite
        self.wall_list   = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list   = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite.append(arcade.Sprite("images/player_1/slimeBlue.png", CHARACTER_SCALING))
        self.player_sprite[0].center_x = 64
        self.player_sprite[0].last_x      = 64
        self.player_sprite[0].center_y = SCREEN_HEIGHT
        self.player_sprite[0].change_x = 5
        self.player_list.append(self.player_sprite[0])

        #Initialize the last position:
        self.last_position          = self.player_sprite[0].right
        # Create the 'physics engine'
        self.physics_engine.append(arcade.PhysicsEnginePlatformer(self.player_sprite[0],
                                                             self.wall_list,
                                                             GRAVITY))

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen to the background color. It is required to be called
        # before drawing anything to the screen.
        arcade.start_render()

        if (self.player_sprite[0].right - self.last_position >= self.obstacle_distance):
            self.last_position = self.player_sprite[0].right
            self.create_obstacle()


        # Draw our sprites
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """



        if key == arcade.key.UP or key == arcade.key.W:
            for player in self.player_sprite:
                player.change_y  = PLAYER_JUMP_SPEED
        elif key == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
            self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        elif key == arcade.key.U: ## debugging
            self.level_up()


    def update(self, delta_time):
        """ Movement and game logic """

        #Update engines:
        for engine in self.physics_engine:
            engine.update()

        self.check_for_horizontal_collision()

        #Game Over!
        if (len(self.player_list)==0):
            self.game_over()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False
        #Ceil limit.
        for player in self.player_sprite:
            if player.top > SCREEN_HEIGHT:
                player.top = SCREEN_HEIGHT

        #Floor limit.
        for player in self.player_sprite:
            if player.bottom < 0:
                player.bottom = 0


        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite[-1].right > right_boundary:
            self.view_left += self.player_sprite[-1].right - right_boundary
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


    def create_obstacle(self):
        ''' Create the next obstacle with a hole.'''
        hole_y = random.random()*(HOLE_Y)
        if(random.randint(0, 1)):
            wall_top       = arcade.Sprite("images/obstaculo/obstaculo.png", TILE_SCALING)
            wall_top.position = (self.last_position + 5*self.obstacle_distance, hole_y + SCREEN_HEIGHT/2 + 4*TILE_SIZE)
            if (len(self.wall_list) >= 6):
                self.wall_list.pop(0)
            self.wall_list.append(wall_top)
        else:
            wall_bottom    = arcade.Sprite("images/obstaculo/obstaculo.png", TILE_SCALING)
            wall_bottom.position = (self.last_position + 5*self.obstacle_distance, hole_y - SCREEN_HEIGHT/2)
            if (len(self.wall_list) >= 6):
                self.wall_list.pop(0)
            self.wall_list.append(wall_bottom)

    def level_up(self):
        self.level                   += 1
        initial_speed = self.player_sprite[0].change_x
        self.obstacle_distance       *= 1.05
        self.life                     = 100
        self.player_sprite.append(arcade.Sprite("images/player_1/slimeBlue.png", CHARACTER_SCALING))
        self.player_sprite[-1].center_x = self.player_sprite[0].right + random.randint(-1, 1)
        self.player_sprite[-1].last_x = self.player_sprite[-1].center_x
        self.player_sprite[-1].center_y = self.player_sprite[0].bottom + random.randint(-1, 1)
        self.player_list.append(self.player_sprite[-1])
        for player in self.player_sprite:
            player.change_x  = initial_speed*1.1
        self.physics_engine.append(arcade.PhysicsEnginePlatformer(self.player_sprite[-1],
                                                                self.wall_list,
                                                                GRAVITY))

    def check_for_horizontal_collision(self):
        ''' Check for horizontal collisions '''
        player_destroy_list = []
        engine_destroy_list = []
        for i in range(len(self.player_sprite)):
            if (self.player_sprite[i].center_x - self.player_sprite[i].last_x <= 0.0001):
                player_destroy_list.append(self.player_sprite[i])
                engine_destroy_list.append(self.physics_engine[i])

        for player in player_destroy_list:
            self.player_sprite.remove(player)
            self.player_list.remove(player)

        for engine in engine_destroy_list:
            self.physics_engine.remove(engine)

        for player in self.player_sprite:
            player.last_x = player.center_x

    def game_over(self):
        self.setup()

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run() #Run the main loop.

if __name__ == "__main__":
    main()

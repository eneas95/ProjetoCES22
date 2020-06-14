"""
Projeto: Ces-22
Views
"""
import arcade, random, time
from constants import *

class InitialView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.GREEN)


    def on_draw(self):
        arcade.start_render()
        self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        arcade.draw_text("Tela inicial", SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Pressione ENTER para iniciar",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2-30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

        arcade.draw_text("Pressione Q para sair",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2-60,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ENTER:  # reset game
            new_game = MyGame()
            self.window.show_view(new_game)
            new_game.setup()
        elif key == arcade.key.F:
            self.window.set_fullscreen(not self.window.fullscreen)
            self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        elif key == arcade.key.Q:
            self.window.close()


class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class (arcade.View) and set up the window
        super().__init__()

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

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.CYAN)

    def setup(self):
        """
        The method 'setup' outside __init__ makes it easier to restart the game.
        Call this function to restart the game.
        """
        #Adjust the initial viewport:
        self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        #Create and initiate the attributes:
        self.obstacle_distance       = 600
        self.last_position           = 0
        self.level                   = 0
        self.score                   = 0 #100 pts to level up.
        self.total_score             = 0
        self.speed                   = 0 #Speed that is measured
        self.distance                = 0
        self.total_distance          = 0
        self.initial_time            = time.time()
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left   = 0

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

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
        self.player_sprite[0].last_x   = 64
        self.player_sprite[0].center_y = SCREEN_HEIGHT
        self.player_sprite[0].change_x = PLAYER_MOVEMENT_SPEED
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


        # Draw our score on the screen, scrolling it with the viewport:
        if (self.speed != self.player_sprite[0].change_x):
            self.distance    += self.speed*(time.time() - self.initial_time)
            self.speed        = self.player_sprite[0].change_x
            self.initial_time = time.time()
        delta_t = time.time() - self.initial_time
        if (delta_t*self.speed + self.distance - self.total_distance >= 100):
            self.total_distance += 100
            self.increase_score(10)
        score_text       = "Pontuação total: {0:<5} (Parcial: {1:<5})".format(self.total_score, self.score)
        speed_text       = "Velocidade: {:<5.2f} m/s".format(self.speed)
        total_distance   = "Distância total: {:<5.0f} m".format(self.total_distance)
        arcade.draw_text(score_text, 10 + self.view_left, SCREEN_HEIGHT - 40,
                         arcade.csscolor.BLACK, 30)
        arcade.draw_text(speed_text, 10 + self.view_left, SCREEN_HEIGHT - 70,
                         arcade.csscolor.BLACK, 30)
        arcade.draw_text(total_distance, 10 + self.view_left, SCREEN_HEIGHT - 100,
                         arcade.csscolor.BLACK, 30)

        # Draw our sprites
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            for player in self.player_sprite:
                player.change_y  = PLAYER_JUMP_SPEED + 20*random.random() - 5
        elif key == arcade.key.F:
            self.window.set_fullscreen(not self.window.fullscreen)
            self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        elif key == arcade.key.P:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)
        elif key == arcade.key.U: ## debugging
            self.increase_score(10)


    def update(self, delta_time):
        """ Movement and game logic """

        #Update engines:
        for engine in self.physics_engine:
            engine.update()

        self.check_for_horizontal_collision()

        #Game Over!
        if (len(self.player_list)==0):
            self.game_over()
            return None #It is necessary to return None, otherwise it will execute
                        #the remaining of update() function and an error will raise.

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
            wall_top.position = (self.last_position + 5*self.obstacle_distance, hole_y + SCREEN_HEIGHT/2 + 3*TILE_SIZE)
            if (len(self.wall_list) >= 6):
                self.wall_list.pop(0)
            self.wall_list.append(wall_top)
        else:
            wall_bottom    = arcade.Sprite("images/obstaculo/obstaculo.png", TILE_SCALING)
            wall_bottom.position = (self.last_position + 5*self.obstacle_distance, hole_y - SCREEN_HEIGHT/2 + 3*TILE_SIZE)
            if (len(self.wall_list) >= 6):
                self.wall_list.pop(0)
            self.wall_list.append(wall_bottom)

    def level_up(self):
        self.level                   += 1
        initial_speed = self.player_sprite[0].change_x
        self.obstacle_distance       *= 1.3
        self.player_sprite.append(arcade.Sprite("images/player_1/slimeBlue.png", CHARACTER_SCALING))
        self.player_sprite[-1].center_x = self.player_sprite[0].right + (5*random.random() -2.5)
        self.player_sprite[-1].last_x = self.player_sprite[-1].center_x
        self.player_sprite[-1].center_y = self.player_sprite[0].bottom + (5*random.random() -2.5)
        self.player_list.append(self.player_sprite[-1])
        for player in self.player_sprite:
            player.change_x  = initial_speed*1.2
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
        game_over = GameOver(self.total_score)
        self.window.show_view(game_over)

    def increase_score(self, amount):
        self.score       += amount
        self.total_score += amount
        if (self.score >= 100): #
            self.level_up()
            self.score = 0


class GameOver(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.score = score
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)


    def on_draw(self):
        arcade.start_render()
        self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        arcade.draw_text("GAME OVER", SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50,
                         arcade.color.RED, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Pressione ENTER para retornar à tela inicial",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2-30,
                         arcade.color.RED,
                         font_size=20,
                         anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Sua pontuação é : {:<5}".format(self.score),
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2-60,
                         arcade.color.RED,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ENTER:  # reset game
            start_view = InitialView()
            self.window.show_view(start_view)
        elif key == arcade.key.F:
            self.window.set_fullscreen(not self.window.fullscreen)
            self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)




class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE)

    def on_draw(self):
        arcade.start_render()
        self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        arcade.draw_text("Jogo pausado", SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        arcade.draw_text("Pressione P para retornar",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Pressione I para retornar à tela inicial",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2-30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.P:   # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.I:  # reset game
            start_view = InitialView()
            self.window.show_view(start_view)

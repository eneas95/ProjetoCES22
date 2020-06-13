"""
Projeto: Ces-22
"""
import arcade
from constants import *
from views     import *


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen = True)
    start_view = InitialView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()

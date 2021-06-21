from settings import *
from src.object_controller import ObjectController
from src.button import Button
from src.game_objects import Player, Enemy, Missile, BoomEffect
import random
import datetime

class GameStarter:
    def __init__(self, level, background):
        self.__level = level
        self.__background = background

    def __init_game_objects(self):
        if self.__level == 1 :
            self.__respone_cycle = datetime.timedelta(0, 3)
            self.__enemy_name = 'enemy1'
            self.__victory_condition = 10

        elif self.__level == 2 :
            self.__enemy_numbers = 20
            self.__init_enemy_num = 5

        for _ in range(self.__init_enemy_num) :
            Enemy((random.randint(1, SCREEN_WIDTH-1), 1))

    def __call__(self):
        ObjectController.reset()
        player = Player(START_POINT)
        button = Button()
        self.__init_game_objects()

        while True :
            kill = player.kill_point

            if button.left : 
                player.move('L')
            elif button.right :
                player.move('R')
            elif button.up : 
                player.move('U')
            elif button.down :
                player.move('D')
        
            if button.a :
                player.shoot()

            DISPLAY.image(self.__background())

            if player.hp == 0 :
                print('Game Over!')
                break

            if player.kill_point == self.__all_enemy_numbers :
                print('You win')
                break

            if player.kill_point - kill > 0 :
                for _ in range(player.kill_point-kill):
                    Enemy((random.randint(1, SCREEN_WIDTH-1), 1))




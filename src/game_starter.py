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
            self.__respawn_cycle = datetime.timedelta(0, 3)
            self.__enemy_name = 'enemy1'
            self.__victory_condition = 10
            self.__enemy_limit = 3

        elif self.__level == 2 :
            self.__respawn_cycle = datetime.timedelta(0, 3)
            self.__enemy_name = 'enemy2'
            self.__victory_condition = 15
            self.__enemy_limit = 5

        elif self.__level == 3 :
            self.__respawn_cycle = datetime.timedelta(0, 3)
            self.__enemy_name = 'enemy3'
            self.__victory_condition = 20
            self.__enemy_limit = 7

        elif self.__level == 4 :
            self.__respawn_cycle = datetime.timedelta(0, 3)
            self.__enemy_name = 'enemy4'
            self.__victory_condition = 25
            self.__enemy_limit = 7

        elif self.__level == 5 :
            self.__respawn_cycle = datetime.timedelta(0, 3)
            self.__enemy_name = 'enemy5'
            self.__victory_condition = 30
            self.__enemy_limit = 7

    def __call__(self):
        ObjectController.reset()
        player = Player(START_POINT)
        button = Button()
        self.__init_game_objects()

        prev_time = datetime.datetime.now()
        while True :
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

            if player.hp <= 0 :
                print('Game Over!')
                break
            if player.kill_point >= self.__victory_condition :
                print("You Win")
                break
            if datetime.datetime.now() - prev_time >= self.__respawn_cycle :
                if len(list(ObjectController.getEnemyObjects()[0])) >= self.__enemy_limit :
                    pass
                else :
                    Enemy((random.randint(0, SCREEN_WIDTH), 0), self.__enemy_name)
                    prev_time = datetime.datetime.now()

            
    


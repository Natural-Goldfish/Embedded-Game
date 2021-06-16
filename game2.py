from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
import time
import random
import os
import sys
import datetime
from settings import *


class Button:
    def __init__(self):
        self._left = BUTTON_L
        self._right = BUTTON_R
        self._up = BUTTON_U
        self._down = BUTTON_D
        self._a = BUTTON_A
        self._b = BUTTON_B
        self._C = BUTTON_C

    @property
    def left(self):
        return False if self._left.value else True
    @property
    def right(self):
        return False if self._right.value else True
    @property
    def up(self):
        return False if self._up.value else True
    @property
    def down(self):
        return False if self._down.value else True
    @property
    def a(self):
        return False if self._a.value else True
    @property
    def b(self):
        return False if self._b.value else True
    @property
    def c(self):
        return False if self._c.value else True

class ObjectController:
    _player_id = set()
    _player_object = dict()
    _player_missile_ids = set()
    _player_missile_objects = dict()

    _enemy_ids = set()
    _enemy_objects = dict()
    _enemy_missile_ids = set()
    _enemy_missile_objects = dict()

    @classmethod
    def getPlayerObjects(cls):
        return cls._player_object, cls._player_missile_objects
    @classmethod
    def getEnemyObjects(cls):
        return cls._enemy_objects, cls._enemy_missile_objects

    # when an object is created, the object must be enrolled.
    @classmethod
    def enroll(cls, my_object):
        object_id = cls.issueID(my_object)
        if my_object.team == 'enemy':
            if my_object.role == 'missile':
                cls._enemy_missile_objects[object_id] = my_object
            elif my_object.role == 'fighter-plane' :
                cls._enemy_objects[object_id] = my_object

        elif my_object.team == 'player':
            if my_object.role == 'missile':
                cls._player_missile_objects[object_id] = my_object
            elif my_object.role == 'fighter-plane' :
                cls._player_object[object_id] = my_object
        return object_id

    @classmethod
    def issueID(cls, my_object):
        while True :
            new_id = random.randrange(sys.maxsize)
            if my_object.team == 'enemy' :
                if my_object.role == 'missile' :
                    if new_id in cls._enemy_missile_ids : continue
                    else : 
                        cls._enemy_missile_ids.add(new_id)
                        return new_id
                elif my_object.role == 'fighter-plane' :
                    if new_id in cls._enemy_ids : continue
                    else : 
                        cls._enemy_ids.add(new_id)
                        return new_id

            elif my_object.team == 'player' :
                if my_object.role == 'missile' :
                    if new_id in cls._player_missile_ids : continue
                    else : 
                        cls._player_missile_ids.add(new_id)
                        return new_id
                elif my_object.role == 'fighter-plane' :
                    if new_id in cls._player_id : continue
                    else : 
                        cls._player_id.add(new_id)
                        return new_id

    # when objects moved, the objects must be renewed.
    @classmethod
    def renew(cls):
        # Enemy attacks
        for enemy_id in cls._enemy_ids:
            enemy_object = cls._enemy_objects[enemy_id]
            if datetime.datetime.now()- enemy_object.prev_attack_time >= enemy_object.attack_cycle:
                enemy_object.attack()

        # All objects move
        for enemy_id in cls._enemy_ids:
            enemy_object = cls._enemy_objects[enemy_id]
            enemy_object.move()
        while True :
            flag = True

            for player_missile_id in cls._player_missile_ids:
                player_missile_object = cls._player_missile_objects[player_missile_id]
                player_missile_object.move()

                # Missiles which are out of screen are eliminated : flag == False
                x, y = player_missile_object.obj_coord
                if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT :
                    flag = False
                    break
            if flag == False :
                cls._player_missile_ids.remove(player_missile_id)
                del cls._player_missile_objects[player_missile_id]
            else : break
        while True :
            flag = True
            for enemy_missile_id in cls._enemy_missile_ids:
                enemy_missile_object = cls._enemy_missile_objects[enemy_missile_id]
                enemy_missile_object.move()

                # Missiles which are out of screen are eliminated : flag == False
                x, y = enemy_missile_object.obj_coord
                if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT :
                    flag = False
                    break    
    
            if flag == False :
                cls._enemy_missile_ids.remove(enemy_missile_id)
                del cls._enemy_missile_objects[enemy_missile_id]
            else : break

        # Renew code
        while True :
            # When the player's airplane is attacked by enemy's missiles
            flag = True
            for player_id in cls._player_id :
                player_object = cls._player_object[player_id]
                player_coord = player_object.image_coord
                for enemy_missile_id in cls._enemy_missile_ids:
                    enemy_missile_object = cls._enemy_missile_objects[enemy_missile_id]
                    enemy_missile_coord = enemy_missile_object.image_coord
                    iou = max(0, min(player_coord[2], enemy_missile_coord[2])- max(player_coord[0], enemy_missile_coord[0]))*max(0, min(player_coord[3], enemy_missile_coord[3])-max(player_coord[1], enemy_missile_coord[1]))

                    # When player is attacked, the flag become false
                    if iou > 0 : 
                        flag = False
                        break
                if flag == False :
                    cls._player_id.remove(player_id)
                    cls._enemy_missile_ids.remove(enemy_missile_id)
                    del cls._player_object[player_id]
                    del cls._enemy_missile_objects[enemy_missile_id]
                    break
            if flag : break

        while True :
            # When player's missiles crashed by enemy's missiles
            flag = True
            for player_missile_id in cls._player_missile_ids :
                player_missile_object = cls._player_missile_objects[player_missile_id]
                player_missile_coord = player_missile_object.image_coord
                for enemy_missile_id in cls._enemy_missile_ids:
                    enemy_missile_object = cls._enemy_missile_objects[enemy_missile_id]
                    enemy_missile_coord = enemy_missile_object.image_coord
                    iou = max(0, min(player_missile_coord[2], enemy_missile_coord[2])- max(player_missile_coord[0], enemy_missile_coord[0]))*max(0, min(player_missile_coord[3], enemy_missile_coord[3])-max(player_missile_coord[1], enemy_missile_coord[1]))

                    # When missiles is crashed, the flag become false
                    if iou > 0 : 
                        flag = False
                        break
                if flag == False :
                    cls._player_missile_ids.remove(player_missile_id)
                    cls._enemy_missile_ids.remove(enemy_missile_id)
                    del cls._player_missile_objects[player_missile_id]
                    del cls._enemy_missile_objects[enemy_missile_id]
                    break
            if flag : break

        while True :
            # When enemies are attacked by player's missile
            flag = True
            for player_missile_id in cls._player_missile_ids :
                player_missile_object = cls._player_missile_objects[player_missile_id]
                player_missile_coord = player_missile_object.image_coord
                for enemy_id in cls._enemy_ids:
                    enemy_object = cls._enemy_objects[enemy_id]
                    enemy_coord = enemy_object.image_coord
                    iou = max(0, min(player_missile_coord[2], enemy_coord[2])- max(player_missile_coord[0], enemy_coord[0]))*max(0, min(player_missile_coord[3], enemy_coord[3])-max(player_missile_coord[1], enemy_coord[1]))

                    # When enemy is attacked, the flag become false
                    if iou > 0 : 
                        flag = False
                        break
                if flag == False :
                    cls._player_missile_ids.remove(player_missile_id)
                    cls._enemy_ids.remove(enemy_id)
                    del cls._player_missile_objects[player_missile_id]
                    del cls._enemy_objects[enemy_id]
                    break
            if flag : break

class Background:
    def __init__(self, name='background'):
        self._name = name
        self._scroll_speed = 5
        self._crop_point = SCREEN_HEIGHT
        self._image = Image.open(BACKGROUND_INFO[self.name]['path'])

    @property
    def name(self):
        return self._name

    def _get_image(self):
        # Scroll crop point calculation
        if self._crop_point - self._scroll_speed <= 0 :
            self._crop_point = SCREEN_HEIGHT
        else :
            self._crop_point -= self._scroll_speed

        # image move
        image = Image.open(BACKGROUND_INFO[self.name]['path'])
        empty_image = Image.new('RGBA', (SCREEN_WIDTH, SCREEN_HEIGHT))
        cropped_image1 = image.crop((0, self._crop_point, SCREEN_WIDTH, SCREEN_HEIGHT))
        cropped_image2 = image.crop((0, 0, SCREEN_WIDTH, self._crop_point))
        empty_image.paste(cropped_image1, (0, 0))
        empty_image.paste(cropped_image2, (0, SCREEN_HEIGHT-self._crop_point))
        self._image = empty_image
        return self._image

    def __call__(self):
        ObjectController.renew()
        background_image = self._get_image()

        # Player's objects are sticked on the background image
        objects = ObjectController.getPlayerObjects()
        player, player_missiles = objects
        for info in player.items() :
            player_object = info[1]
            new_image = Image.alpha_composite(background_image.crop(player_object.image_coord), player_object.image)		
            background_image.paste(new_image, (player_object.image_coord[0], player_object.image_coord[1]))
        for info in player_missiles.items() :
            player_missile_object = info[1]
            new_image = Image.alpha_composite(background_image.crop(player_missile_object.image_coord), player_missile_object.image)		
            background_image.paste(new_image, (player_missile_object.image_coord[0], player_missile_object.image_coord[1]))

        # Enemy's objects are sticked on the background image
        objects = ObjectController.getEnemyObjects()
        enemy, enemy_missiles = objects
        for info in enemy.items() :
            enemy_object = info[1]
            new_image = Image.alpha_composite(background_image.crop(enemy_object.image_coord), enemy_object.image)		
            background_image.paste(new_image, (enemy_object.image_coord[0], enemy_object.image_coord[1]))        
        for info in enemy_missiles.items() :
            enemy_missile_object = info[1]
            new_image = Image.alpha_composite(background_image.crop(enemy_missile_object.image_coord), enemy_missile_object.image)		
            background_image.paste(new_image, (enemy_missile_object.image_coord[0], enemy_missile_object.image_coord[1]))        
        return background_image


class GameObject:
    def __init__(self, obj_coord, name, team):
        self._name = name
        self._team = team
        self._role = OBJECT_INFO[self.name]['role']
        self._speed = OBJECT_INFO[self.name]['speed']
        self._width = OBJECT_INFO[self.name]['width']
        self._height = OBJECT_INFO[self.name]['height']
        self._image = Image.open(OBJECT_INFO[self.name]['path']).resize(OBJECT_INFO[self.name]['size'])
        self._obj_coord = obj_coord
        self._image_coord = self.image_coord
        self._obj_id = ObjectController.enroll(self)

    @property
    def name(self):
        return self._name

    @property
    def team(self):
        return self._team

    @property
    def role(self):
        return self._role

    @property
    def image(self):
        return self._image

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def obj_coord(self):
        return self._obj_coord

    @obj_coord.setter
    def obj_coord(self, new_coord):
        self._obj_coord = new_coord

    @property
    def speed(self):
        return self._speed

    @property
    def image_coord(self):
        self._image_coord = (self.obj_coord[0]-self.width//2, self.obj_coord[1]-self.height//2, 
                            self.obj_coord[0]+self.width//2+1, self.obj_coord[1]+self.height//2+1)
        return self._image_coord

    @property
    def obj_id(self):
        return self._obj_id

    def move(self):
        self._obj_coord = (self.obj_coord[0]+self.speed[0], self.obj_coord[1]+self.speed[1])

class Player(GameObject):
    def __init__(self, obj_coord, name='player1', team='player', role='fighter-plane'):
        super().__init__(obj_coord, name, team)

    def shoot(self):
        missile_coord = (self.obj_coord[0], self.obj_coord[1] - self.height//2 - 5)
        Missile(missile_coord, 'missile2', 'player')
        pass 

    def move(self, key):
        if key == 'L' :
            self.obj_coord = (self.obj_coord[0]-self.speed[0], self.obj_coord[1])
        elif key == 'R' :
            self.obj_coord = (self.obj_coord[0]+self.speed[0], self.obj_coord[1])
        elif key == 'U' :
            self.obj_coord = (self.obj_coord[0], self.obj_coord[1]-self.speed[1])
        elif key == 'D' :
            self.obj_coord = (self.obj_coord[0], self.obj_coord[1]+self.speed[1])      

class Enemy(GameObject):
    def __init__(self, obj_coord, name='enemy1', team='enemy', role='fighter-plane'):
        super().__init__(obj_coord, name, team)
        self.prev_attack_time = datetime.datetime.now()
        self.attack_cycle = OBJECT_INFO[name]['attack_cycle']

    def attack(self):
        missile_coord = (self.obj_coord[0], self.obj_coord[1] + self.height//2 + 5)
        Missile(missile_coord)
        self.prev_attack_time = datetime.datetime.now()

class Missile(GameObject):
    def __init__(self, obj_coord, name='missile1', team='enemy', role='missile'):
        super().__init__(obj_coord, name, team)














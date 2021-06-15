from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
import time
import random
import os
import sys
from settings import *


class Button:
    def __init__(self):
        self._left = BUTTON_L
        self._right = BUTTON_R
        self._up = BUTTON_U
        self._down = BUTTON_D

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
            else :
                cls._enemy_objects[object_id] = my_object
        elif my_object.team == 'player':
            if my_object.role == 'missile':
                cls._player_missile_objects[object_id] = my_object
            else :
                cls._player_object[object_id] = my_object

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
                else :
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
                else :
                    if new_id in cls._player_id : continue
                    else : 
                        cls._player_id.add(new_id)
                        return new_id
    # when objects moved, the objects must be renewed.
    @classmethod
    def renew(cls):
        while True :
            # When player is attacked by enemy's missiles
            flag = True
            for player_id in cls._player_id :
                player_object = cls._player_object[player_id]
                player_coord = player_object.image_coord
                for enemy_id in cls._enemy_missile_ids:
                    enemy_missile_object = cls._enemy_missile_objects[enemy_id]
                    enemy_missile_coord = enemy_missile_object.image_coord
                    iou = max(0, min(player_coord[2], enemy_missile_coord[2])- max(player_coord[0], enemy_missile_coord[0]))*max(0, min(player_coord[3], enemy_missile_coord[3])-max(player_coord[1], enemy_missile_coord[1]))

                    if iou > 0 : # Player is attacked
                        flag = False
                        break
                if flag == False :
                    cls._player_id.remove(player_id)
                    cls._enemy_missile_ids.remove(enemy_id)
                    del cls._player_object[player_id]
                    del cls._enemy_missile_objects[enemy_id]
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

                    if iou > 0 : # Missiles are carshed
                        flag = False
                        break
                if flag == False :
                    cls._player_id.remove(player_missile_id)
                    cls._enemy_missile_ids.remove(enemy_missile_id)
                    del cls._player_object[player_missile_id]
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

                    if iou > 0 : # Missiles are carshed
                        flag = False
                        break
                if flag == False :
                    cls._player_id.remove(player_missile_id)
                    cls._enemy_missile_ids.remove(enemy_id)
                    del cls._player_object[player_missile_id]
                    del cls._enemy_missile_objects[enemy_id]
                    break
            if flag : break

class Background:
    def __call__(self):
        ObjectController.renew()
        image = Image.open(os.path.join(IMAGE_PATH, IMAGE_NAME.format('background'))).resize((SCREEN_WIDTH, SCREEN_HEIGHT))

        objects = ObjectController.getPlayerObjects()
        player, player_missiles = objects
        for info in player.items() :
            pobject = info[1]
            new_image = Image.alpha_composite(image.crop(pobject.image_coord), pobject.image)		
            image.paste(new_image, (pobject.image_coord[0], pobject.image_coord[1]))
        for info in player_missiles.items() :
            pobject = info[1]
            new_image = Image.alpha_composite(image.crop(pobject.image_coord), pobject.image)		
            image.paste(new_image, (pobject.image_coord[0], pobject.image_coord[1]))

        objects = ObjectController.getEnemyObjects()
        enemy, enemy_missiles = objects
        for info in enemy.items() :
            eobject = info[1]
            new_image = Image.alpha_composite(image.crop(eobject.image_coord), eobject.image)		
            image.paste(new_image, (eobject.image_coord[0], eobject.image_coord[1]))        
        for info in enemy_missiles.items() :
            eobject = info[1]
            new_image = Image.alpha_composite(image.crop(eobject.image_coord), eobject.image)		
            image.paste(new_image, (eobject.image_coord[0], eobject.image_coord[1]))        
        return image


class CustomObject:
    def __init__(self, obj_coord, name, team, role):
        self._team = team
        self._role = role
        self._name = name
        self._image = Image.open(OBJECT_INFO[self._name]['path']).resize(OBJECT_INFO[self._name]['size'])
        self._width = OBJECT_INFO[self._name]['width']
        self._height = OBJECT_INFO[self._name]['height']
        self._obj_coord = obj_coord
        self._image_coord = self.image_coord
        ObjectController.enroll(self)

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
    def image_coord(self):
        self._image_coord = (self.obj_coord[0]-self._width//2, self.obj_coord[1]-self._height//2, 
                            self.obj_coord[0]+self._width//2+1, self.obj_coord[1]+self._height//2+1)
        return self._image_coord

    @property
    def obj_coord(self):
        return self._obj_coord

    @obj_coord.setter
    def obj_coord(self, new_coord):
        self._obj_coord = new_coord



class Player(CustomObject):
    def __init__(self, obj_coord, name='player1', team='player', role='player'):
        super().__init__(obj_coord, name, team, role)
        self._speed = OBJECT_INFO[name]['speed']

    def attack(self):
        pass

    def move(self, key):
        if key == 'L' :
            self.obj_coord = (self.obj_coord[0]-self._speed, self.obj_coord[1])
        elif key == 'R' :
            self.obj_coord = (self.obj_coord[0]+self._speed, self.obj_coord[1])
        elif key == 'U' :
            self.obj_coord = (self.obj_coord[0], self.obj_coord[1]-self._speed)
        elif key == 'D' :
            self.obj_coord = (self.obj_coord[0], self.obj_coord[1]+self._speed)      


class Missile(CustomObject):
    def __init__(self, obj_coord, speed, name='missile1', team='enemy', role='missile'):
        '''
        obj_coord : (x_center, y_center)
        speed : (dx, dy)
        '''
        super().__init__(obj_coord, name, team, role)
        self._speed = speed

    def move(self):
        '''
		calculate new coordinate
        '''
        self.obj_coord = (self.obj_coord[0]+self._speed[0], self.obj_coord[1]+self._speed[1])













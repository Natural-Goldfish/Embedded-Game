from settings import *
from src.object_controller import ObjectController
from PIL import Image
import datetime, os

###
# Game object information
###
OBJECT_INFO = {
    'effect-boom1' : {
        'width' : 61,
        'height' : 61,
        'size' : (61, 61),
        'path' : os.path.join(IMAGE_PATH, 'effect-boom2.png'),
        'speed' : (0, 0),
        'team' : 'none',
        'role' : 'effect',
    },
    'missile1' : {
            'width' : 13,
            'height' : 13,
            'size' : (13, 13),
            'path' : os.path.join(IMAGE_PATH, 'missile1.png'),
            'speed' : (0, 5),
            'role' : 'missile',
            'damage' : 11
         
    },
    'missile2' : {
            'width' : 13,
            'height' : 13,
            'size' : (13, 13),
            'path' : os.path.join(IMAGE_PATH, 'missile2.png'),
            'speed' : (0, 6),
            'role' : 'missile',
            'damage' : 13
         
    },
    'missile3' : {
            'width' : 13,
            'height' : 13,
            'size' : (13, 13),
            'path' : os.path.join(IMAGE_PATH, 'missile3.png'),
            'speed' : (0, 7),
            'role' : 'missile',
            'damage' : 15
         
    },
    'missile4' : {
            'width' : 13,
            'height' : 13,
            'size' : (13, 13),
            'path' : os.path.join(IMAGE_PATH, 'missile4.png'),
            'speed' : (0, 8),
            'role' : 'missile',
            'damage' : 17
         
    },
    'missile5' : {
            'width' : 13,
            'height' : 13,
            'size' : (13, 13),
            'path' : os.path.join(IMAGE_PATH, 'missile5.png'),
            'speed' : (0, 10),
            'role' : 'missile',
            'damage' : 20
         
    },
    'player-missile1' : {
            'width' : 13,
            'height' : 13,
            'size' : (13, 13),
            'path' : os.path.join(IMAGE_PATH,'player-missile1.png'),
            'speed' : (0, -10),
            'role' : 'missile',
            'damage' : 15
         
    },
    'player1' : {
                'width' : 51,
                'height' : 51,
                'size' : (51, 51),
                'path' : os.path.join(IMAGE_PATH, 'player1.png'),
                'speed' : (10, 10),
                'role' : 'fighter-plane',
                'missile-name' : 'player-missile1',
                'hp' : 20
    },
    'player2' : {
                'width' : 25,
                'height' : 25,
                'size' : (25, 25),
                'path' : os.path.join(IMAGE_PATH, 'player2.png'),
                'speed' : (10, 10),
                'role' : 'fighter-plane',
                'missile-name' : 'player-missile1',
                'hp' : 20
    },
    'enemy1' : {
                'width' : 47,
                'height' : 47,
                'size' : (47, 47),
                'path' : os.path.join(IMAGE_PATH, 'enemy1.png'),
                'speed' : (1, 1),
                'role' : 'fighter-plane',
                'attack-cycle' : datetime.timedelta(0, 3),
                'missile-name' : 'missile1',
                'hp' : 10
    },
    'enemy2' : {
                'width' : 49,
                'height' : 49,
                'size' : (49, 49),
                'path' : os.path.join(IMAGE_PATH, 'enemy2.png'),
                'speed' : (-2, 2),
                'role' : 'fighter-plane',
                'attack-cycle' : datetime.timedelta(0, 3),
                'missile-name' : 'missile2',
                'hp' : 13
    },
    'enemy3' : {
                'width' : 51,
                'height' : 51,
                'size' : (51, 51),
                'path' : os.path.join(IMAGE_PATH, 'enemy3.png'),
                'speed' : (-3, 1),
                'role' : 'fighter-plane',
                'attack-cycle' : datetime.timedelta(0, 2.5),
                'missile-name' : 'missile3',
                'hp' : 15
    },
    'enemy4' : {
                'width' : 53,
                'height' : 53,
                'size' : (53, 53),
                'path' : os.path.join(IMAGE_PATH, 'enemy4.png'),
                'speed' : (-4, 1),
                'role' : 'fighter-plane',
                'attack-cycle' : datetime.timedelta(0, 2),
                'missile-name' : 'missile4',
                'hp' : 17
    },
    'enemy5' : {
                'width' : 57,
                'height' : 57,
                'size' : (57, 57),
                'path' : os.path.join(IMAGE_PATH, 'enemy5.png'),
                'speed' : (-5, 2),
                'role' : 'fighter-plane',
                'attack-cycle' : datetime.timedelta(0, 1.5),
                'missile-name' : 'missile5',
                'hp' : 20
    }
}

###
# Class
###
class GameObject:
    def __init__(self, obj_coord, name, team):
        self.__name = name
        self.__team = team
        self.__role = OBJECT_INFO[self.name]['role']
        self.__speed = OBJECT_INFO[self.name]['speed']
        self.__width = OBJECT_INFO[self.name]['width']
        self.__height = OBJECT_INFO[self.name]['height']
        self.__image = Image.open(OBJECT_INFO[self.name]['path']).resize(OBJECT_INFO[self.name]['size'])
        self.__obj_coord = obj_coord
        self.__image_coord = self.image_coord
        self.__obj_id = ObjectController.enroll(self)

    @property
    def name(self):
        return self.__name

    @property
    def team(self):
        return self.__team

    @property
    def role(self):
        return self.__role

    @property
    def image(self):
        return self.__image

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def obj_coord(self):
        return self.__obj_coord

    def _set_obj_coord(self, new_coord):
        self.__obj_coord = new_coord

    @property
    def speed(self):
        return self.__speed

    def _reverse_speed(self, x, y):
        if x and y :
            self.__speed = (-self.__speed[0], -self.__speed[1])
        elif x and not y :
            self.__speed = (-self.__speed[0], self.__speed[1])
        elif not x and y :
            self.__speed = (self.__speed[0], -self.__speed[1])
        else :
            pass

    @property
    def image_coord(self):
        self.__image_coord = (self.obj_coord[0]-self.width//2, self.obj_coord[1]-self.height//2, 
                            self.obj_coord[0]+self.width//2+1, self.obj_coord[1]+self.height//2+1)
        return self.__image_coord

    @property
    def obj_id(self):
        return self.__obj_id

    def move(self):
        self._set_obj_coord((self.obj_coord[0]+self.speed[0], self.obj_coord[1]+self.speed[1]))

class Player(GameObject):
    def __init__(self, obj_coord, name='player1', team='player', role='fighter-plane'):
        super().__init__(obj_coord, name, team)
        self.__hp = OBJECT_INFO[self.name]['hp']
        self.__kill_point = 0

    @property
    def hp(self):
        return self.__hp

    @property
    def kill_point(self):
        return self.__kill_point

    def _add_kill_point(self):
        self.__kill_point += 1

    def _be_attacked(self, missile):
        self.__hp -= missile.damage
        if self.__hp <= 0 :
            BoomEffect(self.obj_coord)

    def shoot(self):
        missile_coord = (self.obj_coord[0], self.obj_coord[1] - self.height//2 - 5)
        Missile(missile_coord, OBJECT_INFO[self.name]['missile-name'], self.team)

    def move(self, key):
        if key == 'L' :
            self._set_obj_coord((self.obj_coord[0]-self.speed[0], self.obj_coord[1]))
        elif key == 'R' :
            self._set_obj_coord((self.obj_coord[0]+self.speed[0], self.obj_coord[1]))
        elif key == 'U' :
            self._set_obj_coord((self.obj_coord[0], self.obj_coord[1]-self.speed[1]))
        elif key == 'D' :
            self._set_obj_coord((self.obj_coord[0], self.obj_coord[1]+self.speed[1]))    

class Enemy(GameObject):
    def __init__(self, obj_coord, name='enemy1', team='enemy', role='fighter-plane'):
        super().__init__(obj_coord, name, team)
        self.__prev_attack_time = datetime.datetime.now()
        self.__attack_cycle = OBJECT_INFO[self.name]['attack-cycle']
        self.__hp = OBJECT_INFO[self.name]['hp']

    @property
    def hp(self):
        return self.__hp

    def _be_attacked(self, missile):
        self.__hp -= missile.damage
        if self.__hp <= 0 :
            BoomEffect(self.obj_coord)

    def move(self):
        super().move()
        if self.obj_coord[0] <= 0 or self.obj_coord[0] >= SCREEN_WIDTH :
            self._reverse_speed(True, True)
            super().move()
        elif self.obj_coord[1] <= 0 :
            self._reverse_speed(False, True)
            super().move()

    def shoot(self):
        if datetime.datetime.now()-self.__prev_attack_time >= self.__attack_cycle :
            Missile((self.obj_coord[0], self.obj_coord[1] + self.height//2 + 5), OBJECT_INFO[self.name]['missile-name'])
            self.__prev_attack_time = datetime.datetime.now()

class Missile(GameObject):
    def __init__(self, obj_coord, name='missile1', team='enemy', role='missile'):
        super().__init__(obj_coord, name, team)
        self.__damage = OBJECT_INFO[self.name]['damage']

    @property
    def damage(self):
        return self.__damage

class BoomEffect(GameObject):
    def __init__(self, obj_coord, name='effect-boom1', team='none', role='effect'):
        super().__init__(obj_coord, name, team)


import adafruit_rgb_display.st7789 as st7789
from digitalio import DigitalInOut, Direction
import board
import datetime


# Create the display
PIN_CS = DigitalInOut(board.CE0)
PIN_DC = DigitalInOut(board.D25)
PIN_RESET = DigitalInOut(board.D24)
BAUDRATE = 24000000

SPI = board.SPI()
DISPLAY = st7789.ST7789(
    SPI,
    height=240,
    y_offset=80,
    rotation=180,
    cs=PIN_CS,
    dc=PIN_DC,
    rst=PIN_RESET,
    baudrate=BAUDRATE,
)

SCREEN_WIDTH = DISPLAY.width
SCREEN_HEIGHT = DISPLAY.height
START_POINT = (SCREEN_WIDTH//2, 4*(SCREEN_HEIGHT//5))

# Input pins:
BUTTON_A = DigitalInOut(board.D5)
BUTTON_A.direction = Direction.INPUT

BUTTON_B = DigitalInOut(board.D6)
BUTTON_B.direction = Direction.INPUT


BUTTON_L = DigitalInOut(board.D27)
BUTTON_L.direction = Direction.INPUT
#BUTTON_L_CLICKED = False if BUTTON_L.value else True

def L_CLICKED():
    if BUTTON_L.value : return False
    else : return True
BUTTON_L_CLICKED = L_CLICKED()


BUTTON_R = DigitalInOut(board.D23)
BUTTON_R.direction = Direction.INPUT


BUTTON_U = DigitalInOut(board.D17)
BUTTON_U.direction = Direction.INPUT


BUTTON_D = DigitalInOut(board.D22)
BUTTON_D.direction = Direction.INPUT


BUTTON_C = DigitalInOut(board.D4)
BUTTON_C.direction = Direction.INPUT

# Turn on the Backlight
BACKLIGHT = DigitalInOut(board.D26)
BACKLIGHT.switch_to_output()
BACKLIGHT.value = True

#Image
IMAGE_PATH = 'images'
IMAGE_NAME = '{}.png'

OBJECT_INFO = {
    'missile1' : {
            'width' : 13,
            'height' : 13,
            'size' : (13, 13),
            'path' : 'images/missile1.png',
            'speed' : (0, 2),
            'role' : 'missile',
         
    },
    'player1' : {
                'width' : 25,
                'height' : 25,
                'size' : (25, 25),
                'path' : 'images/player1.png',
                'speed' : (5, 5),
                'role' : 'fighter-plane'
    },
    'enemy1' : {
                'width' : 31,
                'height' : 31,
                'size' : (31, 31),
                'path' : 'images/enemy1.png',
                'speed' : (1, 0),
                'role' : 'fighter-plane',
                'attack_cycle' : datetime.timedelta(0, 3),
                'missile_speed' : (0, 10)
    },
    'enemy2' : {
                'width' : 31,
                'height' : 31,
                'size' : (31, 31),
                'path' : 'images/enemy2.png',
                'speed' : (-1, 0),
                'role' : 'fighter-plane',
                'attack_cycle' : datetime.timedelta(0, 4),
                'missile_speed' : (0, 15)
    }
}

from settings import *
from game2 import *

'''
BUTTON_L_CLICKED = False if BUTTON_L.value else True
BUTTON_R_CLICKED = False if BUTTON_R.value else True
BUTTON_U_CLICKED = False if BUTTON_U.value else True
BUTTON_D_CLICKED = False if BUTTON_D.value else True


def main():
    enemy = Missile((150, 50), (0, 1))

    for time in range(50):
        image_background = Image.open(os.path.join(IMAGE_PATH, IMAGE_NAME.format('background'))).resize((SCREEN_WIDTH, SCREEN_HEIGHT))
        enemy.move()
        DISPLAY.image(image_background)
'''
def main():
    background = Background()
    button = Button()

    player = Player(START_POINT)
    enemy = Missile((150, 50), (0, 3))

    while True:
	
        enemy.move()

        if button.left : 
            player.move('L')
        elif button.right :
            player.move('R')
        elif button.up : 
            player.move('U')
        elif button.down :
            player.move('D')
        DISPLAY.image(background())     

    for time in range(50):
        enemy.move()


main()
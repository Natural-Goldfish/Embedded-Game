from settings import *
from game2 import *
import datetime
import time


import datetime
'''
image = Image.open('images/background-new2.png') 
image = image.convert('RGBA')
cropped_image = image.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
cropped_image.save('images/background-new.png')
'''



def main():
    background = Background()
    button = Button()

    player = Player(START_POINT)
    missile = Missile((150, 50))
    enemy = Enemy((100, 1))
    enemy2 = Enemy((200, 10), 'enemy2')
    start = datetime.datetime.now()

    while True:	

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
        DISPLAY.image(background())     

main()
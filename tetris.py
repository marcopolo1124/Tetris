from block_class import Block
import pygame
import random
from control_layer import PlayArea

pygame.init()

screen = pygame.display.set_mode((800, 600))
 
#load block skin
I = Block((1.5,1.5), 'B', [[0,2], [1,2], [2,2], [3,2]])
J = Block((1,1), 'D', [[0,1], [1,1], [2,1], [0,2]])
L = Block((1,1), 'O', [[0,1], [1,1], [2,1], [2,2]])
T = Block((1,1), 'P', [[0,1], [1,1], [2,1], [1,2 ]])
O = Block((1.5,1.5), 'Y', [[1,1], [2,1], [1,2], [2,2]])
S = Block((1,1), 'G', [[0,1], [1,1], [1,2], [2,2]])
Z = Block((1,1), 'R', [[1,1], [2,1], [0,2], [1,2]])

block_list = [I,J,L,T,O,S,Z]
current_block = random.choice(block_list)
play_area = PlayArea(block_list=block_list, DAS =50, ARR = 0, gravity = 300)


running = True
while running:
    screen.fill((0, 0, 0))
    play_area.execute()
    


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x: 
                play_area.turn_block(1)
            if event.key == pygame.K_z:
                play_area.turn_block(-1)

            if event.key == pygame.K_LEFT:
                play_area.left_key_press()
                play_area.move_side()

            if event.key == pygame.K_RIGHT:
                play_area.right_key_press()
                play_area.move_side()

            if event.key == pygame.K_SPACE:
                play_area.space_press()
            
            if event.key == pygame.K_DOWN:
                play_area.key_down_press() 


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                play_area.left_key_release()

            if event.key == pygame.K_RIGHT:
                play_area.right_key_release()
            if event.key == pygame.K_DOWN:
                play_area.key_down_release()
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

    





import pygame
import random
import numpy as np

screen = pygame.display.set_mode((800, 600))
BLACK = (0,0,0)
WHITE = (255,255,255)


class PlayArea:

    #grid_size
    grid = [10, 20]
    #block size
    block_size = 20
    #placing grid in the middle left of screen instead of corner
    offset = [100, 100]

    gravity_timer = 0
    array = [['' for i in range(10)] for j in range(25)]

    def __init__(self, block_list, DAS, ARR, gravity):
        self.block_list = block_list
        self.current_block = None
        self.available = True

        #Delay auto shift: delay between first movement and subsequent movement
        self.DAS = DAS
        #delay between all subsequenct movement after first movement
        self.ARR = ARR

        #Delay between block moving down
        self.nat_gravity = gravity
        self.gravity_delay = gravity

        #Start point for all blocks
        self.block_pos = np.array([3,20])

        #Current block turn
        self.turn = 0


    #spawning behaviour
    def spawn(self):
        if self.available:
            self.block_pos = np.array([3,20])
            self.current_block = random.choice(self.block_list)
            self.available = False
            self.turn = 0

    #turns the block
    def turn_block(self, direction):
        self.turn += direction
        self.turn %= 4
        self.check_side_turn()

    #Shows the block
    def show_block(self, turn):
        self.current_block.show_block(turn = turn, x = self.offset[0] + self.block_pos[0]*self.block_size, y = self.block_pos[1]*self.block_size+self.offset[1])

    #When 
    def gravity(self):
        if self.gravity_timer >= self.gravity_delay:
            self.block_pos[1] -= 1
            self.gravity_timer = 0


    def draw_grid(self):

        for x in range(0, self.grid[0]*self.block_size, self.block_size):
            for y in range(0, self.grid[1]*self.block_size, self.block_size):
                rect = pygame.Rect(x+ self.offset[0],y+self.offset[1]+20, self.block_size, self.block_size)
                pygame.draw.rect(screen, WHITE, rect, 1)

    def increment_time(self):
        self.gravity_timer += 1

    def check_bottom(self):
        set = False
        for block in self.current_block.rotation_dict[self.turn]:
            x = block[0] + self.block_pos[0]
            y = block[1] + self.block_pos[1]
            if y < 0 or self.array[int(y)][int(x)] != '':

                self.block_pos[1]+=1
                self.available = True
                set = True
        if set:
            self.set_block()
        return set


    key_timer_right = 0
    key_timer_left = 0
    key_down_right = False
    key_down_left = False
    direction = 0

    def right_key_press(self):
        self.key_down_right = True
        self.direction = 1
        self.key_timer_left = 0

    def left_key_press(self):
        self.key_down_left = True
        self.direction = -1
        self.key_timer_right = 0

    def right_key_release(self):
        self.key_down_right = False

        self.key_timer_right = 0

    def left_key_release(self):
        self.key_down_left = False

        self.key_timer_left = 0

    def move_side(self):
        if self.check_side():
            self.block_pos[0] += self.direction


    #Define the long press mechanics.
    def long_press(self):
        #Increment timer as long as the key is pressed     
        #Right key down
        if self.key_down_right:
            self.key_timer_right += 1
            #When the key timer hits the DAS mark, check before moving left
            if self.key_timer_right == self.DAS:
                if self.check_side():
                    self.block_pos[0]+=self.direction
            
            if self.ARR > 0:
                if (self.key_timer_right - self.DAS)%self.ARR == 0 and self.key_timer_right > self.DAS:
                    if self.check_side():
                        self.block_pos[0]+=self.direction
            if self.ARR <= 0:
                if self.key_timer_right > self.DAS:
                    if self.check_side():
                        self.block_pos[0]+=self.direction

        #Left key down
        if self.key_down_left:
            self.key_timer_left += 1

            if self.key_timer_left == self.DAS:

                if self.check_side():
                    self.block_pos[0]+=self.direction
            if self.ARR > 0:
                if (self.key_timer_left - self.DAS)%self.ARR == 0 and self.key_timer_left > self.DAS:
                    if self.check_side():
                        self.block_pos[0]+=self.direction
            if self.ARR <= 0:
                if self.key_timer_left > self.DAS:
                    if self.check_side():
                        self.block_pos[0]+=self.direction
        

    #Prevents out of bounds after moving left/right
    def check_side(self):
        collision = False
        for block in self.current_block.rotation_dict[self.turn]:
            x= block[0]+ self.block_pos[0]
            new_x = x + self.direction
            y = block[1] + self.block_pos[1]
            if new_x <0 or new_x >=10 or self.array[int(y)][int(new_x)] != '':

                return False
            else:
                collision = True
        return collision

    #Prevents out of bounds after turning
    def check_side_turn(self):

        for block in self.current_block.rotation_dict[self.turn]:
            if block[0] + self.block_pos[0] <0:

                self.block_pos[0] -=block[0]+self.block_pos[0]

            elif block[0] + self.block_pos[0]  >=10:

                self.block_pos[0] -= block[0]+self.block_pos[0] - 9

    def set_block(self):
        for i in range(4):
            x=self.block_pos[0] + self.current_block.rotation_dict[int(self.turn)][i][0]
            y=self.block_pos[1] + self.current_block.rotation_dict[int(self.turn)][i][1]
            self.array[int(y)][int(x)] = self.current_block.color
    color_dict = {'B': (0,255,255),'D':(0,0,255),'O':(255,127,0),'P':(128,0,128),'Y':(255,255,0),'G':(0,255,0),'R':(255,0,0)}
    def draw_array(self):
        for j in range(len(self.array)):
            for i in range(len(self.array[j])):
                if self.array[j][i]:
                    # block_skin = pygame.image.load(self.array[j][i]+'.png')
                    rect = pygame.Rect(i*self.block_size+ self.offset[0], (self.block_size * len(self.array) - (j*self.block_size)) + (self.offset[1])-5*self.block_size, self.block_size, self.block_size)
                    pygame.draw.rect(screen, self.color_dict[self.array[j][i]],rect, 0)
                    # screen.blit(block_skin, (i*self.block_size+ self.offset[0], (self.block_size * len(self.array) - (j*self.block_size)) + (self.offset[1])-5*self.block_size))

    def space_press(self):
        free = True
        while free:
            self.block_pos[1] -= 1
            if self.check_bottom():
                free = False
    key_down = False
    def key_down_press(self):
        self.key_down = True
    
    def key_down_release(self):
        self.key_down = False
    
    def key_down_motion(self):
        if self.key_down:
            self.gravity_delay = int(self.nat_gravity*(1/12))
        else:
            self.gravity_delay = self.nat_gravity

    def line_clear(self):
        for row in self.array:
            if all(row):
                self.array.pop(self.array.index(row))
                self.array.append(['' for i in range(10)])


    def execute(self):
        self.spawn()
        self.draw_grid()
        self.long_press()
        self.check_bottom()
        self.show_block(self.turn)
        self.gravity()
        self.key_down_motion()
        self.increment_time()
        self.draw_array()
        self.line_clear()
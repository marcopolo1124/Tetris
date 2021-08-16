from numpy.lib.function_base import copy
import pygame
import random
import numpy as np

screen = pygame.display.set_mode((800, 600))
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (127,127,127)


class PlayArea:

    #grid_size
    grid = [10, 20]
    #block size
    block_size = 20
    #placing grid in the middle left of screen instead of corner
    offset = [100, 100]
    hold_block = []

    gravity_timer = 0
    array = [['' for i in range(10)] for j in range(25)]

    def __init__(self, block_list, DAS, ARR, gravity):
        self.block_list = block_list
        self.bag = block_list.copy()
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

        #Queue
        self.queue = []
        for i in range(5):
            chosen = random.choice(self.bag)
            self.bag.pop(self.bag.index(chosen))
            self.queue.append(chosen)

    def refill_bag(self):
        if len(self.bag) == 0:
            print(self.block_list)
            self.bag = self.block_list.copy()
            print(self.bag)

    #spawning behaviour
    def spawn(self):
        if self.available:
            self.block_pos = np.array([3,20])
            self.current_block = self.queue.pop(0)
            print(self.bag)
            if len(self.bag) > 1:
                chosen = random.choice(self.bag)
            else:
                chosen = self.bag[0]
            self.bag.pop(self.bag.index(chosen))
            self.queue.append(chosen)
            self.available = False
            self.turn = 0
    held = False
    def hold(self):
        if not self.held:
            if len(self.hold_block) == 0:
                self.hold_block.append(self.current_block)
                self.available = True
            else:
                self.hold_block[0], self.current_block = self.current_block, self.hold_block[0]
                self.block_pos = [3,20]
            self.held = True
    def show_hold(self):
        if len(self.hold_block) != 0:
            self.hold_block[0].show_block(0, 10, 440)

    def show_queue(self):
        for i in range(5):
            self.queue[i].show_block(0, 350, 500- (100+(i*4*self.block_size)))

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
                pygame.draw.rect(screen, GREY, rect, 1)

    def increment_time(self):
        self.gravity_timer += 1
    # Checks if the block is at the bottom. If block is below the bottom, or overlapping with a piece, the position will be corrected
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

    #starts timer every time the left/right key is hit
    key_timer_right = 0
    key_timer_left = 0
    key_down_right = False
    key_down_left = False
    direction = 0

    #Left and right key are kept separate in order for the DAS and ARR system to work accordingly
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
    #moves the block in a direction when left/right arrow key is pressed
    def move_side(self):
        #Check if there are obstructions first (If the check is done after a change in the position, then pieces will flicker)
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
            #After the DAS timer is up, every time the timer is a multiple of ARR, move
            if self.ARR > 0:
                if (self.key_timer_right - self.DAS)%self.ARR == 0 and self.key_timer_right > self.DAS:
                    if self.check_side():
                        self.block_pos[0]+=self.direction
            if self.ARR <= 0:
                if self.key_timer_right > self.DAS:
                    if self.check_side():
                        self.block_pos[0]+=self.direction

        #Left key down
        #Same as right key down. I can't seem to merge the two if statements since right key timer and left key timer are separate
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
        self.held = False

    color_dict = {'B': (0,255,255),'D':(0,0,255),'O':(255,127,0),'P':(128,0,128),'Y':(255,255,0),'G':(0,255,0),'R':(255,0,0)}

    def draw_array(self):
        for j in range(len(self.array)):
            for i in range(len(self.array[j])):
                if self.array[j][i]:
                    rect = pygame.Rect(i*self.block_size+ self.offset[0], (self.block_size * len(self.array) - (j*self.block_size)) + (self.offset[1])-5*self.block_size, self.block_size, self.block_size)
                    pygame.draw.rect(screen, self.color_dict[self.array[j][i]],rect, 0)
    #Hard drop mechanics
    def space_press(self):
        free = True
        #While the block is not touching anything, drop down
        while free:
            self.block_pos[1] -= 1
            #If the block touches something, block is no longer free
            if self.check_bottom():
                free = False

    #Soft drop mechanics
    key_down = False

    #Changing True/False values on event allow for long presses
    def key_down_press(self):
        self.key_down = True
    
    def key_down_release(self):
        self.key_down = False

    def key_down_motion(self):
        #Change the gravity when the down key is pressed
        if self.key_down:
            self.gravity_delay = int(self.nat_gravity*(1/12))
        #If not, change back to the natural gravity
        else:
            self.gravity_delay = self.nat_gravity

    #When a row is full, clear row
    def line_clear(self):
        for row in self.array:
            if all(row):
                self.array.pop(self.array.index(row))
                #Append another row on the very top so that the list does not shrink
                self.array.append(['' for i in range(10)])


    def execute(self):
        self.refill_bag()
        self.spawn()
        self.show_queue()
        self.draw_grid()
        self.long_press()
        self.check_bottom()
        self.show_block(self.turn)
        self.gravity()
        self.key_down_motion()
        self.increment_time()
        self.draw_array()
        self.line_clear()
        self.show_hold()
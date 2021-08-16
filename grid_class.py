from numpy.lib.function_base import copy
import pygame
import random
import numpy as np

screen = pygame.display.set_mode((800, 600))
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (127,127,127)


class PlayArea:
    #Score
    score = 0
    #grid_size
    grid = [10, 20]
    #block size
    block_size = 20
    #placing grid in the middle left of screen instead of corner
    offset = [100, 100]
    #The holding queue. Press c to hold block
    hold_block = []
    #The timer to determine how long does it take the piece to move down 1 block
    gravity_timer = 0
    #This array determines line clears and which block is set in place
    array = [['' for i in range(10)] for j in range(25)]
    #The current block position. The initial position is at 3,20
    block_pos = np.array([3,20])
    #Determines if a new block should spawn
    available = True

    def __init__(self, block_list, DAS, ARR, gravity):
        self.block_list = block_list
        #The bag, aka the 7 bag randomizer. Put 7 pieces into the bag and draw until its empty, then refill bag
        self.bag = block_list.copy()
        #The block that is currently controlled by the player
        self.current_block = None

        #Delay auto shift: delay between first movement and subsequent movement
        self.DAS = DAS
        #delay between all subsequenct movement after first movement
        self.ARR = ARR

        #Delay between block moving down
        self.nat_gravity = gravity
        self.gravity_delay = gravity

        #Queue
        self.queue = []
        for i in range(5):
            chosen = random.choice(self.bag)
            self.bag.pop(self.bag.index(chosen))
            self.queue.append(chosen)

    #After the bag is depleted, refill the bag
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


    #Hold mechanics
    held = False
    def hold(self):
        #if statement so that only one hold is allowed per piece
        if not self.held:
            #If list is empty take current block and spawn next block
            if len(self.hold_block) == 0:
                self.hold_block.append(self.current_block)
                self.available = True
            #If list is not empty, then swap currently held block and current block
            else:
                self.hold_block[0], self.current_block = self.current_block, self.hold_block[0]
                self.block_pos = [3,20]
            #Only allow the block to be held once per piece
            self.held = True

    #Shows the held piece on the top left
    def show_hold(self):
        if len(self.hold_block) != 0:
            self.hold_block[0].show_block(0, 10, 440)

    #Shows the next spawning blocks
    def show_queue(self):
        for i in range(5):
            self.queue[i].show_block(0, 350, 500- (100+(i*4*self.block_size)))

    #turns the block
    turn = 0
    def turn_block(self, direction):
        self.turn += direction
        self.turn %= 4
        self.check_side_turn()

    #Shows the block in the current position on grid
    def show_block(self, turn):
        self.current_block.show_block(turn = turn, x = self.offset[0] + self.block_pos[0]*self.block_size, y = self.block_pos[1]*self.block_size+self.offset[1])

    #Gravity mechanics: How the pieces fall
    def gravity(self):
        #After a certain number of frames, the pieces will go down by 1 block
        if self.gravity_timer >= self.gravity_delay:
            self.block_pos[1] -= 1
            self.gravity_timer = 0
    #Increment timer
    def increment_time(self):
        self.gravity_timer += 1

    #Draws a 10 by 20 grid
    def draw_grid(self):
        for x in range(0, self.grid[0]*self.block_size, self.block_size):
            for y in range(0, self.grid[1]*self.block_size, self.block_size):
                rect = pygame.Rect(x+ self.offset[0],y+self.offset[1]+20, self.block_size, self.block_size)
                pygame.draw.rect(screen, GREY, rect, 1)


    # Checks if the block is at the bottom. If block is below the bottom, or overlapping with a piece, the position will be corrected
    def check_bottom(self):
        set = False
        for block in self.current_block.rotation_dict[self.turn]:
            x = block[0] + self.block_pos[0]
            y = block[1] + self.block_pos[1]
            if y < 0 or self.array[int(y)][int(x)] != '':
                self.block_pos[1]+=1
                self.available = True
                #If even 1 block is touching a block at the bottom, block is set
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

    #The DAS is also known as the Delay auto shift. It is the amount of time after the initial press that the block will repeatedly move
    #The ARR is the auto repeat rate. It is how fast the piece will move left to right during a long hold

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
        

    #Prevents out of bounds after moving left/right, as well as overlapping while moving left and right
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
    #Sets the final resting place of the piece.
    def set_block(self):
        for i in range(4):
            x=self.block_pos[0] + self.current_block.rotation_dict[int(self.turn)][i][0]
            y=self.block_pos[1] + self.current_block.rotation_dict[int(self.turn)][i][1]
            self.array[int(y)][int(x)] = self.current_block.color
        self.held = False

    color_dict = {'B': (0,255,255),'D':(0,0,255),'O':(255,127,0),'P':(128,0,128),'Y':(255,255,0),'G':(0,255,0),'R':(255,0,0)}
    
    #Draws the set pieces onto the screen
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
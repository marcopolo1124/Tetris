from numpy.lib.function_base import copy
import pygame
import random
import numpy as np

screen = pygame.display.set_mode((800, 600))

lines_clear_font = pygame.font.Font('DaysLater.ttf', 32)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (127,127,127)


class PlayArea:
    #Score
    score = 0
    lines_cleared = 0
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
    spawn_point = np.array([3, 18])
    block_pos = spawn_point.copy()
    #Determines if a new block should spawn
    available = True

    def __init__(self, block_list, DAS, ARR, gravity, lock_time, ghost_surface):
        self.block_list = block_list
        #The bag, aka the 7 bag randomizer. Put 7 pieces into the bag and draw until its empty, then refill bag
        self.bag = block_list.copy()
        #The block that is currently controlled by the player
        self.current_block = None
        self.ghost_surface = ghost_surface

        #Delay auto shift: delay between first movement and subsequent movement
        self.DAS = DAS
        #delay between all subsequenct movement after first movement
        self.ARR = ARR

        #Delay between block moving down
        self.nat_gravity = gravity
        self.gravity_delay = gravity
        self.lock_time = lock_time

        #Queue
        self.queue = []
        for i in range(5):
            chosen = random.choice(self.bag)
            self.bag.pop(self.bag.index(chosen))
            self.queue.append(chosen)

    #After the bag is depleted, refill the bag
    def refill_bag(self):
        if len(self.bag) == 0:
            self.bag = self.block_list.copy()


    #spawning behaviour
    def spawn(self):
        if self.available:
            self.block_pos = self.spawn_point.copy()
            self.current_block = self.queue.pop(0)
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
                self.block_pos = self.spawn_point.copy()
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

    kick_lst_01 = [np.array([0,0]), np.array([-1,0]), np.array([-1,1]),np.array([0,-2]),np.array([-1,-2])]
    kick_lst_10 = [np.array([0,0]), np.array([1,0]), np.array([1,-1]), np.array([0,2]), np.array([1,2])]
    kick_lst_12 = [np.array([0,0]), np.array([1,0]), np.array([1,-1]), np.array([0,2]), np.array([1,2])]
    kick_lst_21 = [np.array([0,0]), np.array([-1,0]), np.array([-1,1]),np.array([0,-2]),np.array([-1,-2])]
    kick_lst_23 = [np.array([0,0]), np.array([1,0]), np.array([1,1]),np.array([0,-2]),np.array([1,-2])]
    kick_lst_32 = [np.array([0,0]), np.array([-1,0]), np.array([-1,-1]), np.array([0,2]), np.array([-1,-2])]
    kick_lst_30 = [np.array([0,0]), np.array([-1,0]), np.array([-1,-1]),np.array([0,2]),np.array([-1,2])]
    kick_lst_03 = [np.array([0,0]), np.array([1,0]), np.array([1,1]), np.array([0,-2]), np.array([1,-2])]   
    jlstz_kick_dict = {str(0)+str(1): kick_lst_01, str(1)+str(0): kick_lst_10, str(1)+str(2): kick_lst_12, str(2)+str(1): kick_lst_21, str(2)+str(3): kick_lst_23, str(3)+str(2):kick_lst_32, str(3)+str(0):kick_lst_30, str(0)+str(3):kick_lst_03}

    ikick_lst_01 = [np.array([0,0]), np.array([-2,0]), np.array([1,0]),np.array([-2,-1]),np.array([1,2])]
    ikick_lst_10 = [np.array([0,0]), np.array([2,0]), np.array([-1,0]), np.array([2,1]), np.array([-1,-2])]
    ikick_lst_12 = [np.array([0,0]), np.array([-1,0]), np.array([2,0]), np.array([-1,2]), np.array([2,-1])]
    ikick_lst_21 = [np.array([0,0]), np.array([1,0]), np.array([-2,0]),np.array([1,-2]),np.array([-2,1])]
    ikick_lst_23 = [np.array([0,0]), np.array([2,0]), np.array([-1,0]),np.array([2,1]),np.array([-1,-2])]
    ikick_lst_32 = [np.array([0,0]), np.array([-2,0]), np.array([1,0]), np.array([-2,-1]), np.array([1,2])]
    ikick_lst_30 = [np.array([0,0]), np.array([1,0]), np.array([-2,0]),np.array([1,-2]),np.array([-2,1])]
    ikick_lst_03 = [np.array([0,0]), np.array([-1,0]), np.array([2,0]), np.array([-1,2]), np.array([2,-1])]
    i_kick_dict = {str(0)+str(1): ikick_lst_01, str(1)+str(0): ikick_lst_10, str(1)+str(2): ikick_lst_12, str(2)+str(1): ikick_lst_21, str(2)+str(3): ikick_lst_23, str(3)+str(2):ikick_lst_32, str(3)+str(0):ikick_lst_30, str(0)+str(3):ikick_lst_03}

    def check_side_turn(self,direction):
        kick_dict = {}
        overlap = False
        test_turn = (self.turn+direction)%4
        if self.current_block.color == 'B':
            kick_dict = self.i_kick_dict
        else:
            kick_dict = self.jlstz_kick_dict
        kick_lst = kick_dict[str(self.turn)+str(test_turn)]

        
        for trans in kick_lst:
            test_pos = self.block_pos.copy()
            overlap = False
            test_pos += trans
            for block in self.current_block.rotation_dict[test_turn]:
                test_x = int(block[0] + test_pos[0])
                test_y = int(block[1] + test_pos[1])
                if test_x < 0 or test_x >= 10 or test_y <0 or self.array[test_y][test_x]:
                    overlap = True
                    break
            if not overlap:
                self.block_pos = test_pos
                return overlap
        return True
    #turns the block
    turn = 0
    def turn_block(self, direction):
        if not self.check_side_turn(direction):
            self.turn += direction
            self.turn %= 4

    #Shows the block in the current position on grid
    def show_block(self):
        self.current_block.show_block(turn = self.turn, x = self.offset[0] + self.block_pos[0]*self.block_size, y = self.block_pos[1]*self.block_size+self.offset[1])

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
    lock_timer = 0
    def check_bottom(self):
        set = False
        for block in self.current_block.rotation_dict[self.turn]:
            x = block[0] + self.block_pos[0]
            y = block[1] + self.block_pos[1]
            if y < 0 or self.array[int(y)][int(x)] != '':
                self.block_pos[1]+=1
                if self.lock_timer >= self.lock_time:
                    set = True
            if y<= 0 or self.array[int(y)-1][int(x)] !='':
                self.lock_timer+=1
            
        if set:
            self.set_block()
            self.available = True
            self.lock_timer = 0
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

    def ghost(self):
        self.ghost_pos = self.block_pos.copy()
        overlap = False
        while not overlap:
            self.ghost_pos[1] -= 1
            for block in self.current_block.rotation_dict[self.turn]:
                ghost_x = int(block[0] + self.ghost_pos[0])
                ghost_y = int(block[1] + self.ghost_pos[1])
                if ghost_y < 0 or self.array[ghost_y][ghost_x] != '':
                    ghost_y += 1
                    overlap = True
        
    
    def show_ghost(self):
        self.current_block.show_ghost(turn = self.turn, x = self.offset[0] + self.ghost_pos[0]*self.block_size, y = self.ghost_pos[1]*self.block_size+self.offset[1]+20, surface = self.ghost_surface)
      

            


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
            self.gravity_delay = int(self.nat_gravity*(1/48))
        #If not, change back to the natural gravity
        else:
            self.gravity_delay = self.nat_gravity

    #When a row is full, clear row
    def clear(self):
        lines = 0
        for row in self.array:
            if all(row):
                self.array.pop(self.array.index(row))
                #Append another row on the very top so that the list does not shrink
                self.array.append(['' for i in range(10)])
                lines+=1
        self.lines_cleared += lines
    
    def show_lines_cleared(self):
        lines_clear_text = lines_clear_font.render('Lines Cleared: '+ str(self.lines_cleared), True, (255,255,255))
        screen.blit(lines_clear_text, (500, 100))

    def top_out(self):
        for grid in self.array[21]:
            if grid!='':
                return True


    def execute(self):
        if not self.top_out():
            self.spawn()
            self.refill_bag()
            self.long_press()
            self.ghost()
            self.gravity()
            self.increment_time()
            self.key_down_motion()
            self.check_bottom()
            self.clear()

    def draw(self):
        self.draw_grid()
        self.show_queue()
        self.show_block()
        self.show_ghost()
        self.draw_array()
        self.show_lines_cleared()
        self.show_hold()
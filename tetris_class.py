import pygame
import random
import numpy as np

screen = pygame.display.set_mode((800, 600))
BLACK = (0,0,0)
WHITE = (255,255,255)


class grid:
    grid = [10, 20]
    block_size = 20
    offset = [100, 100]
    gravity_timer = 0
    array = [['' for i in range(10)] for j in range(20)]

    def __init__(self, block_list, DAS, ARR, gravity):
        self.block_list = block_list
        self.current_block = None
        self.available = True

        #Delay auto shift: delay between first movement and subsequent movement
        self.DAS = DAS
        #delay between all subsequenct movement after first movement
        self.ARR = ARR

        #Delay between block moving down
        self.gravity_delay = gravity

        #Start point for all blocks
        self.block_pos = np.array([3,20])

        #Current block turn
        self.turn = 0
        print(self.array)



    def spawn(self):
        if self.available:
            self.block_pos = np.array([3,20])
            self.current_block = random.choice(self.block_list)
            self.available = False
            self.turn = 0


    def turn_block(self, direction):
        self.turn += direction
        self.turn %= 4
        self.check_side_turn()

    def show_block(self, turn):
        self.current_block.show_block(turn = turn, x = self.offset[0] + self.block_pos[0]*self.block_size, y = self.block_pos[1]*self.block_size+self.offset[1])

    def gravity(self):
        if self.gravity_timer >= self.gravity_delay:
            self.block_pos[1] -= 1
            self.gravity_timer = 0


    def draw_grid(self):

        for x in range(0, self.grid[0]*self.block_size, self.block_size):
            for y in range(0, self.grid[1]*self.block_size, self.block_size):
                rect = pygame.Rect(x+ self.offset[0],y+self.offset[1], self.block_size, self.block_size)
                pygame.draw.rect(screen, WHITE, rect, 1)

    def increment_time(self):
        self.gravity_timer += 1

    def check_bottom(self):
        for block in self.current_block.rotation_dict[self.turn]:
            if block[1] + self.block_pos[1] <= 0:
                self.block_pos[1]+=1
                self.available = True

    key_timer = 0
    key_down = False
    direction = 0

    def key_press(self):
        self.key_down = True

    def key_release(self):
        self.key_down = False
        self.key_timer = 0

    def move_side(self):
        if self.check_side():
            self.block_pos[0] += self.direction


    #Define the long press mechanics.
    def long_press(self):
        self.key_timer += 1
        if self.key_down == True:
            if self.key_timer == self.DAS:
                if self.check_side():
                    self.block_pos[0]+=self.direction
            if (self.key_timer - self.DAS)%self.ARR == 0 and self.key_timer > self.DAS:
                if self.check_side():
                    self.block_pos[0]+=self.direction

    def check_side(self):
        collision = False
        for block in self.current_block.rotation_dict[self.turn]:
            if block[0] + self.block_pos[0] +self.direction <0 or block[0] + self.block_pos[0] + self.direction >=10:

                return False
            else:
                collision = True
        return collision

    def check_side_turn(self):
        collision = False
        for block in self.current_block.rotation_dict[self.turn]:
            if block[0] + self.block_pos[0]  <0:
                self.block_pos += 1
            
            elif block[0] + self.block_pos[0]  >=10:
                self.block_pos -= 1
      


    def execute(self):
        self.spawn()
        self.draw_grid()
        self.long_press()
        self.show_block(self.turn)
        self.gravity()
        self.check_bottom()
        self.increment_time()
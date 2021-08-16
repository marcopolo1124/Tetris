import numpy as np
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
class Block:
    color_dict = {'B': (0,255,255),'D':(0,0,255),'O':(255,127,0),'P':(128,0,128),'Y':(255,255,0),'G':(0,255,0),'R':(255,0,0)}
    
    def __init__(self, center, color, default_coord):
        self.center = np.array(center)
        self.color = color
        self.default_coord = []
        self.rotation_dict={}

        #Set coordinate to numpy array
        for point in default_coord:
            self.default_coord.append(np.array(point))

        #Create a dictionary of all rotation    
        self.gen_rotation_dict()
        self.block_skin = pygame.image.load(color+'.png')
        self.block_size = 20

    def __repr__(self):
        return self.color

    def rotate(self, turn = 0):

        #Rotation matrices
        identity = np.array([[1,0],
                             [0,1]])
        left = np.array([[0, -1],
                        [1, 0]])
        half = np.array([[-1,0],
                        [0,-1]])
        right = np.array([[0,1],
                          [-1,0]])
        
        #Allow for easier access to the matrices through integers
        rotation_dict = {0: identity, 1: right, 2: half, 3: left}
        
        new_coord = []
        for point in self.default_coord:
            new_point = np.dot(rotation_dict[turn],point-self.center)+self.center
            new_coord.append(new_point)
        return new_coord
    

    
    #dictionary of all rotations of a block
    def gen_rotation_dict(self):
        for i in range(4):
            self.rotation_dict[i] = self.rotate(i)  

    def show_block(self, turn, x, y):
        for i,j in self.rotation_dict[turn]:
            rect = pygame.Rect(x+(i*self.block_size),600 - (y+(j*self.block_size)), self.block_size, self.block_size)
            pygame.draw.rect(screen, self.color_dict[self.color], rect, 0)


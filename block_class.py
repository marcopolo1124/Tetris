import numpy as np
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))



class Block:
    ghost_surface = pygame.Surface((800,600))
    ghost_surface.set_alpha(128)
    alpha = 175
    color_dict = {'B': (0,255,255),'D':(0,0,255),'O':(255,127,0),'P':(128,0,128),'Y':(255,255,0),'G':(0,255,0),'R':(255,0,0)}
    ghost_color_dict = {'B': (0,255,255,alpha),'D':(0,0,255,alpha),'O':(255,127,0,alpha),'P':(128,0,128,alpha),'Y':(255,255,0,alpha),'G':(0,255,0,alpha),'R':(255,0,0,alpha)}
    
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

    def show_block(self, turn, x, y, surface = screen):
        for i,j in self.rotation_dict[turn]:
            rect = pygame.Rect(x+(i*self.block_size),600 - (y+(j*self.block_size)), self.block_size, self.block_size)
            pygame.draw.rect(surface, self.color_dict[self.color], rect, 0)

    def show_ghost(self, turn, x, y, surface):
        for i,j in self.rotation_dict[turn]:
            rect_ghost = pygame.Rect(x+(i*self.block_size),600 - (y+(j*self.block_size)), self.block_size, self.block_size)
            pygame.draw.rect(surface,self.ghost_color_dict[self.color], rect_ghost, 0)

I = Block((1.5,1.5), 'B', [[0,2], [1,2], [2,2], [3,2]])
J = Block((1,1), 'D', [[0,1], [1,1], [2,1], [0,2]])
L = Block((1,1), 'O', [[0,1], [1,1], [2,1], [2,2]])
T = Block((1,1), 'P', [[0,1], [1,1], [2,1], [1,2 ]])
O = Block((1.5,1.5),     'Y', [[1,1], [2,1], [1,2], [2,2]])
S = Block((1,1), 'G', [[0,1], [1,1], [1,2], [2,2]])
Z = Block((1,1), 'R', [[1,1], [2,1], [0 ,2], [1,2]])

block_list = [I,J,L,T,O,S,Z]

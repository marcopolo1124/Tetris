import numpy as np
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
class Block:
    
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

            
    #Shows the blocks in a physical format. Can be further used
    def list_representation(self, turn):
        arr = [[' ' for i in range(4)] for j in range(4)]
        for i,j in self.rotation_dict[turn]:
            arr[int(j)][int(i)] = self.color

        for i in range(3,-1,-1):
            print(arr[i])
        return arr

    def show_block(self, turn, x, y):
        for i,j in self.rotation_dict[turn]:
            screen.blit(self.block_skin, (x+(i*20),600 - (y+(j*20))))

    def show_all(self):
        for i in range(4):
            self.list_representation(i)
            print(' ')


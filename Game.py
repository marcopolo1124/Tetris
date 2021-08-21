import pygame
from menu import *
from grid_class import PlayArea
from block_class import block_list

class Game():
#-------------------------Initialization-------------------------------------
    def __init__(self, das, arr, alpha, soft_drop):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.PAUSE, self.LEFT_KEY, self.RIGHT_KEY= False,False,False,False,False, False, False
        #Diplays
        self.DISPLAY_W, self.DISPLAY_H = 800, 600
        self.ALPHA = alpha
        # self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.ghost_surface = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H), pygame.SRCALPHA)
        self.ghost_surface.set_alpha(self.ALPHA)
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        #Fonts
        self.font_name = 'DaysLater.ttf'
        self.BLACK, self.WHITE = (0,0,0) , (255,255,255)

        self.soft_drop = soft_drop
        self.das = das
        self.arr = arr
        self.grid = PlayArea(block_list = block_list, DAS = self.das, ARR = self.arr, soft_drop = self.soft_drop ,gravity =50, lock_time = 100, screen = self.window, ghost_surface=self.ghost_surface)

        self.main_menu = MainMenu(self)
        self.pause_menu = PauseMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.pause_options_menu = PauseOptionsMenu(self)
        self.pause_credits_menu = PauseCreditsMenu(self)
        self.curr_menu = self.main_menu

#-------------------------Game loop------------------------------------------
    def game_loop(self):
        while self.playing:

            self.window.fill(self.BLACK)
            self.ghost_surface.fill((0,0,0,0))

            self.grid.execute()
            self.grid.draw()
            self.window.blit(self.ghost_surface, (0,0))
            self.draw_text('Lines Cleared: '+ str(self.grid.lines_cleared), size = 32, x= 500, y = 100)
            self.check_events()
            #When start key is pressed, stop playing
            if self.START_KEY:
                self.curr_menu = self.main_menu
                self.grid.reset()
                self.playing = False

            if self.PAUSE:
                self.curr_menu = self.pause_menu
                self.playing = False


            if self.grid.game_over():
                self.draw_text('GAME OVER', 30, 200, 300)
            self.grid.space = False
            self.reset_keys()
            pygame.display.update()
#-------------------------User input-----------------------------------------
    def check_events(self):
        for event in pygame.event.get():
            #QUIT
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            #UNIVERSAL
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pygame.K_p:
                    self.PAUSE = True
            #MENU ONLY KEYDOWN
            if event.type == pygame.KEYDOWN and self.curr_menu.run_display:
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True

            #PLAYING ONLY KEYDOWN
            if event.type == pygame.KEYDOWN and self.playing:
                if event.key == pygame.K_x or event.key == pygame.K_UP: 
                    self.grid.turn_block(1)
                if event.key == pygame.K_z:
                    self.grid.turn_block(-1)

                if event.key == pygame.K_LEFT:
                    self.grid.left_key_press()
                    self.grid.move_side()

                if event.key == pygame.K_RIGHT:
                    self.grid.right_key_press()
                    self.grid.move_side()

                if event.key == pygame.K_SPACE:
                    self.grid.space_press()
                
                if event.key == pygame.K_DOWN:
                    self.grid.key_down_press()

                if event.key == pygame.K_c:
                    self.grid.hold()

                if event.key == pygame.K_r:
                    self.grid.reset()


            #PLAYING ONLY KEYUP
            if event.type == pygame.KEYUP and self.playing:
                if event.key == pygame.K_LEFT:
                    self.grid.left_key_release()

                if event.key == pygame.K_RIGHT:
                    self.grid.right_key_release()
                if event.key == pygame.K_DOWN:
                    self.grid.key_down_release()


            self.options_menu.check_text_input(event)
            self.pause_options_menu.check_text_input(event)
#-------------------------Reset key------------------------------------------
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.PAUSE,self.LEFT_KEY, self.RIGHT_KEY = False,False,False,False,False,False,False
#-------------------------Misc.----------------------------------------------
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = x,y
        self.window.blit(text_surface, text_rect)
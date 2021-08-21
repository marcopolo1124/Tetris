import pygame

class Menu():
#-----------------Initialization----------------------------------
    def __init__(self,game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.offset = -100
#-----------------Show cursor and screen--------------------------
    def draw_cursor(self):
        self.game.draw_text('*', 15,self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.window, (0,0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
#-----------------Initialization----------------------------------
    def __init__(self,game):
        Menu.__init__(self, game)
        self.index = 0
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.state_dict = {0:["Start", self.startx, self.starty], 1:["Options",self.optionsx, self.optionsy], 2:["Credits",self.creditsx, self.creditsy]}
#-----------------Show main menu----------------------------------
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.window.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            for state in self.state_dict.values():
                self.game.draw_text(state[0], 20, state[1], state[2])
            self.draw_cursor()
            self.blit_screen()
#-----------------Move cursor(up and down)------------------------
    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.index+=1
            self.index%=len(self.state_dict.keys())
                 

        elif self.game.UP_KEY:
            self.index-=1
            self.index%=len(self.state_dict.keys())
        
        self.state = self.state_dict[self.index][0]
        self.cursor_rect.midtop = (self.state_dict[self.index][1] + self.offset, self.state_dict[self.index][2])
#-----------------Check user input--------------------------------
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options_menu
                self.game.options_menu.update()
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits_menu
            self.run_display = False

class PauseMenu(Menu):
#-----------------Initialization----------------------------------
    def __init__(self, game):
        Menu.__init__(self, game)
        self.offset = -50
        self.index = 0
        self.state = 'Reset'
        self.continuex, self.continuey = self.mid_w - 150, self.mid_h
        self.optionsx, self.optionsy = self.mid_w, self.mid_h
        self.creditsx, self.creditsy = self.mid_w + 150, self.mid_h
        self.cursor_rect.midtop = (self.continuex + self.offset, self.continuey)
        self.state_dict = {0:['Continue', self.continuex, self.continuey], 1:['Options', self.optionsx, self.optionsy], 2:['Credits', self.creditsx, self.creditsy]}
#-----------------Show Pause screen-------------------------------
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.window.fill(self.game.BLACK)
            self.game.draw_text('PAUSED', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -50)
            for state in self.state_dict.values():
                self.game.draw_text(state[0], 20, state[1], state[2])
            self.draw_cursor()
            self.blit_screen()
#-----------------Move cursor(left and right)---------------------
    def move_cursor(self):
        if self.game.RIGHT_KEY:
            self.index+=1
            self.index%=len(self.state_dict.keys())
                 

        elif self.game.LEFT_KEY:
            self.index-=1
            self.index%=len(self.state_dict.keys())
        
        self.state = self.state_dict[self.index][0]
        self.cursor_rect.midtop = (self.state_dict[self.index][1] + self.offset, self.state_dict[self.index][2])
#-----------------Check user input--------------------------------
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Continue':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.pause_options_menu
                self.game.pause_options_menu.update()
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.pause_credits_menu
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.index = 0
        self.state = 'DAS'
        self.das_str = str(game.grid.DAS)
        self.arr_str = str(game.grid.ARR)
        self.alpha_str = str(game.ALPHA)
        self.dasx, self.dasy = self.mid_w - 50, self.mid_h+40
        self.arrx, self.arry = self.mid_w - 50, self.mid_h + 60
        self.alphax, self.alphay = self.mid_w - 50, self.mid_h + 80
        self.cursor_rect.midtop = (self.dasx+self.offset,self.dasy)
        self.state_dict = {0:['DAS', self.dasx, self.dasy], 1:['ARR', self.arrx, self.arry], 2:['Ghost', self.alphax, self.alphay]}
    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.window.fill(self.game.BLACK)
            self.game.draw_text('Options', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            for state in self.state_dict.values():
                self.game.draw_text(state[0], 20, state[1], state[2])
            self.game.draw_text(self.das_str, 20, self.mid_w, self.mid_h+40)
            self.game.draw_text(self.arr_str, 20, self.mid_w, self.mid_h+60)
            self.game.draw_text(self.alpha_str, 20, self.mid_w, self.mid_h+80)
            if self.das_str == '':
                self.game.grid.DAS = 0
            else:
                self.game.grid.DAS = int(self.das_str)
            if self.arr_str == '':
                self.game.grid.ARR=0
            else:
                self.game.grid.ARR = int(self.arr_str)
            if self.alpha_str == '':
                self.game.ALPHA = 0
                self.game.ghost_surface.set_alpha(0)
            else:
                self.game.ALPHA = int(self.alpha_str)
                self.game.ghost_surface.set_alpha(self.game.ALPHA)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        self.move_cursor()

        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False


    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.index+=1
            self.index%=len(self.state_dict.keys())
                 

        elif self.game.UP_KEY:
            self.index-=1
            self.index%=len(self.state_dict.keys())
        
        self.state = self.state_dict[self.index][0]
        self.cursor_rect.midtop = (self.state_dict[self.index][1] + self.offset, self.state_dict[self.index][2])

    def check_text_input(self, event):
        if self.run_display:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    if self.state == 'DAS':
                        self.das_str += str(0)
                    elif self.state == 'ARR':
                        self.arr_str += str(0)
                    elif self.state == 'Ghost':
                        self.alpha_str += str(0)
                if event.key == pygame.K_1:
                    if self.state == 'DAS':
                        self.das_str += str(1)
                    elif self.state == 'ARR':
                        self.arr_str += str(1)
                    elif self.state == 'Ghost':
                        self.alpha_str += str(1)
                if event.key == pygame.K_2:
                    if self.state == 'DAS':
                        self.das_str += str(2)
                    elif self.state == 'ARR':
                        self.arr_str += str(2)
                    elif self.state == 'Ghost':
                        self.alpha_str += str(2)
                if event.key == pygame.K_3:
                    if self.state == 'DAS':
                        self.das_str += str(3)
                    elif self.state == 'ARR':
                        self.arr_str += str(3)
                    elif self.state == 'Ghost':
                        self.alpha_str += str(3)
                if event.key == pygame.K_4:
                    if self.state == 'DAS':
                        self.das_str += str(4)
                    elif self.state == 'ARR':
                        self.arr_str += str(4)
                    elif self.state == 'Ghost':
                        self.alpha_str += str(4)
                if event.key == pygame.K_5:
                    if self.state == 'DAS':
                        self.das_str += str(5)
                    elif self.state == 'ARR':
                        self.arr_str += str(5)
                    elif self.state == 'Ghost':
                        self.alpha_str += str(5)
                if event.key == pygame.K_6:
                    if self.state == 'DAS':
                        self.das_str += str(6)
                    elif self.state == 'ARR':
                        self.arr_str += str(6)
                    elif self.state == 'Ghost':
                        self.alpha_str += str(6)

                if event.key == pygame.K_7:
                    if self.state == 'DAS':
                        self.das_str += str(7)
                    elif self.state == 'ARR':
                        self.arr_str += str(7)
                    elif self.state == 'Ghost':
                        self.alpha_str += str(7)
                if event.key == pygame.K_8:
                    if self.state == 'DAS':
                        self.das_str += str(8)
                    elif self.state == 'ARR':
                        self.arr_str += str(8)
                    elif self.state == 'Ghost':
                        self.alpha_str += str(8)
                if event.key == pygame.K_9:
                    if self.state == 'DAS':
                        self.das_str += str(9)
                    elif self.state == 'ARR':
                        self.arr_str += str(9)
                    elif self.state == 'Ghost':
                        self.alpha_str += str(9)
                

                if event.key == pygame.K_BACKSPACE:
                    if self.state == 'DAS':
                        self.das_str = self.das_str[:-1]
                    elif self.state == 'ARR':
                        self.arr_str = self.arr_str[:-1]
                    elif self.state == 'Ghost':
                        self.alpha_str = self.alpha_str[:-1]
            else:
                pass

    
    def update(self):
        if self.run_display:
            self.das_str = str(self.game.grid.DAS)
            self.arr_str = str(self.game.grid.ARR)
            self.alpha_str = str(self.game.ALPHA)


                

    
class CreditsMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.index=0

    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.window.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2-20)
            self.game.draw_text('Made by Marco', 15, self.game.DISPLAY_W/2, self.game.DISPLAY_H / 2 +10)
            self.blit_screen()

class PauseOptionsMenu(OptionsMenu):
    def check_input(self):
        self.move_cursor()

        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.pause_menu
            self.run_display = False


class PauseCreditsMenu(CreditsMenu):
    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.pause_menu
                self.run_display = False
            self.game.window.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2-20)
            self.game.draw_text('Made by Marco', 15, self.game.DISPLAY_W/2, self.game.DISPLAY_H / 2 +10)
            self.blit_screen()


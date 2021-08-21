from Game import Game

g = Game(das = 10, arr = 10, alpha = 128, soft_drop=0)

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
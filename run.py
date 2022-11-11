import math

import pygame
from entities import *
from misc_classes import *
from data_structures import *
from settings import *



#BUTTONS AND TEXT USED IN MENUS.
pacman_title_text = pygame.font.SysFont('arial', 24).render("PACMAN PLUS", True, YELLOW)
pacman_title_rect = pacman_title_text.get_rect(center=(224, 100))
play_text_button = Button(image=None, pos=(224, 200), text="Play",font=pygame.font.SysFont('arial', 24), colour=WHITE)
leaderboard_button = Button(image=None, pos=(224, 250), text="Leaderboard",font=pygame.font.SysFont('arial', 24), colour=WHITE)
exit_button = Button(image=None, pos=(224, 300), text='Exit',font=pygame.font.SysFont('arial', 24), colour=WHITE)
continue_button = Button(image=None, pos=(224, 100), text="Continue", font=pygame.font.SysFont('arial', 24),colour=WHITE)
main_menu_button = Button(image=None, pos=(224, 150), text="Main Menu", font=pygame.font.SysFont('arial', 24),colour=WHITE)
normal_button = Button(image=None, pos=(224, 150), text="Original",font=pygame.font.SysFont('arial', 24), colour=WHITE)
advanced_button = Button(image=None, pos=(224, 225), text="Advanced",font=pygame.font.SysFont('arial', 24), colour=WHITE)
pause_button = Button(image=None, pos=(175, 600), text="Paused", font=pygame.font.SysFont('arial', 24),colour=WHITE)
play_button = Button(image=None, pos=(175, 600), text="Playing", font=pygame.font.SysFont('arial', 24),colour=WHITE)
back_button = Button(pos=(26, 20), text="Back", font=pygame.font.SysFont('arial', 24), colour=YELLOW, image=None)
test_button = Button(pos=(224, 300), text="Test Generation", font=pygame.font.SysFont('arial', 24), colour=WHITE, image=None)
enter_button = Button(image=None, pos=(TOTAL_WIDTH // 2, 400), text="ENTER", font=pygame.font.SysFont('arial', 24), colour=YELLOW)
logout_button = Button(image=None, pos=(35, 15), text="Logout", font=pygame.font.SysFont('arial', 24),colour=YELLOW)
login_button = Button(image=None, pos=(35, 15), text="Login", font=pygame.font.SysFont('arial', 24), colour=YELLOW)
custom_button = Button(image=None, pos=(224, 300), text="Custom", font=pygame.font.SysFont('arial', 24), colour=WHITE)
advanced_leaderboard_button = Button(image=None, pos=(310, 100), text="Advanced", font=pygame.font.SysFont('arial', 24), colour=WHITE)
original_leaderboard_button = Button(image=None, pos=(112, 100), text="Original", font=pygame.font.SysFont('arial', 24), colour=WHITE)




class Main(object):
    def __init__(self, current_user, current_index, level, lives, db):
        pygame.init()
        pygame.display.set_caption("Normal Mode")
        self.win = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.lives = lives
        self.db = db
        self.files = ["Maps/Map1.txt", "Maps/Map2.txt"]
        self.db.current_user = current_user  #test of this works with reference to self.db.current_user without passing in the data from outside the class.
        self.db.current_index = current_index
        self.level = level
        self.frightened_timer = Timer()
        self.frightened_delay = Timer()
        self.pacman_timer = Timer()
        self.move_delay = Timer()
        self.frightened_delay = Timer()
        self.eaten_delay = Timer()
        self.flash_timer = Timer()
        self.points = 0
        self.modes = 1 #attribute purely to enter user data



    def update_entity_mode(self, ghosts, reset_mode, mode=None):  # mode is int value 1 or 2 which resets all the ghosts to chase or scatter    #ghosts take self.ghost_list in normal and advanced
        for ghost in ghosts:
            if ghost.modes['scatter'] or ghost.modes['chase']:   #method used for updating for time intervals
                if mode == "advanced":
                    ghost.reset()
                ghost.reset_mode(reset_mode)


    def draw_entities(self, pacman, ghosts, draw_pacman=True):
        if draw_pacman:
            pacman.draw(self.win)

        for ghost in ghosts:
            if self.frightened_timer.nearly_up:
                ghost.draw(self.win, ghost.sheet, frightened_nearly_up=True)
            else:
                ghost.draw(self.win, ghost.sheet, frightened_nearly_up=False)



    def draw_lives_counter(self, lives):
        if lives == 3:
            self.win.blit(pacman_lives_counter, (300, 588))
            self.win.blit(pacman_lives_counter, (275, 588))
            self.win.blit(pacman_lives_counter, (250, 588))

        elif lives == 2:
            self.win.blit(pacman_lives_counter, (275, 588))
            self.win.blit(pacman_lives_counter, (250, 588))

        elif lives == 1:
            self.win.blit(pacman_lives_counter, (250, 588))


    def game_over_screen(self, mode, score):
        score_text = standard_font.render(f"High Score: {score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(224, 300))

        if self.db.current_user != None:
            self.db.update_level(self.level)
            self.db.update_score(score)
            self.db.update_file(logged_in=True)

        self.win.fill(BLACK)
        self.win.blit(game_over_text, game_over_rect)
        self.win.blit(score_text, score_rect)
        pygame.display.update()
        pygame.time.delay(2000)
        options_menu(mode, self.db, self.level)


    def level_screen(self):
        self.win.fill(BLACK)
        big_level_text = pygame.font.SysFont('arial', 50).render(f"Level {self.level}", True, YELLOW)
        big_level_rect = big_level_text.get_rect(center=(TOTAL_WIDTH // 2, 250))
        self.win.blit(big_level_text, big_level_rect)
        pygame.display.update()
        pygame.time.delay(1000)


    def level_flash(self, current_time_ms, graph):
        colours = [GREEN, BLUE, RED, PINK, ORANGE, TEAL, WHITE]
        if self.flash_timer.is_up(current_time_ms, 500):
            del colours[colours.index(graph.maze_colour)]
            graph.maze_colour = random.choice(colours)

    def points_event(self, ghost, score, pacman, ghosts, level_text, level_rect):
        SCORE_TEXT = pygame.font.SysFont('arial', 24).render(f"Score: {score}", True,WHITE)  # DYNAMIC ATTRIBUTES, SCORE VARIABLE AND LIVES VARIABLE UPDATE WITHIN THE MAIN GAME LOOP SO STORED HERE
        SCORE_RECT = SCORE_TEXT.get_rect(center=(55, 600))
        self.draw_entities(pacman, ghosts, False)
        WIN.blit(level_text, level_rect)
        self.draw_lives_counter(self.lives)
        self.win.blit(SCORE_TEXT, SCORE_RECT)
        ghost.draw_points(self.win, self.points)

        pygame.display.update()
        pygame.time.delay(1500)




class GameState(object):  #class should contain all the necessary data to represent each state of the game and update everything.
    def __init__(self, frightened_counter, frightened_state, score, pacman, ghosts, graph, delay, pacman_delay, current_time, lives, mode):
        self.frightened_state = frightened_state
        self.score = score
        self.pacman = pacman
        self.ghosts = ghosts
        self.graph = graph
        self.delay = delay
        self.pacman_delay = pacman_delay
        self.current_time = current_time
        self.lives = lives
        self.mode = mode
        self.frightened_counter = frightened_counter
        self.frightened_state = False
        self.points = 0

    def update_power_pellets(self, frightened_timer, node):
        for ghost in self.ghosts:
            if not ghost.modes['eaten']:
                ghost.reset_mode(3)

            if self.mode == "advanced":
                ghost.reset()

            if ghost.modes['frightened']:
                frightened_timer.reset()

        self.frightened_counter = 0
        node.power_pellet = False
        if not self.frightened_state:
            self.frightened_state = True
        self.score += 50
        node.draw(WIN)



    def update_grid(self, frightened_timer):
        for row in self.graph.grid:
            for node in row:
                if collision(self.pacman, node):
                    if node.pellet == True:
                        node.pellet = False
                        self.score += 10
                        node.draw(WIN)

                    elif node.power_pellet == True:
                        self.update_power_pellets(frightened_timer, node)

                else:
                    node.draw(WIN)

    def update_frightened(self, ghost, frightened_timer):
        if frightened_timer.is_up(self.current_time // 1000, 5):
            self.frightened_state = False
            for ghost in self.ghosts:
                if ghost.modes['frightened']:
                    ghost.reset_mode(1)
                    if self.mode == "advanced":
                        ghost.reset()

                    elif self.mode == "custom":
                        if ghost.name in ['SuperElroy', 'Patient', 'Brainless', 'Hurricane']:
                            ghost.reset()
        else:
            ghost.frightened()


    def update_ghosts(self, frightened_timer, move_delay, path_visible):
        if self.frightened_state:
            frightened_timer.reset()

        if move_delay.is_up(self.current_time, self.delay):
            for ghost in self.ghosts:
                if not ghost.modes['frightened']:
                    if ghost.name == 'Inky':
                        ghost.update(self.pacman, self.ghosts[0])

                    elif ghost.name == "Blinky" or ghost.name == "Pinky" or ghost.name == "Clyde":
                        ghost.update(self.pacman)

                    elif ghost.name == "Brainless":
                        ghost.update(self.pacman, WIN, path_visible)

                    else:
                        ghost.update(self.pacman, WIN, self.graph.grid, path_visible)

                else:
                    self.update_frightened(ghost, frightened_timer)

    def reset_entity_positions(self):
        self.pacman.node = self.graph.get_randomised_start_pos()
        self.ghosts[0].node = self.graph.get_start_pos(1)

        if len(self.ghosts) == 2:
            self.ghosts[1].node = self.graph.get_start_pos(2)

        elif len(self.ghosts) == 3:
            self.ghosts[1].node = self.graph.get_start_pos(2)
            self.ghosts[2].node = self.graph.get_start_pos(3)

        elif len(self.ghosts) == 4:
            self.ghosts[1].node = self.graph.get_start_pos(2)
            self.ghosts[2].node = self.graph.get_start_pos(3)
            self.ghosts[3].node = self.graph.get_start_pos(4)


    def reset_entity_mode(self, ghost, reset_mode, mode):
        ghost.reset_mode(reset_mode)
        if mode == "advanced":
            ghost.reset()

        elif mode == "custom":
            if ghost.name in ['SuperElroy', 'Patient', 'Brainless', 'Hurricane']:
                ghost.reset()

    def update_frightened_collision(self, level_text, level_rect, ghost):
        self.update_frightened_counter()
        self.score += self.points
        SCORE_TEXT = pygame.font.SysFont('arial', 24).render(f"Score: {self.score}", True,
                                                             WHITE)  # DYNAMIC ATTRIBUTES, SCORE VARIABLE AND LIVES VARIABLE UPDATE WITHIN THE MAIN GAME LOOP SO STORED HERE
        SCORE_RECT = SCORE_TEXT.get_rect(center=(55, 600))

        self.graph.draw(WIN)

        for g in self.ghosts:
            g.draw(WIN, g.sheet)

        ghost.draw_points(WIN, self.points, self.graph.wall_colour)

        if self.lives == 3:
            WIN.blit(pacman_lives_counter, (300, 588))
            WIN.blit(pacman_lives_counter, (275, 588))
            WIN.blit(pacman_lives_counter, (250, 588))

        elif self.lives == 2:
            WIN.blit(pacman_lives_counter, (275, 588))
            WIN.blit(pacman_lives_counter, (250, 588))

        elif self.lives == 1:
            WIN.blit(pacman_lives_counter, (250, 588))

        WIN.blit(level_text, level_rect)
        play_button.draw(WIN)
        WIN.blit(SCORE_TEXT, SCORE_RECT)

        pygame.display.update()
        pygame.time.delay(1500)
        
        if self.mode == "advanced":
            ghost.reset()
        
        elif self.mode == "custom":
            if ghost.name in ['SuperElroy', 'Patient', 'Brainless', 'Hurricane']:
                ghost.reset()


        ghost.reset_mode(4)


    def update_collisions(self, level_text, level_rect):
        for ghost in self.ghosts:
            if ghost.collision(self.pacman.node):
                if ghost.modes['chase'] or ghost.modes['scatter']:
                    self.reset_entity_mode(ghost, 1, self.mode)
                    pygame.time.delay(1000)
                    self.lives -= 1
                    self.reset_entity_positions()
                    self.pacman.curr_direction = random.choice([RIGHT, LEFT, UP, DOWN])

                elif ghost.modes['frightened']:
                    self.update_frightened_collision(level_text, level_rect, ghost)



    def update_frightened_counter(self):
        self.frightened_counter += 1
        if self.frightened_counter == 1:
            self.points = 200
        elif self.frightened_counter == 2:
            self.points = 400
        elif self.frightened_counter == 3:
            self.points = 800
        elif self.frightened_counter == 4:
            self.points = 1600


    def update(self, pacman_timer, frightened_timer, move_delay, path_visible, level_text, level_rect, generated_maze=False):
        if pacman_timer.is_up(self.current_time, self.pacman_delay):
            self.pacman.update(generated_maze)
        self.update_ghosts(frightened_timer, move_delay, path_visible)
        self.update_collisions(level_text, level_rect)
        self.update_grid(frightened_timer)


    def get_score(self):
        return self.score

    def get_frightened_state(self):
        return self.frightened_state



class Normal(Main):
    def __init__(self, current_user, current_index, level, lives, db):
        super().__init__(current_user, current_index, level, lives, db)
        self.file = self.files[0]


    def settings(self):
        if self.level == 1:
            self.flash = False
            self.delay = 150
            self.graph = Graph(self.file, 0, 4, BLUE)
            self.pacman = Pacman(self.graph.get_randomised_start_pos())
            self.ghosts = [Blinky(self.graph.get_start_pos(2))]
            self.pacman_delay = 60

        elif self.level == 2:
            self.flash = False
            self.delay = 150
            self.graph = Graph(self.file, 0, 4, BLUE)
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [Blinky(self.graph.get_start_pos(1)), Pinky(self.graph.get_start_pos(2))]
            self.pacman_delay = 60

        elif self.level == 3:
            self.flash = False
            self.delay = 150
            self.graph = Graph(self.file, 0, 4, BLUE)
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [Blinky(self.graph.get_start_pos(1)), Pinky(self.graph.get_start_pos(2)),Clyde(self.graph.get_start_pos(3))]
            self.pacman_delay = 60

        elif self.level == 4:
            self.flash = False
            self.delay = 150
            self.graph = Graph(self.file, 0, 4, BLUE)
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [Blinky(self.graph.get_start_pos(1)), Pinky(self.graph.get_start_pos(2)),Clyde(self.graph.get_start_pos(3)),
                               Inky(self.graph.get_start_pos(4))]
            self.pacman_delay = 60

        elif self.level == 5:
            self.flash = False
            self.delay = 125
            self.graph = Graph(self.file, 0, 3, RED)
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [Blinky(self.graph.get_start_pos(1))]
            self.pacman_delay = 60

        elif self.level == 6:
            self.flash = False
            self.delay = 125
            self.graph = Graph(self.file, 0, 3, RED)
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [Blinky(self.graph.get_start_pos(1)), Pinky(self.graph.get_start_pos(2))]
            self.pacman_delay = 60

        elif self.level == 7:
            self.flash = False
            self.delay = 100
            self.graph = Graph(self.file, 0, 3, RED)
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [Blinky(self.graph.get_start_pos(1)), Pinky(self.graph.get_start_pos(2)), Clyde(self.graph.get_start_pos(3))]
            self.pacman_delay = 60

        elif self.level == 8:
            self.flash = False
            self.delay = 90
            self.graph = Graph(self.file, 0, 3, GREEN)
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [Blinky(self.graph.get_start_pos(1)), Pinky(self.graph.get_start_pos(2)), Clyde(self.graph.get_start_pos(3)),
                               Inky(self.graph.get_start_pos(4))]
            self.pacman_delay = 60

        elif self.level == 9:
            self.flash = True
            self.delay = 90
            self.graph = Graph(self.file, 0, 2, BLUE)
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [Blinky(self.graph.get_start_pos(1)), Pinky(self.graph.get_start_pos(2)), Clyde(self.graph.get_start_pos(3)),
                               Inky(self.graph.get_start_pos(4))]
            self.pacman_delay = 60

        elif self.level == 10:
            self.flash = True
            self.delay = 80
            self.graph = Graph(self.file, 0, 1, BLUE)
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [Blinky(self.graph.get_start_pos(1)), Pinky(self.graph.get_start_pos(2)), Clyde(self.graph.get_start_pos(3)),
                               Inky(self.graph.get_start_pos(4))]
            self.pacman_delay = 60

    def update_modes_by_time(self, current_time_s):
        if self.level == 1:
            if current_time_s <= 5:
                self.update_entity_mode(self.ghosts, 2)

            elif 5 < current_time_s <= 25:
                self.update_entity_mode(self.ghosts, 1)

            elif 25 < current_time_s <= 30:
                self.update_entity_mode(self.ghosts, 2)

            elif 30 < current_time_s <= 50:
                self.update_entity_mode(self.ghosts, 1)

            elif 50 < current_time_s <= 55:
                self.update_entity_mode(self.ghosts, 2)

            elif 55 < current_time_s <= 75:
                self.update_entity_mode(self.ghosts, 1)

            elif 75 < current_time_s <= 80:
                self.update_entity_mode(self.ghosts, 2)

            else:
                self.update_entity_mode(self.ghosts, 1)


        elif 2 <= self.level <= 4:
            if current_time_s <= 5:
                self.update_entity_mode(self.ghosts, 2)

            elif 5 < current_time_s <= 25:
                self.update_entity_mode(self.ghosts, 1)

            elif 25 < current_time_s <= 30:
                self.update_entity_mode(self.ghosts, 2)

            elif 30 < current_time_s <= 50:
                self.update_entity_mode(self.ghosts, 1)

            elif 50 < current_time_s <= 55:
                self.update_entity_mode(self.ghosts, 2)

            elif 55 < current_time_s <= 955:
                self.update_entity_mode(self.ghosts, 1)

            elif 955 < current_time_s <= 957:
                self.update_entity_mode(self.ghosts, 2)

            else:
                self.update_entity_mode(self.ghosts, 1)

        elif self.level > 4:
            if current_time_s <= 5:
                self.update_entity_mode(self.ghosts, 2)

            elif 5 < current_time_s <= 25:
                self.update_entity_mode(self.ghosts, 1)

            elif 25 < current_time_s <= 30:
                self.update_entity_mode(self.ghosts, 2)

            elif 30 < current_time_s <= 50:
                self.update_entity_mode(self.ghosts, 1)

            elif 50 < current_time_s <= 55:
                self.update_entity_mode(self.ghosts, 2)

            elif 55 < current_time_s <= 1255:
                self.update_entity_mode(self.ghosts, 1)

            elif 1255 < current_time_s <= 1256:
                self.update_entity_mode(self.ghosts, 2)

            else:
                self.update_entity_mode(self.ghosts, 1)



    def level_up(self):
        self.level += 1
        self.frightened_counter = 0
        self.lives = 3
        if self.db.current_user != None:
            self.db.update_level(self.level)

        self.level_screen()
        self.run()

    def draw(self, score, level_text, level_rect, playing=True, draw_pacman=True):
        WIN.fill(BLACK)
        self.graph.draw(WIN)
        self.draw_entities(self.pacman, self.ghosts, draw_pacman)
        SCORE_TEXT = pygame.font.SysFont('arial', 24).render(f"Score: {score}", True,WHITE)  # DYNAMIC ATTRIBUTES, SCORE VARIABLE AND LIVES VARIABLE UPDATE WITHIN THE MAIN GAME LOOP SO STORED HERE
        SCORE_RECT = SCORE_TEXT.get_rect(center=(55, 600))
        WIN.blit(level_text, level_rect)
        self.draw_lives_counter(self.lives)
        WIN.blit(SCORE_TEXT, SCORE_RECT)
        if playing:
            play_button.draw(self.win)
        else:
            pause_button.draw(self.win)

        pygame.display.update()



    def run(self):
        self.win.fill(BLACK)  # fills the window with black on each run of the loop to refresh lives and scores counter
        LEVEL_TEXT = pygame.font.SysFont('arial', 24).render(f"Level {self.level}", True, WHITE)
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(400, 600))

        self.settings()

        self.graph.draw(self.win)  # displays ready on the screen for 1 second, everything is drawn and updated
        self.draw_entities(self.pacman, self.ghosts)
        pygame.display.update()
        pygame.time.delay(1000)
        self.win.blit(ready_text, ready_rect)
        pygame.display.update()

        self.win.fill(BLACK)

        pygame.time.delay(1000)
        self.graph.draw(self.win)  # displays go on the screen for 1 second, everything on the screen is redrawn and reupdated.
        self.draw_entities(self.pacman, self.ghosts)
        self.win.blit(go_text, go_rect)
        pygame.display.update()
        pygame.time.delay(500)

        score = 0
        frightened_state = False
        frightened_counter = 0

        while True:
            self.win.fill(BLACK)
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_hovering(pygame.mouse.get_pos()):
                        paused = True
                        while paused:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()

                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if pause_button.is_hovering(pygame.mouse.get_pos()):
                                        paused = False

                            self.draw(score, LEVEL_TEXT, LEVEL_RECT, playing=False)


            if self.lives == 0:  # DISPLAY EXIT, MAIN MENU AND CONTINUE (CONTINUE RESTARTS THE CURRENT LEVEL)
                self.game_over_screen("normal", score)

            if self.graph.is_complete():
                self.level_up()

            self.update_modes_by_time(current_time // 1000)
            self.clock.tick(60)

            g = GameState(frightened_counter, frightened_state, score, self.pacman, self.ghosts, self.graph, self.delay, self.pacman_delay, current_time, self.lives, "normal")
            g.update(self.pacman_timer, self.frightened_timer, self.move_delay, False, LEVEL_TEXT, LEVEL_RECT)
            score, frightened_state = g.get_score(), g.get_frightened_state() #COULD CALL ATTRIBUTES DIRECTLY BUT I BELIEVE THIS IS BAD PRACTICE
            self.lives = g.lives
            frightened_counter = g.frightened_counter

            if self.flash:
                self.level_flash(current_time, self.graph)

            if self.db.current_user != None:
                self.db.update_score(score)

            self.draw(score, LEVEL_TEXT, LEVEL_RECT)
            pygame.display.update()


class Advanced(Main):
    def __init__(self, current_user, current_index, level, lives, db, generated=False):
        super().__init__(current_user, current_index, level, lives, db)
        self.generated = generated
        self.file = self.files[0]
        pygame.display.set_caption("Advanced Mode")

    def settings(self):
        if self.level == 1:
            self.flash = False
            self.delay = 75
            self.graph = Graph(self.file, 0, 4, BLUE, self.generated)
            self.pacman = Pacman(self.graph.get_randomised_start_pos())
            self.ghosts = [Brainless(PURPLE, self.graph.get_start_pos(1))]
            self.pacman_delay = 60

        elif self.level == 2:
            self.flash = False
            self.delay = 75
            self.graph = Graph(self.file, 0, 4, BLUE)
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [SuperElroy(LIGHT_GREEN, self.graph.get_start_pos(2)), Brainless(PURPLE, self.graph.get_start_pos(1))]
            self.pacman_delay = 60

        elif self.level == 3:
            self.flash = False
            self.delay = 75
            self.graph = Graph(self.file, 0, 4, BLUE)
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [SuperElroy(LIGHT_GREEN, self.graph.get_start_pos(2)),Brainless(PURPLE, self.graph.get_start_pos(1)),
                               Patient(YELLOW, self.graph.get_start_pos(3))]
            self.pacman_delay = 60

        elif self.level == 4:
            self.flash = False
            self.delay = 75
            self.graph = Graph(self.file, 0, 4, BLUE)
            self.super_elroy = SuperElroy(LIGHT_GREEN, self.graph.get_start_pos(2))
            self.brainless = Brainless(PURPLE, self.graph.get_start_pos(1))
            self.patient = Patient(YELLOW, self.graph.get_start_pos(3))
            self.hurricane = Hurricane(GREY, self.graph.get_start_pos(4))
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [self.hurricane, self.super_elroy, self.patient, self.brainless]
            self.pacman_delay = 60

        elif self.level == 5:
            self.flash = False
            self.delay = 65
            self.graph = Graph(self.file, 0 , 3, RED)
            self.brainless = Brainless(PURPLE, self.graph.get_start_pos(1))
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [self.brainless]
            self.pacman_delay = 60

        elif self.level == 6:
            self.flash = False
            self.delay = 65
            self.graph = Graph(self.file, 0, 3, RED)
            self.super_elroy = SuperElroy(LIGHT_GREEN, self.graph.get_start_pos(2))
            self.brainless = Brainless(PURPLE, self.graph.get_start_pos(1))
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [self.super_elroy, self.brainless]
            self.pacman_delay = 60

        elif self.level == 7:
            self.flash = False
            self.delay = 65
            self.graph = Graph(self.file, 0, 3, RED)
            self.super_elroy = SuperElroy(LIGHT_GREEN, self.graph.get_start_pos(2))
            self.brainless = Brainless(PURPLE, self.graph.get_start_pos(1),)
            self.patient = Patient(YELLOW, self.graph.get_start_pos(3))
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [self.super_elroy, self.brainless, self.patient]
            self.pacman_delay = 60

        elif self.level == 8:
            self.flash = False
            self.delay = 65
            self.graph = Graph(self.file, 0, 3, BLUE)
            self.super_elroy = SuperElroy(LIGHT_GREEN, self.graph.get_start_pos(2))
            self.brainless = Brainless(PURPLE, self.graph.get_start_pos(1))
            self.patient = Patient(YELLOW, self.graph.get_start_pos(3))
            self.hurricane = Hurricane(GREY, self.graph.get_start_pos(4))
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [self.hurricane, self.super_elroy, self.patient, self.brainless]
            self.pacman_delay = 60

        elif self.level == 9:
            self.flash = True
            self.delay = 65
            self.graph = Graph(self.file, 0, 2, BLUE)
            self.super_elroy = SuperElroy(LIGHT_GREEN, self.graph.get_start_pos(2))
            self.brainless = Brainless(PURPLE, self.graph.get_start_pos(1))
            self.patient = Patient(YELLOW, self.graph.get_start_pos(3))
            self.hurricane = Hurricane(GREY, self.graph.get_start_pos(4))
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [self.hurricane, self.super_elroy, self.patient, self.brainless]
            self.pacman_delay = 60

        elif self.level == 10:
            self.flash = True
            self.delay = 55
            self.graph = Graph(self.file, 0, 1, BLUE)
            self.super_elroy = SuperElroy(LIGHT_GREEN, self.graph.get_start_pos(2))
            self.brainless = Brainless(PURPLE, self.graph.get_start_pos(1))
            self.patient = Patient(YELLOW, self.graph.get_start_pos(3))
            self.hurricane = Hurricane(GREY, self.graph.get_start_pos(4))
            self.pacman = Pacman(self.graph.get_start_pos(0))
            self.ghosts = [self.hurricane, self.super_elroy, self.patient, self.brainless]
            self.pacman_delay = 60


    def level_up(self):
        self.level += 1
        self.frightened_counter = 0
        self.lives = 3
        if self.db.current_user != None:
            self.db.update_level(self.level)

        self.level_screen()
        pygame.time.delay(1000)
        self.run()

    def draw(self, score, level_text, level_rect, playing=True, draw_pacman=True):
        WIN.fill(BLACK)
        self.graph.draw(WIN)
        self.draw_entities(self.pacman, self.ghosts, draw_pacman)
        SCORE_TEXT = pygame.font.SysFont('arial', 24).render(f"Score: {score}", True,WHITE)  # DYNAMIC ATTRIBUTES, SCORE VARIABLE AND LIVES VARIABLE UPDATE WITHIN THE MAIN GAME LOOP SO STORED HERE
        SCORE_RECT = SCORE_TEXT.get_rect(center=(55, 600))
        WIN.blit(level_text, level_rect)
        self.draw_lives_counter(self.lives)
        WIN.blit(SCORE_TEXT, SCORE_RECT)
        self.toggle_visibility_button.draw(self.win)
        if playing:
            play_button.draw(self.win)
        else:
            pause_button.draw(self.win)

        pygame.display.update()


    def run(self):
        self.win.fill(BLACK)
        LEVEL_TEXT = pygame.font.SysFont('arial', 24).render(f"Level {self.level}", True, WHITE)
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(400, 600))

        self.settings()

        self.graph.draw(self.win)
        self.draw_entities(self.pacman, self.ghosts)
        pygame.display.update()
        pygame.time.delay(1000)
        self.win.blit(ready_text, ready_rect)
        pygame.display.update()

        self.win.fill(BLACK)

        pygame.time.delay(1000)
        self.graph.draw(self.win)  # displays go on the screen for 1 second, everything on the screen is redrawn and reupdated.
        self.draw_entities(self.pacman, self.ghosts)
        self.win.blit(go_text, go_rect)
        pygame.display.update()
        pygame.time.delay(500)

        path_visible = False
        button_text = None

        score = 0
        frightened_state = False
        frightened_counter = 0

        while True:
            if path_visible == False:
                button_text = "OFF"

            elif path_visible == True:
                button_text = "ON"

            self.toggle_visibility_button = Button(image=None, pos=(75, 25), text=f"Visibility: {button_text}",font=pygame.font.SysFont('arial', 24), colour=WHITE)
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.toggle_visibility_button.is_hovering(pygame.mouse.get_pos()):
                        if not path_visible:
                            path_visible = True
                        else:
                            path_visible = False

                    if play_button.is_hovering(pygame.mouse.get_pos()):
                        paused = True
                        while paused:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()

                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if pause_button.is_hovering(pygame.mouse.get_pos()):
                                        paused = False

                            self.draw(score, LEVEL_TEXT, LEVEL_RECT, playing=False)

            if self.lives == 0:  # DISPLAY EXIT, MAIN MENU AND CONTINUE (CONTINUE RESTARTS THE CURRENT LEVEL)
                self.game_over_screen("advanced", score)

            if self.graph.is_complete():
                self.level_up()

            if current_time // 1000 <= 5:
                self.update_entity_mode(self.ghosts, 2, "advanced")  # only resets the path if mode is switched to scatter

            else:
                self.update_entity_mode(self.ghosts, 1)

            self.win.fill(BLACK)
            self.clock.tick(60)

            g = GameState(frightened_counter, frightened_state, score, self.pacman, self.ghosts, self.graph, self.delay, self.pacman_delay, current_time, self.lives, "advanced")
            g.update(self.pacman_timer, self.frightened_timer, self.move_delay, path_visible, LEVEL_TEXT, LEVEL_RECT)
            score, frightened_state = g.get_score(), g.get_frightened_state()
            frightened_counter, self.lives = g.frightened_counter, g.lives

            if self.flash:
                self.level_flash(current_time, self.graph)

            self.draw(score, LEVEL_TEXT, LEVEL_RECT)

standard_font = pygame.font.SysFont('arial' , 24)

class Custom(Main):
    def __init__(self, current_user, current_index, level, lives, db, generated=False):
        super().__init__(current_user, current_index, level, lives, db)
        self.generated = generated
        self.file = self.files[0]
        pygame.display.set_caption("Custom Mode")
        self.ghost1_text, self.ghost2_text = standard_font.render("Ghost 1:", True, YELLOW), standard_font.render("Ghost 2:", True, YELLOW)
        self.ghost1_rect, self.ghost2_rect = self.ghost1_text.get_rect(center=(50, 50)), self.ghost2_text.get_rect(center=(50, 200))
        self.pacman_speed_text, self.pellets_text, self.ghosts_speed_text = pygame.font.SysFont('arial', 18).render("PacmanSpeed: ", True, YELLOW), pygame.font.SysFont('arial', 18).render("PowerPellets: ", True, YELLOW), pygame.font.SysFont('arial', 18).render("GhostsSpeed: ", True, YELLOW)
        self.pacman_speed_rect, self.pellets_rect, self.ghosts_speed_rect = self.pacman_speed_text.get_rect(center=(50, 200)), self.pellets_text.get_rect(center=(50, 100)), self.ghosts_speed_text.get_rect(center=(50, 300))
        self.settings = {"Ghost1":"Blinky", "Ghost2":'Blinky', "Ghost3":'Blinky', "Ghost4":'Blinky', "Powerpellets":0, "PacmanSpeed":0, "GhostsSpeed":0} #default settings.
        self.pellets_slider = Slider()
        self.pacman_speed_slider = Slider(100, 195, 250, 185)
        self.ghosts_speed_slider = Slider(100, 295, 250, 285)
        self.ghost1_idx, self.ghost2_idx, self.ghost3_idx, self.ghost4_idx = 0, 0, 0, 0



    def draw(self, score, level_text, level_rect, playing=True, draw_pacman=True):
        self.win.fill(BLACK)
        self.graph.draw(self.win)
        self.draw_entities(self.pacman, self.ghosts, draw_pacman)
        SCORE_TEXT = pygame.font.SysFont('arial', 24).render(f"Score: {score}", True,WHITE)  # DYNAMIC ATTRIBUTES, SCORE VARIABLE AND LIVES VARIABLE UPDATE WITHIN THE MAIN GAME LOOP SO STORED HERE
        SCORE_RECT = SCORE_TEXT.get_rect(center=(55, 600))
        self.win.blit(level_text, level_rect)
        self.toggle_visibility_button.draw(self.win)
        self.draw_lives_counter(self.lives)
        self.win.blit(SCORE_TEXT, SCORE_RECT)
        if playing:
            play_button.draw(self.win)
        else:
            pause_button.draw(self.win)

        pygame.display.update()

    def customise_menu(self):
        self.win.fill(BLACK)
        run_button = Button(image=None, pos=(224, 600), text="RUN", font=standard_font, colour=GREEN)
        ghosts_text = pygame.font.SysFont('arial', 18).render("Ghosts: ", True, YELLOW)
        ghosts_rect = ghosts_text.get_rect(center=(30, 400))
        high1_text, high2_text = pygame.font.SysFont('arial', 10).render("HIGH", True, YELLOW), pygame.font.SysFont('arial', 10).render("HIGH", True, YELLOW)
        high1_rect, high2_rect = high1_text.get_rect(center=(100, 175)), high2_text.get_rect(center=(100, 275))
        low1_text, low2_text = pygame.font.SysFont('arial', 10).render("LOW", True, YELLOW), pygame.font.SysFont('arial', 10).render("LOW", True, YELLOW)
        low1_rect, low2_rect = low1_text.get_rect(center=(400, 175)), low2_text.get_rect(center=(400, 275))
        map_button = Button(image=None, pos=(224, 500), text="Customise Map", font=standard_font, colour=YELLOW)
        ghosts = ['Blinky', 'Pinky', 'Inky', 'Clyde', 'SuperElroy', 'Brainless', 'Patient', 'Hurricane', 'None']


        while True:
            self.win.fill(BLACK)
            pellets_value = int(self.pellets_slider.get_setting_value(scale=100))
            pacman_speed_value = int(self.pacman_speed_slider.get_setting_value(scale=10))
            ghosts_speed_value = int(self.ghosts_speed_slider.get_setting_value(scale=10))
            pellets_value_text = standard_font.render(f"{pellets_value}", True, RED)
            pacman_speed_value_text = standard_font.render(f"{pacman_speed_value}", True, RED)
            ghosts_speed_value_text = standard_font.render(f"{ghosts_speed_value}", True, RED)
            pellets_value_rect = pellets_value_text.get_rect(center=(425, 100))
            pacman_speed_value_rect = pacman_speed_value_text.get_rect(center=(425, 200))
            ghosts_speed_value_rect = ghosts_speed_value_text.get_rect(center=(425, 300))
            ghost1_button = Button(image=None, pos=(100, 400), text=f"{self.settings['Ghost1']}", font=pygame.font.SysFont('arial', 22),colour=WHITE)
            ghost2_button = Button(image=None, pos=(200, 400), text=f"{self.settings['Ghost2']}", font=pygame.font.SysFont('arial', 22),colour=WHITE)
            ghost3_button = Button(image=None, pos=(300, 400), text=f"{self.settings['Ghost3']}", font=pygame.font.SysFont('arial', 22),colour=WHITE)
            ghost4_button = Button(image=None, pos=(400, 400), text=f"{self.settings['Ghost4']}", font=pygame.font.SysFont('arial', 22),colour=WHITE)



            m_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if m_pos[0] in range(self.pellets_slider.rect.left, self.pellets_slider.rect.right) and m_pos[1] in range(self.pellets_slider.rect.top, self.pellets_slider.rect.bottom):
                        self.move_slider(self.pellets_text, self.pellets_rect, self.pellets_slider, 100, 425, 100)

                    if m_pos[0] in range(self.pacman_speed_slider.rect.left, self.pacman_speed_slider.rect.right) and m_pos[1] in range(self.pacman_speed_slider.rect.top, self.pacman_speed_slider.rect.bottom):
                        self.move_slider(self.pacman_speed_text, self.pacman_speed_rect, self.pacman_speed_slider, 10, 425, 200)

                    if m_pos[0] in range(self.ghosts_speed_slider.rect.left, self.ghosts_speed_slider.rect.right) and m_pos[1] in range(self.ghosts_speed_slider.rect.top, self.ghosts_speed_slider.rect.bottom):
                        self.move_slider(self.ghosts_speed_text, self.ghosts_speed_rect, self.ghosts_speed_slider, 10, 425, 300)

                    if ghost1_button.is_hovering(m_pos):
                        self.customise_ghost('Ghost1', self.ghost1_idx, ghosts)

                    if ghost2_button.is_hovering(m_pos):
                        self.customise_ghost("Ghost2", self.ghost2_idx, ghosts)

                    if ghost3_button.is_hovering(m_pos):
                        self.customise_ghost("Ghost3", self.ghost3_idx, ghosts)

                    if ghost4_button.is_hovering(m_pos):
                        self.customise_ghost("Ghost4", self.ghost4_idx, ghosts)


                    if run_button.is_hovering(m_pos):
                        self.settings['Powerpellets'] = pellets_value
                        self.settings['PacmanSpeed'] = pacman_speed_value
                        self.settings['GhostsSpeed'] = ghosts_speed_value
                        self.run()

                    if map_button.is_hovering(m_pos):
                        self.settings['Powerpellets'] = pellets_value
                        self.settings['PacmanSpeed'] = pacman_speed_value
                        self.settings['GhostsSpeed'] = ghosts_speed_value
                        self.customise_map()

                    if back_button.is_hovering(m_pos):
                        mode_menu(self.db, 1)


            self.pellets_slider.draw()
            self.ghosts_speed_slider.draw()
            self.pacman_speed_slider.draw()
            run_button.draw(self.win)
            map_button.draw(self.win)
            ghost1_button.draw(self.win)
            ghost2_button.draw(self.win)
            ghost3_button.draw(self.win)
            ghost4_button.draw(self.win)
            self.win.blit(pellets_value_text, pellets_value_rect)
            self.win.blit(self.pellets_text, self.pellets_rect)
            self.win.blit(pacman_speed_value_text, pacman_speed_value_rect)
            self.win.blit(self.pacman_speed_text, self.pacman_speed_rect)
            self.win.blit(ghosts_speed_value_text, ghosts_speed_value_rect)
            self.win.blit(self.ghosts_speed_text, self.ghosts_speed_rect)
            self.win.blit(ghosts_text, ghosts_rect)
            self.win.blit(high1_text, high1_rect)
            self.win.blit(high2_text, high2_rect)
            self.win.blit(low1_text,low1_rect)
            self.win.blit(low1_text, low2_rect)
            back_button.draw(self.win)
            pygame.display.update()


    def customise_ghost(self, ghost, ghost_idx, ghosts):  #CUSTOMISE (NO OF GHOSTS, GHOST SPEED, GHOST ALGORITHM, GHOST SEARCH DEPTH, PACMAN SPEED) AS SLIDERS (NEED TO CREATE THE SLIDERS)    #RETURN DICTIONARY OF GHOSTS AND SETTINGS
        if ghost_idx < len(ghosts) - 1:
            print("here")
            ghost_idx += 1

        else:
            ghost_idx = 0


        self.settings[ghost] = ghosts[ghost_idx]
        if ghost == "Ghost1":
            self.ghost1_idx = ghost_idx
        elif ghost == "Ghost2":
            self.ghost2_idx = ghost_idx
        elif ghost == "Ghost3":
            self.ghost3_idx = ghost_idx
        elif ghost == "Ghost4":
            self.ghost4_idx = ghost_idx



    def move_slider(self, category_text, category_rect, slider, scale, value_x, value_y):
        self.win.fill(BLACK)
        while True:
            value = int(slider.get_setting_value(scale))
            value_text = standard_font.render(f"{value}",True, RED)
            value_rect = value_text.get_rect(center=(value_x, value_y))
            m_pos = pygame.mouse.get_pos()
            self.win.fill(BLACK)
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    return value


            slider.move_slider(m_pos)
            self.win.blit(category_text, category_rect)
            self.win.blit(value_text, value_rect)
            slider.draw()
            back_button.draw(self.win)
            pygame.display.update()


    def customise_map(self):
        self.graph = Graph(self.file, 0, self.settings['Powerpellets'], BLUE, True)
        self.run(custom_graph=True)

    def get_ghosts(self, ghost_names):
        ghosts = []
        for ghost_name in ghost_names:
            if ghost_name == "Blinky":
                ghosts.append(Blinky(self.graph.get_start_pos(1)))
            elif ghost_name == "Pinky":
                ghosts.append(Pinky(self.graph.get_start_pos(2)))
            elif ghost_name == "Inky":
                ghosts.append(Inky(self.graph.get_start_pos(3)))
            elif ghost_name == "Clyde":
                ghosts.append(Clyde(self.graph.get_start_pos(4)))
            elif ghost_name == "SuperElroy":
                ghosts.append(SuperElroy(LIGHT_GREEN, self.graph.get_start_pos(1)))
            elif ghost_name == "Patient":
                ghosts.append(Patient(YELLOW, self.graph.get_start_pos(2)))
            elif ghost_name == "Hurricane":
                ghosts.append(Hurricane(GREY, self.graph.get_start_pos(3)))
            elif ghost_name == "Brainless":
                ghosts.append(Brainless(PURPLE, self.graph.get_start_pos(4)))

            elif ghost_name == "None":
                continue

        return ghosts

    @staticmethod
    def convert_speed_value(value):
        delay_bound = 500
        scale = 10
        return value * (delay_bound / scale)


    def config(self, custom_graph=False):
        self.flash = False
        self.delay = self.convert_speed_value(self.settings['GhostsSpeed'])
        if not custom_graph:
            self.graph = Graph(self.file, 0, self.settings['Powerpellets'], BLUE, False)    #this will be changed later in customise_map
        self.pacman = Pacman(self.graph.get_randomised_start_pos())
        self.pacman_delay = self.convert_speed_value(self.settings['PacmanSpeed'])
        ghost_names = []
        for k, v in self.settings.items():
            if k[:5] == "Ghost":
                ghost_names.append(v)

        self.ghosts = self.get_ghosts(ghost_names)
        self.update_entity_mode(self.ghosts, 1)
        return self.ghosts

    def run(self, custom_graph=False):   #NEED TO MAKE APPROPRIATE MIGRATIONS FROM THE RUN METHOD IN ADVANCED TO UPDATE THE ADVANCED GHOSTS.
        self.win.fill(BLACK)  
        LEVEL_TEXT = pygame.font.SysFont('arial', 24).render("Custom", True, WHITE)
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(400, 600))

        self.config(custom_graph)

        self.graph.draw(self.win)  # displays ready on the screen for 1 second, everything is drawn and updated
        self.draw_entities(self.pacman, self.ghosts)
        pygame.display.update()
        pygame.time.delay(1000)
        self.win.blit(ready_text, ready_rect)
        pygame.display.update()

        self.win.fill(BLACK)

        pygame.time.delay(1000)
        self.graph.draw(self.win)  # displays go on the screen for 1 second, everything on the screen is redrawn and reupdated.
        self.draw_entities(self.pacman, self.ghosts)
        self.win.blit(go_text, go_rect)
        pygame.display.update()
        pygame.time.delay(500)

        score = 0
        frightened_state = False
        frightened_counter = 0
        path_visible = False
        button_text = ""

        while True:
            if path_visible == False:
                button_text = "OFF"

            elif path_visible == True:
                button_text = "ON"

            self.toggle_visibility_button = Button(image=None, pos=(75, 25), text=f"Visibility: {button_text}",font=pygame.font.SysFont('arial', 24), colour=WHITE)
            self.win.fill(BLACK)
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.toggle_visibility_button.is_hovering(pygame.mouse.get_pos()):
                        if not path_visible:
                            path_visible = True
                        else:
                            path_visible = False

                    if play_button.is_hovering(pygame.mouse.get_pos()):
                        paused = True
                        while paused:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()

                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if pause_button.is_hovering(pygame.mouse.get_pos()):
                                        paused = False

                            self.draw(score, LEVEL_TEXT, LEVEL_RECT, playing=False)

            if self.lives == 0:  # DISPLAY EXIT, MAIN MENU AND CONTINUE (CONTINUE RESTARTS THE CURRENT LEVEL)
                self.game_over_screen("custom", score)

            if self.graph.is_complete():
                print("Completed a custom game")    #Here reset to the settings page or something.

            #self.update_modes_by_time(current_time // 1000)
            self.clock.tick(60)

            g = GameState(frightened_counter, frightened_state, score, self.pacman, self.ghosts, self.graph, self.delay,self.pacman_delay, current_time, self.lives, "custom")
            g.update(self.pacman_timer, self.frightened_timer, self.move_delay, path_visible, LEVEL_TEXT, LEVEL_RECT)
            score, frightened_state = g.get_score(), g.get_frightened_state()  # COULD CALL ATTRIBUTES DIRECTLY BUT I BELIEVE THIS IS BAD PRACTICE
            self.lives = g.lives
            frightened_counter = g.frightened_counter

            if self.flash:
                self.level_flash(current_time, self.graph)

            if self.db.current_user != None:
                self.db.update_score(score)

            self.draw(score, LEVEL_TEXT, LEVEL_RECT)
            pygame.display.update()




class Slider(object):
    def __init__(self, box_left=100, box_top=95, rect_left=250, rect_top=85, box_width=300, box_height=10, rect_width=10, rect_height=30):
        self.rect = pygame.Rect(rect_left, rect_top, rect_width, rect_height)  # little rectangle which slides along the box
        self.box = pygame.Rect(box_left, box_top, box_width, box_height)  # box containing the slider

    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.box, 3)
        pygame.draw.rect(WIN, WHITE, self.rect, 20)

    def get_setting_value(self, scale):  #calculate ratio of slider_rect.left to slider_box.left then round, weight stretches the values over the slider.
        accuracy = len(str(scale)) - 1
        distance = self.rect.left - self.box.left
        if distance == 0:
            return 0
        else:
            return (round(distance / self.box.width, accuracy) * scale) // 1

    def check_slider_bounds(self):
        if self.rect.left <= self.box.left:
            self.rect.left = self.box.left

        elif self.rect.right >= self.box.right:
            self.rect.right = self.box.right


    def move_slider(self, mouse_pos):
        self.rect.left = mouse_pos[0]
        self.check_slider_bounds()





def login_menu(db):
    WIN.fill(BLACK)
    pygame.display.set_caption("Welcome")
    login_button = Button(image=None, pos=(224, 150), text="Login", font=pygame.font.SysFont('calibri', 30), colour=YELLOW)
    register_button = Button(image=None, pos=(224, 250), text="Register", font=pygame.font.SysFont('calibri', 30), colour=YELLOW)
    guest_button = Button(image=None, pos=(224, 350), text="Enter as Guest", font=pygame.font.SysFont('calibri', 30), colour=YELLOW)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.is_hovering(pygame.mouse.get_pos()):
                    login(db)

                if register_button.is_hovering(pygame.mouse.get_pos()):
                    register(db)

                if guest_button.is_hovering(pygame.mouse.get_pos()):
                    main_menu(db, 4)



        login_button.draw(WIN)
        register_button.draw(WIN)
        guest_button.draw(WIN)
        pygame.display.update()



def enter_data(db, capital, username_box, password_box, confirm_box, p_text, p_rect, u_text, u_rect, data, type, login=True):
    nums = ['0', '1', '2', '3', '4', '5', '6' ,'7' ,'8' ,'9']
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


    while True:
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_hovering(pygame.mouse.get_pos()):
                    login_menu(db)

            if event.type == pygame.KEYDOWN:
                current = pygame.key.name(event.key)
                if current == 'return':
                    return data

                elif current == 'backspace':
                    data = data[:len(data) - 1]

                elif current == 'caps lock':
                    if not capital:
                        capital = True
                    else:
                        capital = False

                elif current == "space":
                    data += ' '

                else:
                    if len(data) <= 24 and current in letters or current in nums:
                        if capital:
                            current = current.capitalize()
                            data += current
                        else:
                            data += current



        temp_text = pygame.font.SysFont('arial', 24).render(f"{data}", True, YELLOW)
        temp_rect = None

        if type == "username":
            temp_rect = temp_text.get_rect(center=(username_box.x + 150, username_box.y + 12))
        elif type == "password":
            temp_rect = temp_text.get_rect(center=(password_box.x + 150, password_box.y + 12))
        elif type == "confirm":
            temp_rect = temp_text.get_rect(center=(confirm_box.x + 150, confirm_box.y + 12))

        WIN.blit(temp_text, temp_rect)
        pygame.draw.rect(WIN, WHITE, username_box, 3)
        pygame.draw.rect(WIN, WHITE, password_box, 3)
        WIN.blit(u_text, u_rect)
        WIN.blit(p_text, p_rect)

        if not login:
            c_text = pygame.font.SysFont('arial', 24).render("Confirm Pass:", True, WHITE)
            c_rect = c_text.get_rect(center=(60, 290))
            pygame.draw.rect(WIN, WHITE, confirm_box, 3)
            WIN.blit(c_text, c_rect)

        enter_button.draw(WIN)
        back_button.draw(WIN)
        pygame.display.update()



def login(db):   #enter if user is registering or signing in by optional parameter and just change db.login() to db.register() when text is entered into boxes.
    WIN.fill(BLACK)
    pygame.display.set_caption("Register")

    u_text = pygame.font.SysFont('arial', 24).render("Username:", True, WHITE)
    u_rect = u_text.get_rect(center=(70, 150))
    p_text = pygame.font.SysFont('arial', 24).render("Password:", True, WHITE)
    p_rect = p_text.get_rect(center=(70, 220))


    username = ""
    password = ""
    password_box, password_text = pygame.Rect(125, 210, 300, 25), pygame.font.SysFont('arial', 24).render(f"{password}", True, YELLOW)
    username_box, username_text = pygame.Rect(125, 140, 300, 25), pygame.font.SysFont('arial', 24).render(f"{username}", True, YELLOW)
    confirm_box = pygame.Rect(125, 280, 300, 25)
    error_text, error_rect = None, None
    capital = False


    while True:
        WIN.fill(BLACK)
        password_text, username_text = pygame.font.SysFont('arial', 24).render(f"{password}", True, YELLOW), pygame.font.SysFont('arial', 24).render(f"{username}", True, YELLOW)
        password_rect, username_rect = password_text.get_rect(center=(password_box.x + 150, password_box.y + 12)), username_text.get_rect(center=(username_box.x + 150, username_box.y + 12))
        m_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_hovering(m_pos):
                    login_menu(db)

                if m_pos[0] in range(password_box.left, password_box.right) and m_pos[1] in range(password_box.top, password_box.bottom):
                    error_text, error_rect = None, None
                    password = enter_data(db, capital, username_box, password_box, confirm_box, p_text, p_rect, u_text, u_rect, password, "password")


                if m_pos[0] in range(username_box.left, username_box.right) and m_pos[1] in range(username_box.top, username_box.bottom):
                    error_text, error_rect = None, None
                    username = enter_data(db, capital, username_box, password_box, confirm_box, p_text, p_rect, u_text, u_rect, username, "username")


                if enter_button.is_hovering(pygame.mouse.get_pos()):     #MAYBE MAKE DIFFERENT PAGE FOR REGISTER AND LOGIN
                    if not password == None or username == None:
                        login = db.login(username, password)
                        if login == "worked":
                            print("worked")
                            main_menu(db, 1)

                        else:
                            error_text = pygame.font.SysFont('arial', 24).render(f"INVALID: {login}", True, WHITE)
                            error_rect = error_text.get_rect(center=(225, 350))



        pygame.draw.rect(WIN, WHITE, username_box, 3)
        pygame.draw.rect(WIN, WHITE, password_box, 3)
        if error_text is not None and error_rect is not None:
            WIN.blit(error_text, error_rect)
        WIN.blit(u_text, u_rect)
        WIN.blit(p_text, p_rect)
        WIN.blit(username_text, username_rect)
        WIN.blit(password_text, password_rect)
        enter_button.draw(WIN)
        back_button.draw(WIN)
        pygame.display.update()



def register(db):
    WIN.fill(BLACK)
    pygame.display.set_caption("Register")

    u_text = pygame.font.SysFont('arial', 24).render("Username", True, WHITE)
    u_rect = u_text.get_rect(center=(70, 150))
    p_text = pygame.font.SysFont('arial', 24).render("Password", True, WHITE)
    p_rect = p_text.get_rect(center=(70, 220))

    username = ""
    password = ""
    confirm_password = ""
    error_text, error_rect = None, None
    password_box = pygame.Rect(125, 210, 300, 25)
    username_box= pygame.Rect(125, 140, 300, 25)
    confirm_box = pygame.Rect(125, 280, 300, 25)
    capital = False

    while True:
        WIN.fill(BLACK)
        password_text, username_text, confirm_text= pygame.font.SysFont('arial', 24).render(f"{password}", True,YELLOW), pygame.font.SysFont('arial',24).render( f"{username}", True, YELLOW), pygame.font.SysFont('arial', 24).render(f"{confirm_password}", True, YELLOW)
        password_rect, username_rect, confirm_rect = password_text.get_rect(center=(password_box.x + 150, password_box.y + 12)), username_text.get_rect( center=(username_box.x + 150, username_box.y + 12)), confirm_text.get_rect(center=(confirm_box.x + 150, confirm_box.y + 12))


        m_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_hovering(m_pos):
                    login_menu(db)

                if m_pos[0] in range(password_box.left, password_box.right) and m_pos[1] in range(password_box.top,password_box.bottom):
                    error_text, error_rect = None, None
                    password = enter_data(db, capital, username_box, password_box, confirm_box, p_text, p_rect, u_text,u_rect, password, "password", login=False)

                if m_pos[0] in range(username_box.left, username_box.right) and m_pos[1] in range(username_box.top,username_box.bottom):
                    error_text, error_rect = None, None
                    username = enter_data(db, capital, username_box, password_box, confirm_box, p_text, p_rect, u_text,u_rect, username, "username", login=False)

                if m_pos[0] in range(confirm_box.left, confirm_box.right) and m_pos[1] in range(confirm_box.top, confirm_box.bottom):
                    error_text, error_rect = None, None
                    confirm_password = enter_data(db, capital, username_box, password_box, confirm_box, p_text, p_rect, u_text, u_rect, confirm_password, "confirm", login=False)

                if enter_button.is_hovering(pygame.mouse.get_pos()):  # MAYBE MAKE DIFFERENT PAGE FOR REGISTER AND LOGIN
                    if not password is None or username is None or confirm_password is None:
                        register = db.register(username, password, confirm_password)
                        if register == "worked":
                            db.login(username, password)
                            main_menu(db, 1)

                        else:
                            error_text = pygame.font.SysFont('arial', 24).render(f"INVALID: {register}", True, WHITE)
                            error_rect = error_text.get_rect(center=(225, 350))

        pygame.draw.rect(WIN, WHITE, username_box, 3)
        pygame.draw.rect(WIN, WHITE, password_box, 3)
        pygame.draw.rect(WIN, WHITE, confirm_box, 3)

        WIN.blit(u_text, u_rect)
        WIN.blit(p_text, p_rect)
        WIN.blit(username_text, username_rect)
        WIN.blit(password_text, password_rect)
        WIN.blit(confirm_text, confirm_rect)
        if error_text is not None and error_rect is not None:
            WIN.blit(error_text, error_rect)
        c_text = pygame.font.SysFont('arial', 24).render("Confirm Pass:", True, WHITE)
        c_rect = c_text.get_rect(center=(60, 290))
        WIN.blit(c_text, c_rect)
        enter_button.draw(WIN)
        back_button.draw(WIN)
        pygame.display.update()





def main_menu(db, current_level):
    pygame.init()
    WIN.fill(BLACK)
    pygame.display.set_caption("Menu")


    if db.current_user != None:
        welcome_text = pygame.font.SysFont('arial', 24).render(f"Welcome, {db.current_user[0]}!", True, YELLOW)


    else:
        welcome_text = pygame.font.SysFont('arial', 24).render(f"Welcome, Guest!", True ,YELLOW)


    welcome_rect = welcome_text.get_rect(center=(330,590))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_text_button.is_hovering(pygame.mouse.get_pos()):
                    mode_menu(db, current_level)

                if exit_button.is_hovering(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()

                if leaderboard_button.is_hovering(pygame.mouse.get_pos()):
                    leaderboard(db)

                if logout_button.is_hovering(pygame.mouse.get_pos()):
                    db.logout()
                    login_menu(db)

                if login_button.is_hovering(pygame.mouse.get_pos()):
                    login_menu(db)



        play_text_button.draw(WIN)
        exit_button.draw(WIN)
        leaderboard_button.draw(WIN)
        if db.current_user is not None:
            logout_button.draw(WIN)

        else:
            login_button.draw(WIN)

        WIN.blit(pacman_title_text, pacman_title_rect)
        WIN.blit(welcome_text, welcome_rect)
        pygame.display.update()



def mode_menu(db, current_level):
    pygame.init()
    WIN.fill(BLACK)
    pygame.display.set_caption("Modes")
    choose_mode_text = pygame.font.SysFont('arial', 30).render('Choose Mode ', True, YELLOW)
    choose_mode_rect = choose_mode_text.get_rect(center=(224, 75))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if normal_button.is_hovering(pygame.mouse.get_pos()):
                    play("normal", db, 3, current_level)

                elif advanced_button.is_hovering(pygame.mouse.get_pos()):
                    play("advanced", db, 3, current_level)


                elif custom_button.is_hovering(pygame.mouse.get_pos()):
                    play("custom", db, 3, current_level)


                elif back_button.is_hovering(pygame.mouse.get_pos()):
                    main_menu(db, current_level)

            normal_button.draw(WIN)
            advanced_button.draw(WIN)
            back_button.draw(WIN)
            custom_button.draw(WIN)
            WIN.blit(choose_mode_text, choose_mode_rect)
            pygame.display.update()





def leaderboard(db):  # CONTINUE THIS FUNCTION TO PRESENT THE DATA FROM SELF.DB.SHOW() INTO TEXT ON THE GAME WINDOW, THEREFORE INTRODUCE GAME LOOP
    pygame.init()
    WIN.fill(BLACK)
    pygame.display.update()
    leaderboard_data = db.get_leaderboard_data("normal")
    original_leaderboard_button.highlighted = True
    advanced_leaderboard_button.highlighted = False
    complete = False
    Y = 200
    leaderboard_text = pygame.font.SysFont('arial', 30).render("Leaderboards", True, WHITE)
    leaderboard_rect = leaderboard_text.get_rect(center=(224, 15))
    rank_text = pygame.font.SysFont('arial', 24).render("Rank", True, WHITE)
    rank_rect = leaderboard_text.get_rect(center=(100, 175))
    username_text = pygame.font.SysFont('arial', 24).render("Username", True, WHITE)
    username_rect = leaderboard_text.get_rect(center=(175, 175))
    level_text = pygame.font.SysFont('arial', 24).render("Level", True, WHITE)
    level_rect = leaderboard_text.get_rect(center=(310, 175))
    score_text = pygame.font.SysFont('arial', 24).render("High Score", True, WHITE)
    score_rect = leaderboard_text.get_rect(center=(400, 175))
    small_font = pygame.font.SysFont('arial', 20)



    while True:
        m_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if advanced_leaderboard_button.is_hovering(m_pos):
                    leaderboard_data = db.get_leaderboard_data("advanced")
                    advanced_leaderboard_button.highlighted = True
                    original_leaderboard_button.highlighted = False
                    WIN.fill(BLACK)
                    complete = False
                    Y = 200

                elif original_leaderboard_button.is_hovering(m_pos):
                    leaderboard_data = db.get_leaderboard_data("normal")
                    original_leaderboard_button.highlighted = True
                    advanced_leaderboard_button.highlighted = False
                    WIN.fill(BLACK)
                    complete = False
                    Y = 200

                if back_button.is_hovering(m_pos):
                    main_menu(db, 1)


        WIN.blit(leaderboard_text, leaderboard_rect)
        WIN.blit(rank_text, rank_rect)
        WIN.blit(username_text, username_rect)
        WIN.blit(level_text, level_rect)
        WIN.blit(score_text, score_rect)
        original_leaderboard_button.draw(WIN)
        advanced_leaderboard_button.draw(WIN)
        back_button.draw(WIN)
        pygame.display.update()

        if complete:
            continue

        for i, user in enumerate(leaderboard_data):  # maintain x and increment y pos in the for loop
            if Y >= TOTAL_HEIGHT:                                # if there are too many text boxes bounded by the height of the screen stop the while loop from accessing this for loop and maintain the current leaderboard in viable range.
                break

            else:
                if db.current_user is not None and user[0] == db.current_user[0]:
                    text_colour = GREEN
                else:
                    text_colour = YELLOW

                rank_value_text = small_font.render(f"{i + 1}", True, text_colour)
                rank_value_rect = rank_value_text.get_rect(center=(45, Y))
                username_value_text = small_font.render(f"{user[0]}", True, text_colour)
                username_value_rect = username_value_text.get_rect(center=(145, Y))
                level_value_text = small_font.render(f"{user[1]}", True, text_colour)
                level_value_rect = level_value_text.get_rect(center=(257, Y))
                score_value_text = small_font.render(f"{user[2]}", True, text_colour)
                score_value_rect = score_value_text.get_rect(center=(370, Y))
                WIN.blit(rank_value_text, rank_value_rect)
                WIN.blit(username_value_text, username_value_rect)
                WIN.blit(level_value_text, level_value_rect)
                WIN.blit(score_value_text, score_value_rect)
                pygame.display.update()
                Y += 25

        complete = True




def play(mode, db, lives, current_level, generated=False):
    if mode == "normal":
        if db.current_user != None:
            db.update_mode(1)
            db.update_level(1)
        Normal(db.current_user, db.current_index, current_level, lives, db).run()

    elif mode == "advanced":
        if db.current_user != None:
            db.update_mode(2)
            db.update_level(1)
        Advanced(db.current_user, db.current_index, current_level, lives, db, generated).run()

    elif mode == "custom":
        Custom(db.current_user, db.current_index, current_level, lives, db, generated).customise_menu()



def options_menu(mode, db, current_level):
    pygame.init()
    WIN.fill(BLACK)
    pygame.display.set_caption("Options")

    CONTINUE_BUTTON = Button(image=None, pos=(224, 100), text="Continue", font=pygame.font.SysFont('arial', 24),
                                 colour=WHITE)

    MAIN_MENU_BUTTON = Button(image=None, pos=(224, 150), text="Main Menu", font=pygame.font.SysFont('arial', 24),
                                  colour=WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONTINUE_BUTTON.is_hovering(pygame.mouse.get_pos()):
                    WIN.fill(BLACK)
                    play(mode, db, 3, current_level)

                if exit_button.is_hovering(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()

                if MAIN_MENU_BUTTON.is_hovering(pygame.mouse.get_pos()):
                    WIN.fill(BLACK)
                    main_menu(db, 1)


        continue_button.draw(WIN)
        main_menu_button.draw(WIN)
        pygame.display.update()




if __name__ == "__main__":
    db = Database()
    main_menu(db ,4)
    #login_menu(db)







import random
import pygame.time
from algs import *
from data_structures import *
from settings import *
from misc_classes import *




class Pacman(object):
    def __init__(self, node):
        '''
        :param node:
        '''
        self.colour = YELLOW
        self.radius = TILE_WIDTH // 2  # diameter fits into each individual tile which is 2r
        self.node = node  # delegated as the parameter 'node' so that Pacman's position can be updated due to player input accordingly.
        self.pos = self.node.pos
        self.curr_direction = LEFT
        self.last_direction = self.curr_direction
        self.sheet_index = 0
        self.drawing_delay = 0



    def input(self):
        '''
        :return:
        '''
        keys = pygame.key.get_pressed() # check arrow keys or WASD for if they are pressed, return direction corresponding to each arrow key / WASD, if no keys are pressed return STOP (no movement
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.curr_direction = RIGHT  # changes the current direction so that the pacman will continue to move in the same direction if there is no new key press. This matches real gameplay :)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.curr_direction = LEFT
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.curr_direction = DOWN
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.curr_direction = UP
        return self.curr_direction  # continues to move if no different key press..



    def update(self, generated_maze=False):
        '''
        :return:
        '''
        self.input()
        self.node = self.get_target_node(self.curr_direction, generated_maze)
        self.pos = self.node.pos

        if self.valid_direction(self.curr_direction, generated_maze):
            self.last_direction = self.curr_direction

        # update the new position of the player as the adjacent node in the direction of the player's choice.

    def draw(self, window):
        '''
        :param window:
        :return:
        '''
        center = (self.pos.x, self.pos.y - 4)
        self.drawing_delay += 1

        if self.sheet_index > 2:
            self.sheet_index = 0


        if self.last_direction == LEFT:
            window.blit(pacman_movingleft_sheet[self.sheet_index], center)


        elif self.last_direction == RIGHT:
            window.blit(pacman_movingright_sheet[self.sheet_index], center)


        elif self.last_direction == UP:
            window.blit(pacman_movingup_sheet[self.sheet_index], center)


        elif self.last_direction == DOWN:
            window.blit(pacman_movingdown_sheet[self.sheet_index], center)



        if self.drawing_delay > 3:
            self.sheet_index += 1
            self.drawing_delay = 0





        #return pygame.draw.circle(window, self.colour, center, self.radius)

    def valid_direction(self, direction, generated_maze):  # validate the player's movement
        '''
        :param direction:
        :return:
        '''
        if direction is not STOP:
            if not generated_maze:
                if self.node.adjacent_nodes[direction] is not None:  # if the player presses the arrow keys or WASD
                    return True
        else:
            if self.node.walls[direction]:     #CHECKS IF THERE ISNT A WALL IN THE WAY WHEN CONSIDERING MOVING THROUGH CELLS IN THE GENERATED MAZE.
                return True

        return False


    def get_target_node(self, direction, generated_maze):
        '''

        :param direction:
        :return:
        '''
        if self.valid_direction(direction, generated_maze):  # if the player moves in a valid direction
            return self.node.adjacent_nodes[direction]  # return the node that it is moving to as it new position

        elif self.valid_direction(self.last_direction, generated_maze):
            return self.node.adjacent_nodes[self.last_direction]

        else:
            return self.node



class Ghost(object):
    def __init__(self, node):
        '''
        :param node:
        :param frightened_sheet:
        :param eaten_sheet:
        '''
        self.colour = None
        self.node = node
        self.orientation = UP
        self.pos = self.node.pos
        self.modes = {'frightened': False, 'chase': False, 'scatter': False, 'eaten': False}
        self.directions = [UP, DOWN, LEFT, RIGHT, STOP]

    def reset_mode(self, curr):
        '''

        :param curr:
        :return:
        '''
        if curr == 1:
            update_dict = {'chase': True, 'frightened': False, 'scatter': False, 'eaten': False}
            self.modes.update(update_dict)

        elif curr == 2:  # scatter
            update_dict = {'chase': False, 'frightened': False, 'scatter': True, 'eaten': False}
            self.modes.update(update_dict)

        elif curr == 3:  # frightened
            update_dict = {'chase': False, 'frightened': True, 'scatter': False, 'eaten': False}
            self.modes.update(update_dict)

        elif curr == 4:  # eaten
            update_dict = {'chase': False, 'frightened': False, 'scatter': False, 'eaten': True}
            self.modes.update(update_dict)


    def get_direction(self, target):  # implementation of greedy best-first search for original ghost pathfinding
        '''
        :param target:
        :return:
        '''
        self.direction_list = [d for d in self.directions if self.valid_direction(d) and d != (self.orientation * -1)]
        directions = {direction: distance(self.node.adjacent_nodes[direction], target) for direction in self.direction_list}

        mins = [k for k, v in directions.items() if v == min(directions.values())]  # creates a list of minimising directions (in terms of distance to target node) in the edge case there are multiple min values by selecting all the directions with the smallest distance and entering that into a list using list comprehension


        if UP in mins:
            self.orientation = UP  # order of directions prioritised in the case there are multiple minimising directions (UP, LEFT, DOWN, RIGHT)
            return UP

        elif LEFT in mins:
            self.orientation = LEFT
            return LEFT

        elif DOWN in mins:
            self.orientation = DOWN
            return DOWN

        elif RIGHT in mins:
            self.orientation = RIGHT
            return RIGHT

        else:
            return STOP

    def chase(self, target):  # need to find all calls of chase, scatter and frightened and pass temp_time, current_time or pygame.time.get_ticks()
        self.node = self.node.adjacent_nodes[self.get_direction(target)]
        self.pos = self.node.pos

    def scatter(self, home_node):
        self.node = self.node.adjacent_nodes[self.get_direction(home_node)]
        self.pos = self.node.pos

    def frightened(self):
        d = random.choice([d for d in self.directions if self.valid_direction(d) and d != (self.orientation * -1)])
        self.orientation = d
        self.node = self.node.adjacent_nodes[d]
        self.pos = self.node.pos

    def eaten(self):
        base = Node(14, 13)
        self.chase(base)
        if self.node.pos == base.pos:
            self.reset_mode(1)

    def collision(self, target):
        if self.pos == target.pos:
            return True
        return False

    def valid_direction(self, direction):   #UPDATE THIS FOR CELLS.
        if direction is not STOP and self.node.adjacent_nodes[direction] is not None:
            return True
        return False


    def draw(self, window, sheet, frightened_nearly_up=False):
        position = (self.pos.x, self.pos.y - 2)
        if self.modes['chase'] == True or self.modes['scatter'] == True:
            if self.orientation == RIGHT:
                window.blit(sheet[0], position)

            elif self.orientation == LEFT:
                window.blit(sheet[1], position)

            elif self.orientation == UP:
                window.blit(sheet[2], position)

            elif self.orientation == DOWN:
                window.blit(sheet[3], position)


        elif self.modes['frightened'] == True:
            if not frightened_nearly_up:  # need to edit with a timer to show flashing ghost when frightened nearly up
                window.blit(frightened_sheet[0], position)
            else:
                window.blit(frightened_sheet[1], position)

        elif self.modes['eaten'] == True:
            if self.orientation == RIGHT:
                window.blit(eaten_sheet[0], position)

            elif self.orientation == LEFT:
                window.blit(eaten_sheet[1], position)

            elif self.orientation == UP:
                window.blit(eaten_sheet[2], position)

            elif self.orientation == DOWN:
                window.blit(eaten_sheet[3], position)


    def draw_points(self, window, points, wall_colour):
        colours = [GREEN, RED, BLUE, PINK]
        if wall_colour in colours:
            del colours[colours.index(wall_colour)]
        colour = random.choice(colours)  # random colour selection for bonus points
        print(points)
        points_text = pygame.font.SysFont('arial', 15).render(f"{str(points)}", True, colour)
        points_rect = points_text.get_rect(center=(self.pos.x + 10, self.pos.y - 10))

        window.blit(points_text, points_rect)




class Blinky(Ghost):
    def __init__(self, node):
        super().__init__(node)
        self.name = 'Blinky'
        self.colour = RED
        self.orientation = UP
        self.home = Node(0, COLUMNS - 1)
        self.reset_mode(2)
        self.sheet = blinky_sheet

    def update(self, player):
        if self.modes['chase']:
            self.chase(player.node)

        elif self.modes['scatter']:
            self.scatter(self.home)

        elif self.modes['eaten']:
            self.eaten()





class Pinky(Ghost):
    def __init__(self, node):
        super().__init__(node)
        self.name = 'Pinky'
        self.colour = PINK
        self.orientation = LEFT
        self.home = Node(0, 0)
        self.sheet = pinky_sheet
        self.reset_mode(2)



    def update(self, player):
        if self.modes['chase']:
            if player.curr_direction == UP:
                self.chase(Node(player.node.row - 4,player.node.col))  # for some reason allocating all this redundant code into a method doesnt work?
            elif player.curr_direction == DOWN:
                self.chase(Node(player.node.row + 4, player.node.col))
            elif player.curr_direction == LEFT:
                self.chase(Node(player.node.row, player.node.col - 4))
            elif player.curr_direction == RIGHT:
                self.chase(Node(player.node.row, player.node.col + 4))

        elif self.modes['scatter']:
            self.scatter(self.home)

        elif self.modes['eaten']:
            self.eaten()


class Clyde(Ghost):
    def __init__(self, node):
        super().__init__(node)
        self.name = 'Clyde'
        self.colour = ORANGE
        self.orientation = LEFT
        self.home = Node(ROWS - 1, 0)
        self.reset_mode(2)
        self.sheet = clyde_sheet


    def update(self, player):
        if self.modes['chase']:
            distance = total_distance(self.node, player)
            print(distance, "-->")
            if distance <= 8:
                self.scatter(self.home)
                print("scattering")
            else:
                print("chasing")
                if player.curr_direction == UP:
                    n = Node(player.node.row - 4, player.node.col)
                    self.chase(n)
                elif player.curr_direction == DOWN:
                    n = Node(player.node.row + 4, player.node.col)
                    self.chase(n)
                elif player.curr_direction == LEFT:
                    n = Node(player.node.row, player.node.col - 4)
                    self.chase(n)
                elif player.curr_direction == RIGHT:
                    n = Node(player.node.row, player.node.col + 4)
                    self.chase(n)


        elif self.modes['scatter']:
            self.scatter(self.home)

        elif self.modes['eaten']:
            self.eaten()


class Inky(Ghost):
    def __init__(self, node):
        super().__init__(node)
        self.name = 'Inky'
        self.colour = TEAL
        self.orientation = RIGHT
        self.home = Node(ROWS - 1, COLUMNS - 1)
        self.reset_mode(2)
        self.sheet = inky_sheet

    # based on the formula 2[(p+2) - b] + b where p is the player position, b is blinky's position and +2 denotes 2 spaces in front of the player dependent on current direction

    def update(self, player, blinky):
        if self.modes['chase']:
            if player.curr_direction == LEFT:
                pos = [(2 * (player.node.row - blinky.node.row)) + blinky.node.row,
                       (2 * ((player.node.col - 2) - blinky.node.col)) + blinky.node.col]
                self.chase(Node(pos[0], pos[1]))

            elif player.curr_direction == RIGHT:
                pos = [(2 * (player.node.row - blinky.node.row)) + blinky.node.row,
                       (2 * ((player.node.col + 2) - blinky.node.col)) + blinky.node.col]
                self.chase(Node(pos[0], pos[1]))

            elif player.curr_direction == DOWN:
                pos = [(2 * ((player.node.row + 2) - blinky.node.row)) + blinky.node.row,
                       (2 * (player.node.col - blinky.node.col)) + blinky.node.col]
                self.chase(Node(pos[0], pos[1]))


            elif player.curr_direction == UP:
                pos = [(2 * ((player.node.row - 2) - blinky.node.row)) + blinky.node.row,
                       (2 * (player.node.col - blinky.node.col)) + blinky.node.col]
                self.chase(Node(pos[0], pos[1]))


        elif self.modes['scatter']:
            self.scatter(self.home)

        elif self.modes['eaten']:
            self.eaten()


class AdvancedGhost(Ghost):
    def __init__(self, path_colour, node):
        super().__init__(node)
        self.path_colour = path_colour

    def move(self):
        print(self.curr_path_idx)
        self.node = self.path[self.curr_path_idx][0]
        self.orientation = self.path[self.curr_path_idx][1]
        self.node.colour = BLACK
        self.pos = self.node.pos
        self.curr_path_idx += 1

    def set_path_visible(self, window):  #MAYBE CHANGE THIS SO THAT IF THE COLOUR OF THE PATH IS SET TO SOMETHING DIFFERENT THAN THE CURRENT MAZE COLOUR THEN DONT OVERRIDE.
        for node in self.path:
            if not node[0].is_path():    #IF NODE.COLOUR == BLACK
                node[0].colour = self.path_colour   #node.colour = self.path_colour
            node[0].draw(window)

    def reset_path_colour(self):
        for node in self.path:
            node[0].colour = BLACK    #node.colour = BLACK

    def reset(self):
        self.reset_path_colour()
        self.curr_path_idx = 0
        self.path = []


class SuperElroy(AdvancedGhost):
    def __init__(self, path_colour, node):
        super().__init__(path_colour, node)
        self.name = "SuperElroy"
        self.path_colour = LIGHT_GREEN
        self.orientation = UP
        self.home = Node(ROWS - 1, COLUMNS - 1)
        self.reset_mode(2)
        self.sheet = super_elroy_sheet
        self.path = []
        self.curr_path_idx = 0

    def update(self, player, window, graph, path_visible):
        if self.modes['chase']:
            if not self.path:
                self.path = self.get_path(player, graph)
                if path_visible:
                    self.set_path_visible(window)
                self.move()

            else:
                if self.curr_path_idx > len(self.path) - 1:   #edit here so that all the nodes in the path return to their original colour, for now set this to blue. Also change current path index to 0
                    self.reset()
                    self.path = self.get_path(player, graph)
                    if path_visible:
                        self.set_path_visible(window)
                    self.move()

                else:
                    self.move()

        elif self.modes['scatter']:
            self.scatter(self.home)

        elif self.modes['eaten']:
            self.eaten()



    def get_path(self, target, graph):
        path = Astar(self.node, target.node).run(graph)
        return path



class Brainless(AdvancedGhost):   #make advanced ghost higher object which all these inherit from due to reusing methods.
    def __init__(self, path_colour, node):
        super().__init__(path_colour, node)
        self.name = "Brainless"
        self.orientation = LEFT
        self.sheet = brainless_sheet
        self.home = Node(0, COLUMNS-1)
        self.reset_mode(2)
        self.path = []
        self.curr_path_idx = 0
        self.path_colour = path_colour

    def update(self, player, window, path_visible):
        if self.modes['chase']:
            if not self.path:
                self.path = self.get_path(player)
                if path_visible:
                    self.set_path_visible(window)
                self.move()

            else:
                if self.curr_path_idx > len(self.path) - 1:   #edit here so that all the nodes in the path return to their original colour, for now set this to blue. Also change current path index to 0
                    self.reset()
                    self.path = self.get_path(player)
                    if path_visible:
                        self.set_path_visible(window)
                    self.move()

                else:
                    self.move()

        elif self.modes['scatter']:
            self.scatter(self.home)

        elif self.modes['eaten']:
            self.eaten()


    def get_path(self, target):
        return dls(self.node, target.node, limit=20)





class Patient(AdvancedGhost):  #djisktra
    def __init__(self, path_colour, node):
        super().__init__(path_colour, node)
        self.name = "Patient"
        self.orientation = LEFT
        self.sheet = patient_sheet
        self.home = Node(ROWS-1, 0)
        self.reset_mode(2)
        self.path = []
        self.curr_path_idx = 0

    def update(self, player, window, graph, path_visible):
        if self.modes['chase']:
            if not self.path:
                self.path = self.get_path(player, graph)
                if path_visible:
                    self.set_path_visible(window)
                self.move()

            else:
                if self.curr_path_idx > len(self.path) - 1:   #edit here so that all the nodes in the path return to their original colour, for now set this to blue. Also change current path index to 0
                    self.reset()
                    self.path = self.get_path(player, graph)
                    if path_visible:
                        self.set_path_visible(window)
                    self.move()

                else:
                    self.move()

        elif self.modes['scatter']:
            self.scatter(self.home)

        elif self.modes['eaten']:
            self.eaten()



    def get_path(self, target, graph):
        path = Djikstra(self.node, target.node).run(graph, target)
        print("Dijkstra: ", path)
        return path[:10]




class Hurricane(AdvancedGhost):   #TO BE TWEAKED: THE GENERAL IDEA IS TO HAVE SOME RADIUS, FOR NOW 10 TILES BEFORE A* SEARCH IS CALLED, AND OUTSIDE THIS RADIUS DFS IS CALLED.
    def __init__(self, path_colour, node):
        super().__init__(path_colour, node)  #ALSO BUG FIX BECAUSE EATEN MODE DOESNT WORK HERE FOR SOME REASON
        self.name = "Hurricane"
        self.orientation = LEFT
        self.sheet = hurricane_sheet
        self.home = Node(0, 0)
        self.reset_mode(2)
        self.path = []
        self.curr_path_idx = 0

    def update(self, player, window, graph, path_visible):
        if self.modes['chase']:
            if not self.path:
                self.path = self.get_path(player, graph)
                if path_visible:
                    self.set_path_visible(window)
                self.move()

            else:
                if self.curr_path_idx > len(self.path) - 1:   #edit here so that all the nodes in the path return to their original colour, for now set this to blue. Also change current path index to 0
                    self.reset()
                    self.path = self.get_path(player, graph)
                    if path_visible:
                        self.set_path_visible(window)
                    self.move()

                else:
                    self.move()

        elif self.modes['scatter']:
            self.scatter(self.home)

        elif self.modes['eaten']:
            self.eaten()


    def get_algorithm(self, target):
        if total_distance(self.node, target) <= 15:
            return "Astar"
        return "DLS"


    def get_path(self, target, graph):
        curr = self.get_algorithm(target)
        if curr == "Astar":
            return Astar(self.node, target.node).run(graph)

        elif curr == "DLS":
            return dls(self.node, target.node, limit=30)

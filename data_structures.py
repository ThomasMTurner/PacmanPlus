import random

import pygame

from settings import *
from misc_classes import  *

def shuffle_array(array):
    '''
    Parameters: array to shuffle
    Return Value: array
    Description: randomly changes the order of items in the array.
    Author: Thomas Turner
    Creation Date:
            '''
    random.shuffle(array)
    return array



def collision(player, node):
    if player.pos == node.pos:
        return True
    return False


def get_map(file):
        '''
        Parameters: string text file to be read into the program.
        Return Value: a 2-dimensional array.
        Description: The method will first open the text file read into the class, iterating over all data points
        where all spaces are removed (space keys are redundant data) and each value is translated from string to integer
        and then translating each row to a subarray, finally constructing a 2d array with the given m x n dimensions of the
        input grid of 0's and 1's from the text file.
        Author: Thomas Turner
        Creation Date: July 2022
        '''
        with open(file, mode='r') as f:
            data = ([list(map(int, line.strip())) for line in f])
            return data



########################################################################################
def distance(curr, target):
    ''' Function or Class Name:
    Parameters:
    Return Value:
    Description:
    Author:
    Creation Date:
        '''
    return Node((curr.row - target.row),(curr.col - target.col)).pos.magnitude

########################################################################################


class PriorityQueue(object):
    ''' Function or Class Name:
        Parameters:
        Return Value:
        Description:
        Author:
        Creation Date:
            '''
    def __init__(self):
        ''' Function or Class Name:
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''
        self.queue = []   #choose array as opposed to dictionary despite pairings of node and f_score due to lack of ordering in dict leading to inability to grab item by index.

    def put(self, item):
        ''' Function or Class Name:
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''

        self.queue.append([item[0], item[1]])   #[node, node.f_score]

    def get(self):
        ''' Function or Class Name:
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''
        minimums = [item for item in self.queue if item[1] == min([i[1] for i in self.queue])]    #return an array containing minimum f score nodes.                                                                                                                           #dictionary which takes the item placed in the queue if it is a minimum value in terms of f_score as a key, alongside a value which is the index of that item in the temp list.
        if len(minimums) > 1:   #more than one node with the same f score
            minimum = self.queue[min([self.queue.index(i) for i in minimums])]
        else:
            minimum = minimums[0]

        del self.queue[self.queue.index(minimum)]   #want to delete the entire subarray
        return minimum[0] #just want to return the node here (item[0])


    def is_empty(self):
        ''' Function or Class Name:
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''
        if len(self.queue) == 0:
            return True
        return False



class Vector(object):
    ''' Function or Class Name:
    Parameters:
    Return Value:
    Description:
    Author:
    Creation Date:
        '''


    def __init__(self, col, row):
        ''' Function or Class Name: vector constructor method
    Parameters: integer column position and integer row position relative to 2d array representing the game grid.
    Return Value:  Vector object
    Description: Constructs an instance of the vector class with a given x and y position as well as a length
    Author: Thomas Turner
    Creation Date: June 2022
        '''
        self.x = col * TILE_WIDTH
        self.y = row * TILE_WIDTH
        self.magnitude = self.magnitude_squared()

    def __add__(self, other):
        ''' Function or Class Name: special add method
            Parameters: another vector object
            Return Value: a vector object
            Description: constructs a new vector object by adding the x components of the input vectors and the y components.
            Author: Thomas Turner
            Creation Date: June 2022
                '''
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        ''' Function or Class Name: special substraction method
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, value):
        ''' Function or Class Name: special multiplication method
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''
        return (self.x * value, self.y * value)

    def __eq__(self, other):
        ''' Function or Class Name: special equality method
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''
        if abs(self.x - other.x) < 0.0001 and abs(self.y - other.y) < 0.0001:
            return True
        return False

    def __repr__(self):
        ''' Function or Class Name: special representation method (when the class is printed)
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''
        return "[" + str(self.x) + ", " + str(self.y) + "]"


    def magnitude_squared(self):
        ''' Function or Class Name: magnitude method
    Parameters: self (the vector object the method is being applied to)
    Return Value: integer
    Description: determines the magnitude of the vector squared by pythagoras' theorem, squaring and adding the x and y components.
    Author: Thomas Turner
    Creation Date: June 2022
        '''
        return (self.x ** 2) + (self.y ** 2)


#########FURTHER CONSTANTS DEFINED HERE TO AVOID CIRCULAR IMPORT######################
J = Vector(0,1)
MINUS_J = Vector(0,-1)
MINUS_I = Vector(-1, 0)
I = Vector(1,0)
ZERO_VECTOR = Vector(0,0)
######################################################################################


class Node(object):
    ''' Function or Class Name
        Description: A node class to abstractly represent each tile position in the grid as a state which then represents a search
        space and can be used by pathfinding algorithms.
        Author: Thomas Turner
        Creation Date: June 2022
            '''
    def __init__(self, row, col):
        ''' Function or Class Name: node constructor method
    Parameters: integer row and column position relative to the 2d array representing the game grid.
    Return Value: returns an instance of a node object
    Description: Node class holds the specified width of the tile it is embedded in so they can be drawn to the screen, a
    set of other nodes in the game graph it is connected to in specified directions as a dictionary, boolean attributes determining
    whether the node holds a type of pellet and a colour of the tile.
    Author: Thomas Turner
    Creation Date: Initial, July 2022, Updated in September 2022
        '''
        self.row = row
        self.col = col
        self.width = TILE_WIDTH
        self.pos = Vector(col, row)
        self.adjacent_nodes = {UP: None, DOWN: None, LEFT: None, RIGHT: None}
        self.pellet = True
        self.power_pellet = False
        self.colour = BLACK
        self.wall_colours = [GREEN, BLUE, RED, PINK, ORANGE, TEAL, WHITE]


    def has_power_pellet(self):
        ''' Function or Class Name:
            Parameters:
            Return Value: Boolean
            Description: will return True if the power pellet attribute is True, and vice versa.
            Author: Thomas Turner
            Creation Date: July 2022
                '''
        return self.power_pellet == True

    def has_pellet(self):
        ''' Function or Class Name:
            Parameters:
            Return Value:
            Description:
            Author: Thomas Turner
            Creation Date: July 2022
                '''
        return self.pellet == True

    def is_wall(self):
        ''' Function or Class Name:
            Parameters:
            Return Value:
            Description:
            Author: Thomas Turner
            Creation Date: July 2022
                '''
        return self.colour in self.wall_colours

    def is_path(self):
        return not self.is_wall() and not self.colour == BLACK


    def mark_wall(self):
        ''' Function or Class Name:
    Parameters:
    Return Value:
    Description: A wall is defined as such that it cannot contain a pellet, and the colour is initially blue which is the
    identifying condition for a wall in the construction procedure of the graph.
    Author: Thomas Turner
    Creation Date: July 2022
        '''
        self.pellet = False    #HERE WE DONT NEED TO SET ALL THE ADJACENT NODES AS NONE, AS THE CONNECTING PROCEDURE DOESNT INCLUDE PRE-IDENTIFIED NODES.
        self.power_pellet = False
        self.colour = BLUE

    def mark_path(self):
        self.pellet = True
        self.colour = BLACK


    def draw_pellet(self, window):
        ''' Function or Class Name:
    Parameters:
    Return Value:
    Description:
    Author: Thomas Turner
    Creation Date: July 2022
        '''
        if self.has_pellet():
            Pellet(self).draw(window)
        elif self.has_power_pellet():
            Power_Pellet(self).draw(window)




    def draw(self, window):  #NEED TO SEPARATE DRAW METHOD FOR INPUT MAZES AND GENERATED MAZES, AS GENERATED MAZES CONSIST OF CELLS OF FOUR WALLS EACH AND INPUT MAZES CONSIDER NODES AS WALLS IF NOT CONNECTED TO THE MAIN GAME GRAPH.
        ''' Function or Class Name:
    Parameters:
    Return Value:
    Description:
    Author:
    Creation Date:
        '''
        #if not self.is_path():
            #pygame.draw.rect(window, self.colour, (self.pos.x, self.pos.y, self.width, self.width), 1)

        #else:
        pygame.draw.rect(window, self.colour, (self.pos.x, self.pos.y, self.width, self.width))


        self.draw_pellet(window)


    def update_adjacent_nodes(self, grid):   #connects all the nodes together that are horizontally or vertically adjacent
        ''' Function or Class Name:
    Parameters: The game grid.
    Return Value: None
    Description: Current node looks at all grid positions in all horizontal and vertical directions from itself
    and connects to a node in that direction given that the nodes row and column position isn't out of bounds and the
    node in that direction isn't pre-specified to be a wall.
    Author: Thomas Turner
    Creation Date: July 2022, Updated August 2022
        '''
        if self.row < ROWS - 1:
            if not grid[self.row + 1][self.col].is_wall():
                self.adjacent_nodes[DOWN] = grid[self.row + 1][self.col]

        if self.row > 0:
            if not grid[self.row - 1][self.col].is_wall():
                self.adjacent_nodes[UP] = grid[self.row - 1][self.col]

        if self.col < COLUMNS - 1:
            if not grid[self.row][self.col + 1].is_wall():
                self.adjacent_nodes[RIGHT] = grid[self.row][self.col + 1]

        if self.col > 0:
            if not grid[self.row][self.col - 1].is_wall():
                self.adjacent_nodes[LEFT] = grid[self.row][self.col - 1]


    def __repr__(self):
        ''' Function or Class Name:
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''
        return f"[{self.row},{self.col}]"




class Graph(object):
    ''' Function or Class Name:
    Parameters:
    Return Value:
    Description:
    Author:
    Creation Date:
        '''


    def __init__(self, file, score, pellet_amount, wall_colour, custom=False):
        ''' Function or Class Name:
        Parameters:
            - file : text file read by the graph to produce the maze
            - score: the current score achieved by the player.
            - pellet_amount: the amount of pellets that will be produced in the maze
            - maze_colour: the colour of the walls in the maze
            - generated: optional parameter whether the maze is produced from a text file or is procedurally
            generated.

        Return Value:
        Description: constructs a grid as will be described in the make_grid method taking the parameter
        whether it is generated or not. If the graph is not generated it will read the text file containing corresponding
        1's and 0's representing walls and nodes, augment the game grid (2d array) to make some nodes walls by comparing
        to the text file data, create all power pellets given an input amount at random locations and then connect
        all nodes in the graph. If it is generated it will run a game loop demonstrating a generation with a specified
        algorithm.

        Creation Date: July 2022, Updated September 2022
        '''
        self.file = file
        self.score = score
        self.pellet_amount = pellet_amount
        self.wall_colour = wall_colour

        self.rows = ROWS
        self.cols = COLUMNS
        self.grid = self.make_grid()

        if not custom:
            self.create_preset_maze()

        else:
            self.create_custom_maze()

        self.create_power_pellets()
        self.connect(custom)







    def make_grid(self):
        ''' Function or Class Name:
        Parameters: boolean generated
        Return Value: a 2d array representing a grid of node or cell objects.
        Description: The method will initialise an empty list, it will then iterate over the amount of specified rows of size n
        and construct a subarray of size n, it will then complete a nested for loop iterating over the amount of specified columns,
        placing a node object or a cell object in each [row][col] position in the 2d array depending on whether the maze is generated
        or not.
        Author: Thomas Turner
        Creation Date: July 2022, Updated September 2022.
        '''
        grid = []
        for i in range(self.rows):
            grid.append([])
            for j in range(self.cols):
                grid[i].append(Node(i, j))


        return grid



    def create_preset_maze(self):
        ''' Function or Class Name:
        Parameters:
        Return Value:
        Description:
        Author:
        Creation Date:
        '''
        map = get_map(self.file)

        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 1:
                    self.grid[i][j].mark_wall()


    def create_custom_maze(self):
        run_button = Button(image=None, pos=(224, 600), text="RUN", font=pygame.font.SysFont('arial', 20),colour=WHITE)
        select_button = Button(image=None, pos=(105, 600), text="SELECT", font=pygame.font.SysFont('arial', 18), colour=GREEN)
        delete_button = Button(image=None, pos=(343, 600), text="DELETE", font=pygame.font.SysFont('arial', 18), colour=RED, highlight_colour=RED)
        red_rect, blue_rect, green_rect = pygame.Rect((400, 580), (12, 12)), pygame.Rect((415, 580), (12, 12)), pygame.Rect(430, 580, 12, 12)
        colour_buttons = [[red_rect, RED], [blue_rect, BLUE], [green_rect, GREEN]]



        selecting = True
        running = True
        while running:
            if selecting:
                select_button.highlighted = True
                delete_button.highlighted = False
            else:
                delete_button.highlighted = True
                select_button.highlighted = False

            m_pos = pygame.mouse.get_pos()
            print(m_pos[1])
            WIN.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if m_pos[1] < 576:
                        run = True
                        while run:
                            mouse_pressed = pygame.mouse.get_pressed()[0]
                            m_pos = pygame.mouse.get_pos()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()

                                if not mouse_pressed:
                                    run = False

                                if run_button.is_hovering(pygame.mouse.get_pos()):
                                    running = False

                                if select_button.is_hovering(m_pos):
                                    selecting = True

                                if delete_button.is_hovering(m_pos):
                                    selecting = False

                            for row in self.grid:
                                for node in row:
                                    if m_pos[0] in range(node.pos.x, node.pos.x + 16) and m_pos[1] in range(node.pos.y, node.pos.y + 16):
                                        if selecting:
                                            node.mark_wall()
                                        else:
                                            node.mark_path()


                            self.custom_draw(WIN)
                            run_button.draw(WIN)
                            select_button.draw(WIN)
                            delete_button.draw(WIN)
                            for b in colour_buttons:
                                pygame.draw.rect(WIN, b[1], b[0])
                            pygame.display.update()


                    if run_button.is_hovering(pygame.mouse.get_pos()):
                        running = False

                    if select_button.is_hovering(m_pos):
                        selecting = True

                    if delete_button.is_hovering(m_pos):
                        selecting = False

                    for b in colour_buttons:
                        if m_pos[0] in range(b[0].left, b[0].right) and m_pos[1] in range(b[0].top, b[0].bottom):
                            self.wall_colour = b[1]





            self.custom_draw(WIN)
            run_button.draw(WIN)
            select_button.draw(WIN)
            delete_button.draw(WIN)
            for b in colour_buttons:
                pygame.draw.rect(WIN, b[1], b[0])

            pygame.display.update()





    def connect_nodes(self):
        ''' Function or Class Name:
    Parameters:
    Return Value:
    Description:
    Author:
    Creation Date:
        '''
        for row in self.grid:
            for node in row:
                node.update_adjacent_nodes(self.grid)



    def connect_portal(self):
        ''' Function or Class Name:
    Parameters:
    Return Value:
    Description:
    Author:
    Creation Date:
        '''
        portals = [self.grid[17][0], self.grid[17][27]]
        portals[0].adjacent_nodes[LEFT] = portals[1]
        portals[1].adjacent_nodes[RIGHT] = portals[0]

        #ATTEMPT TO DETERMINE WHETHER CONNECTIONS ARE EITHER HORIZONTAL OR VERTICAL ...



    def get_nodes(self):
        ''' Function or Class Name:
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''
        nodes = []
        for row in self.grid:
            for node in row:
                if not node.is_wall():
                    nodes.append(node)

        return nodes




    def connect(self, custom=False):
        ''' Function or Class Name:
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''
        self.connect_nodes()
        if not custom:
            self.connect_portal()

    def custom_draw(self, window):
        print(self.wall_colour)
        for row in self.grid:
            for node in row:
                if node.is_wall():
                    pygame.draw.rect(window, self.wall_colour, (node.pos.x, node.pos.y, node.width, node.width))
                else:
                    pygame.draw.rect(window, BLACK, (node.pos.x, node.pos.y, node.width, node.width))

                pygame.draw.line(window, self.wall_colour, (node.pos.x, node.pos.y), (node.pos.x, node.pos.y + 16))
                pygame.draw.line(window, self.wall_colour, (node.pos.x, node.pos.y), (node.pos.x + 16, node.pos.y))
                pygame.draw.line(window, self.wall_colour, (node.pos.x, node.pos.y + 16), (node.pos.x + 16, node.pos.y + 16))
                pygame.draw.line(window, self.wall_colour, (node.pos.x + 16, node.pos.y), (node.pos.x + 16, node.pos.y + 16))


    def draw(self, window):
        ''' Function or Class Name:
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''
        for row in self.grid:
            for node in row:
                if node.is_wall(): #WANT TO CHANGE THIS CONDITION TO CHECK IF A PARTICULAR NODE HAS NO ADJACENT NODES, NOT THE TEMPORARY CONDITION IN TERMS OF COLOUR.
                    node.colour = self.wall_colour

                node.draw(window)





    def get_start_pos(self, i):
        ''' Function or Class Name:
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''
        start_positions = [self.grid[8][4], self.grid[14][13], self.grid[15][13], self.grid[14][14], self.grid[15][14], self.grid[8][5]]
        return start_positions[i]

    def get_randomised_start_pos(self):
        ''' Function or Class Name:
            Parameters:
            Return Value:
            Description:
            Author:
            Creation Date:
                '''
        return random.choice([node for row in self.grid for node in row if not node.is_wall()])

    def create_power_pellets(self):
        ''' Function or Class Name:
    Parameters:
    Return Value:
    Description:
    Author:
    Creation Date:
        '''
        for node in (random.choices(self.get_nodes(), k=self.pellet_amount)):
            node.power_pellet = True
            node.pellet = False


    def is_complete(self):
        ''' Function or Class Name:
    Parameters:
    Return Value:
    Description:
    Author:
    Creation Date:
        '''
        for row in self.grid:
            for node in row:
                if not node.is_wall():
                    if node.pellet or node.power_pellet == True:
                        return False

        return True





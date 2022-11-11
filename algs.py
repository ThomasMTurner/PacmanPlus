import random
from data_structures import *


def total_distance(curr, target):
    '''Returns the total number of tiles between a current entity and a target entity by determining the total steps both horizontal and vertical between them in terms of tiles.
    :params curr and target: current entity and target entity as node objects (each entity has a node attribute, for example if clyde and pacman were called they both have a node which they occupy denoted self.node)
    It will then return a distance in terms of tiles, keeping in mind each tile is a 16x16 block, so will integer divide by 16.
    '''
    total_distance = abs(curr.pos.x - target.pos.x) + abs(curr.pos.y - target.pos.y)
    return (total_distance // 16)

def shuffle_array(array):
    random.shuffle(array)
    return array

#GREEDY BFS IS REFERENCED INSIDE GHOST CLASS IN ENTITIES AS OPPOSED A STAND ALONE FUNCTION.


def dls(source, target, limit):
    '''
    Parameters: node objects source and target, source to begin the search and target to be found. Integer limit determining the
    depth of the search.
    Return Value: Boolean or array.
    Description: An implementation of depth-limited search. Searches through the graph representing the maze by adding adjacent nodes
    to a stack iteratively/recursively, these are then added to a visited array. Next nodes to search are popped from the top of the
    stack, if they are already in the visited array the algorithm backtracks through the stack to get an unvisited node. If the algorithm
    searches through the limit of nodes then it will return the visited array as a path.
    Author: Thomas Turner
    Creation Date:
     '''
    s = [source]
    visited = []

    while len(s) > 0:
        current = s.pop(len(s) - 1)
        while current in visited:
            current = s.pop(len(s) - 1)

        if current == target:
            return visited

        for node in shuffle_array([node for node in current.adjacent_nodes.values()]):  # look at all of the adjacent nodes of that node and if they are valid push them to the back of the queue
            if node != None:                                    #shuffle_array function randomly shuffles the order of nodes to be entered to the stack, which are all valid dfs searches but increases the search capacity of the ghost(in the sense that it will cover more of the graph as opposed to following the strict order of nodes in adjacent_nodes dict)
                s.append(node)

        visited.append(current)
        if len(visited) == limit:
            return visited

    return False


def bfs(source, target):
    q  = [source]
    came_from = {}
    path = []
    visited = []

    while len(q) > 0:
        current = q.pop(0)
        while current in visited:
            current = q.pop(0)

        if current == target:
            path.append(current)
            while current in came_from:
                current = came_from[current]
                path.append(current)

            return path[::-1]

        for node in current.adjacent_nodes.values():
            if node != None:
                q.append(node)
                came_from[current] = node





class InformedSearch(object):
    '''
    Return Value:
    Description: Higher-level abstraction of important tools used within both Djikstra's algorithm and A* search.
    Author: Thomas Turner
    Creation Date:
    '''
    def __init__(self):
        '''
        Parameters:
        Return Value:
        Description: constructor method which produces an open set to track nodes to search, produces a dictionary to store all
        parents/predecessors of searched nodes so that a path can be returned, and a final path to return.
        Author: Thomas Turner
        Creation Date:
            '''
        self.open_set = PriorityQueue()
        self.node_history = {}
        self.path = []
        self.direction_history = []

    def construct_score_table(self, graph):
        '''
            Parameters: graph object
            Return Value: dictionary / hash map
            Description: produces a table with the same amount of entries as nodes in the graph and is filled with
            an infinity value for initialisation.
            Author: Thomas Turner
            Creation Date:
        '''
        score_table = {}
        for row in graph:
            for node in row:
                score_table[node] = float("inf")

        return score_table


    def get_path(self, current):
        '''
            Parameters: node object current, the last node explored in the frontier.
            Return Value: array
            Description: backtracks through the hash map storing the parent of each node searched, this returns a path
            in reverse order so the resultant path must be flipped at the end of the procedure.
            Author: Thomas Turner
            Creation Date:
         '''
        self.path.append(current)
        while current in self.node_history:
            current = self.node_history[current]
            self.path.append(current)

        path = [[node, direction] for node in self.path[::-1] for direction in self.direction_history[::-1]]
       
        return path




class Astar(InformedSearch):
    '''
    Parameters: inherits from InformedSearch
    Return Value:
    Description: Class which encapsulates the A* search algorithm, important tools and implementation.
    Author:
    Creation Date:
            '''
    def __init__(self, source, target):
        super().__init__()
        self.source = source
        self.target = target

    @staticmethod
    def heuristic1(current, target):
        return abs(current.pos.x - target.pos.x) + abs(current.pos.y - target.pos.y)

    @staticmethod
    def heuristic2(current, target):
        #return Node((current.row - target.row), (current.col - target.col)).pos.magnitude
        return Vector(current.col - target.col, current.row - target.row).magnitude_squared()


    def run(self, graph):
        print(self.source, self.target)
        g_score, f_score = self.construct_score_table(graph), self.construct_score_table(graph)
        g_score[self.source] = 0
        f_score[self.source] = self.heuristic2(self.source, self.target)
        self.open_set.put([self.source, f_score[self.source]])

        while not self.open_set.is_empty():
            current = self.open_set.get()
            if current == self.target:
                return self.get_path(current)

            for direction, node in current.adjacent_nodes.items():
                if node == None:
                    continue

                else:
                    if g_score[current] + 1 < g_score[node]:
                        self.node_history[node] = current
                        self.direction_history.append(direction)
                        g_score[node] = g_score[current] + 1
                        f_score[node] = g_score[current] + 1 + self.heuristic2(node, self.target)
                        if node not in [i[0] for i in self.open_set.queue]:
                            self.open_set.put([node, f_score[node]])

        return False


class Djikstra(InformedSearch):
    def __init__(self, source, target):
        super().__init__()
        self.source = source
        self.target = target



    def traverse(self, player):
        last_target = self.target
        while True:
            print(player.curr_direction)
            new_target = self.target.adjacent_nodes[player.curr_direction]
            if new_target is None:
                break

            else:
                new_target = self.target.adjacent_nodes[player.curr_direction]
                last_target = new_target


        return last_target



    def run(self, graph, player):
        g_score = self.construct_score_table(graph)
        g_score[self.source] = 0
        self.open_set.put([self.source, g_score[self.source]])

        while not self.open_set.is_empty():
            current = self.open_set.get()
            if current == self.target:
                return self.get_path(current)

            for node in current.adjacent_nodes.values():
                if node == None:
                    continue

                else:
                    if g_score[current] + 1 < g_score[node]:
                        self.node_history[node] = current
                        g_score[node] = g_score[current] + 1
                        if node not in [i[0] for i in self.open_set.queue]:
                            self.open_set.put([node, g_score[node]])


        return False


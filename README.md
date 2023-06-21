# Pacman-Plus
A recreation of and updated version of the classic game Pac-Man in PyGame. Includes Greedy Best-First Search for the classic ghosts, as well as A* search, Dijkstra's algorithm and limited Depth-First Search for the new ghosts.

## Background
This is my first ever long-term coding project, and facilitated my passion not only for coding, but also for artificial intelligence and the world of algorithmic thinking. This was built for the non-exam assessment component of my Computer Science A-level, of which I was awarded the top mark band. In order to build the algorithms from scratch in the "algs.py" file, I moved away from support online and consulted my AI textbook (Peter Norvig) which contained detailed information on how to implement all of the search algorithms.

## Implementation of Search Algorithms

### GBFS
The primary algorithm used within the original Pac-Man game is that of GBFS (greedy best-first search), this approach yielded the best results for a dynamic game, single path approaches are difficult as the player object is always moving spaces (i.e. does not exist at the destination node once the path is generated). I embed in the "data_structures.py" file a graph on top of the maze structure, although this was not done effectively in retrospect, taking nodes as path tiles which meant there were more nodes to search than necessary. Using this graph structure, GBFS enumerates all of its nearest neighbours, excluding wall tiles, and chooses the node with the shortest distance to the target node each frame using a euclidean distancing function. The choice of target node depended on the Ghost using the algorithm, BFS was passed as a compostional function to each Ghost object individually, who then made their choice of target node.

### A* search and Dijkstra's Algorithm

### Depth-limited search

## Implementation of Ghost Behaviour

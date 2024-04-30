# import the library
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

import os
import numpy as np
import pandas as pd


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(BASE_PATH, 'csv_file.csv')

path = []
grid = []

# navigation map
matrix = [
  [1, 1, 1, 0, 1, 1],
  [1, 0, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1]]


def finding(matrix, nstart, nend): 
    global path
    global grid
    # 1. create the grid with the nodes 
    grid = Grid(matrix=matrix)
    # get start and end point
    start = grid.node(nstart[0], nstart[1])
    end = grid.node(nend[0], nend[1])
    # create a finder with A* algorithm
    finder = AStarFinder() 
    # returns a list with the path and the amount of times the finder had to run to get the path 
    path, runs = finder.find_path(start, end, grid)

#main program ---------------------------------------
finding(matrix, (0, 0), (5, 2))
# print result
for point in path:
    x = point.x
    y = point.y
    print(x," ", y)

path = []
grid = []

# reading a csv file
matrix2 = np.array(pd.io.parsers.read_csv(CSV_FILE, header=None)).astype("int")
print(matrix2)

finding(matrix2, (0, 0), (3, 4))
# print result 
for point in path:
    x = point.x
    y = point.y
    print(x," ", y)
print(path[0].x)
    
    
    
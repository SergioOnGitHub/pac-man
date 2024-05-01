import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

import os
import numpy as np
import pandas as pd

import random

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(BASE_PATH, 'matriz_ceros.csv')

matrix = np.array(pd.io.parsers.read_csv(CSV_FILE, header=None)).astype("int")
grid = Grid(matrix=matrix)


class Ghost_inteligente:
    def __init__(self, ubiX, ubiZ, vel, dimHor, dimVer, allCol, allFil, matriz, interId):
        self.DimBoardHor = dimHor
        self.DimBoardVer = dimVer
        #Se inicializa una posicion en el tablero
        self.Position = []
        self.Position.append(ubiX)
        self.Position.append(1.0)
        self.Position.append(ubiZ)
        #Se inicializa un vector de direccion aleatorio
        self.Direction = []
        self.Direction.append(1)
        self.Direction.append(0)
        self.Direction.append(0)
        #Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel
        
        
        self.allCol = allCol
        self.allFil = allFil
        self.matriz = matriz
        self.interId = interId
        
        self.path = []
        self.finder = AStarFinder()
        
        
        
    def finding(self, nstart, nend): 
        global grid
        grid.cleanup()
        # get start and end point
        start = grid.node(nstart[0], nstart[1])
        end = grid.node(nend[0], nend[1])
        # create a finder with A* algorithm
        
        # returns a list with the path and the amount of times the finder had to run to get the path 
        self.path, runs = self.finder.find_path(start, end, grid)
        
        


    def update(self, keys, posPacX, posPacZ):
        
        # up 0, 
        # right 1
        # down 2
        # left 3
        offsetX = 21
        offsetZ = 22
        
        #DEBUGGING
        # print("x:", self.Position[0], self.allCol[int(self.Position[0]) - offsetX], "offset: ", int(self.Position[0]) - offsetX)
        # print("z:", self.Position[2], self.allFil[int(self.Position[2]) - offsetZ], "offset: ", int(self.Position[2]) - offsetZ)
        # print("\n")
        
        # Condición, checa si la posición del Pac-Man es una intersección, 
        # cuando el índice del array de columnas y de filas se encuentra en números diferentes de -1 entra
        # Se le resta el offset respectivo a la posición del pac-man para que coincida con las matrices de control
        if self.allCol[int(self.Position[0]) - offsetX] != -1 and self.allFil[int(self.Position[2]) - offsetZ] != -1:
            id = self.matriz[self.allFil[int(self.Position[2]) - offsetZ]][self.allCol[int(self.Position[0]) - offsetX]]
            
            # DEBUGGING
            # print(self.allCol[int(self.Position[0]) - offsetX])
            # print(self.allFil[int(self.Position[2]) - offsetZ])
            #print("id", id, "\n")
            
            # Condición que identifica si el pac-man está en una posición de intersección válida
            if abs(posPacX - self.Position[0]) > 28 or abs(posPacZ - self.Position[2]) > 28:
                self.finding((self.Position[0] - offsetX, self.Position[2] - offsetZ), (posPacX - offsetX, posPacZ - offsetZ))
                print("Ghost: ", self.path[0].x, self.path[0].y)
                print("Ghost_next: ", self.path[1].x, self.path[1].y, "\n")               
                print("Pac-man: ", posPacX, posPacZ, "\n\n")
                
                if self.path[0].x > self.path[1].x:
                    self.Direction[0] = -1
                    self.Direction[2] = 0
                elif self.path[0].x < self.path[1].x:
                    self.Direction[0] = 1
                    self.Direction[2] = 0
                elif self.path[0].y > self.path[1].y:
                    self.Direction[0] = 0
                    self.Direction[2] = -1
                elif self.path[0].y < self.path[1].y:
                    self.Direction[0] = 0
                    self.Direction[2] = 1
                    
            else:
                self.Direction[0] = 0
                self.Direction[2] = 0
                


        
        
        new_x = self.Position[0] + self.Direction[0]
        new_z = self.Position[2] + self.Direction[2]
        
        # Condición para detener el pacman cuando llega a un borde del mapa
        # 375 px de columnas
        if(new_x <= 375 + offsetX and new_x >= offsetX):
            self.Position[0] = new_x
        else:
            self.Direction[0] = 0
        # 420 px de filas
        if(new_z <= 420  + offsetZ and new_z >= offsetZ):
            self.Position[2] = new_z
        else:
            self.Direction[2] = 0
            


    def drawFace(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x1, y1, z1)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x2, y2, z2)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x3, y3, z3)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x4, y4, z4)
        glEnd()
        
    def drawCube(self, texture, id):
        size = 9.5
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        #glScaled(10,10,10)
        glColor3f(1.0, 1.0, 1.0)
        #Activate textures
        glEnable(GL_TEXTURE_2D)
        
        #top face
        glBindTexture(GL_TEXTURE_2D, texture[id])
        self.drawFace(-size, 1, -size, -size, 1, size, size, 1, size, size, 1, -size)
        # glBindTexture(GL_TEXTURE_2D, texture[id])
        # self.drawFace(-1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, +1.0, 1.0, 1.0)
        
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        
        
        
import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math


class Cubo:
    
    def __init__(self, dimHor, dimVer, vel, X1, Z1, allCol, allFil, matriz):
        self.DimBoardHor = dimHor
        self.DimBoardVer = dimVer
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = []
        self.Position.append(0)
        self.Position.append(5.0)
        self.Position.append(0)
        #Se inicializa un vector de direccion aleatorio
        self.Direction = []
        self.Direction.append(0)
        self.Direction.append(5.0)
        self.Direction.append(1)
        #Se normaliza el vector de direccion
        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[2]*self.Direction[2])
        self.Direction[0] /= m
        self.Direction[2] /= m
        #Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel
        

    def update(self, keys):
        new_x = self.Position[0] + self.Direction[0]
        new_z = self.Position[2] + self.Direction[2]

        if keys == "d":
            self.Direction[2] = 1
            self.Direction[0] = 0
        elif keys == "u":
            self.Direction[2] = -1
            self.Direction[0] = 0
        elif keys == "l":
            self.Direction[0] = -1
            self.Direction[2] = 0
        elif keys == "r":
            self.Direction[0] = 1
            self.Direction[2] = 0
        
        if(new_x <= self.DimBoardHor and new_x >= 0):
            self.Position[0] = new_x
        else:
            self.Direction[0] = 0
        
        if(new_z <= self.DimBoardVer and new_z >= 0):
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
        size = 1
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5,5,5)
        glColor3f(1.0, 1.0, 1.0)
        #Activate textures
        glEnable(GL_TEXTURE_2D)
        
        #top face
        glBindTexture(GL_TEXTURE_2D, texture[id])
        self.drawFace(-size, size, size, -size, size, -size, size, size, -size, +size, size, size)
        # glBindTexture(GL_TEXTURE_2D, texture[id])
        # self.drawFace(-1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, +1.0, 1.0, 1.0)
        
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
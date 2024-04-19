import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math

class Cubo:
    
    def __init__(self, dimHor, dimVer, vel):
        #Se inicializa las coordenadas de los vertices del cubo
        size = 5
        self.vertexCoords = [  
                   size, size, size,   size,size,-size,   size,-size,-size,   size,-size,size,
                  -size,size,size,  -size,size,-size,  -size,-size,-size,  -size,-size,size  ]
        # self.vertexCoords = [  
        #            1,1,1,   1,1,-1,   1,-1,-1,   1,-1,1,
        #           -1,1,1,  -1,1,-1,  -1,-1,-1,  -1,-1,1  ]
        
        
        #Se inicializa los colores de los vertices del cubo
        self.vertexColors = [ 
                   1,1,1,   1,0,0,   1,1,0,   0,1,0,
                   0,0,1,   1,0,1,   0,0,0,   0,1,1  ]
        # self.vertexColors = [ 
        #            1,1,1,   1,0,0,   1,1,0,   0,1,0,
        #            0,0,1,   1,0,1,   0,0,0,   0,1,1  ]
        
        
        #Se inicializa el arreglo para la indexacion de los vertices
        self.elementArray = [ 
                  0,1,2,3, 0,3,7,4, 0,4,5,1,
                  6,2,1,5, 6,5,4,7, 6,7,3,2  ]

        self.DimBoardHor = dimHor
        self.DimBoardVer = dimVer
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = []
        self.Position.append(random.randint(0, self.DimBoardHor))
        self.Position.append(5.0)
        self.Position.append(random.randint(0, self.DimBoardVer))
        #Se inicializa un vector de direccion aleatorio
        self.Direction = []
        self.Direction.append(random.random())
        self.Direction.append(5.0)
        self.Direction.append(random.random())
        #Se normaliza el vector de direccion
        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[2]*self.Direction[2])
        self.Direction[0] /= m
        self.Direction[2] /= m
        #Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel
        

    def update(self):
        new_x = self.Position[0] + self.Direction[0]
        new_z = self.Position[2] + self.Direction[2]
        
        if(new_x <= self.DimBoardHor and new_x >= 0):
            self.Position[0] = new_x
        else:
            self.Direction[0] *= -1.0
            self.Position[0] += self.Direction[0]
        
        if(new_z <= self.DimBoardVer and new_z >= 0):
            self.Position[2] = new_z
        else:
            self.Direction[2] *= -1.0
            self.Position[2] += self.Direction[2]

    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5,5,5)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertexCoords)
        glColorPointer(3, GL_FLOAT, 0, self.vertexColors)
        glDrawElements(GL_QUADS, 24, GL_UNSIGNED_INT, self.elementArray)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glPopMatrix()

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
        size = 2
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5,5,5)
        glColor3f(1.0, 1.0, 1.0)
        #Activate textures
        glEnable(GL_TEXTURE_2D)
        # #front face
        # glBindTexture(GL_TEXTURE_2D, texture[id])
        # self.drawFace(-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0)
        # #right face
        # glBindTexture(GL_TEXTURE_2D, texture[id])
        # self.drawFace(1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
        # #back face
        # glBindTexture(GL_TEXTURE_2D, texture[id])
        # self.drawFace(1.0, 1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0)
        # #left face
        # glBindTexture(GL_TEXTURE_2D, texture[id])
        # self.drawFace(-1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0)
        
        #top face
        glBindTexture(GL_TEXTURE_2D, texture[id])
        self.drawFace(-size, size, size, -size, size, -size, size, size, -size, +size, size, size)
        # glBindTexture(GL_TEXTURE_2D, texture[id])
        # self.drawFace(-1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, +1.0, 1.0, 1.0)
        
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
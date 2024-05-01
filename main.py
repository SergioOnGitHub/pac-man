# OPEN GL PACMAN

# Sergio David Pimentel Pérez A01737331
# José Eduardo Puentes Martínez A01733177
# Luis Isaias Montes Rico A01737664
# Manuel Covarrubias Rodríguez A01737781
# Luis Isaias Montes Rico A01737664


# Programa que realiza una implementación de pacman
# El programa le permite al pacman moverse unicamente 
# por los caminos correctos
# Existen tres fantasmas con  movimiento random pero 
# que no pueden regresar por el lugar que vinieron




import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from Pacman import Pacman


import sys
sys.path.append('..')
from Ghost import Ghost

import sys
sys.path.append('..')
from Ghost_inteligente import Ghost_inteligente




# UBICACION DEL PAC-MAN
# Esquina (0, 0) superior izquierda
ubi_x_pac = 21
ubi_z_pac = 22

# Esquina (3, 3)
# ubi_x_pac = 141
# ubi_z_pac = 172
# Esquina (6, 9)
# ubi_x_pac = 276
# ubi_z_pac = 397
velocidad_pac = 0


# UBICACION DEL GHOST1
ubi_x_g1 = 396
ubi_z_g1 = 22
velocidad_g1 = 0

# UBICACION DEL GHOST2
ubi_x_g2 = 21
ubi_z_g2 = 442
velocidad_g2 = 0

# UBICACION DEL GHOST3
ubi_x_g3 = 396
ubi_z_g3 = 442
velocidad_g3 = 0

# UBICACION DEL GHOST4
ubi_x_g4 = 321
ubi_z_g4 = 217
velocidad_g4 = 0


# Tamaño de la pantalla
screen_width = 750
screen_height = 800

#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X = 210.0
EYE_Y = 425.0
EYE_Z = 232.0
CENTER_X = 210.0  # Center along positive x-axis
CENTER_Y = 0.0
CENTER_Z = 232.0  # Center along positive z-axis
UP_X = 0  # Looking down along positive y-axis
UP_Y = 0
UP_Z = -1
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500

#Dimension del plano
DimBoardHor = 420
DimBoardVer = 465

#offset de los posibles caminos del pacman con respecto al punto (0, 0, 0)
offsetX = 20
offsetZ = 21

#Variables asociados a los objetos de la clase Cubo
pacman = []
ghosts = []
ghost_inteligente = []

#Arreglo para el manejo de texturas
textures = []

pacman_text = "textures/Pac8bit.bmp"
#map_text = "textures/red_lines_map.bmp"
map_text = "textures/clean_map.bmp"
ghost_red = "textures/Blinky8bit.bmp"
ghost_pink = "textures/Pinky8bit.bmp"
ghost_cyan = "textures/Inky8bit.bmp"
ghost_orange = "textures/Clyde-sue-tim-8bit.bmp"

# Matriz de tipos de adyacencias
matriz = [
    # 1  2   3   4    5   6  7    8  9   10
    [10, 0,  21, 0,  11, 10, 0,  21, 0,  11],
    [24, 0,  25, 21, 23, 23, 21, 25, 0,  22],
    [12, 0,  22, 12, 11, 10, 13, 24, 0,  13],
    [0,  0,  0,  10, 23, 23, 11, 0,  0,  0],
    [0,  0,  24, 22, 0,  0,  24, 22, 0,  0],
    [0,  0,  0,  24, 0,  0,  22, 0,  0,  0],
    [10, 0,  25, 23, 11, 10, 23, 25, 0,  11],
    [12, 11, 24, 21, 23, 23, 21, 22, 10, 13],
    [10, 23, 13, 12, 11, 10, 13, 12, 23, 11],
    [12, 0,  0,  0,  23, 23, 0,  0,  0,  13]
]

# Array con la el id a posibles caminos 
# up 0
# right 1
# down 2
# left 3
interId = {
    10: [1, 2],
    11: [2, 3],
    12: [0, 1],
    13: [0, 3],
    21: [1, 2, 3],
    22: [0, 2, 3],
    23: [0, 1, 3],
    24: [0, 1, 2],
    25: [0, 1, 2, 3]
}

#Arrays con coordenadas de las fila y columnas en px
X1 = [0, 30, 75, 120, 165, 210, 255, 300, 345, 375]
Z1 = [0, 60, 105, 150, 195, 240, 285, 330, 375, 420]

#Array con la posición en px de las columnas, de tamaño 376, de índice 0 a 375
allCol = [-1] * 376
index = 0
for i in range(len(allCol)):
    if i == X1[index]:
        allCol[i] = index
        index += 1

#Array con la posición en px de las filas, de tamaño 421, de índice 0 a 420
allFil = [-1] * 421
index = 0
for i in range(len(allFil)):
    if i == Z1[index]:
        allFil[i] = index
        index += 1

    

pygame.init()



def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image,"RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D) 

def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Pac-Man")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    Texturas(map_text)   
    Texturas(pacman_text)
    Texturas(ghost_red)
    Texturas(ghost_pink)
    Texturas(ghost_cyan)
    Texturas(ghost_orange)


    # Creamos los objetos que representan los elementos del juego
    # Pacman
    pacman.append(Pacman(ubi_x_pac, ubi_z_pac, velocidad_pac, DimBoardHor, DimBoardVer, allCol, allFil, matriz, interId))
    # Fantasmas tontos
    ghosts.append(Ghost(ubi_x_g1, ubi_z_g1, velocidad_g1, DimBoardHor, DimBoardVer, allCol, allFil, matriz, interId))
    ghosts.append(Ghost(ubi_x_g2, ubi_z_g2, velocidad_g2, DimBoardHor, DimBoardVer, allCol, allFil, matriz, interId))
    ghosts.append(Ghost(ubi_x_g3, ubi_z_g3, velocidad_g3, DimBoardHor, DimBoardVer, allCol, allFil, matriz, interId))
    #Fantasma inteligente
    ghost_inteligente.append(Ghost_inteligente(ubi_x_g4, ubi_z_g4, velocidad_g4, DimBoardHor, DimBoardVer, allCol, allFil, matriz, interId))

    
    
def PlanoTexturizado():
    #Activate textures
    glColor3f(1.0,1.0,1.0)
    glEnable(GL_TEXTURE_2D)
    #front face
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(0, 0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(0, 0, DimBoardVer)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(DimBoardHor, 0, DimBoardVer)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(DimBoardHor, 0, 0)
    glEnd()              
    glDisable(GL_TEXTURE_2D)
    
    
def display(code):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    PlanoTexturizado()
    posX = 0
    posZ = 0
    for obj in pacman:
        obj.drawCube(textures,1)
        obj.update(code)
        posX = obj.positionPacmanX()
        posZ = obj.positionPacmanZ()
    
    # Accedemos a la textura correspondiente
    i = 2
    for obj in ghosts:
        obj.drawCube(textures,i)
        obj.update(code)
        i += 1
        
    for obj in ghost_inteligente:
        obj.drawCube(textures, 5)
        obj.update(code, posX, posZ)
        

done = False
code = ""
Init()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                code = "u"
            if event.key == pygame.K_RIGHT:
                code = "r"
            if event.key == pygame.K_DOWN:
                code = "d"
            if event.key == pygame.K_LEFT:
                code = "l"
            if event.key == pygame.K_ESCAPE:
                done = True

    display(code)

    pygame.display.flip()
    pygame.time.wait(8)

pygame.quit()
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
from Cubo import Cubo

import sys
sys.path.append('..')
from Ghost import Ghost

key = ""

ghost = object

screen_width = 800
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
DimBoardHor = 419
DimBoardVer = 464


#Variables asociados a los objetos de la clase Cubo
#cubo = Cubo(DimBoard, 1.0)
cubos = []
ncubos = 1

#Variables para el control del observador
theta = 0.0
radius = 300

#Arreglo para el manejo de texturas
textures = []
filename1 = r"C:\Users\makreb\OneDrive\Documentos\scol\pacmanglobal\pac-man\Original_PacMan.png"
filename2 = r"C:\Users\makreb\OneDrive\Documentos\scol\pacmanglobal\pac-man\mapa.bmp"

matriz = [
    # 1  2   3   4    5   6  7    8  9   10
    [10, 0,  21, 0,  11, 10, 0,  21, 0,  11],
    [24, 0,  25, 21, 23, 23, 21, 25, 0,  22],
    [12, 0,  22, 12, 11, 10, 13, 24, 0,  13],
    [0,  0,  0,  10, 23, 23, 11, 0,  0,  0],
    [0,  0,  24, 22, 0,  0,  24, 22, 0,  0],
    [0,  0,  0,  24, 0,  0,  22, 0,  0,  0],
    [0,  0,  25, 23, 11, 10, 23, 25, 0,  11],
    [12, 11, 24, 21, 23, 23, 21, 22, 10, 13],
    [10, 23, 13, 12, 11, 10, 13, 12, 23, 11],
    [12, 0,  0,  0,  23, 23, 0,  0,  0,  13]
]

X1 = [0, 30, 75, 120, 165, 210, 251, 300, 345, 375]
Z1 = [0, 62, 105, 150, 195, 240, 385, 330, 375, 420]

allCol = [-1] * 375
index = 0
for i in range(len(allCol)):
    if i == X1[index]:
        allCol[i] = index
        index += 1

allFil = [-1] * 420
index = 0
for i in range(len(allFil)):
    if i == Z1[index]:
        allFil[i] = index
        index += 1

pygame.init()

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(0.5,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(0.0,0.0,0.0)
    glEnd()
    
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    
    #Y axis in green
    glColor3f(0.0,0.5,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,0,0.0)
    glEnd()
    
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    
    #Z axis in blue
    glColor3f(0.0,0.0,0.5)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,0.0)
    glEnd()
    
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,0.0)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    
    
    glLineWidth(1.0)

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
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    Texturas(filename1)
    Texturas(filename2)
    
    for i in range(ncubos):
        cubos.append(Cubo(DimBoardHor, DimBoardVer, 1.0, X1, Z1, allCol, allFil, matriz))

    cubos.append(Ghost(DimBoardHor, DimBoardVer, 1.0, X1, Z1, allCol, allFil, matriz))


#Se mueve al observador circularmente al rededor del plano XZ a una altura fija (EYE_Y)
def lookat():
    global EYE_X
    global EYE_Z
    global radius
    EYE_X = radius * (math.cos(math.radians(theta)) + math.sin(math.radians(theta)))
    EYE_Z = radius * (-math.sin(math.radians(theta)) + math.cos(math.radians(theta)))
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    #glutPostRedisplay()
    
def Plano():
    #Se dibuja el plano gris
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    # glVertex3d(-DimBoard, 0, -DimBoard)
    # glVertex3d(-DimBoard, 0, DimBoard)
    # glVertex3d(DimBoard, 0, DimBoard)
    # glVertex3d(DimBoard, 0, -DimBoard)
    
    glVertex3d(-DimBoardHor, 0, -DimBoardHor)
    glVertex3d(-DimBoardHor, 0, DimBoardHor)
    glVertex3d(DimBoardHor, 0, DimBoardHor)
    glVertex3d(DimBoardHor, 0, -DimBoardHor)
    
    glEnd()   
    
def PlanoTexturizado():
    #Activate textures
    glColor3f(1.0,1.0,1.0)
    glEnable(GL_TEXTURE_2D)
    #front face
    glBindTexture(GL_TEXTURE_2D, textures[1])
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
    Axis()
    #Plano()
    PlanoTexturizado()
    #Se dibuja cubos
    #cubo.draw()
    #cubo.Update()
    for obj in cubos:
        #obj.draw()
        obj.drawCube(textures,0)
        keys = pygame.event.get()
        obj.update(code)
    """ ghost.drawCube(textures, 0)
    keys = pygame.event.get()
    ghost.update(0) """

done = False
Init()
while not done:
    code = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                code = "r"
            if event.key == pygame.K_LEFT:
                code = "l"
            if event.key == pygame.K_UP:
                code = "u"
            if event.key == pygame.K_DOWN:
                code = "d"
            if event.key == pygame.K_ESCAPE:
                done = True

    display(code)

    pygame.display.flip()
    pygame.time.wait(5)

pygame.quit()
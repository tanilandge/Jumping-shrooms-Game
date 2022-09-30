import math
import pygame
import os
import random
import time
import sys

WIDTH = 550
HEIGHT = 643
FPS = 64
PLAYER_STARTING_COORDINATES = 595
FONTNAME = 'freesansbold.ttf'
COLOUR =  (225, 215, 191)
BLACK = (0, 0, 0)
PINK = (255, 182, 193)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy birds ig')
clock = pygame.time.Clock()

# set up asset folders
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, 'img')
bg = pygame.image.load(os.path.join(imgFolder, "bg_shroom.png")).convert()
playerImg = pygame.image.load(os.path.join(imgFolder, 'p3_front.png')).convert() 
playerImg2 = pygame.image.load(os.path.join(imgFolder, 'p3_jump.png')).convert()
pipesBottomImg = pygame.image.load(os.path.join(imgFolder, 'bottomShroom3.png')).convert()
pipesTopImg = pygame.image.load(os.path.join(imgFolder, 'topShroom3.png')).convert()
pygame.display.flip()

# set up superclass sprite
class Sprite:
    def __init__(self, x, y, spriteImg1, spriteImg2):
        pygame.sprite.Sprite.__init__(self)
        self.image = spriteImg1
        self.image2 = spriteImg2
        self.image.set_colorkey((0, 0, 0))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Pipes(Sprite, pygame.sprite.Sprite):
    def __init__(self, x, y, spriteImg1, spriteImg2):
        Sprite.__init__(self, x, y, spriteImg1, spriteImg2)
        self.x = x
        self.y = y
        self.listOfPipes = []
        self.namesOfPipes = [["bottomShroom1.png", "topShroom1.png"], ["bottomShroom2.png", "topShroom2.png"], ["bottomShroom3.png", "topShroom3.png"],  ["bottomShroom4.png", "topShroom4.png"]]
        self.pipesCoords = [[105, 531], [125, 551], [62, 487], [160, 585]]

    def getPipesImage(self, item):  
        pipesBottomImg = pygame.image.load(os.path.join(imgFolder, item[0])).convert()
        pipesTopImg = pygame.image.load(os.path.join(imgFolder, item[1])).convert()
        return pipesBottomImg, pipesTopImg

    def checkIfThereWerePreviousPipes(self):
        if len(self.listOfPipes) > 0:
            return True
        else:
            return False
        
    def createPipes(self, numberOfPipes):
        prevPipes = self.checkIfThereWerePreviousPipes()
        if prevPipes:
            pipeX, pipeY = self.listOfPipes[-1].getPipesCoordinates()
            self.x = pipeX + 400
        
        for count in range(0, numberOfPipes):
            item = random.randint(0, len(self.namesOfPipes) - 1)
            pipesBottomImg, pipesTopImg = self.getPipesImage(self.namesOfPipes[item])
            bottomPipes = BottomPipe(self.x, self.pipesCoords[item][1], pipesTopImg, pipesBottomImg)
            topPipes = TopPipe(self.x, self.pipesCoords[item][0], pipesTopImg, pipesBottomImg)
            allSprites.add(bottomPipes)
            allSprites.add(topPipes)
            self.listOfPipes.append(bottomPipes)
            self.listOfPipes.append(topPipes)
            self.x += 400 
    
    def movePipesForward(self):
        for item in self.listOfPipes:
            pipeX, pipeY = item.getPipesCoordinates()
            pipeX -= 1
            item.setPipesCoordinates(pipeX, pipeY)

    def checkIfPipeIsNoLongerOnScreen(self):
        PipeX, PipeY = self.listOfPipes[0].getPipesCoordinates()
        if PipeX <= -100:
            pipes.createPipes(1)
            allSprites.remove(self.listOfPipes[0])
            self.listOfPipes.remove(self.listOfPipes[0])

    def getCurrentPipe(self):
        return self.listOfPipes[0], self.listOfPipes[1]
        return p1b.y, p2t.y
        
# set up pipes subclass 
class BottomPipe(Pipes, pygame.sprite.Sprite):
    def __init__(self, x, y, topPipeImg, bottomPipeImg):
        Pipes.__init__(self, x, y, topPipeImg, bottomPipeImg)
        self.image = bottomPipeImg
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def getPipesCoordinates(self):
        return self.x, self.y

    def setPipesCoordinates(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)

class TopPipe(Pipes, pygame.sprite.Sprite):
    def __init__(self, x, y, topPipeImg, bottomPipeImg):
        Pipes.__init__(self, x, y, topPipeImg, bottomPipeImg)
        self.image = topPipeImg
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def getPipesCoordinates(self):
        return self.x, self.y

    def setPipesCoordinates(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        
# set up subclass Player to inherit from the superclass 'sprite'
class Player(Sprite, pygame.sprite.Sprite):
    def __init__(self, x, y, spriteImg1, spriteImg2):
        Sprite.__init__(self, x, y, spriteImg1, spriteImg2)
        spriteImg1 = playerImg
        spriteImg2 = playerImg2
        self.score = 0
        self.heightJumped = 0

    def changeSpriteImg(self, jumpImg):
        if jumpImg:
            self.image = playerImg2
        else:
            self.image = playerImg
        self.image.set_colorkey((0, 0, 0))

    def moveUp(self, xValueOfSin):  # move player sprite upwards
        self.y = playerInitialPos[-1] - (90 * math.sin(math.radians(xValueOfSin)))
        self.heightJumped = self.y
        self.rect.center = (self.x, self.y)

    def moveDown(self, xValueOfCos):  # move player sprite downwards
        self.y = HEIGHT - ((HEIGHT-self.heightJumped) * math.cos(math.radians(xValueOfCos)))
        self.rect.center = (self.x, self.y)

    def getCoordinates(self):
        return self.x, self.y

    def isDead(self, pipes, gameStarted):
        playerXValue, playerYValue = self.getCoordinates()
        bottomPipe, topPipe = pipes.getCurrentPipe()
        if gameStarted:
            if self.rect.colliderect(bottomPipe.rect) or self.rect.colliderect(topPipe.rect) or self.y >= 595:
                return True
        return False
    
    def increaseScore(self):
        playerX, playerY = self.getCoordinates()
        bottomPipe, topPipe = pipes.getCurrentPipe()
        bottomPipeX, bottomPipeY = bottomPipe.getPipesCoordinates()
        topPipeX, topPipeY = topPipe.getPipesCoordinates()
        if (playerX + 34) == (bottomPipeX - 103) or (playerX + 34) == (topPipeX - 103):
            return True
        return False
            
def game():
    done = False
    playerCurrentlyMovingUp = False
    playerCurrentlyMovingDown = False
    gameStarted = False
    timeDelay = 0

    while not done :
        dt = clock.tick(FPS) / 1000
        timeDelay += + dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
        pygame.init()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            gameStarted = True

            playerCurrentlyMovingUp = True
            playerInitialPos.append(player.y)
            xValueOfSin = 0

        if playerCurrentlyMovingUp == True and player.isDead(pipes, gameStarted) == False: # and timeDelay > 0.001
            player.changeSpriteImg(True)
            player.moveUp(xValueOfSin)
        
            if (playerInitialPos[-1] - player.y) >= 90:
                playerCurrentlyMovingUp = False
                playerInitialPos.pop()
                xValueOfSin = 0       #player has finished moving up so reset x
            else:
                xValueOfSin += 2.5
            xValueOfCos = 0 #player is no longer moving down so reset x
    
        if player.y < PLAYER_STARTING_COORDINATES and playerCurrentlyMovingUp == False and gameStarted == True and player.isDead(pipes, gameStarted) == False: #and timeDelay > 0.01
            player.changeSpriteImg(False)
            playerCurrentlyMovingDown == True
            player.moveDown(xValueOfCos)
            xValueOfCos += 1

        if player.y >= PLAYER_STARTING_COORDINATES: #keeeps player on the floor
            player.y = PLAYER_STARTING_COORDINATES

        if player.y < 45: #keeps player for going up out ofthe screen
            player.y = 45
            playerCurrentlyMovingUp = False

        pipes.movePipesForward()
        pipes.checkIfPipeIsNoLongerOnScreen()
        increaseScore = player.increaseScore()
        dead = player.isDead(pipes, gameStarted)

        if dead == False and increaseScore == True:
            player.score += 1

        allSprites.update()
        screen.blit(bg, (0, 0))
        font = pygame.font.Font(FONTNAME, 40)
        text = 'Score:' + str(player.score)
        textSurface = font.render(text, True, BLACK)
        textRect = textSurface.get_rect()
        textRect.center = (450, 60)
        screen.blit(textSurface, textRect)

        if dead == False:
            allSprites.draw(screen)

        if dead == True:
            pygame.draw.rect(screen, PINK, pygame.Rect(20, 250, 520, 160))
            pygame.draw.rect(screen, BLACK, pygame.Rect(20, 250, 520, 160), 2)
            text = 'You died'
            textSurface = font.render(text, True, BLACK)
            textRect = textSurface.get_rect()
            textRect.center = (275, 330)
            screen.blit(textSurface, textRect)
            text = 'Press X to quit or press P to play again'
            font = pygame.font.Font(FONTNAME, 20)
            textSurface = font.render(text, True, BLACK)
            textRect = textSurface.get_rect()
            textRect.center = (275, 380)
            screen.blit(textSurface, textRect)
            keys1 = pygame.key.get_pressed()

            if keys1[pygame.K_x]:
                done = True
            if keys1[pygame.K_p]:
                os.system("game.py")
                done = True

        pygame.init()
        pygame.display.flip()
    
#set up sprites
player = Player(50, 300, playerImg, playerImg2)
pipes = Pipes(500, 488, pipesTopImg, pipesBottomImg)

allSprites = pygame.sprite.Group()
allSprites.add(player)
pipes.createPipes(3)

xValueOfCos = 0
xValueOfSin = 0
playerInitialPos = [player.y]

game()
pygame.quit()




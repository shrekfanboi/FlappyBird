import random
import pygame,sys
from pygame.locals import QUIT,K_SPACE,K_ESCAPE,K_UP,KEYDOWN

#Global Variables
FPS= 32
SCREENWIDTH= 289
SCREENHEIGHT= 511
GROUNDY = SCREENHEIGHT* 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'
screen=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))


def welcomeScreen():

    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT- GAME_SPRITES['player'].get_height())/2
    messagex = int(SCREENWIDTH- GAME_SPRITES['message'].get_width())/2
    messagey = int(SCREENHEIGHT*0.1)
    basex = 0
    pygame.time.wait(1000)
    screen.blit(GAME_SPRITES['background'],(0,0))
    screen.blit(GAME_SPRITES['player'],(playerx,playery))
    screen.blit(GAME_SPRITES['message'],(messagex,messagey))
    screen.blit(GAME_SPRITES['base'],(basex,GROUNDY))
   
           

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
            return
        '''else:
            screen.blit(GAME_SPRITES['background'],(0,0))
            screen.blit(GAME_SPRITES['player'],(playerx,playery))
            screen.blit(GAME_SPRITES['message'],(messagex,messagey))
            screen.blit(GAME_SPRITES['base'],(basex,GROUNDY))'''
    pygame.display.update()
    fpsClock.tick(FPS)


def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    #create two pipes
    newPipe1 = getRandomPipe()#2 pipes
    newPipe2 = getRandomPipe()#2 pipes

    upperPipe=[{'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
               {'x':SCREENWIDTH+200 + (SCREENWIDTH/2), 'y':newPipe2[0]['y']}]
    lowerPipe=[{'x':SCREENWIDTH+200,'y':newPipe1[1]['y']},
               {'x':SCREENWIDTH+200 + (SCREENWIDTH/2), 'y':newPipe2[1]['y']}]

    pipeVelx = -4
    playerVely = -9
    playerMaxVel = 10
    playerMinVel = -8
    playerAcc = 1

    playerFlapAccv = -8
    playerFlapped = False
    
    
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVely = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx,playery,upperPipe,lowerPipe)
        if crashTest:
            return
        playerMid = playerx + GAME_SPRITES['player'].get_width()/2
        #if player's mid point crosses the pipe, increase point
        for pipe in upperPipe:
            pipeMid = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if (pipeMid <= playerMid) and (playerMid < pipeMid+4):
                score += 1
                #print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()
        if playerVely < playerMaxVel and not playerFlapped:
            playerVely += playerAcc
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        #change the y cordinates of bird according to the velocity
        playery = playery + min(playerVely, GROUNDY - playerHeight - playery)

        #move pipes to the left
        for upperpipe, lowerpipe in zip(upperPipe, lowerPipe):
            upperpipe['x'] += pipeVelx
            lowerpipe['x'] += pipeVelx
        #remove pipes if they leave the screen
        if upperPipe[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipe.pop(0)
            lowerPipe.pop(0)
        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipe[0]['x']<5:
            newPipe = getRandomPipe()
            upperPipe.append(newPipe[0])
            lowerPipe.append(newPipe[1])

        # Bliting all the elements on the screen
        screen.blit(GAME_SPRITES['background'],(0,0))
        for upperpipe, lowerpipe in zip(upperPipe, lowerPipe):
            screen.blit(GAME_SPRITES['pipe'][0],(lowerpipe['x'],lowerpipe['y']))
            screen.blit(GAME_SPRITES['pipe'][1],(upperpipe['x'],upperpipe['y']))
        screen.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        screen.blit(GAME_SPRITES['player'],(playerx,playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()

        Xoffset = (SCREENWIDTH - width)/2
        for digit in myDigits:
            screen.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        fpsClock.tick(FPS)
        

def isCollide(playerx,playery,upperPipe,lowerPipe):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipe:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipe:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

        
        
    return False



def getRandomPipe():
    #generates random pipes"
    pipeheight = GAME_SPRITES['pipe'][1].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT- GAME_SPRITES['base'].get_height() - (1.2*offset)))
    pipex = SCREENWIDTH + 10
    y1 = pipeheight - y2 + offset
    #upper,lower
    pipe = [{'x':pipex, 'y':-y1},{'x':pipex, 'y':y2}]
    return pipe                                   
    
       

if __name__=="__main__":

    pygame.init()
    fpsClock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    #Game Sprites
    GAME_SPRITES['numbers']=(
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
        )
    GAME_SPRITES['message']=(pygame.image.load('gallery/sprites/message.png'))
    GAME_SPRITES['base']=(pygame.image.load('gallery/sprites/base.png'))
    GAME_SPRITES['pipe']=(pygame.image.load('gallery/sprites/pipe.png').convert_alpha(),
                       pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180))

    #Game Sounds
    GAME_SOUNDS['die']=(pygame.mixer.Sound('gallery/audio/die.wav'))
    GAME_SOUNDS['hit']=(pygame.mixer.Sound('gallery/audio/hit.wav'))
    GAME_SOUNDS['point']=(pygame.mixer.Sound('gallery/audio/point.wav'))
    GAME_SOUNDS['swoosh']=(pygame.mixer.Sound('gallery/audio/swoosh.wav'))
    GAME_SOUNDS['wing']=(pygame.mixer.Sound('gallery/audio/wing.wav'))

    #Background and player
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()
    #main loop
    while True:
         welcomeScreen()
         maingame()
    

    
    

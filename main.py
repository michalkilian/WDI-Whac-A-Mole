import  random
from classes import *
import os


pygame.mixer.pre_init(44100, 16, 2, 4096)
# Const variables
width = 800
height = 600
FPS = 100
black = (0,0,0)
white = (255,255,255)
gray = (47,79,79)
green = (0,255,0)
darkGreen = (25,160,60)
red = (255,0,0)
blue = (0,0,255)
maps = ["background.png","background2.png","background3.jpg"]
mapsHoles = [9,3,11]

gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder,"img")
musicFolder = os.path.join(gameFolder,"music")

pygame.init()

#window var and music
gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('Whac-A-Mole')
pygame.mixer.init()
pygame.mixer.music.set_volume(0.1)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

#objects init

cursors = pygame.sprite.Group()
hammer = Cursor(os.path.join(imgFolder, "hammer.gif"))
hammer_hit = Cursor(os.path.join(imgFolder, "hammer_hit.gif"))
menuCursor = Cursor(os.path.join(imgFolder, "cursor.png"))
cursors.add(hammer,hammer_hit,menuCursor)

mole = Mole(os.path.join(imgFolder,"mole.png"))
moleHit = Mole(os.path.join(imgFolder,"moleHit.png"))

menuBackground = Background(os.path.join(imgFolder,"menu.jpg"))
optionsBacground = Background(os.path.join(imgFolder,"options.png"))
winBackground = Background(os.path.join(imgFolder,"gameWin.png"))
loseBackground = Background(os.path.join(imgFolder,"gameLose.png"))
heart = pygame.image.load(os.path.join(imgFolder,"heart.png"))

hitSound = pygame.mixer.Sound(os.path.join(musicFolder,"hit.wav"))
swingSound = pygame.mixer.Sound(os.path.join(musicFolder,"swing.wav"))

startGameButton = Buttons(140,75,330,307)
optionButton = Buttons(140,75,330,400)
diffUpButton = Buttons(25,38,463,160)
diffDownButton = Buttons(25,38,305,160)
mapUpButton = Buttons(25,38,463,258)
mapDownButton = Buttons(25,38,305,258)
backButton = Buttons(100,57,338,375)
playAgainButton = Buttons(140,75,313,268)
returnToMenuButton = Buttons(140,75,313,375)

# buttons = pygame.sprite.Group()
# buttons.add(playAgainButton,returnToMenuButton)


#defining screen messages
def screenMessage(msg, color,mWidtg, mHeight):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [mWidtg, mHeight])

#main loop def
def gameLoop():

    #in game variables
    chosenMap = 0
    holes = [[(175,138),(390,138),(620,138),(175,270),(390,270),(620,270),(175,400),(390,405),(615,405)],[(175,138),(620,138),(390,405)],[(130,130),(310,130),(495,130),(690,130),(210,295),(410,295),(603,295),(130,440),(310,440),(505,440),(695,440)]]

    gameExit = False
    isMenu = True
    gameOver = False
    isGame = False
    gameStart = False
    isOptions = False
    isMoleHitted = False
    victory = False

    diff = 1
    lives = 3
    score = 0

    mousePosition = (width/2,height/2)
    pressedTime = 10
    moleHitAnimation = 30

    isMusicPlaying = False

    #program loop
    while not gameExit:
        #hiding cursor
        pygame.mouse.set_visible(False)

        #main menu loop
        while isMenu:

            if isMusicPlaying == False:
                pygame.mixer.music.load(os.path.join(musicFolder,"Menu.mp3"))
                pygame.mixer.music.play()
                isMusicPlaying = True

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(os.path.join(musicFolder,"MenuLoop.mp3"))
                pygame.mixer.music.play(-1)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    gameExit = True
                    isMenu = False

                if event.type == pygame.MOUSEMOTION:
                    mousePosition = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickStart = startGameButton.rect.collidepoint(mousePosition)
                    clickOptions = optionButton.rect.collidepoint(mousePosition)

                    if clickStart:
                        isMenu = False
                        isGame = True
                        gameStart = True
                        isMusicPlaying = False

                    elif clickOptions:
                        isMenu = False
                        isOptions = True

            menuCursor.update(mousePosition)
            gameDisplay.fill(black)
            gameDisplay.blit(menuBackground.image, menuBackground.rect)
            menuCursor.draw(gameDisplay)

            pygame.display.update()

        #option menu loop
        while isOptions:

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(os.path.join(musicFolder,"MenuLoop.mp3"))
                pygame.mixer.music.play(-1)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    gameExit = True
                    isOptions = False

                if event.type == pygame.MOUSEMOTION:
                    mousePosition = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    diffUp = diffUpButton.rect.collidepoint(mousePosition)
                    diffDown = diffDownButton.rect.collidepoint(mousePosition)
                    mapUp = mapUpButton.rect.collidepoint(mousePosition)
                    mapDown = mapDownButton.rect.collidepoint(mousePosition)
                    back = backButton.rect.collidepoint(mousePosition)

                    if diffUp and diff < 3:
                        diff +=1
                    elif diffDown and diff > 1:
                        diff -=1
                    elif mapUp and chosenMap < 2:
                        chosenMap +=1
                    elif mapDown and chosenMap > 0:
                        chosenMap -= 1
                    elif back:
                        isOptions = False
                        isMenu = True

            menuCursor.update(mousePosition)

            gameDisplay.fill(black)
            gameDisplay.blit(optionsBacground.image,optionsBacground.rect)
            menuCursor.draw(gameDisplay)

            screenMessage(str(diff),red,380,165)
            screenMessage(str(chosenMap+1),red,380,263)

            pygame.display.update()

        #main game loop
        while isGame:

            if gameStart:
                gameBackground = Background(os.path.join(imgFolder, maps[chosenMap]))
                maxMoleTime = (4 - diff) * 30
                moleHole = random.randint(0, mapsHoles[chosenMap] - 1)
                mole.update(holes[chosenMap][moleHole])
                if lives == 3 and diff == 3:
                    lives -= 2
                    maxMoleTime +=15
                moleTime = -200
                gameStart = False

            if not isMusicPlaying:
                pygame.mixer.music.load(os.path.join(musicFolder,"game.mp3"))
                pygame.mixer.music.play(-1)
                isMusicPlaying = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    isGame = False
                if event.type == pygame.MOUSEMOTION:
                    mousePosition = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressedTime = 0
                    hit = pygame.sprite.spritecollide(mole,cursors,False)
                    if hit and moleTime<maxMoleTime:
                        hitSound.play()
                        moleHit.update(holes[chosenMap][moleHole])
                        moleHitAnimation=0
                        score +=1
                        moleTime = maxMoleTime
                        isMoleHitted = True
                    else:
                        swingSound.play()

            hammer.update(mousePosition)
            hammer_hit.update(mousePosition)
            gameDisplay.fill(black)
            gameDisplay.blit(gameBackground.image,gameBackground.rect)
            screenMessage("Your score {}".format(str(score)), red,10, 550)

            for i in range(lives):
                gameDisplay.blit(heart,(550+75*i,500))

            if(moleTime>=maxMoleTime):
                if isMoleHitted==False:
                    lives-=1
                moleTime = -1*maxMoleTime
                moleHole = random.randint(0,mapsHoles[chosenMap]-1)
                mole.update(holes[chosenMap][moleHole])
                isMoleHitted =False
            elif moleTime >0:
                moleTime+=1
                mole.draw(gameDisplay)
            else:
                moleTime +=1

            if(lives == 0 or score == 25):
                gameOver = True
                isGame = False
                if score == 25:
                    victory = True
                cursors.update((0,0))

            if(pressedTime < 10):
                if moleHitAnimation<30:
                    moleHitAnimation+=1
                    moleHit.draw(gameDisplay)
                hammer_hit.draw(gameDisplay)
                pressedTime +=1
            else:
                if moleHitAnimation < 30:
                    moleHitAnimation += 1
                    moleHit.draw(gameDisplay)
                hammer.draw(gameDisplay)
            pygame.display.update()

            clock.tick(FPS)

        while gameOver:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(os.path.join(musicFolder,"game.mp3"))
                pygame.mixer.music.play(-1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.MOUSEMOTION:
                    mousePosition = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    playAgain = playAgainButton.rect.collidepoint(mousePosition)
                    returnToMenu = returnToMenuButton.rect.collidepoint(mousePosition)
                    if playAgain:
                        gameOver = False
                        isGame = True
                        lives = 3
                        score = 0
                        pressedTime = 10
                        moleHitAnimation = 30
                        victory = False
                    elif returnToMenu:
                        gameOver = False
                        isMenu = True
                        lives = 3
                        score = 0
                        pressedTime = 10
                        moleHitAnimation = 30
                        victory = False
            menuCursor.update(mousePosition)
            gameDisplay.fill(black)
            if victory:
                gameDisplay.blit(winBackground.image, winBackground.rect)
            else:
                gameDisplay.blit(loseBackground.image,loseBackground.rect)
            screenMessage("Your score: {}".format(str(score)), red, 300, 200)
            menuCursor.draw(gameDisplay)
            pygame.display.update()
gameLoop()

pygame.quit()

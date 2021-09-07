import pygame
import random
import sys

pygame.init()
class Bomb:
    def __init__(self):# this is the init function, in this function the x,y and speed of the bomb will initialise
        self.x = random.randint(10,780)
        self.y = random.randint(10,400)
        self.speed = [random.randint(1,5),random.randint(1,5)]
        self.radius = 5
        if random.randint(0,1000) > 500:# the 'RightMove' and 'LeftMove' are boolean variable values
            self.RightMove = True
        else:
            self.RightMove = False
        if random.randint(0,1000) > 500:
            self.TopMove = True
        else:
            self.TopMove = False
    def DrawBomb(self):
        self.image = pygame.image.load("bomb.jpg")# draw the bomb
        screen.blit(self.image,[self.x,self.y])
    def Move(self):
        if self.RightMove == True:# Move the bomb
            self.x += self.speed[0]
        else:
            self.x -= self.speed[0]
        if self.TopMove == True:
            self.y += self.speed[1]
        else:
            self.y -= self.speed[1]
    def Display(self):
        screen.blit(self.image,[self.x,self.y])# update the location of the bomb and draw it
    def AvoidOut(self):# avoid the bomb to move out of the window
        global Score
        if self.x < 1 or self.x > 770:
            self.RightMove = not self.RightMove
            Score += 1
        if self.y < 1 or self.y > 570:
            self.TopMove = not self.TopMove
            Score += 1
    def Detect(self):# this is a function to cacluate the distance to trump if he hit the bomb, his health value will decrease
        global Life
        self.R = (self.x+15-(x+30))**2+(self.y+15-(y+30))**2
        if self.R < 4200:
            Life -= 1

def AddBomb():  # when you score increase, more and more bombs will apear until there are ten bombs on the screen
    global BombNumber
    global Score
    if Score % 100 == 0 and Score <= 500:
        BombList.append(Bomb())
        BombNumber += 1
        BombList[BombNumber-1].DrawBomb()
        Score += 1

Score = 1
Life = 1000
Level = 1
BombNumber = 5
screen = pygame.display.set_mode([800,600])
plane = pygame.image.load("you.jpg")
GameOver = pygame.image.load("game_over.jpg")
clock = pygame.time.Clock()
clour = (217,231,249)
Black = (0,0,0)
White = (255,255,255)
Red = (225,127,80)
Black = (0,0,0)
x = 400
y = 400
STEP = 5
done = False

BombList = []           #the instantiated objects are stored in a list
for number in range(5):
    BombList.append(Bomb())
for item in BombList:
    item.DrawBomb()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

#key pressing
    keys = pygame.key.get_pressed()             #i learned this on github and google
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        x -= STEP
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        x += STEP
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        y -= STEP
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        y += STEP

    if x < 0:    #avoid the plane to fly outside the window
        x += STEP
    elif x > 740:
        x -= STEP
    if y < 0:
        y += STEP
    elif y > 540:
        y -= STEP

    screen.fill(clour)
    screen.blit(plane,[x,y])
    AddBomb()

    for item in BombList:
        item.Move()
        item.Display()
        item.AvoidOut()
        item.Detect()

    Font = pygame.font.Font('freesansbold.ttf', 24)         #the score is printed on the screen
    ScoreRender = Font.render('Your score: '+ str(Score),True,Black)
    TxtRender = Font.render('Health',True,Black)
    ScoreRect = ScoreRender.get_rect()
    TxtRect = TxtRender.get_rect()
    ScoreRect.center = (100,20)
    TxtRect.center = (350,20)
    pygame.display.set_caption("Trump vs bombs")
    screen.blit(ScoreRender,ScoreRect)
    screen.blit(TxtRender,TxtRect)
    pygame.draw.polygon(screen,Red,[(400,15),(400,25),(400+0.3*Life,25),(400+0.3*Life,15)],0) # the health value is printed on the screen
    pygame.display.flip()
    clock.tick(80)

    if Life < 0:
        while True: #if the health value is under 0 , the game ends
            screen.fill(Black)
            screen.blit(GameOver,[0,100])
            HighScoreTxt = open('high_score.txt', 'r+') # open the file to get the highest score
            HighScore = HighScoreTxt.read()
            try:
                int(HighScore)
            except:
                HighScore = int(0)
            if int(Score) > int(HighScore):
                HighScore = Score
                HighScoreTxt.seek(0)
                HighScoreTxt.truncate()
                HighScoreTxt.write(str(Score))
                HighScoreTxt.close()
            ScoreRect.center = (200,100)
            ScoreRender = Font.render('Your score: '+ str(Score),True,White)
            screen.blit(ScoreRender,ScoreRect)
            HighScoreRender = Font.render('Highest Score: ' + str(HighScore),True,White)
            HighScoreRect = HighScoreRender.get_rect()
            HighScoreRect.center = (200,150)
            screen.blit(HighScoreRender,HighScoreRect)

            pygame.display.flip()
            pygame.time.delay(5000)
            pygame.quit()
pygame.quit()           # game ends here

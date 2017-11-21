import pygame
import math
import random

# Define some colors

black = ( 0, 0, 0)
white = ( 255, 255, 255)
green = ( 0, 255, 0)
red = ( 255, 0, 0)
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)


class player:
    def __init__(self,sx,sy):
        self.score = 0
        self.dead = False
        self.x = sx
        self.y = sy
        self.angle = 0
        self.friction = 0.05
        self.velocityH = 0
        self.velocityV = 0
        self.vmax = 5
        self.velocity = 0
        self.I = 0
        self.shoot = pygame.mixer.Sound('shoot.wav')
        self.shoot.set_volume(0.1)
        self.death = pygame.mixer.Sound('death.wav')
        self.death.set_volume(0.2)

    def move(self):
        key = pygame.key.get_pressed()


        if key[pygame.K_w]:
            self.forward()
        if key[pygame.K_a]:
            self.angle +=5
        if key[pygame.K_d]:
            self.angle -=5
        if key[pygame.K_SPACE]:
            self.I +=1
            if self.I%5 == 0:
                bulletList.append(bullet(   (((math.sin(self.angle*math.pi/180)*15 + self.x),(math.cos(self.angle*math.pi/180)*15 + self.y))   ),  (self.angle*math.pi)/180  ))
                self.shoot.play()
                
        if self.I == 10:
            self.I = 0

        if not key[pygame.K_w]:
            if self.velocity > 0:
                self.velocity -= self.friction
                
            if self.velocityH < 0:
                self.velocityH += self.friction
            if self.velocityH > 0:
                self.velocityH -= self.friction
                
            if self.velocityV < 0:
                self.velocityV += self.friction
            if self.velocityV > 0:
                self.velocityV -= self.friction

        self.velocityH = math.sin((self.angle*math.pi)/180)*self.velocity
        self.velocityV = math.cos((self.angle*math.pi)/180)*self.velocity


        if self.x < 0:
            self.x = size[0]
        if self.x > size[0]:
            self.x = 0
        if self.y < 0:
            self.y = size[1]
        if self.y > size[1]:
            self.y = 0

        
        
        self.x += self.velocityH
        self.y += self.velocityV
        self.draw()

    def forward(self):
        if self.velocity < self.vmax:
            self.velocity += 0.05

##        self.velocityH = math.sin((self.angle*math.pi)/180)*self.velocity
##        self.velocityV = math.cos((self.angle*math.pi)/180)*self.velocity

            
        

        
    def draw(self):
        size = 15
        a1 = self.angle
        a2 = self.angle + 150
        a3 = self.angle - 150

        a1 = (a1*3.141)/180
        a2 = (a2*3.141)/180
        a3 = (a3*3.141)/180
        
        p1 = ((math.sin(a1)*size + self.x),(math.cos(a1)*size + self.y))
        p2 = ((math.sin(a2)*size + self.x),(math.cos(a2)*size + self.y))
        p3 = ((math.sin(a3)*size + self.x),(math.cos(a3)*size + self.y))
        pygame.draw.line(screen,white,p1,p2,3)
        pygame.draw.line(screen,white,p2,p3,3)
        pygame.draw.line(screen,white,p3,p1,3)

    def explode(self):
        self.death.play()
        self.dead = True

class bullet:
    def __init__(self,pos,sangle):
        self.x = pos[0]
        self.y = pos[1]
        self.angle = sangle
        

    def move(self):
        speed = 10
        self.x += math.sin(self.angle)*speed
        self.y += math.cos(self.angle)*speed

        self.draw()

        if (self.x < 0) or (self.x > size[0]) or (self.y < 0) or (self.y > size[1]):
            bulletList.remove(self)

    def draw(self):
        speed = 10
        p1 = ((math.sin(self.angle)*speed+self.x),math.cos(self.angle)*speed+self.y)
        p2 = ((math.sin(self.angle+math.pi)*speed+self.x),math.cos(self.angle + math.pi)*speed+self.y)

        pygame.draw.line(screen,white,p1,p2,1)

class asteroid:
    def __init__(self,sx,sy,ssize,sangle):
        self.I = 0
        self.x = sx
        self.y = sy
        self.size = ssize
        self.Points = []
        self.explode = pygame.mixer.Sound('explode.wav')
        self.explode.set_volume(0.3)
        if sangle == None:
            if (self.y > player1.y):
                self.angle = math.atan((self.x-player1.x)/(self.y-player1.y))
            else:
                self.angle = math.atan((self.x-player1.x)/(self.y-player1.y)) + math.pi
        else:
            self.angle = sangle
            

            
        self.speed = -2
        for I in range(0,6):
            a1 = float
            a1 = ((360/6) * I)*math.pi / 180
            self.Points.append((math.sin(a1)*self.size + self.x,(math.cos(a1)*self.size + self.y)))
        
    def move(self):
        self.I += 5
        for I in range(0,6):
            a1 = ((((360)/6) * I) + self.I)*math.pi / 180
            self.Points[I] = ((math.sin(a1)*self.size + self.x,(math.cos(a1)*self.size + self.y)))
            
        self.x += math.sin(self.angle)*self.speed
        self.y += math.cos(self.angle)*self.speed

        self.draw()

        if self.I > 6000:
            astList.remove(self)
            exit

        for I in range(0,len(bulletList)):
            if I < len(bulletList):
                if (math.sqrt((self.x - bulletList[I].x)*(self.x - bulletList[I].x) + (self.y - bulletList[I].y)*(self.y - bulletList[I].y)) < self.size):
                    if self.size > 24:                      
                        astList.append(asteroid(self.x + random.randrange(-self.size/2,self.size/2),self.y + random.randrange(-self.size/2,self.size/2),self.size/2,self.angle))
                        astList.append(asteroid(self.x + random.randrange(-self.size/2,self.size/2),self.y + random.randrange(-self.size/2,self.size/2),self.size/2,self.angle))
                        astList.append(asteroid(self.x + random.randrange(-self.size/2,self.size/2),self.y + random.randrange(-self.size/2,self.size/2),self.size/2,self.angle))
                    self.explode.play()
                    player1.score += 100
                    bulletList.remove(bulletList[I])
                    astList.remove(self)
                    exit
        if (math.sqrt((self.x - player1.x)*(self.x - player1.x) + (self.y - player1.y)*(self.y - player1.y)) < self.size) and (not player1.dead):
            player1.explode()
            
                    
                
            

        

        
    def draw(self):
        for I in range(0,len(self.Points)):
            if I < len(self.Points)-1:
                pygame.draw.line(screen,white,self.Points[I],self.Points[I+1])
            else:
                pygame.draw.line(screen,white,self.Points[I],self.Points[0])
                                 
        #pygame.draw.line(screen,white,(self.x,self.y),(player1.x,player1.y))
        
        
        
        

bulletList = []
astList = []
astNum = int
astNum = 40


myfont = pygame.font.SysFont("monospace", 15)

# Set the width and height of the screen [width,height]
size=[1280,720]
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Asteroids")


#Loop until the user clicks the close button.
done=False

player1 = player(size[0]/2,size[1]/2)
    

# Used to manage how fast the screen updates
clock=pygame.time.Clock()

# -------- Main Program Loop -----------
while done==False:
# ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop


    screen.fill(black)


    label = myfont.render(("SCORE: " + str(player1.score)), 1, (255,255,255))
    screen.blit(label, (0, 0))
    
    if not player1.dead:
        player1.move()
    else:
        label1 = myfont.render("Press space to try again", 1, (255,255,255))
        screen.blit(label1,(size[0]/2 - 100,size[1]/2))
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            player1.dead = False
            player1.score = 0
            player1.x = size[0]/2
            player1.y = size[1]/2

    if len(astList) < astNum:
        randAngle = random.randrange(0,360)*math.pi/180
        astList.append(asteroid(math.sin(randAngle)*size[0]+(size[0]/2),math.cos(randAngle)*size[1]+(size[1]/2),50,None))

    for I in range(0,len(astList)):
        if I < len(astList):
            astList[I].move()


    for I in range(0,len(bulletList)):
        if I < len(bulletList):
            bulletList[I].move()

    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # Limit to 20 frames per second
    clock.tick(60)

pygame.quit ()




 

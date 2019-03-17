import pygame,sys
from pygame.locals import *
from random import randint
import pygame.freetype
def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))
class MyObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=None
        self.rect=None
    def init(self,size,COLOR):
        self.image=pygame.Surface(size)
        self.image.fill(COLOR)
        self.rect=self.image.get_rect()
    def set_pos(self,x,y):
        self.rect.x,self.rect.y=x,y
class img_static(MyObject):
    def load(self,filename):
        self.image=pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
class Ball(img_static):
    def __init__(self,dx,dy,border):
        MyObject.__init__(self)
        self.dx=dx
        self.dy=dy
        self.border=border
    def Bounce(self,rect):
        if self.rect.right > rect.left + 2 and self.rect.left < rect.right - 2:
            self.dy *= -1
        if self.rect.bottom > rect.top + 2 and self.rect.top < rect.bottom - 2:
            self.dx *= -1
    def move(self):
        if self.rect.x< self.border.left or self.rect.right > self.border.right:
            self.dx *= -1
        if self.rect.y< self.border.top or self.rect.bottom > self.border.bottom:
            self.dy *= -1
        self.rect.move_ip(self.dx,self.dy)
    def set_vel(self,dx,dy):
        self.dx = dx
        self.dy = dy

class Block(MyObject):
    def __init__(self,myType):
        MyObject.__init__(self)
        self.type=myType
    def reduce(self,):
        if self.type not in (8,9):
            self.type -=1
    def CreateBlocks(self,n_row,n_col,size,offset,COLOR,group):
        for i in range(n_col*n_row):
            cur_x = (i%n_row)*offset[0]
            cur_y = (i//n_row)*offset[1]

            sprite=MyObject()
            sprite.init(size,COLOR)
            sprite.set_pos(cur_x,cur_y)

            group.add(sprite)
class Paddle(MyObject):
    def __init__(self,line_segment):
        MyObject.__init__(self)
        self.segment=line_segment
    def move(self,v):
        if self.segment[0] < self.rect.x and v < 0:
            self.rect.x += v
        if self.segment[1] > self.rect.x and v > 0:
            self.rect.x += v
size=w,h=600,400
COLOR_SET={
    'GOLD':(255,215,0),
    'BLACK':(0,0,0),
    'WHITE':(255,255,255),
}
pW,pH=64,8
bX,bY=0,0
STATE_SET={'GAME_OVER':-2,'PENDING':-1,'INIT':0,'RUN':1,'FINISH':2}
STATE=-1

#pygame 初始化
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('BASIC')
MainClock=pygame.time.Clock()
font_18=pygame.freetype.Font("C://windows//Fonts//msyh.ttc",18)
font_24=pygame.freetype.Font("C://windows//Fonts//msyh.ttc",24)
font_en=pygame.font.Font("C://windows//Fonts//msyh.ttc",18)
#对象 初始化
ball=Ball(1,1,pygame.Rect(0,0,w,h+100))
ball.load('ball_static.png')
ball.set_pos(w-30,bY)
balls=pygame.sprite.Group()
balls.add(ball)

paddle=Paddle((0,w-pW))
paddle.init((64,8),COLOR_SET['GOLD'])
paddle.set_pos(w//2,h-20)
paddles=pygame.sprite.Group()
paddles.add(paddle)

blocks=pygame.sprite.Group()
block=Block(1)
block.CreateBlocks(10,5,(30,30),(40,40),COLOR_SET['GOLD'],blocks)

border=pygame.Rect(0,0,w,h)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_SPACE and STATE != STATE_SET['RUN']:
                STATE = STATE_SET['INIT']


    # --------挡板部分--------
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]: paddle.move(-2)
    elif keys[K_RIGHT]: paddle.move(2)
    # --------模式部分--------
    if STATE == STATE_SET['PENDING']:
        ball.rect.center = paddle.rect.center
        ball.rect.bottom = paddle.rect.top
    elif STATE == STATE_SET['INIT']:
        print('initing...\n')
        ball.dx = randint(-2, 2)
        # ball_dx = 0
        ball.dy = -2
        STATE = STATE_SET['RUN']
    # --------碰撞部分--------
    ball.move()
    if ball.rect.bottom >= h:
        ball.set_vel(0,0)
        STATE = STATE_SET['PENDING']
    if pygame.sprite.collide_rect(ball,paddle):
        ball.Bounce(paddle.rect)
        if keys[pygame.K_LEFT]:
            ball.dx -= randint(0,3)
        elif keys[pygame.K_RIGHT]:
            ball.dx += randint(0,3)

    collision=pygame.sprite.spritecollideany(ball, blocks)
    if collision:
        ball.Bounce(collision.rect)
        collision.kill()

    # --------绘制部分--------
    screen.fill(COLOR_SET['BLACK'])

    paddles.draw(screen)
    blocks.draw(screen)
    balls.draw(screen)

    print_text(font_en,border.centerx,border.top,"车万零壹传")
    pygame.display.update()
    MainClock.tick(120)
    #print(MainClock.get_fps())
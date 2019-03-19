import pygame,sys
from pygame.locals import *
from random import randint
import pickle
import pygame.freetype
def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))
def LoadLevel(fname):
    with open(fname,'rb') as f:
        return pickle.load(f)

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
    def reduce(self):
        if self.type not in (8,9):
            self.type -=1
            if self.type:
                self.image.fill(COLORS[str(self.type)])

    def EmptyBlocks(self,group):
        group.empty()
    def CreateBlocks(self,n_row,n_col,size,offset,COLORS,group,mask):
        for i in range(n_col*n_row):
            if mask[i] not in ('0','8','9'):
                cur_x = (i%n_row)*offset[0]
                cur_y = (i//n_row)*offset[1]

                sprite=Block(int(mask[i]))
                sprite.init(size,COLORS[mask[i]])
                sprite.set_pos(cur_x+10,cur_y+10)

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
class Data(object):
    def __init__(self,score,life,cur_level):
        self.score=score
        self.life=life
        self.level=cur_level

size=w,h=640,480
pW,pH=64,8
bX,bY=0,0
COL,ROW=20,5
Lv=LoadLevel('levels.txt')
COLOR_SET={
    'GOLD':(255,215,0),
    'BLACK':(0,0,0),
    'WHITE':(255,255,255),
}
COLORS={'1':(255,215,0),'2':(175, 135, 0),'8':(0, 0, 215),'9':(215,0,0)}
STATE_SET={'GAME_OVER':-2,'PENDING':-1,'INIT':0,'RUN':1,'FINISH':2}
STATE=-1
TOTAL_LIFE=10
#pygame 初始化
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('BASIC')
MainClock=pygame.time.Clock()
font_18=pygame.freetype.Font("C://windows//Fonts//msyh.ttc",18)
font_24=pygame.freetype.Font("C://windows//Fonts//msyh.ttc",24)
font_en=pygame.font.Font("C://windows//Fonts//msyh.ttc",18)
#对象 初始化
data=Data(0,TOTAL_LIFE,1)

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
block.CreateBlocks(COL,ROW,(28,28),(31,31),COLORS,blocks,"".join(Lv[data.level-1]))

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
    # --------参数更新--------
    if data.life ==0:
        #ball.rect.x,ball.rect.y=0,0
        STATE=STATE_SET['GAME_OVER']
    if STATE!=STATE_SET['FINISH'] and not blocks.sprites():
        ball.rect.center=paddle.rect.center
        STATE = STATE_SET['FINISH']
    # --------挡板部分--------
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]: paddle.move(-2)
    elif keys[K_RIGHT]: paddle.move(2)
    # --------模式部分--------
    if STATE == STATE_SET['PENDING']:
        ball.rect.centerx = paddle.rect.centerx
        ball.rect.bottom = paddle.rect.top
    elif STATE == STATE_SET['INIT']:
        ball.dx = randint(-2, 2)
        ball.dy = -2
        STATE = STATE_SET['RUN']
    elif STATE==STATE_SET['GAME_OVER']:
        print_text(font_en, *border.center, "GAME OVER")
        print_text(font_en, border.centerx, border.centery+50, "SCORE:%d" % data.score)
        print_text(font_en, border.centerx, border.centery+100, "Press Any Key to Restart.")

        pygame.display.update()
        pygame.event.wait()

        block.EmptyBlocks(blocks)
        block.CreateBlocks(COL,ROW, (28, 28), (31, 31), COLOR_SET['GOLD'], blocks,"".join(Lv[0]))
        data.score,data.life=0,TOTAL_LIFE
        ball.rect.right,ball.rect.bottom = paddle.rect.left,paddle.rect.top
        STATE = STATE_SET['PENDING']
    elif STATE==STATE_SET['FINISH']:
        data.level += 1
        data.life += 1
        STATE = STATE_SET['PENDING']
        block.CreateBlocks(COL, ROW, (28, 28), (31, 31), COLOR_SET['GOLD'], blocks,"".join(Lv[data.level-1]))
        #initlevel

    # --------碰撞部分--------
    ball.move()
    if ball.rect.bottom >= h:
        data.life -= 1
        ball.set_vel(0,0)
        STATE = STATE_SET['PENDING']
    if pygame.sprite.collide_rect(ball,paddle):
        ball.Bounce(paddle.rect)
        if keys[pygame.K_LEFT]:
            ball.dx -= randint(0,1)
        elif keys[pygame.K_RIGHT]:
            ball.dx += randint(0,1)

    collision=pygame.sprite.spritecollideany(ball, blocks)
    if collision:
        ball.Bounce(collision.rect)
        collision.reduce()
        if collision.type ==0:
            collision.kill()
        data.score +=10

    # --------绘制部分--------
    screen.fill(COLOR_SET['BLACK'])

    paddles.draw(screen)
    blocks.draw(screen)
    balls.draw(screen)

    print_text(font_en,border.centerx-50,border.top,"车万零壹传")
    print_text(font_en, border.left, border.bottom-30, "fps:%.1f" % MainClock.get_fps())
    print_text(font_en, border.right-180, border.bottom-30, "LIFE:%d SCORE:%d"%(data.life,data.score))
    pygame.display.update()
    MainClock.tick(126)
import pygame,sys
import pygame.freetype
from random import randint
import pickle
def InitBlocks(W,H):
    return [[1]*W for i in range(H)]
def InitLevel(data):
    level=[]
    for v in data:
        level.append([int(x) for x in v])
    return level
def Index2D(L,value):
    out=[]
    for i,v in enumerate(L):
        for j,u in enumerate(v):
            if u==value:
                out.append((i,j))
    return out
def LoadLevel(fname):
    with open(fname,'rb') as f:
        return pickle.load(f)
levels=LoadLevel('levels.txt')

levels_hits=[84,26,32]
special_info={'Lv1':((2,5),(2,14))}
level_count=0

size=w,h=640,480
R=8
pW,pH=64,8
pX,pY=(w-pW)//2, h-10
pV=4
bW,bH=28,28
ball_x,ball_y=w//2,h-18
ball_dx,ball_dy=0,0

NUM_BLOCK_ROWS = 10
NUM_BLOCK_COLUMNS = 20
x_GAP=3+bW
y_GAP=3+bH

STATE_SET={'GAME_OVER':-2,'PENDING':-1,'INIT':0,'RUN':1,'FINISH':2}
STATE=-1
TOTAL_LIFE=10
Score=0
Life=TOTAL_LIFE
Hits=0

BALL_COLOR = (0, 0, 255)
PADDLE_COLOR = (128, 64, 64)
BLOCK_COLOR_1 = (255, 215, 0)
BLOCK_COLOR_2 = (175, 135, 0)
BLOCK_COLOR_9 = (215,0,0)
BLACK=0,0,0
WHITE=255,255,255
fps=120

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('车万灵异传')
MainClock=pygame.time.Clock()
#font=pygame.font.SysFont(None, 24)
font=pygame.freetype.Font("C://windows//Fonts//msyh.ttc",24)

Blocks = InitLevel(levels[1])
#level_count += 1
level_count += 2
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                sys.exit()
            elif event.key==pygame.K_SPACE and STATE!=STATE_SET['RUN']:
                STATE=STATE_SET['INIT']
    # --------参数更新--------
    ball_x += ball_dx
    ball_y += ball_dy
    if Life ==0:
        ball_x,ball_y=0,0
        STATE=STATE_SET['GAME_OVER']
    if Hits == levels_hits[level_count-1]:
        ball_x,ball_y=0,0
        STATE=STATE_SET['FINISH']
    # --------挡板部分--------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if pX>0:
            pX -= pV
    if keys[pygame.K_RIGHT]:
         if pX<w-pW:
            pX += pV
    # --------模式部分--------
    if STATE == STATE_SET['PENDING']:
        ball_x = pX+pW//2
        ball_y = h-18
    elif STATE == STATE_SET['INIT']:
        print('initing...\n')
        #ball_dx = randint(-2,2)
        ball_dx = 0
        ball_dy = -2
        STATE = STATE_SET['RUN']
        ball_x += ball_dx   #break out fringe
        ball_y += ball_dy
        print('running...\n')
    elif STATE==STATE_SET['GAME_OVER']:
        titlerect=font.render_to(screen, (w//2, h//2), "GAME OVER",fgcolor=WHITE)
        FinalScorerect=font.render_to(screen, (w//2, h//2+50), "SCORE:%d" % Score,fgcolor=WHITE)
        info=font.render_to(screen, (w//2,h//2+100), "Press Any Key to Restart.",fgcolor=WHITE)
        pygame.display.update()
        pygame.event.wait()

        Score,Hits = 0,0
        Life = TOTAL_LIFE

        Blocks = InitLevel(levels[0])
        level_count = 1

        #Blocks=InitBlocks(NUM_BLOCK_COLUMNS,NUM_BLOCK_ROWS)
        STATE = STATE_SET['PENDING']    #Blocks also?
    elif STATE==STATE_SET['FINISH']:
        level_count += 1
        Life += 1
        Hits = 0
        STATE = STATE_SET['PENDING']

        Blocks = InitLevel(levels[level_count-1])


    # --------碰撞部分--------
    if ball_x-R<0 or ball_x+R>w:
        ball_dx = -ball_dx
    if ball_y-R<0:
        ball_dy = -ball_dy

    # ------------球与挡板----
    if ball_y+R>pY and (ball_x>pX and ball_x<pX+pW):
        ball_dy = -ball_dy
        if keys[pygame.K_LEFT]:
            ball_dx -= randint(0,3)
        elif keys[pygame.K_RIGHT]:
            ball_dx += randint(0,3)
        else:
            ball_dx += randint(-1,1)
    if ball_y>h:
        Life -= 1
        STATE=STATE_SET['PENDING']
    # ------------球与砖块----
    cur_x,cur_y=8,28
    if ball_y<w//2:
        for row in range(NUM_BLOCK_ROWS):
            cur_x=8
            for col in range(NUM_BLOCK_COLUMNS):
                if Blocks[row][col]:
                    if ball_x+R>cur_x and ball_x-R<cur_x+bW and ball_y+R>cur_y and ball_y-R<cur_y+bH:
                        if ball_x + R  > cur_x + 2 and ball_x - R < cur_x + bW-2:
                            ball_dy = -ball_dy
                        if ball_y+R>cur_y+2 and ball_y-R<cur_y+bH-2:
                            ball_dx = -ball_dx
                        if Blocks[row][col] ==8:
                            for v in special_info['Lv1']:
                                if (row,col) !=v:
                                    ball_x=8+v[1]*x_GAP+bW//2
                                    ball_y=28+v[0]*y_GAP-bH//2
                                    ball_dx=randint(-2,2)

                        if Blocks[row][col] not in (8,9):
                            Blocks[row][col] -= 1
                            Hits += 1
                            Score += 10
                        break
                cur_x += x_GAP
            cur_y += y_GAP

    # --------绘制部分--------
    screen.fill(BLACK)
    cur_x,cur_y=8,28
    # ------------绘制砖块----
    for i in range(NUM_BLOCK_ROWS):
        cur_x=8 #return to head
        for j in range(NUM_BLOCK_COLUMNS):
            if Blocks[i][j]==1:
                pygame.draw.rect(screen,BLOCK_COLOR_1,(cur_x,cur_y,bW,bH))
            elif Blocks[i][j]==2:
                pygame.draw.rect(screen, BLOCK_COLOR_2, (cur_x, cur_y, bW, bH))
            elif Blocks[i][j]==8:
                pygame.draw.circle(screen, BALL_COLOR, (cur_x+bW//2,cur_y+bH//2), bW//2,2)
            elif Blocks[i][j]==9:
                pygame.draw.rect(screen, BLOCK_COLOR_9, (cur_x, cur_y, bW, bH),5)
            cur_x+=x_GAP
        cur_y+=y_GAP
    pygame.draw.circle(screen,BALL_COLOR,(ball_x,ball_y),R)
    pygame.draw.rect(screen,PADDLE_COLOR,(pX,pY,pW,pH))
    # ------------绘制文字----
    info=font.render_to(screen, (w//2-80,10), "车万零壹传",fgcolor=WHITE)
    Levelrect=font.render_to(screen, (w-100, 10), "Level:%d" % level_count,fgcolor=WHITE)
    Liferect=font.render_to(screen, (10, h-40), "LIFE:%d" % Life,fgcolor=WHITE)
    Scorerect=font.render_to(screen, (w-130, h-40), "mark:%d" % Score,fgcolor=WHITE)
    pygame.display.update()
    MainClock.tick(fps)
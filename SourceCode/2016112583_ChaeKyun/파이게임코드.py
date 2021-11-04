import pygame
import random
import time
from datetime import datetime

# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [700, 800]
screen = pygame.display.set_mode(size)

title = 'My Game'
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()

class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
    def put_img(self, address):
            self.img = pygame.image.load(address).convert_alpha()
            self.sx, self.sy = self.img.get_size()
    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img, (sx,sy))
        self.sx, self.sy = self.img.get_size()
    def show(self):
        screen.blit(self.img, (self.x, self.y))

def crash(a ,b):
    if (a.x - b.sx <= b.x) and (b.x <= a.x + a.sx):
        if (a.y - b.sy <= b.y) and (b.y <= a.y + a.sy):
            return True
        else: 
            return False
    else : return False

so = obj()
b1 = so.put_img("SourceCode\Image\image1.png")
so.change_size(200,200)
so.x = round(size[0]/2 - so.sx/2)
so.y = size[1] - so.sy - 100
so.move = 10

m_list = []
a_list = []

left_go = False
right_go = False
space_go = False
'''
so = pygame.image.load("so.png").convert_alpha()
so = pygame.transform.scale(so, (50,80))
so_sx, so_sy = so.get_size()
so_x = round(size[0]/2 - so_sx/2)
so_y = size[1] - so_sy - 15
'''
black = (0,0,0)
white = (255,255,255)
k = 0
GO = 0
kill = 0
loss = 0

# 4-0. 게임 시작 대기 화면
SB = 0
while SB == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                SB = 1
    screen.fill(black)
    font = pygame.font.Font(None, 15)
    text = font.render('PRESS SPACE KEY TO START THE GAME', True, (255,255,255))
    screen.blit(text, (40, round(size[1]/2-50)))
    pygame.display.flip()

# 4. 메인 이벤트
start_time = datetime.now()
SB = 0
while SB == 0:

    # 4-1. FPS 설정
    clock.tick(60)

    # 4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_go = True
            elif event.key == pygame.K_RIGHT:
                right_go = True
            elif event.key == pygame.K_SPACE:
                space_go = True
                k = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            elif event.key == pygame.K_RIGHT:
                right_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False

    # 4-3 입력, 시간에 따른 변화
    now_time = datetime.now()
    delta_time = round((now_time - start_time).total_seconds())

    if left_go == True:
        so.x -= so.move
        if so.x <= 0:
            so.x = 0
    elif right_go == True:
        so.x += so.move
        if so.x >= size[0] - so.sx:
            so.x = size[0] - so.sx
    
    if space_go == True and k % 6 == 0:
        mm = obj()
        mm.put_img("SourceCode\Image\pngtree-blue-intelligent-robot-element-illustration-png-image_1154235.jpg")
        mm.change_size(30,30)
        mm.x = round(so.x + so.sx/2 - mm.sx/2)
        mm.y = so.y - mm.sy - 10
        mm.move = 15
        m_list.append(mm)
    k += 1

    d_list = []
    for i in range(len(m_list)):
        m = m_list[i]
        m.y -= m.move
        if m.y <= -m.sy:
            d_list.append(i)
    for d in d_list:
        del m_list[d]

    if random.random() > 0.98:
        aa = obj( )
        b2 = aa.put_img("SourceCode\Image\so2.jpg")
        aa.change_size(90,90)
        aa.x = random.randrange(0, size[0] - aa.sx - round(so.sx/2))
        aa.y = 10
        aa.move = 2
        a_list.append(aa)
    d_list = []
    for i in range(len(a_list)):
        a = a_list[i]
        a.y += a.move
        if a.y >= size[1]:
            d_list.append(i)
    for d in d_list:
        del a_list[d]
        loss += 1
    
    dm_list = []
    da_list = []
    for i in range(len(m_list)):
        for j in range(len(a_list)):
            m = m_list[i]
            a = a_list[j]
            if crash(m,a) == True:
                dm_list.append(i)
                da_list.append(j)
    dm_list = list(set(dm_list))
    da_list = list(set(da_list))

    for dm in dm_list:
        del m_list[dm]
    for da in da_list:
        del a_list[da]
        kill += 1
    for i in range(len(a_list)):
        a = a_list[i]
        if crash(a, so) == True:
            SB = 1
            GO = 1

    # 4-4 그리기
    screen.fill(black)
    so.show()
    for m in m_list:
        m.show()
    for a in a_list:
        a.show()

    font = pygame.font.Font(None,20)
    text_kill = font.render('killed: {} loss: {}'.format(kill, loss), True, (255,255,0))
    screen.blit(text_kill, (10, 5))

    text_time = font.render('time : {}'.format(delta_time), True, (0,00,0))
    screen.blit(text_time, (size[0]-100, 5))


    # 4-5 업데이트
    pygame.display.flip()

# 5. 게임종료
while GO == 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GO = 0
    font = pygame.font.Font(None,40)
    text = font.render('GAME OVER', True, (255,0,0))
    screen.blit(text, (80, round(size[1]/2-80)))
    pygame.display.flip()
pygame.quit()
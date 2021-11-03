import pygame
import random
import time
from datetime import datetime
from pygame.constants import VIDEORESIZE
# sx, sy => 피사체의 x위치 y 위치
# x, y => 비행기의 가로길이, 세로길이
# 1. 게임초기화
pygame.init()

# 2. 게임창 옵션 설정

# 2-1 고정된 화면 크기
# size = [700,800]
# screen = pygame.display.set_mode(size)

# 2-2 플레이어의 컴퓨터 환경에 맞춘 화면의 크기 
infoObject = pygame.display.Info()
# 896 * 1020
size = [infoObject.current_w,infoObject.current_h]
screen = pygame.display.set_mode(size,pygame.RESIZABLE)


class Move:
    # 좌방향 이동키
    left_go = False
    # 우방향 이동키
    right_go = False
    # 윗방향 이동키
    up_go = False
    # 아랫방향 이동키
    down_go = False
    # 미사일 발사 키
    space_go = False
    # 게임의 FPS
    FPS = 60
    # 객체의 변경된 위치변경의 Key
    position = False
    # 객체들이 화면 밖으로 나갔는지 판정에 필요한 boundary 값
    boundary = 0

class Color:
    # RGB 검정
    black = (0,0,0)
    # RGB 흰색
    white = (255,255,255)
    red = (255,0,0)
    purple = (100,40,225)
    yellow = (255,255,0)

class Size:
    # 비행체의 x,y사이즈
    a_xsize = size[0]//18
    a_ysize = size[1]//13
    # 미사일의 x,y사이즈
    m_xsize = size[0]//179
    m_ysize = size[1]//68
    # 미사일의 크기 조정(최대값, 최소값)
    min_size = (sum(size)//50)*2//3
    max_size = (sum(size)//30)*2//3
    block_max_size = size[0]//10
    # 2등분 3등분 값을 찾기위한 num
    half_split_num = 2
    third_split_num = 3

    m_rand_size = 10
    

class Speed:
    # 미사일의 스피드
    m_speed = 0 # 초기화`
    m_initiate_speed_30 = 30
    m_initiate_speed_15 = 15
    # 미사일의 max 스피드
    m_max_speed = 6
    # 비행체 스피드
    s_speed =5
    # 미사일 빈도 조정 
    k=0
    create_rate_r = 0.995
    create_rate_c = 0.98
    # 미사일 스피드의 초기값 15 고정
    speed_initializing_15 = 15
    # 초기 스피드
    a_init_speed = 2
    m_init_speed = 2
    b_init_speed = 2
    
    
    

class Util:
    # 미사일을 발사할때 미사일 객체가 저장되는 리스트 공간
    m_list = []
    # 피사체 출현시 피사체 객체가 저장되는 리스트 공산
    a_list = []
    # 장애물 객체가 저장되는 리스트 
    block_list=[]
    # 피사체를 미사일로 맞추었을때 맞춘 피사체의 개수
    kill = 0 
    # 피사체를 죽이지못하고 화면밖으로 놓친 피사체의 개수
    loss = 0 
    # 현재 내가 획득한 점수
    score = 0
    # Game Over
    GO = 0   
    
    score_10 = 10
    score_100 = 100
    score_200 = 200
    score_300 = 300
    score_400 = 400

    m_loc_10 = 10
    a_loc_10 = 10
    start_loc = (0,0)

class FontSize:
    size_start = 20
    lensize_start = 50
    size_kill_loss = sum(size)//85
    size_gameover = sum(size)//47
    lensize_gameover = 65
    len_for_time = size[0]//6
    len_for_time_ysize = 5
    loc_kill_loss = (10,5)


class Sound:
    m_sound = 0.2
    crash1_sound = 0.3
    crash2_sound = 0.2
    game_over_sound = 0.3
    background_sound = 0.3
    

class obj:
    def __init__(self):
        self.x =0
        self.y=0
        self.move =0

    def put_img(self,address):
        # png파일 일때
        # convert해줘야하는 문제가 있기때문에
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()    
        else: 
            self.img = pygame.image.load(address)
        self.sx, self.sy = self.img.get_size()

    # 피사체의 그림 조정
    def change_size(self,sx,sy):
        self.img = pygame.transform.scale(self.img,(sx,sy)) # 그림의 크기를 조정한다.
        self.sx, self.sy = self.img.get_size()

    def show(self):
        screen.blit(self.img,(self.x,self.y))





# print(size)
title = "My Game"
pygame.display.set_caption(title) # 창의 제목 표시줄 옵션
# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()
#파이게임 배경음악
pygame.mixer.init()
pygame.mixer.music.load("SourceCode/Sound/ariant.mp3")
# 미사일 효과음
missile1 = pygame.mixer.Sound("SourceCode/Sound/weapon-sound8.ogg")
missile1.set_volume(Sound.m_sound)
missile2 = pygame.mixer.Sound("SourceCode/Sound/weapon-sound9 .ogg")
missile2.set_volume(Sound.m_sound)
missile3 = pygame.mixer.Sound("SourceCode/Sound/weapon-sound16.ogg")
missile3.set_volume(Sound.m_sound)
# 피사체 파괴시 효과음
monster1 = pygame.mixer.Sound("SourceCode/Sound/monster-sound7.ogg")
monster1.set_volume(Sound.crash1_sound)
# 피사체와 비행체 충돌시 효과음
boom1 = pygame.mixer.Sound("SourceCode/Sound/weapon-sound9 .ogg")
boom1.set_volume(Sound.crash2_sound)
# 게임오버 효과음
game_over = pygame.mixer.Sound("SourceCode/Sound/gameover.wav")
game_over.set_volume(Sound.game_over_sound)



# 충돌이 일어났는지 확인하는 함수!
# return 값이 boolean 타입임
def crash(a,b):
    # 요 범위 안에 있을때 충돌이 일어남
    if (a.x-b.sx <=b.x) and (b.x<=a.x + a.sx):
        if(a.y-b.sy <= b.y) and (b.y <= a.y+a.sy):
            return True
        else:
            return False
            
    else:
        return False

def cal_score(kill,loss):
    Util.score = (Util.kill*5 - Util.loss*8)

def change_size_rate(size):
    Size.a_xsize = size[0]//18
    Size.a_ysize = size[1]//13
    Size.m_xsize = size[0]//179
    Size.m_ysize = size[1]//68
    Size.min_size = (size[0]//50 + size[1]//50)*2//3
    Size.max_size = (size[0]//30 + size[1]//30)*2//3
    Size.block_max_size = size[0]//10
    FontSize.size_kill_loss = sum(size)//85
    FontSize.size_gameover = sum(size)//47
    FontSize.len_for_time = size[0]//6
    

    # 오른쪽 끝 선에서 크기를 줄일 시 객체가 화면 밖으로 못나가게 제한 함
    if ss.x + ss.sx > size[0]:
        ss.x = size[0]- ss.sx
    # 바닥 선에서 크기를 줄일 시 객체가 화면 밖으로 못나가게 제한 함
    if ss.y + ss.sy >size[1]:
        ss.y = size[1] - ss.sy
    # 비행체 객체의 사이즈 변경
    try:
        ss.change_size(Size.a_xsize, Size.a_ysize)
    except :
        pass
    try:
        # 지금 현재 미사일을 발생시키지 않는 상태 일 수도 있기 때문
        for i in Util.m_list:
            i.change_size(Size.m_xsize,Size.m_ysize)
    except :
        pass
    # try:
    #     # 점수가 아직 도달하지 못하여 mm2객체가 만들어지지 않았을 수도 있음
    #     for i in Util.m_list:
    #         mm2.change_size(Size.m_xsize, Size.m_ysize)
    # except :
    #     pass
    try:
        random_size = random.randint(Size.min_size,Size.block_max_size)
        for i in Util.block_list:
            i.change_size(Size.block_max_size,Size.block_max_size)
    except :
        pass
    try:
        # 그림이 깨지는 경우가 생겨서 다시 이미지를 넣어줌
        aa.put_img("SourceCode/Image/scorphion1-removebg-preview.png")
    except :
        pass
    try:
        random_size = random.randint(Size.min_size,Size.max_size)
        for i in Util.a_list:
            i.change_size(random_size,random_size)
    except :
        pass


# 4-0 게임 시작 대기 화면(작은 event)
SB=0
while SB==0:
    clock.tick(Move.FPS)
    for event in pygame.event.get(): # 이벤트가 있다면 
        if event.type == pygame.KEYDOWN: # 그 이벤트가 어떤 버튼을 누르는 것이라면
            if event.key == pygame.K_SPACE: # 그 버튼이 스페이스 버튼이라면?
                SB=1
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            size =[width,height]
            window = pygame.display.set_mode(size, pygame.RESIZABLE)
    screen.fill(Color.black)
    
    font = pygame.font.Font("SourceCode/Font/DXHanlgrumStd-Regular.otf",FontSize.size_start)
    text_kill = font.render("PRESS \"SPACE\" KEY TO START THE GAME",True,Color.white) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
    screen.blit(text_kill,(size[0]//Size.half_split_num-(size[0]//Size.half_split_num)//Size.half_split_num,round((size[1]/Size.half_split_num)-FontSize.lensize_start))) # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨 
    
    pygame.display.flip() # 그려왔던게 화면에 업데이트가 됨

# 객체 생성
ss = obj()
# 우리들이 움직여야할 물체
ss.put_img("SourceCode/Image/DesertLV1Car-removebg-preview.png")
# 그림(비행체)의 크기를 조정
ss.change_size(Size.a_xsize,Size.a_ysize)
# 비행체의 위치를 하단의 중앙으로 바꾸기위해!
# x값의 절반에서 피사체의 길이의 절반만큼 왼쪽으로 이동해야 정확히 가운데임
ss.x = round(size[0]/Size.half_split_num - ss.sx/Size.half_split_num)
# 맨 밑에서 피사체의 y길이만큼 위로 올라와야함
ss.y = size[1] - ss.sy
# 비행체가 움직이는 속도를 결정함
ss.move = Speed.s_speed

# 게임의 배경화면 설정
background_image_desert = pygame.image.load("SourceCode/Image/Desertmap.png")
background_image_desert = pygame.transform.scale(background_image_desert,size) # 그림의 크기를 조정한다.



# 4. 메인 이벤트
#사막맵 배경음악 실행
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(Sound.background_sound)
# 코드를 첫 실행한 시간 저장
start_time = datetime.now()
SB=0
while SB==0:
    # 4-1. FPS 설정 
    # FPS를 60으로 설정함
    clock.tick(Move.FPS)

    # 4-2. 각종 입력 감지 
    for event in pygame.event.get():  # 어떤 동작을 했을때 그 동작을 받아옴
        if event.type == pygame.QUIT: # x버튼을 눌렀을때!
            SB=1 # SB 가 1이되면 while문을 빠져나오게 된다!
        if event.type == pygame.KEYDOWN: # 어떤 키를 눌렀을때!(키보드가 눌렸을 때)
            # 키를 누르고있는 상태 : True
            # 키를 떼고있는 상태 : False
            if event.key == pygame.K_LEFT:  # 만약 누른 키가 왼쪽 방향키 라면?
                Move.left_go = True
            if event.key == pygame.K_RIGHT:  # 만약 누른 키가 오른쪽 방향키 라면?
                Move.right_go = True
            if event.key == pygame.K_SPACE:  # 만약 누른키가 space키 라면?
                Move.space_go = True
                # 속도를 1/6으로 낮췄는데 누를때마다도 한번씩 발사하고싶어서 누르면 k=0으로 초기화시킴 -> while문 조건 통과하기위해
                # k=0
            if event.key == pygame.K_UP :
                Move.up_go = True
            if event.key == pygame.K_DOWN:
                Move.down_go = True
            
        elif event.type == pygame.KEYUP: # 키를 누르는것을 뗐을때!
            if event.key == pygame.K_LEFT: # 키를 뗐다면 그 키가 왼쪽 방향키 인가?
                Move.left_go = False
            elif event.key == pygame.K_RIGHT: # 키를 뗐다면 그 키가 오른쪽 방향키 인가?
                Move.right_go = False
            elif event.key == pygame.K_SPACE: # 키를 뗐다면 그 키가 스페이스 키인가?
                Move.space_go = False
            elif event.key == pygame.K_UP:
                Move.up_go = False
            elif event.key == pygame.K_DOWN:
                Move.down_go = False
        
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            size =[width,height]
            window = pygame.display.set_mode(size, pygame.RESIZABLE)
            Move.position = True

    # 마우스로 인해 화면이 작아지면 다른 객체들의 사이즈도 전부 변경
    if Move.position is True:
        change_size_rate(size)
    
    
    
        # 4-3. 입력과 시간에 따른 변화 
    now_time = datetime.now()
        # 코드실행 시점에서 현재시간과릐 차이를 초로 바꿈
    delta_time = (now_time - start_time).total_seconds()


    # 버튼을 꾹 길게 눌렀을때 움직이게 하기
    # 왼쪽 방향키를 눌렀을 때
    if Move.left_go == True:
        ss.x -= ss.move
        # 물체가 왼쪽 끝 경계값으로 이동하면 더이상 나가지 않게끔 만듬!
        # 배경이 뭐냐에 따라 달라질 듯 !
        if ss.x < Move.boundary:
            # 더 이상 나가지 못하도록 0 으로 막아줌
            ss.x = Move.boundary 
    # 오른쪽 방향키를 눌렀을 때
    elif Move.right_go == True:
        ss.x += ss.move
        # 오른쪽 끝에서 비행선의 가로크기만큼 빼줘야한다
        if ss.x >= size[0] - ss.sx:
            # 더 이상 오른쪽 바깥으로 못나가게 오른쪽 끝값으로 초기화
            ss.x = size[0] - ss.sx
    # 윗 방향키를 눌렀을때
    # 윗 방향키를 elif에서 if로 시작
    # 좌우와 상하가 독립된 상태로 구분됨
    if Move.up_go == True:
        ss.y -= ss.move
        # 게임화면 위쪽 화면으로 나가는 경우
        if ss.y < Move.boundary:
            # 더이상 나가지 못하게 위치값 고정
            ss.y = Move.boundary
    # 아래 방향키를 눌렀을때
    elif Move.down_go == True:
        ss.y += ss.move
        # 게임화면 위쪽 화면으로 나가는 경우
        if ss.y >= size[1] - ss.sy:
            # 더이상 나가지 못하게 위치값 고정
            ss.y = size[1] - ss.sy


    # 미사일의 속도 조정
    if Speed.m_initiate_speed_30-(Util.score // Util.score_10)>=Speed.m_max_speed:
        m_speed = Speed.m_initiate_speed_30 - (Util.score // Util.score_10)
    else:
        m_speed = Speed.m_max_speed



    # 점수와 관련해서 미사일의 속도를 바꾸면 좋을듯 !
    # k%6 이면 미사일의 발생 확률을 1/6으로  낮춤!
    if (Move.space_go == True) and Speed.k % m_speed == 0:
        # 미사일 객체 생성
        mm = obj()
        # 미사일의 사진
        mm.put_img('SourceCode/Image/pngtree-brass-bullet-shells-png-image_3258604.jpeg')
        # 미사일의 크기 조정
        # m_xsize = 5, m_ysize = 15
        mm.change_size(Size.m_xsize,Size.m_ysize)
        # 미사일 생성시 효과음
        missile1.play()
        # 미사일의 x값 (위치)
        if Util.score < Util.score_200:
            mm.x = round(ss.x + ss.sx / Size.half_split_num - mm.sx / Size.half_split_num)
            # 미사일의 위치 = 비행기의 위치 - 미사일의 y크기 
            mm.y = ss.y - mm.sy - Util.m_loc_10
        elif Util.score >= Util.score_200 and Util.score < Util.score_400:
            mm.x = round(ss.x + ss.sx / Size.third_split_num - mm.sx / Size.half_split_num)
            # 미사일의 위치 = 비행기의 위치 - 미사일의 y크기 
            mm.y = ss.y - mm.sy - Util.m_loc_10
        elif Util.score >= Util.score_400:
            mm.x = round(ss.x + ss.sx / Size.half_split_num - mm.sx / Size.half_split_num)
            mm.y = ss.y - mm.sy - Util.m_loc_10
        
        
        # 미사일의 움직이는 속도를 결정함
        mm.move = Speed.m_initiate_speed_15
        # 미사일의 객체를 리스트에 저장한다.
        Util.m_list.append(mm)

    # 점수가 200점 이상이라면 미사일이 한개 더 늘어남
    # 점수가 400점 이상이라면 미사일의 발사 형태가 바뀜
    if (Move.space_go == True) and (Speed.k%m_speed == 0) and Util.score >= Util.score_200:
        # 두번째 미사일 객체 생성
        missile1.stop()
        missile2.play()
        mm2 = obj()
        mm2.put_img('SourceCode/Image/pngtree-brass-bullet-shells-png-image_3258604.jpeg')
        mm2.change_size(Size.m_xsize, Size.m_ysize)
        mm2.x = round(ss.x +(ss.sx * Size.half_split_num) / Size.third_split_num - mm.sx / Size.half_split_num)
        mm2.y = ss.y - mm2.sy - Util.m_loc_10
        mm2.move = Speed.m_initiate_speed_15
        Util.m_list.append(mm2)


    # 미사일의 발생 빈도 조절
    Speed.k += 1

    # 피사체의 리스트를 초기화함
    # delete list
    d_list = []
    for i in range(len(Util.m_list)):
        # i 번째 미사일
        m = Util.m_list[i]
        # 미사일 속도만큼 미사일이 y축방향으로 빠져나간다.
        m.y -= m.move
        if Util.score > Util.score_400:
            missile2.stop()
            missile3.play()
            # 점수가 400점 이상이면 미사일이 꼬여서 나가는것 처럼 보이게 함
            m.x+= random.uniform(-Util.m_loc_10,Util.m_loc_10)
        # 미사일의 사이즈만큼 나갔을때 지워준다.
        if m.y < -m.sx:
            d_list.append(i)
    d_list.reverse()
    for d in d_list:
        del Util.m_list[d]
    
    # score 400점마다 비행체의 속도 1씩 증가
    Speed.s_speed = Speed.s_speed + Util.score // Util.score_400


    # score 가 10점 증가함에따라 피사체 발생 개수 0.01확률 증가 
    if random.random() > Speed.create_rate_c -(Util.score//Util.score_200)//Util.score_100:
        # 피사체 객체 생성
        aa = obj()
        aa.put_img("SourceCode/Image/scorphion1-removebg-preview.png")
        # 피사체의 그림 크기 조정
        random_size = random.randint(Size.min_size,Size.max_size)
        # print("Size.min_size : {} Size.max_size : {} ss.x : {} ss.y : {} ss.sx : {} ss.sy : {} size : {} aa.sx : {} aa.sy : {}".format(Size.min_size, Size.max_size,ss.x,ss.y,ss.sx,ss.sy,size,aa.sx,aa.sy))
        # 정사각형 모양의 피사체
        # 이미 사이즈가 한번 바뀌었으므로 다시 바뀔 필요가 없음 또 바꾸면 오류 발생
        if Move.position is not True:
            aa.change_size(random_size,random_size)
        # 0부터 오른쪽 끝까지의 랜덤변수인데 비행기크기보다 작으므로 미사일을 안맞는 외계인도 고려해야함(비행선크기/2 를 뺴줘야함)
        aa.x = random.randrange(0, size[0] - aa.sx - round(ss.sx/Size.half_split_num))
        aa.y = Util.a_loc_10
        aa.move = Speed.a_init_speed + (Util.score//Util.score_300)
        Util.a_list.append(aa)
    
    # 장애물 등장
    if random.random() > Speed.create_rate_r:
        # 장애물 객체 생성
        block = obj()
        block.put_img('SourceCode/Image/CATUS.png')
        random_size = random.randint(Size.min_size,Size.block_max_size)
        block.change_size(random_size, random_size)
        # block.change_size(Size.block_size, Size.block_size)
        block.x = Util.a_loc_10
        block.y = random.randint(0, size[0] - block.sx - round(ss.sx/Size.half_split_num))
        block.move = Speed.b_init_speed + (Util.score//Util.score_100)
        Util.block_list.append(block)

    d2_list=[]
    for i in range(len(Util.block_list)):
        b = Util.block_list[i]
        b.x += b.move
        if b.x >= size[0]:
            d2_list.append(i)

    d2_list.reverse()
    for d2 in d2_list:
        del Util.block_list[d2]


    # 살생부 리스트 초기화
    d_list = []
    for i in range(len(Util.a_list)):
        a = Util.a_list[i]
        a.y += a.move
        # 외계인이 화면 밖으로 나갔다면 지워준다.
        if a.y >= size[1]:
            d_list.append(i)

    # 메모리 효율을 위해 삭제
    # 앞에서 부터 지워지면 리스트가 앞당겨져서 오류가 일어나기때문에 reverse해주고 지워준다.
    d_list.reverse()
    for d in d_list:
        del Util.a_list[d]
        # 외계인이 화면 밖으로 나간 횟수
        Util.loss += 1

    dm_list = []
    da_list = []

    for i in range(len(Util.m_list)):
        for j in range(len(Util.a_list)):
            m = Util.m_list[i]
            a = Util.a_list[j]
            if crash(m,a) is True:
                dm_list.append(i)
                da_list.append(j)
    
    # 미사일2개와 외계인 1개가 같이 만나는 경우가 있을 수도 있으니까 배제하기위해 중복제거를 해준다.
    dm_list = list(set(dm_list))
    da_list = list(set(da_list))
    # reverse 하지않고 지우면 앞에서 부터 지워지고 앞에서부터지워지면 index의 변화가 일어나서 reverse를 해야함
    dm_list.reverse()
    da_list.reverse()


    # del로 미사일과 외계인 삭제하기
    try:
        for dm in dm_list:
            del Util.m_list[dm]
    except :
        pass
    try:
        for da in da_list:
            del Util.a_list[da]
            # 피사체 사망시 효과음
            monster1.play()
            # 피사체를 파괴한 횟수
            Util.kill += 1
    except :
        pass

    for i in range(len(Util.a_list)):
        a = Util.a_list[i]
        # 만약 외계인이 ss 와 부딛치면 게임 종료
        if crash(a,ss) is True:
            # 부딛칠 때 효과음
            boom1.play()
            # 1초뒤에 꺼지도록 함
            time.sleep(1)
            # while 문이 종료되도록 하는 key
            SB = 1
            # Go 가 0 인상태로 while문을 빠져나왔다면 x버튼으로 빠져나온것
            Util.GO = 1


    for i in range(len(Util.block_list)):
        b = Util.block_list[i]
        # 만약 장애물과 ss가 부딛치면 게임 종료시킴
        if crash(b,ss) is True:
            # 부딛칠 때 효과음
            boom1.play()
            time.sleep(1)
            # while문 종료 키 
            SB =1
            Util.GO = 1


    # score 가 0 점이 되면 프로그램 종료
    if Util.score < 0:
        SB = 1
    


    # 4-4. 그리기 
    #  마우스에의해 창크기가 바뀜에 따라 배경화면 크기가 바뀜
    background_image_desert = pygame.transform.scale(background_image_desert, size)
    screen.blit(background_image_desert, Util.start_loc)
    

    # 비행체 보여주기
    ss.show()
    # 미사일 보여주기
    for m in Util.m_list:
        m.show()
    # 피사체 보여주기
    for a in Util.a_list:
        a.show()
    # 선인장 장애물 보여주기
    for d in Util.block_list:
        d.show()
    # 점수 산정
    # Util.score = (Util.kill*5 - Util.loss*8)
    cal_score(Util.kill, Util.loss)
    
    font = pygame.font.Font("SourceCode/Font/DXHanlgrumStd-Regular.otf", FontSize.size_kill_loss)
    text_kill = font.render("Killed : {} Loss : {}  Score : {}".format(Util.kill, Util.loss, Util.score), True, Color.yellow) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
    screen.blit(text_kill,FontSize.loc_kill_loss) # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨 
    
    # 현재 흘러간 시간
    text_time = font.render("Time : {:.2f}".format(delta_time), True, Color.purple)
    screen.blit(text_time,(size[0]-FontSize.len_for_time, FontSize.len_for_time_ysize))
    
    # 4-5. 업데이트
    pygame.display.flip() # 그려왔던게 화면에 업데이트가 됨
    Move.position = False



# 5. 게임종료(1. x키를 눌러서 게임이 종료된 경우, 2. 죽어서 게임이 종료된 경우)
# 이건 게임오버가 된 상황!
game_over.play()
while Util.GO==1:
    clock.tick(Move.FPS)
    for event in pygame.event.get(): # 이벤트가 있다면 
        if event.type == pygame.QUIT:
            Util.GO=0
    
    font = pygame.font.Font("SourceCode/Font/DXHanlgrumStd-Regular.otf", FontSize.size_gameover)
    text_kill = font.render("GAME OVER", True, Color.red) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
    screen.blit(text_kill,(size[0] // Size.half_split_num - (size[0] // Size.half_split_num) // Size.half_split_num + FontSize.lensize_gameover, round((size[1] / Size.half_split_num) - FontSize.lensize_gameover))) # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨 
    
    pygame.display.flip() # 그려왔던게 화면에 업데이트가 됨
    
pygame.quit()


# 텍스트 띄우는 방법(내용, 위치, 글자체, 크기, 색깔)
# 1. 폰트 설정
# font = pygame.font.Font(address,size)
# 2. Surface 생성(텍스트의 이미지화)
# text = font.render(contents,True,color)
# 3. Surface 화면에 표시
# screen.blit(text,position)


# 위 코드 세줄이 한 묶음으로 다니게 될것임






# 점수가 올라감에 따라 더 작은 피사체가 나올수도있게 끔 해보자 !


# 채균
# 첫화면 인터페이스 
# 스코어별로 다른피사체 그림
# 스코어 별로 다른 미사일 사운드 
# 스코어 별로 다른 미사일 이미지 
# 스코어 별로 다른 비행체 그림






# 변수정리
# 가로로 나오는 장애물 (격추안됨, 피하기만 해야함)
# 1000 점 이상되면 가로 세로 막 졸라 (과제과제, 오픈소스 ) 10~15
# score 400점마다 비행체의 속도 1씩 증가
# 선인장 장애물 생성


# 해야할거

# 점수가 증가하면 선인장의 크기도 증가
# 크기를 줄였다가 늘렸다가 할때 객체들의 위치도 이동이 되어야 함(가로로 발생하는 선인장 만 즉시반영이 안됨)
# 화면 크기조절 동영상 드리기 
# 해야될꺼 보내드리기 


# 이전에는 사이즈 변경이 발생하면 비행체가 아닌다른 객체들은 새로 생성될때 변경사항이 적용되어 나타났지만 이제는 즉시 사이즈의 변경이 일어나도록 change_size_rate 안에 현상태를 직접 모든객체에 적용시키기위해 for loop를 돌려 각 객체마다 모든 변경사항을 적용시켜주고 게임을 실행 시ㅣㅁ


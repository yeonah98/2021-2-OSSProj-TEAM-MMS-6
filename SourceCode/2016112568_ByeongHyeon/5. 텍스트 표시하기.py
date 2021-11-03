import pygame
import random
import time
from datetime import datetime
# 1. 게임초기화 
pygame.init()

# 2. 게임창 옵션 설정
size=[400,900] # 게임창 크기
screen = pygame.display.set_mode(size)

title = "My game"
pygame.display.set_caption(title) # 창의 제목 표시줄 옵션
# 3. 게임 내 필요한 설정
clock = pygame.time.Clock() # 이걸로 FPS설정함

class obj :
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0

    def put_img(self,address):
        if address[-3:]=="png":
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
        self.sx, self.sy = self.img.get_size()        

    def change_size(self,sx,sy):
        self.img = pygame.transform.scale(self.img,(sx,sy)) # 그림의 크기 조정
        self.sx, self.sy = self.img.get_size()
    
    def show(self):
        screen.blit(self.img,(self.x,self.y))

# 충돌을 판단하는 함수
def crash(a,b):
    # 요 범위 안에 있을때 충돌이 일어남
    if (a.x-b.sx <=b.x) and (b.x<=a.x + a.sx):
        if(a.y-b.sy <= b.y) and (b.y <= a.y+a.sy):
            return True
        else:
            return False
            
    else:
        return False

ss=obj() # 객체 생성
ss.put_img("SourceCode/Image/pngtree-airplane-vector-illustration-png-image_332890.jpeg")
ss.change_size(50,80) # 그림의 크기 조정
ss.x = round(size[0]/2- ss.sx/2)
ss.y = size[1] -ss.sy
ss.move=5 # 움직이는 속도를 결정함

k=0
left_go = False
right_go = False
space_go = False
# 미사일 발사!
m_list = [] # 미사일 리스트
a_list = [] # 외계인 리스트

black=(0,0,0) # RGB임
white=(255,255,255)

kill =0 # 외계인에게 미사일을 맞췄을때 kill이 올라감
loss =0 # 외계인을 죽이지 못하고 화면상에 사라질때

GO = 0 # Game Over
# 4-0 게임 시작 대기 화면(작은 event)
SB=0
while SB==0:
    clock.tick(60)
    for event in pygame.event.get(): # 이벤트가 있다면 
        if event.type == pygame.KEYDOWN: # 그 이벤트가 어떤 버튼을 누르는 것이라면
            if event.key == pygame.K_SPACE: # 그 버튼이 스페이스 버튼이라면?
                SB=1
    screen.fill(black)
    font = pygame.font.Font("SourceCode/Font/DXHanlgrumStd-Regular.otf",15)
    text_kill = font.render("PRESS \"SPACE\" KEY TO START THE GAME",True,(255,255,255)) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
    screen.blit(text_kill,(40,round((size[1]/2)-50))) # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨 
    
    pygame.display.flip() # 그려왔던게 화면에 업데이트가 됨
# 4. 메인 이벤트
start_time = datetime.now() #코드첫 실행한 시간이 저장됨
SB =0
while SB==0:
    # 4-1. FPS설정
    clock.tick(60) # FPS를 60으로 설정함
    # 4-2. 각종 입력 감지
    for event in pygame.event.get(): #동작을 했을때 행동을 받아오게됨
        if event.type ==pygame.QUIT: # x버튼을 누르면 while문빠져나옴
            SB=1 # SB 가 1이되면 while 문을 벗어나오게 됨
        if event.type ==pygame.KEYDOWN: # 어떤 키가 눌렸나?
            # 키를 떼지 않았을때는 항상 True인상태 키를 뗐을때는 False인 상태가 되게 됨
            if event.key ==pygame.K_LEFT: # 키가 눌렸다면 눌린키가 왼쪽키가 맞냐?
                left_go = True
            elif event.key == pygame.K_RIGHT: # 키가 눌렸다면 눌린키가 오른쪽키가 맞냐?
                right_go = True
            elif event.key == pygame.K_SPACE: # 키가 눌렸다면 그게 space키냐?
                space_go = True
                k=0 # 속도를 1/6으로 낮췄는데 누를때마다도 한번씩 발사하고싶어서 누르면 k=0으로 초기화시킴 -> while문 조건 통과하기위해
        elif event.type == pygame.KEYUP:
            if event.key ==pygame.K_LEFT: # 키가 눌렸다면 눌린키가 왼쪽키가 맞냐?
                left_go = False
            elif event.key == pygame.K_RIGHT: # 키가 눌렸다면 눌린키가 오른쪽 키냐?
                right_go = False
            elif event.key == pygame.K_SPACE: # 키가 눌렸다면 그게 space키냐?
                space_go = False
    # 4-3. 입력, 시간에 따른 변화
    now_time = datetime.now()
    delta_time = (now_time - start_time).total_seconds() # 실행했던 첫 시간에서 현재시간을 뺴서 초로 바꿔줌 
    # 비행기가 이렇게 꾹 눌렀을때는 움직이게 됨
    if left_go ==True:
        ss.x-=ss.move
        if ss.x<0 : # 물체가 왼쪽끝 경계값으로 이동하면 더이상 안나가게끔
            ss.x=0 # 더이상 왼쪽으로 못가게 0으로 막아줌
    elif right_go ==True:
        ss.x+=ss.move 
        if ss.x >=size[0]-ss.sx: # 오른쪽끝에서 비행선 가로크기만큼뺴줘야함!
            ss.x = size[0]-ss.sx # 더이상 오른쪽으로 못가게 오른쪽 끝값으로 막아줌
    if space_go ==True and k%6 ==0: # k%6으로 미사일의 발생 비율을 1/6로 낮춤
        mm = obj() # mm이라는 객체 생성
        mm.put_img("SourceCode/Image/pngtree-brass-bullet-shells-png-image_3258604.jpeg")
        mm.change_size(5,15) # 그림의 크기 조정
        mm.x = round(ss.x + ss.sx/2 - mm.sx/2)
        mm.y = ss.y - mm.sy -10 # 총알의 위치 = 비행기위치 - 총알의 y 크기
        mm.move=15 # 움직이는 속도를 결정함
        m_list.append(mm) # 객체를 리스트에 저장
    k+=1 
    d_list=[] # 삭제할 리스트
    for i in range(len(m_list)):
        m = m_list[i] # i 번째 미사일
        m.y -= m.move
        if m.y < -m.sx: # 미사일의 사이즈 만큼 나갔을때 지워준다!
            d_list.append(i) # 살생부
    d_list.reverse() # 앞에서 부터 지우면 앞당겨와져서 오류가 일어나기떄문에 reverse해주고 지워주자
    for d in d_list:
        del m_list[d]
    if random.random()>0.98: # 약 2프로의 확률
        aa=obj() # 객체 생성
        aa.put_img("SourceCode/Image/png-clipart-alien-alien.png")
        aa.change_size(40,40) # 그림의 크기 조정
        aa.x = random.randrange(0,size[0]-aa.sx - round(ss.sx/2)) # 0부터 오른쪽 끝까지의 랜덤변수인데 비행기크기보다 작으므로 미사일을 안맞는 외계인도 고려해야함(비행선크기/2 를 뺴줘야함)
        aa.y = 10  
        aa.move = 2 # 움직이는 속도를 결정함
        a_list.append(aa)
    # 살생부 리스트 초기화
    d_list=[]
    for i in range(len(a_list)):
        a = a_list[i]
        a.y += a.move
        if a.y>=size[1]: # 외계인이 화면밖으로 나갔다면 지워준다.
            d_list.append(i)
    # 메모리 효율을 위해 삭제시켜줌
    d_list.reverse() # 앞에서 부터 지우면 앞당겨와져서 오류가 일어나기떄문에 reverse해주고 지워주자
    for d in d_list:
        del a_list[d]
        loss+=1 # 외계인이 화면 밖으로 나간횟수
    # 미사일을 맞추면 총알과함께 사라짐 
    # 삭제하기위한 리스트
    dm_list = []
    da_list = []
    for i in range(len(m_list)):
        for j in range(len(a_list)):
            m = m_list[i]
            a = a_list[j]
            if crash(m,a) is True:
                dm_list.append(i)
                da_list.append(j)
    # 미사일2개와 외계인 1개가 같이 만나는 경우가 있을 수도 있으니까 배제하기위해 중복제거를 해준다.
    dm_list = list(set(dm_list))
    da_list = list(set(da_list))
    # reverse 하지않고 지우면 앞에서 부터 지워지고 앞에서부터지워지면 index의 변화가 일어나서 reverse를 해야함
    dm_list.reverse()
    da_list.reverse()
    # del 로 미사일과 외계인 삭제하기
    for dm in dm_list:
        del m_list[dm]
    for da in da_list:
        del a_list[da]
        kill+=1 # 외계인을 사살한 횟수
    for i in range(len(a_list)):
        a = a_list[i]
        # 만약 외계인이 ss와 부딛친다면 꺼짐
        if crash(a,ss) is True:
            time.sleep(1) # 1초뒤에 꺼지도록 함
            SB=1 # while문이 종료되도록 하는 key
            GO=1 # GO 가 0인 상태로 while문을 빠져나왔다면 x버튼으로 빠져나온것
    # 4-4 그리기
    screen.fill(black)
    ss.show()
    for m in m_list:
        m.show()
    for a in a_list:
        a.show()
    
    font = pygame.font.Font("SourceCode/Font/DXHanlgrumStd-Regular.otf",20)
    text_kill = font.render("Killed : {} Loss : {}".format(kill,loss),True,(255,255,0)) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
    screen.blit(text_kill,(10,5)) # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨 
    
    # 현재 흘러간 시간 
    text_time = font.render("Time : {:.2f}".format(delta_time),True,(225,225,225))
    screen.blit(text_time,(size[0]-150,5))
    # 4-5. 업데이트
    pygame.display.flip() # 그려왔던게 화면에 업데이트가 됨

# 5. 게임종료(1. x키를 눌러서 게임이 종료된 경우, 2. 죽어서 게임이 종료된 경우)
# 이건 게임오버가 된 상황!
while GO==1:
    clock.tick(60)
    for event in pygame.event.get(): # 이벤트가 있다면 
        if event.type == pygame.QUIT:
            GO=0
    
    font = pygame.font.Font("SourceCode/Font/DXHanlgrumStd-Regular.otf",40)
    text_kill = font.render("GAME OVER",True,(255,0,0)) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
    screen.blit(text_kill,(80,round((size[1]/2)-70))) # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨 
    
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

import pygame
import random

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



# 4. 메인 이벤트
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
            elif event.key == pygame.K_SPACE:
                space_go = True
                k=0 # 속도를 1/6으로 낮췄는데 누를때마다도 한번씩 발사하고싶어서 누르면 k=0으로 초기화시킴 -> while문 조건 통과하기위해

        elif event.type == pygame.KEYUP:
            if event.key ==pygame.K_LEFT: # 키가 눌렸다면 눌린키가 왼쪽키가 맞냐?
                left_go = False
            elif event.key == pygame.K_RIGHT: # 키가 눌렸다면 눌린키가 오른쪽 키냐?
                right_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False
            

    # 4-3. 입력, 시간에 따른 변화

    # 비행기가 이렇게 꾹 눌렀을때는 움직이게 됨
    if left_go ==True:
        ss.x-=ss.move
        if ss.x<0 : # 물체가 왼쪽끝 경계값으로 이동하면 더이상 안나가게끔
            ss.x=0
    elif right_go ==True:
        ss.x+=ss.move
        if ss.x >=size[0]-ss.sx: # 오른쪽끝에서 비행선 가로크기만큼뺴줘야함!
            ss.x = size[0]-ss.sx
    
    
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
        if a.y>=size[1]: # a가 화면밖으로 나갔다면 지워준다.
            d_list.append(i)
    # 메모리 효율을 위해 삭제시켜줌
    d_list.reverse() # 앞에서 부터 지우면 앞당겨와져서 오류가 일어나기떄문에 reverse해주고 지워주자
    for d in d_list:
        del a_list[d]
    
    # 4-4 그리기
    screen.fill(black)
    ss.show()
    for m in m_list:
        m.show()
    for a in a_list:
        a.show()
        
    # 4-5. 업데이트
    pygame.display.flip() # 그려왔던데 화면에 업데이트가 됨

# 5. 게임종료
pygame.quit()

import pygame

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
ss.put_img("/Users/byeonghyeon/Documents/GitHub/2021-1-OSSPC-MUHIRYO-4/2016112568_ByeongHyeon/Image/pngtree-airplane-vector-illustration-png-image_332890.jpeg")
ss.change_size(50,80) # 그림의 크기 조정
ss.x = round(size[0]/2- ss.sx/2)
ss.y = size[1] -ss.sy


# ss: 이미지
# ss_x, ss_y : 위치
# ss_sx, ss_sy : 크기
# ss_move : 이동속도

# ss = pygame.image.load("/Users/byeonghyeon/Documents/GitHub/2021-1-OSSPC-MUHIRYO-4/2016112568_ByeongHyeon/Image/pngtree-airplane-vector-illustration-png-image_332890.jpeg")
# ss = pygame.transform.scale(ss,(50,80)) # 그림의 크기 조정
# ss_sx , ss_sy = ss.get_size()
# ss_x = round(size[0]/2- ss_sx/2) #절반의 위치에서 비행기 가로크기의 절반만큼 왼쪽으로 가줘야 정중앙에 배치됨
# ss_y = size[1] -ss_sy # 끝갚에서 비행기의 크기만큼 올라와야 비행선이 보임

black=(0,0,0) # RGB임
white=(255,255,255)
k=0
# 4. 메인 이벤트
SB =0
while SB==0:
    
    # 4-1. FPS설정
    clock.tick(60) # FPS를 60으로 설정함

    # 4-2. 각종 입력 감지
    for event in pygame.event.get(): #동작을 했을때 행동을 받아오게됨
        if event.type ==pygame.QUIT: # x버튼을 누르면 while문빠져나옴
            SB=1 # SB 가 1이되면 while 문을 벗어나오게 됨
            
    # 4-3. 입력, 시간에 따른 변화
    k+=1
    
    # 4-4 그리기
    screen.fill(black)
    ss.show()
    # 4-5. 업데이트
    pygame.display.flip() # 그려왔던데 화면에 업데이트가 됨

# 5. 게임종료
pygame.quit()




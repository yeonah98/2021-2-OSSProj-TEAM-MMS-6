import pygame, sys

from random import *



# Sprite : 개별 공의 움직임 프레임 

class MyBallClass ( pygame.sprite.Sprite ) : 

    def __init__( self, image_file, location, speed ) : 

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load( image_file )

        self.rect = self.image.get_rect()

        self.rect.left, self.rect.top = location

        self.speed = speed 



    def move ( self ) :     # 공을 움직이는 메서드 

        self.rect = self.rect.move( self. speed )

        if self.rect.left < 0 or self.rect.right > width :

            self.speed[0] = - self.speed[0]



        if self.rect.top < 0 or self.rect.bottom > height :

            self.speed[1] = -self.speed[1]



# 클래스로 움직이는 공들이 충돌시 처리함수 

def animate ( group ) :

    screen.fill ([255,255,255])

    for ball in group :

        group.remove( ball ) 



        #  .sprite.spritecollide 스프라이트 간 충돌검사

        if pygame.sprite.spritecollide (ball, group, False) :

            ball.speed[0] = -ball.speed[0]

            ball.speed[1] = -ball.speed[1]



        group.add ( ball )

        ball. move ()

        screen. blit ( ball.image,  ball.rect )

    pygame.display.flip()

    pygame.time.delay( 20 )



size = width, height = 640,480   # 변수 1개에 2개의 객체를 삽입

screen = pygame.display.set_mode( size )

screen.fill([255,255,255])

img_file = "SourceCode/Image/Catus.png"

group = pygame.sprite.Group()



for row in range(0,2):

    for column in range(0,2):

        location = [column * 180 + 10, row * 180 + 10]

        speed = [ choice([-2,2]) , choice([-2,2]) ]

        ball = MyBallClass ( img_file , location , speed )

        group.add ( ball )



running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    animate( group )

    

pygame.quit()
